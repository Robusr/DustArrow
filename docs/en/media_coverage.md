# Media coverage: Young Edison Season 8, Tomorrow’s World

<p align="center">
  <a href="media_coverage.md">English</a> |
  <a href="../zh-CN/media_coverage.md">中文</a> |
  <a href="../fr/media_coverage.md">Français</a>
</p>

This note collects the public record of the DustArrow feature in Shanghai TV’s
youth science programme *Young Edison* Season 8, *Tomorrow’s World*. It keeps the
broadcast narrative separate from the design files, source code and verification
results in this repository. The programme is narrative evidence, not a telemetry
log or an experimental report.

## 1. Programme and broadcast

| Item | Detail |
|---|---|
| Programme | *Young Edison* Season 8, *Tomorrow’s World* |
| Production and broadcast | Shanghai Municipal Science and Technology Commission, Shanghai Municipal Education Commission, Shanghai Media Group; STV News Channel and Kankan News app |
| Guo Mohan preview | 2024-01-25 19:53, Kankan News |
| Guo Mohan episode page | 2024-01-27 23:09, Kankan News |
| Season overview | 2024-02-25 10:28, Kankan News |
| Season context | Premiered 2024-01-20; 16 teams from more than 40 countries and regions |
| Science advisers | Chen Kaixian, Ni Minjing, Tao Hu, Jia Yang, David Evans, Wang Jingya and others |

The pages disagree on the exact slot: the preview says 19:45 on 27 January, while
the overview says Saturdays at 20:30. Both are recorded here; the exact minute is
not treated as verified.

Official pages:

- Preview: <https://www.kankanews.com/detail/ELwxNKJWGy9>
- Episode: <https://www.kankanews.com/detail/LMwVGm9WB2z>
- Overview: <https://www.kankanews.com/detail/boy4AKjBxQ1>

## 2. Local video record

| Property | Value |
|---|---|
| File | `F:\Desktop\Robusr\《少年爱迪生》郭沫晗.mp4` |
| Duration | 19:43.02 |
| Resolution | 640 × 360 |
| Frame rate | 25 fps |
| Video | H.264 Main, about 447 kb/s |
| Audio | AAC LC, 44.1 kHz, stereo, about 65 kb/s |
| Size | 76,333,836 bytes, about 72.8 MB |
| SHA-256 | `27854a95a43206bc7dd3ea3188fd81b3f9bddbf61c9e64516de09805426529c9` |

The video is a third-party television production and is **not** copied into this
repository. Only short quotations and time codes are retained; the full video,
full subtitles and still frames are not redistributed.

### Transcription note

The audio was transcribed locally with `faster-whisper small` and manually
corrected for names and obvious homophones. It is not an official transcript and
the time codes are approximate. The burned-in Chinese subtitles were used as a
cross-check. The full machine transcript is kept outside the repository and is
not versioned.

## 3. What the episode documents

### 3.1 Three generations and the name

| Time | Broadcast statement |
|---|---|
| 2023-02 | The first-generation rocket was completed; it could monitor attitude and return data to the PC ground software |
| Later | The second generation introduced the first modular design |
| Third generation | Named **DustArrow X**; “X means infinite possibilities” |
| Third-generation structure | The episode says “four parts in total, which can be connected freely”; the dust sensor can be joined with the gas sensor to form a three-sensor detection section |
| Modular goal | For sandstorms, acid rain and other weather, replace the relevant module instead of the whole airframe |

The episode says “four parts” around 08:08, while the formal CAD divides the
airframe into ten functional bays. The two are not necessarily contradictory:
the programme uses four functional groups, the CAD uses ten manufacturable bays.
The difference is marked for confirmation by the author.

### 3.2 Test flight

The opening places the flight on “a day in late autumn or early winter 2023” at a
“Gobi site on the outskirts of Guyuan”.

1. The remote ignition programme failed. The episode attributes this to a
   protection mechanism on the development board’s I/O; the original plan was
   rejected.
2. The team switched to wired ignition and tested it successfully at 7.5 m.
3. A temporary launch rail was installed on the Gobi site, followed by a countdown
   and launch.
4. The rocket flew and was recovered. The broadcast states: “the parachute bay and
   the propulsion module were both lost”, “the most important sensor section was
   kept”, and “the recovery completeness reached 80%”.
5. The student says the result was “much better than expected”; the programme uses
   the caption “success” for the flight.

A careful summary is therefore: **the rocket left the rail and part of the
vehicle was recovered. The sensor section was retrieved, but the parachute bay and
propulsion module were lost, so the airframe recovery was incomplete.** The 80%
figure is the student’s on-site estimate, not an independent measurement.

### 3.3 Ground station and data link

Around 08:47 the episode says the ground segment “reads data from a text file and
completes some simple attitude-feedback tasks”. This matches the archived code:
the serial regular expression writes `data.txt`, the six plots are placeholders
and the OpenGL widget is disabled.

Around 18:04 the student describes two intended data paths:

- an SD-card recorder;
- a remote telemetry device in the main-control section;
- “in theory, the data can be sent back in real time”.

These are design intentions, not demonstrated results. The episode does not show
a telemetry log, SD-card data or a live downlink.

### 3.4 Design philosophy

- Modular and recoverable; several rockets could be launched in one plane for a
  three-dimensional analysis of a dust event.
- Commercial dust sensors are mostly analog and carry error; the student wants
  more professional, precise sensors in future.
- The project moved from personal curiosity toward a tool for monitoring dust
  weather in the author’s home region.

## 4. What the episode does not provide

The episode does **not** give:

- flight altitude, speed, acceleration, attitude, pressure, temperature or humidity;
- dust or gas concentrations, or sensor calibration;
- communication range, RSSI, bit-error rate or link margin;
- parachute deployment altitude, impact speed or recovery location;
- total mass, thrust, centre of mass or inertia.

The programme therefore cannot replace a flight log, sensor calibration or link
budget. It proves that a test flight took place and that part of the vehicle was
recovered; it does not prove kilometre-scale telemetry or quantitative
meteorological measurements.

## 5. Terminology and version differences

| Topic | Broadcast | Repository | Treatment |
|---|---|---|---|
| Project type | Climate-monitoring rocket | Meteorological sounding rocket, modular telemetry system | Same object; the repository uses the technical term |
| Third-generation structure | Four parts, freely connected | Ten functional bays | Functional grouping versus CAD breakdown; to be confirmed |
| First-generation completion | 2023-02 | Report and BOM are dated 2023-08 | Not contradictory: first generation in February, competition material in August |
| Recovery | “Success”, 80% complete | No flight log in the archive | “Partial recovery”; 80% marked as a student estimate |
| Data link | “In theory, real-time return” | No telemetry log | Design intention, not a measured result |
| Award | SkillsMP profile claims a national second prize | Repository only says the project was presented at the national contest | Official list not retrieved; marked `[unverified]` |

On the award: a third-party SkillsMP profile states that the project won a second
prize at the 37th National Youth Science and Technology Innovation Competition in
August 2023. No official winner list attachment was retrieved, so it is not
written as a fact or added to the main README specifications.

## 6. Fact-check table

| Statement | Evidence | Status |
|---|---|---|
| A test flight took place | Episode 00:27–17:24; Kankan episode page | Confirmed by broadcast |
| Remote ignition failed; wired ignition used | Episode 11:30–12:23 | Confirmed by broadcast |
| Wired ignition worked at 7.5 m | Episode 12:21–12:23 | Confirmed by broadcast |
| Sensor section recovered; parachute bay and propulsion module lost | Episode 17:09–17:24 | Confirmed by broadcast |
| Recovery completeness 80% | Episode 17:16–17:19 | Student estimate, not measured |
| Ground station reads a text file and gives simple attitude feedback | Episode 08:47–08:49; archived code | Confirmed, prototype |
| Real-time data return | Episode 18:20–18:22 | Design intention, not demonstrated |
| Kilometre-scale link | Report claim | Unverified |
| National second prize | SkillsMP profile | `[unverified]`; no official list |
| X means infinite possibilities | Episode 08:02–08:05 | Confirmed by broadcast |
| Flight date: late autumn/early winter 2023 | Episode 00:27–00:32 | Broadcast statement; no exact date |

## 7. Citation, rights and limits

- The programme is copyright Shanghai Media Group and its producers. Kankan News
  states that the material may not be reproduced without authorization.
- This repository contains no full video, full subtitles or broadcast stills; only
  short quotations, time codes and a factual summary.
- Suggested citation: Shanghai Media Group, *Young Edison* Season 8, *Tomorrow’s
  World*, Guo Mohan feature, 2024-01-27; local file SHA-256 as above.
- Statements by the student are personal accounts. Technical performance figures
  from the broadcast must be cited as “broadcast statement”, not “measured data”.

## 8. Impact on repository information

- The three READMEs gain a media-coverage section and the X naming origin.
- The design-specification table changes “flight test: none in the archive” to a
  TV-documented test flight with partial recovery and no telemetry log.
- Errata item E-16 records the scope and limits of the broadcast evidence.
- No theory, BOM, CAD or verification result is changed; the broadcast is not used
  as a quantitative source.
