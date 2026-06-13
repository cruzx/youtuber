Use $youtube-first30-retention.

Analyze this YouTube edit for first-30-second retention risk.

Inputs:
- video export: exports/first30.mp4
- transcript: transcripts/transcript.srt
- metadata: metadata/metadata.json
- analytics: analytics/youtube_studio.csv
- timeline: timeline/timeline.fcpxml

Tasks:
1. Inspect the first 30 seconds.
2. Score hook clarity, promise match, first value time, pacing, visual change, specificity, and target viewer fit.
3. Identify exact timestamp problems.
4. Calculate Packaging-to-30s Conversion if analytics data exists.
5. Recommend cut/move/rewrite actions.
6. Write a stronger 0-30 second replacement opening.
7. Save the report to reports/first30_retention_report.md.
