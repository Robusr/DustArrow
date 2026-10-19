import sys
import unittest
from pathlib import Path


def main():
    start = Path(__file__).resolve().parent
    suite = unittest.TestLoader().discover(str(start), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(
        "\nSUMMARY tests=%d failures=%d errors=%d skipped=%d"
        % (result.testsRun, len(result.failures), len(result.errors), len(result.skipped))
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
