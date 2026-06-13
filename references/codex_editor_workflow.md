# Codex + Editing Software Workflow

Created by **Cruz Olli**

Codex does not reliably see a video editor's live UI. The stable workflow is to export files from the editor and let Codex inspect the project folder.

## Minimum input

```text
exports/first30.mp4
transcripts/transcript.srt
metadata/first30_metadata.json
```

## Better input

```text
exports/full_video.mp4
exports/first30.mp4
transcripts/transcript.srt
metadata/channel_profile.json
metadata/first30_metadata.json
metadata/upload_package.json
analytics/youtube_studio.csv
analytics/vidiq_keywords.csv
analytics/audience_times.csv
timeline/timeline.fcpxml or timeline.xml or timeline.edl
thumbnails/thumbnail_a.png
thumbnails/thumbnail_b.png
```

## Editing software exports

### Final Cut Pro

- Export XML/FCPXML from project timeline.
- Export first 30 seconds as MP4.
- Export caption file if available.

### DaVinci Resolve

- Export timeline as FCPXML/XML/EDL.
- Export first 30 seconds as MP4.
- Export subtitles as SRT.

### Premiere Pro

- Export Final Cut Pro XML or EDL.
- Export first 30 seconds as MP4.
- Export captions as SRT.

## Codex prompt

```text
Use $youtuber.
Analyze this YouTube edit for first-30-second retention risk.
Read exports/first30.mp4, transcripts/transcript.srt, metadata/first30_metadata.json, analytics/youtube_studio.csv, and timeline/timeline.fcpxml if present.
Generate reports/first30_retention_report.md with timestamp-level edit recommendations and a rewritten 0-30s opening.
```

## Full upload optimization prompt

```text
Use $youtuber.
Analyze this YouTube upload package.
Read exports/, transcripts/, metadata/upload_package.json, analytics/, timeline/, and thumbnails/ if present.
Tell me how to edit the video for better playback, which title/thumbnail/description/keywords to use, when to publish, whether to support it with live/Shorts/Premiere, and forecast CTR, first-30-second retention, and Packaging-to-30s Conversion.
Generate reports/upload_package_optimization.md.
```
