"""Repository checks for links, media, math delimiters and hygiene.

Run from any directory:

    python scripts/validate_repo.py
"""

import re
import struct
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "build", "dist", "release"}
TEXT_SUFFIXES = {".md", ".py", ".csv", ".svg", ".txt", ".yml", ".yaml"}
README_FILES = ["README.md", "README.zh-CN.md", "README.fr.md"]


def iter_files(suffix=None):
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if suffix is None or path.suffix.lower() in suffix:
            yield path


def strip_code(text):
    lines = text.splitlines()
    out = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence:
            out.append("")
        else:
            out.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def extract_links(text):
    clean = strip_code(text)
    patterns = [
        r"!?\[[^\]]*\]\(([^)]+)\)",
        r"<img[^>]+src=\"([^\"]+)\"",
        r"<a[^>]+href=\"([^\"]+)\"",
    ]
    links = []
    for pattern in patterns:
        links.extend(re.findall(pattern, clean, flags=re.IGNORECASE))
    return links


def is_external(target):
    lowered = target.lower()
    return (
        lowered.startswith(("http://", "https://", "mailto:", "tel:", "data:"))
        or lowered.startswith("#")
    )


def check_links():
    errors = []
    checked = 0
    for path in iter_files({".md"}):
        text = path.read_text(encoding="utf-8")
        for raw in extract_links(text):
            target = raw.strip().split()[0].strip("<>")
            if is_external(target):
                continue
            target = urllib.parse.unquote(target.split("#")[0].split("?")[0])
            if not target:
                continue
            checked += 1
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append("%s -> %s" % (path.relative_to(ROOT), target))
    return checked, errors


def check_readme_structure():
    errors = []
    stats = {}
    for name in README_FILES:
        path = ROOT / name
        if not path.exists():
            errors.append("missing %s" % name)
            continue
        text = path.read_text(encoding="utf-8")
        headings = re.findall(r"^## .+$", text, flags=re.MULTILINE)
        images = re.findall(r"<img\b", text, flags=re.IGNORECASE)
        table_rows = [line for line in text.splitlines() if line.startswith("|")]
        stats[name] = (len(headings), len(images), len(table_rows))
    if len(set(stats.values())) > 1:
        errors.append("README structure differs: %s" % stats)
    return stats, errors


def check_math():
    errors = []
    for path in iter_files({".md"}):
        text = strip_code(path.read_text(encoding="utf-8"))
        if text.count("$$") % 2:
            errors.append("%s: unbalanced $$" % path.relative_to(ROOT))
        without_display = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
        if without_display.count("$") % 2:
            errors.append("%s: unbalanced inline $" % path.relative_to(ROOT))
        for delimiter in ("\\(", "\\)", "\\[", "\\]"):
            if delimiter in without_display:
                errors.append(
                    "%s: GitHub does not render %s; use $...$ or $$...$$"
                    % (path.relative_to(ROOT), delimiter)
                )
        if re.search(r"\\operatorname\b", text):
            errors.append(
                "%s: GitHub blocks \\operatorname; use \\mathrm"
                % path.relative_to(ROOT)
            )
        in_display = False
        for line in text.splitlines():
            if line.strip() == "$$":
                in_display = not in_display
                continue
            if in_display and re.match(r"^\s{0,3}[+*-]\s", line):
                errors.append(
                    "%s: list marker inside $$ block: %s"
                    % (path.relative_to(ROOT), line.strip())
                )
    return errors


def gif_size(path):
    data = path.read_bytes()[:10]
    if data[:3] != b"GIF":
        return None
    return struct.unpack("<HH", data[6:10])


def check_media():
    errors = []
    gifs = []
    for path in iter_files({".gif"}):
        size = path.stat().st_size
        dims = gif_size(path)
        gifs.append((str(path.relative_to(ROOT)), dims, size))
        if size > 10 * 1024 * 1024:
            errors.append("%s exceeds 10 MB" % path.relative_to(ROOT))
        if dims is None:
            errors.append("%s is not a valid GIF" % path.relative_to(ROOT))
    for path in iter_files({".svg"}):
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append("%s: invalid SVG (%s)" % (path.relative_to(ROOT), exc))
    for poster in ["cfd_demo_poster.png", "canard_deployment_poster.png"]:
        if not (ROOT / "media/photos/project" / poster).exists():
            errors.append("missing poster %s" % poster)
    return gifs, errors


def check_hygiene():
    errors = []
    total = 0
    largest = []
    for path in iter_files():
        total += path.stat().st_size
        largest.append((path.stat().st_size, str(path.relative_to(ROOT))))
        name = path.name
        if name.startswith("~$") or path.suffix.lower() == ".pyc":
            errors.append("temporary file: %s" % path.relative_to(ROOT))
        if name == "data.txt":
            errors.append("runtime file: %s" % path.relative_to(ROOT))
        if any(part in {"__pycache__", "build", "dist"} for part in path.parts):
            errors.append("build artifact: %s" % path.relative_to(ROOT))
        if path.stat().st_size > 50 * 1024 * 1024:
            errors.append("file over 50 MB: %s" % path.relative_to(ROOT))
    largest.sort(reverse=True)
    return total, largest[:10], errors


def check_line_endings():
    errors = []
    for path in iter_files(TEXT_SUFFIXES):
        rel = path.relative_to(ROOT)
        # Archived originals and solver output keep their original line endings.
        if rel.parts[:2] == ("docs", "archive") or rel.parts[:1] == ("simulation",):
            continue
        data = path.read_bytes()
        if path.suffix.lower() == ".bat":
            continue
        if b"\r\n" in data:
            errors.append("CRLF in text file: %s" % rel)
    return errors


def main():
    failures = []
    checked, link_errors = check_links()
    print("links checked: %d, broken: %d" % (checked, len(link_errors)))
    failures.extend(link_errors)

    stats, structure_errors = check_readme_structure()
    print("README structure:", stats)
    failures.extend(structure_errors)

    math_errors = check_math()
    print("math delimiter errors:", len(math_errors))
    failures.extend(math_errors)

    gifs, media_errors = check_media()
    print("GIFs:", gifs)
    failures.extend(media_errors)

    total, largest, hygiene_errors = check_hygiene()
    print("repository size: %.1f MB" % (total / 1024 / 1024))
    print("largest files:")
    for size, name in largest:
        print("  %8.1f MB  %s" % (size / 1024 / 1024, name))
    failures.extend(hygiene_errors)

    endings = check_line_endings()
    print("line-ending errors:", len(endings))
    failures.extend(endings)

    if failures:
        print("\nFAILURES:")
        for failure in failures:
            print(" -", failure)
        return 1
    print("\nAll repository checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
