Use $youtuber.

Project goal:
Diagnose my YouTube channel, validate upcoming topics, and audit the first 30 seconds of my current edit.

Inputs available:
- metadata/metadata.json
- transcripts/transcript.srt
- exports/first30.mp4
- analytics/youtube_studio.csv
- analytics/vidiq_keywords.csv
- analytics/competitors.csv
- timeline/timeline.fcpxml
- thumbnails/thumbnail.png

Tasks:
1. Classify the channel stage.
2. Diagnose positioning, topic pillars, title/thumbnail, update rhythm, and monetization path.
3. Use vidIQ-style data if files exist to validate the current topic.
4. Audit the first 30 seconds and calculate Packaging-to-30s Conversion if analytics data exists.
5. Identify timestamp-level cuts, moves, and rewrites.
6. Produce a stronger 0-30s opening.
7. Default to GPT img2 for the thumbnail render and give me 1 primary prompt plus 2 alternate prompts.
8. If possible, generate the real thumbnail PNG into thumbnails/generated_thumbnail_primary.png.
9. Produce a 7-day and 30-day action plan.
10. Save:
   - reports/channel_diagnosis.md
   - reports/topic_validation.md
   - reports/first30_retention_report.md
   - reports/thumbnail_prompt_primary.txt
   - thumbnails/generated_thumbnail_primary.png
