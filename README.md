# Youtuber Codex Skill

**English description:** A practical Codex skill for YouTube creators who want better videos, stronger packaging, and a repeatable growth workflow. Drop in video exports, transcripts, thumbnails, keyword data, and YouTube Studio metrics; the skill helps audit the edit, improve the first 30 seconds, write titles/descriptions/keywords, plan thumbnails, choose publish timing, design live/Shorts support, and estimate packaging-to-retention conversion before publishing.

**中文简介：** 一个面向 YouTube 创作者的 Codex Skill，用来做视频发布前优化和频道增长复盘。你可以把视频片段、字幕、封面草图、关键词数据、YouTube Studio 数据放进项目文件夹，它会帮你判断怎么剪、标题/简介/关键词怎么写、封面怎么设计、什么时候发布、是否配合直播/Shorts，并给出封标转化和首 30 秒留存的发布前预测。

This package contains operational templates, local helper scripts, and creator-growth workflows. It does not promise virality, subscriber counts, or view counts; it produces evidence-based recommendations and conservative forecasts.

## What It Helps With

- YouTube channel diagnosis and positioning
- Topic and keyword validation with vidIQ-style CSV data
- YouTube Studio post-publish review
- First-30-second retention audits
- Full upload-package optimization before publishing
- Title, description, keyword, and thumbnail planning
- Publish-time recommendations from audience activity data
- Live-stream, Premiere, and Shorts support plans
- Packaging-to-30-second conversion forecasts
- YPP, copyright, AI, and reused-content risk checks

## 中文功能概览

- YouTube 频道诊断与定位
- 选题和关键词验证
- YouTube Studio 发布后复盘
- 首 30 秒留存审计
- 发布前完整上传包优化
- 标题、简介、关键词、封面方案
- 基于观众活跃时间的发布时间建议
- 直播、Premiere、Shorts 支持方案
- 封标转化与首 30 秒留存预测
- YPP、版权、AI、重复内容风险检查

## Install

### macOS / Linux

```bash
git clone https://github.com/cruzx/youtuber.git
cd youtuber
bash install.sh
```

If you downloaded a zip instead:

```bash
unzip youtuber.zip
cd youtuber
bash install.sh
```

### Windows PowerShell

```powershell
git clone https://github.com/cruzx/youtuber.git
cd youtuber
powershell -ExecutionPolicy Bypass -File install.ps1
```

The installer copies this folder to:

```text
~/.agents/skills/youtuber
```

## Use in Codex

```text
Use $youtuber.
Analyze this YouTube upload package.
Read exports/, transcripts/, metadata/upload_package.json, analytics/, timeline/, and thumbnails/ if present.
Tell me how to edit the video for better playback, which title/thumbnail/description/keywords to use, when to publish, whether to support it with live/Shorts/Premiere, and forecast CTR, first-30-second retention, and Packaging-to-30s Conversion.
Generate reports/upload_package_optimization.md.
```

## Scripts

### Channel/topic/data audit

```bash
python scripts/youtube_ops_audit.py \
  --channel metadata/channel_profile.json \
  --topics analytics/vidiq_keywords.csv \
  --analytics analytics/youtube_studio.csv \
  --out-dir reports
```

### First 30s audit

```bash
python scripts/analyze_first30.py \
  --video exports/first30.mp4 \
  --transcript transcripts/transcript.srt \
  --metadata metadata/first30_metadata.json \
  --analytics analytics/youtube_studio.csv \
  --out-dir reports
```

### Upload package optimization

Use this when you want to drop a video project folder into Codex and get edit notes, title options, description, keywords, thumbnail concepts, publish timing, live/Shorts support, and a packaging forecast.

```bash
python scripts/optimize_upload_package.py \
  --project-dir . \
  --out-dir reports
```

## Recommended project structure

```text
/project
  /exports
    first30.mp4
    full_video.mp4
  /transcripts
    transcript.srt
  /metadata
    channel_profile.json
    first30_metadata.json
    upload_package.json
  /analytics
    youtube_studio.csv
    vidiq_keywords.csv
    audience_times.csv
  /timeline
    timeline.fcpxml
    timeline.xml
    timeline.edl
  /thumbnails
    thumbnail_a.png
    thumbnail_b.png
  /reports
```

## Recommended Input Files

Minimum upload optimization input:

```text
exports/first30.mp4
transcripts/transcript.srt
metadata/upload_package.json
```

Better input:

```text
exports/full_video.mp4
timeline/timeline.fcpxml
thumbnails/thumbnail_a.png
thumbnails/thumbnail_b.png
analytics/vidiq_keywords.csv
analytics/audience_times.csv
analytics/youtube_studio.csv
```

## Output Reports

- `reports/upload_package_optimization.md`
- `reports/upload_package_optimization.json`
- `reports/first30_retention_report.md`
- `reports/first30_retention_report.json`
- `reports/youtube_ops_audit.md`
- `reports/youtube_ops_audit.json`

## Repository Description

English:

```text
A Codex skill for YouTube creators: audit edits, optimize titles/thumbnails/descriptions, plan publishing and live/Shorts growth loops, and forecast packaging-to-retention conversion from local video project folders.
```

中文：

```text
一个面向 YouTube 创作者的 Codex Skill：从本地视频项目文件夹出发，审计剪辑、优化标题封面简介、规划发布时间和直播/Shorts 增长链路，并预测封标转化与首 30 秒留存。
```