# First 30s Retention Workflow

## Required project folders

```text
exports/       video exports, ideally first30.mp4
transcripts/   SRT/VTT/TXT transcript
metadata/      metadata.json with title, thumbnail text, target viewer, video promise
analytics/     optional YouTube Studio CSV
timeline/      optional FCPXML/XML/EDL
reports/       generated output
```

## Recommended review order

1. Read `metadata/metadata.json`.
2. Read `transcripts/transcript.srt` and isolate 0-30s.
3. Inspect `exports/first30.mp4` if present.
4. Inspect `timeline/` files if present.
5. Run `scripts/analyze_first30.py` if local execution is allowed.
6. Open `reports/first30_retention_report.md`.
7. Add editorial judgment and a direct rewrite.

## Common timestamp fixes

| Problem | Fix |
|---|---|
| 0-5s greeting | Cut it. Start with viewer pain/result. |
| Logo animation | Move after first payoff or remove. |
| Background setup | Move after first proof or contradiction. |
| First value after 15s | Move it into 0-8s. |
| Title says one thing, intro says another | Rewrite first sentence to mirror the title promise. |
| Static visual for 30s | Add purposeful cutaway, caption emphasis, screen proof, or camera crop. |
| Fast cuts but no meaning | Reduce noise; add sharper verbal payoff. |

## Analytics interpretation

- High CTR + low Intro Retention: opening fails to deliver on packaging.
- Low CTR + high Intro Retention: packaging is weak but content holds viewers.
- Low CTR + low Intro Retention: topic/packaging/opening all need repair.
- High CTR + high Intro Retention: clone the structure into a series.

## Report quality bar

The report must include exact timestamp edits, not generic advice.
