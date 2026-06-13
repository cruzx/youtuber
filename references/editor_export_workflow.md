# Editing Software Export Workflow

Created by **Cruz Olli**

Codex should prefer exported files over trying to infer from a live editing interface.

## Final Cut Pro

Export:

- First 30 seconds as `exports/first30.mp4`.
- Captions/subtitles as `transcripts/transcript.srt` if available.
- Timeline as FCPXML: `timeline/timeline.fcpxml`.

## Premiere Pro

Export:

- First 30 seconds as `exports/first30.mp4`.
- Captions as SRT.
- Timeline as Final Cut XML when possible.

## DaVinci Resolve

Export:

- First 30 seconds as MP4.
- Subtitle track as SRT.
- Timeline as XML/EDL/FCPXML depending on project.

## CapCut

Export:

- First 30 seconds as MP4.
- Captions as SRT if available.
- Project/timeline files when accessible, but MP4 + SRT + metadata is enough for the audit.

## Minimum fallback

When timeline export is unavailable, use:

```text
exports/first30.mp4
transcripts/transcript.srt
metadata/metadata.json
```
