---
name: youtuber
description: Use to diagnose and grow a YouTube channel with creator-business operating principles, vidIQ keyword and competitor data, YouTube Studio metrics, YPP/copyright/AI risk checks, live-stream growth loops, upload-package optimization, title/thumbnail/description planning, publishing schedules, and first-30-second retention audits from local video/editing files. Trigger on YouTube运营, 频道诊断, 选题, 标题封面, vidIQ, 首30秒留存, Codex剪辑审计, 上传优化, 直播涨粉, 发布时间, 封标转化, YPP, 版权, Shorts/长视频策略, 日更, 起号计划.
---

# Youtuber Skill

## Purpose

This skill is a Codex-ready YouTube operations system based on public, high-level creator-business YouTube themes and normalized into a reusable workflow for creators.

It combines eight layers:

1. **Creator-business operating principles**: YouTube as a long-term creator-business system, not a single-video lottery.
2. **Channel strategy**: positioning, niche selection, content pillars, publishing cadence, and monetization path.
3. **Data validation**: vidIQ keyword/competitor research before publishing, YouTube Studio metrics after publishing.
4. **First-30-second retention audit**: title/thumbnail promise versus opening delivery, timestamp-level editing recommendations.
5. **Policy safety**: YPP, copyright, reused content, AI disclosure, and originality risk checks.
6. **Upload-package optimization**: title, thumbnail, description, keywords/tags, chapters, pinned comment, end-screen, and playlist plan.
7. **Publishing schedule and live growth loops**: audience-time analysis, Premiere/live scheduling, Live Redirect, Shorts highlights, and subscriber-conversion CTAs.
8. **Packaging-to-retention forecasting**: pre-publish risk estimates for CTR, first-30-second retention, and packaging-to-30-second conversion.

Do not present this skill as a verbatim transcript archive. It is a summarized and operationalized methodology. It must not reproduce protected channel scripts or private content.

## When to use this skill

Use this skill when the user asks to:

- Diagnose a YouTube channel or account.
- Build a YouTube channel strategy or 30-day execution plan.
- Validate topics, niches, keywords, or competitor opportunities.
- Optimize titles, thumbnails, first 30 seconds, long-video structure, or Shorts strategy.
- Optimize a folder of video materials before publishing, including edit order, title, description, tags, thumbnail, schedule, and conversion forecast.
- Build a live-stream growth plan that turns live viewers into subscribers, VOD viewers, Shorts viewers, or Premiere viewers.
- Analyze local video exports, SRT transcripts, FCPXML/XML/EDL timelines, or YouTube Studio CSV files.
- Use vidIQ data inside a YouTube workflow.
- Check YPP, copyright, reused-content, AI-generation, or monetization risk.
- Create a Codex workflow that reads files exported from video-editing software.

## Operating philosophy

### 1. Video is homework, not a masterpiece

A video is a market-facing assignment. Its first job is to create feedback.

Default rule:

```text
先交作业，再优化作业。
```

Do not let equipment, editing polish, or endless strategy research block publishing. Quality matters, but an unpublished perfect video generates no market signal.

### 2. High-frequency publishing is a training system

Daily posting is not the final goal. It compresses the learning cycle.

Use high-frequency publishing when the creator needs to train:

- topic judgment
- camera or voice delivery
- title writing
- audience sensing
- consistency
- data review discipline

Do not recommend blind daily posting when production cost is high, mental bandwidth is low, or there is no review mechanism.

### 3. Extreme lean creator stack

Prioritize in this order:

1. topic
2. viewpoint
3. target viewer
4. opening hook
5. title
6. thumbnail
7. publishing rhythm
8. data review
9. editing polish
10. gear

Gear is not the business model.

### 4. YouTube is a business system

Every channel diagnosis must connect content to a business model:

- AdSense
- affiliate
- consulting
- course
- membership
- community
- lead generation
- paid product
- brand sponsorship

A channel can be worth doing without immediate monetization, but the strategic tradeoff must be explicit.

### 5. Learn from competitors, do not copy them

Use competitors to identify demand, structure, packaging patterns, and market gaps.

Never recommend:

- script copying
- title swapping with minor word changes
- re-uploading
- AI washing
- compilation without transformation
- low-effort reaction or narration over reused footage

## Required input schema

When possible, gather this information:

```text
channel_name:
channel_url:
language:
target_viewer:
creator_identity:
niche:
subscriber_count:
video_count:
recent_30_video_average_views:
best_video_views:
lowest_recent_video_views:
publishing_frequency:
current_content_types:
monetization_status:
business_goal:
time_available_per_week:
face_or_voice:
ai_usage:
third_party_material_usage:
main_problem:
```

If information is missing, proceed with assumptions and mark them.

## Standard project folder

For Codex projects, use this structure:

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
    thumbnail_c.png
  /reports
```

## Main workflow

### Step 1: Determine channel stage

| Stage | Typical state | Main job |
|---|---|---|
| 0-1 | no channel, no consistent uploads, or under 10 serious videos | build publishing system |
| 1-10 | some videos, weak data, inconsistent positioning | find working topic/viewer fit |
| 10-100 | some winning videos or repeatable signals | replicate successful patterns |
| 100-1000 | clear audience, stable content pillars | build operating system and monetization |
| 1000+ | brand asset exists | scale, delegate, productize, improve economics |

Do not judge only by subscriber count. Also inspect upload count, recent performance, best/worst spread, packaging, comments, cadence, and monetization fit.

### Step 2: Rewrite positioning

Use this formula:

```text
I help [target viewer] use [content format / creator edge] to solve [core problem] and achieve [specific benefit].
```

Chinese version:

```text
我帮助【目标观众】，通过【内容形式/创作者优势】，解决【核心问题】，获得【明确收益】。
```

Bad positioning:

```text
分享我的生活和想法。
```

Better positioning:

```text
我帮助想做中文 YouTube 的新手创作者，用账号诊断、案例拆解和数据复盘，解决选题、起号、YPP 和变现问题。
```

### Step 3: Score niche and topic opportunities

Use the scoring model:

```text
Topic Value = Pain Strength × Audience Size × Search Demand × Competition Opportunity × Channel Fit × Commercial Value × Sustainability
```

Score each dimension from 1 to 10.

| Dimension | Meaning | Evidence source |
|---|---|---|
| Pain Strength | viewers care now | comments, search intent, community questions |
| Audience Size | enough people exist | YouTube search, vidIQ, Google Trends |
| Search Demand | people actively search | vidIQ keywords, YouTube search autosuggest |
| Competition Opportunity | small/mid channels can rank or break out | competitor videos, vidIQ competitors |
| Channel Fit | creator has credibility and format fit | channel identity, experience, resources |
| Commercial Value | audience may pay or convert | product/service fit |
| Sustainability | can become a series | topic tree depth |

Output:

```text
Recommended / Cautious / Not recommended
Top reason:
Main risk:
Best format:
Title direction:
Thumbnail direction:
First 30s hook:
Post-publish metrics to watch:
```

### Step 4: Use vidIQ as data validation, not final strategy

vidIQ is the external opportunity layer. YouTube Studio is the first-party result layer.

Use vidIQ for:

- keyword volume
- competition score
- related keywords
- competitor channel/video tracking
- SEO metadata gaps
- trend and content-idea discovery

Do not treat vidIQ score as content quality.

Rules:

```text
High search volume is an entry signal, not a win signal.
Low competition may mean opportunity, or no demand.
SEO score is a metadata health check, not proof that viewers will watch.
```

### Step 5: Build content pillars

A channel should have 3-5 repeatable content pillars.

For YouTube-ops channels, use:

| Pillar | Purpose |
|---|---|
| Core cognition | explain the creator-business logic |
| Practical tutorials | solve operational problems |
| Case studies | reverse-engineer working channels/videos |
| Q&A | convert audience confusion into videos |
| Risk avoidance | YPP, copyright, AI, reused-content safety |
| Trend interpretation | AI, platform changes, monetization changes |

### Step 6: Package titles and thumbnails

Title is not a summary. It is the viewer's reason to click.

A strong title usually contains one or more of:

- target viewer
- pain
- outcome
- contradiction
- risk
- timeline
- number
- identity stakes

Avoid generic titles like:

```text
YouTube运营心得分享
```

Use specific titles like:

```text
新手做 YouTube，最容易死在这 3 个认知误区
```

Thumbnail rules:

- readable on mobile
- one clear subject
- 3-6 words if using text
- emotion or contradiction
- complements title instead of repeating it
- does not create a promise the intro cannot deliver

Title/thumbnail A/B plan:

- Prepare up to 3 materially different title/thumbnail combinations when the channel has access to YouTube Studio A/B testing.
- Test combinations by watch time, not just CTR, because a high-click low-retention package can damage trust.
- Use older underperforming videos first when testing is risky for a new upload.
- For new uploads without A/B access, create 3 options anyway and choose the one with the strongest promise-match to the first 30 seconds.

Package scoring:

| Area | Question |
|---|---|
| Click reason | Does the viewer know why this is worth clicking now? |
| Promise match | Can the first 30 seconds quickly prove the title/thumbnail promise? |
| Specificity | Does the title avoid vague diary wording? |
| Mobile readability | Is the thumbnail legible at phone feed size? |
| Differentiation | Would this stand out beside competitor videos on the same topic? |
| Trust | Is the promise accurate without bait-and-switch? |

### Step 7: Audit the first 30 seconds

The opening must convert the click into continued viewing.

Assess:

| Time window | Job |
|---|---|
| 0-3s | prove the viewer clicked the right video |
| 3-8s | state the problem, contradiction, or result |
| 8-15s | deliver first concrete value or proof |
| 15-30s | create a reason to keep watching |

Core metric:

```text
Packaging-to-30s Conversion = CTR × Intro Retention
```

Decision tree:

| CTR | Intro retention | Diagnosis |
|---|---|---|
| High | Low | packaging attracts but intro fails to deliver |
| Low | High | content retains but packaging is weak |
| Low | Low | topic, packaging, and intro likely all weak |
| High | High | replicate topic, packaging, and intro structure |

When local files exist, run:

```bash
python scripts/analyze_first30.py \
  --video exports/first30.mp4 \
  --transcript transcripts/transcript.srt \
  --metadata metadata/first30_metadata.json \
  --analytics analytics/youtube_studio.csv \
  --out-dir reports
```

If video analysis is unavailable, use transcript and metadata analysis only.

### Step 8: Optimize the full upload package

When a project folder exists, inspect it as a publishing package, not just as a video file.

Minimum input:

```text
exports/full_video.mp4 or exports/first30.mp4
transcripts/transcript.srt or transcript.txt
metadata/upload_package.json
```

Better input:

```text
timeline/timeline.fcpxml
thumbnails/thumbnail_a.png
thumbnails/thumbnail_b.png
analytics/vidiq_keywords.csv
analytics/audience_times.csv
analytics/youtube_studio.csv
```

Run:

```bash
python scripts/optimize_upload_package.py \
  --project-dir . \
  --out-dir reports
```

The output must include:

- best edit structure and timestamp-level changes
- what to cut, move earlier, or turn into Shorts
- 3 title options with different angles
- description draft with first two lines optimized for the viewer promise
- keywords/tags with a warning that tags have limited discovery impact
- thumbnail brief plus 2-3 thumbnail concepts
- recommended publish window based on audience data when available
- live/Premiere/Shorts support plan when relevant
- pre-publish CTR, intro-retention, and packaging-to-30-second forecast

Upload-package decision tree:

| Signal | Diagnosis | Fix |
|---|---|---|
| Strong footage, weak topic promise | viewer does not know why to click | rewrite title/thumbnail around outcome, conflict, or rare access |
| Strong title, slow opening | click converts poorly into watch time | move proof/payoff into 0-8s |
| Good video, no subscriber reason | views do not become fans | add series promise, pinned comment, end screen, next-video path |
| Search topic, weak metadata | discovery is under-supported | tighten title/description/chapters/playlist; tags are secondary |
| Live topic, no replay plan | live spike disappears | clip Shorts, redirect to Premiere/VOD, pin next action |

### Step 9: Use live streams as a growth loop

Live can accelerate subscriber growth when it is designed as a repeatable funnel, not as a random broadcast.

Use live when:

- the creator can answer real questions or react to developing events
- the topic benefits from immediacy, community, or shared decision-making
- the stream can feed the next upload, Shorts, Premiere, or community post
- the channel already has enough audience timing data to schedule intelligently

Live growth loop:

```text
pre-live topic promise -> scheduled live -> pinned subscribe/next-video reason -> live CTA -> Live Redirect/Premiere/VOD -> Shorts highlights -> follow-up long video -> analytics review
```

Live planning checklist:

- choose one clear promise, not a loose chat topic
- schedule based on "When your viewers are on YouTube" when available
- prepare 3-5 segments so replay viewers can watch later
- pin the next action: subscribe, watch next video, join Premiere, comment a question
- create 3-7 Shorts or clips from the best moments
- review subscribers gained, average concurrent viewers, chat rate, replay views, and Shorts lift

### Step 10: Publish timing and distribution

Do not rely on generic "best time to post" rules when channel data exists.

Priority order:

1. Use YouTube Studio audience data: "When your viewers are on YouTube."
2. If no data exists, publish 1-3 hours before the likely audience peak and keep the cadence consistent for 4 weeks.
3. For live or Premiere, schedule when the audience is active and promote it before going live.
4. For global channels, pick the time zone of the highest-value audience segment, not the creator's local time by default.

Distribution checklist:

- add to the correct playlist
- prepare pinned comment
- add end screen to the next best video
- prepare 1 community post or Short to support the upload
- if using live, set up Live Redirect or a Premiere path when eligible
- record post-publish metrics at 2h, 24h, 72h, and 7d

### Step 11: Review post-publish data

Never interpret one metric alone.

Use combinations:

| Pattern | Likely problem | First fix |
|---|---|---|
| high impressions, low CTR | title/thumbnail/topic packaging | rewrite packaging |
| high CTR, low 30s retention | intro promise mismatch | recut first 30s |
| high 30s retention, low average view duration | middle section weak | improve structure and pacing |
| high views, low subscribers | weak channel promise or creator identity | add series and follow reason |
| high comments, low views | narrow but engaged audience | deepen niche and test adjacent topics |

### Step 12: Apply YPP / copyright / AI risk review

Always separate:

- monetization eligibility
- copyright claim
- copyright strike
- reused/inauthentic content policy
- AI disclosure
- fair use/fair dealing legal analysis

Do not provide final legal conclusions. Provide risk levels and safer alternatives.

Risk levels:

| Risk | Examples |
|---|---|
| Low | original filming, original voice, clear analysis, sourced clips used minimally and transformatively |
| Medium | stock footage-heavy videos, AI voice, templates, limited original commentary |
| High | compilations, copied scripts, reuploaded clips, AI-washed summaries, minimal transformation |

Hard rule:

```text
Permission to use content does not automatically mean it is monetizable.
```

### Step 13: Produce action plan

Every output must end with concrete next steps:

- next 3 actions
- next 7-day publishing plan
- next 30-day testing plan
- metrics to review
- exact assets/files to change

## Output templates

### Channel diagnosis

```markdown
# Channel Diagnosis

## One-line positioning

## Current stage

## Main issue
1.
2.
3.

## Main opportunity
1.
2.
3.

## Content system
- Pillars:
- Publishing cadence:
- Long video / Shorts split:
- Series opportunities:

## Packaging
- Title issue:
- Thumbnail issue:
- First 30s issue:

## Data layer
- vidIQ keyword opportunities:
- YouTube Studio metrics to inspect:
- Competitors to track:

## Policy risk
- YPP risk:
- Copyright risk:
- AI/reused-content risk:

## 7-day plan

## 30-day plan
```

### Topic validation

```markdown
# Topic Validation

| Dimension | Score | Evidence |
|---|---:|---|
| Pain strength | | |
| Audience size | | |
| Search demand | | |
| Competition opportunity | | |
| Channel fit | | |
| Commercial value | | |
| Sustainability | | |

## Verdict
Recommended / Cautious / Not recommended

## Packaging
- Title A:
- Title B:
- Thumbnail text:
- First 3 seconds:
- First value time target:

## Production notes

## Post-publish metrics
```

### First-30-second report

```markdown
# First 30s Retention Audit

## Risk level

## Score

## Promise match
- Title promise:
- Thumbnail promise:
- Opening delivery:

## Timestamp issues
| Time | Issue | Fix |
|---|---|---|

## What to cut

## What to move earlier

## Rewritten 0-30s opening

## Post-publish review metrics
```

### Upload-package optimization report

```markdown
# Upload Package Optimization

## Verdict
- Publish readiness:
- Biggest bottleneck:
- Highest-leverage fix:

## Edit Plan
| Time | Keep / Cut / Move | Reason | Exact edit |
|---|---|---|---|

## Opening Rewrite
- 0-3s:
- 3-8s:
- 8-15s:
- 15-30s:

## Title Options
| Option | Title | Angle | Risk |
|---|---|---|---|

## Thumbnail Concepts
| Concept | Visual | Text | Why it may work |
|---|---|---|---|

## Description Draft

## Keywords / Tags

## Publish Schedule
- Recommended window:
- Reason:
- Backup window:

## Live / Shorts / Premiere Support

## Packaging Forecast
| Metric | Conservative | Target | Notes |
|---|---:|---:|---|
| CTR | | | |
| First 30s retention | | | |
| Packaging-to-30s conversion | | | |

## Next 3 actions
```

## Scripts

This skill includes:

```text
scripts/analyze_first30.py       # first-30s opening audit
scripts/youtube_ops_audit.py     # channel/topic/data diagnosis helper
scripts/optimize_upload_package.py # folder-based edit, packaging, schedule, and forecast helper
```

Run the operations audit:

```bash
python scripts/youtube_ops_audit.py \
  --channel metadata/channel_profile.json \
  --topics analytics/vidiq_keywords.csv \
  --analytics analytics/youtube_studio.csv \
  --out-dir reports
```

Run the upload-package optimizer:

```bash
python scripts/optimize_upload_package.py \
  --project-dir . \
  --out-dir reports
```

## Quality bar

The assistant using this skill must:

- be direct
- use tables where useful
- identify the highest-leverage bottleneck first
- distinguish assumption from evidence
- never promise virality
- never promise a specific CTR, subscriber count, or view count; provide ranges and assumptions
- never use “algorithm likes it” as an explanation without operational evidence
- never recommend copying competitors
- never treat AI mass production as a durable strategy
- never let policy-sensitive answers depend only on memory when internet access is available
- never over-weight tags; title, thumbnail, description, retention, and viewer satisfaction are more important
- always separate pre-publish estimates from post-publish measured data

## Reference files

Load these only when needed:

- `references/creator_methodology.md`: normalized creator-business operating principles.
- `references/vidiq_data_layer.md`: how to use vidIQ data without over-trusting it.
- `references/first30_retention_conversion.md`: first-30-second retention audit model.
- `references/ypp_copyright_ai_safety.md`: monetization, copyright, reused-content, AI risk review.
- `references/codex_editor_workflow.md`: how to connect Codex to editing exports.
- `references/growth_playbook.md`: live, Shorts, schedule, packaging test, and distribution loop.
- `references/rubrics.md`: scoring tables.
