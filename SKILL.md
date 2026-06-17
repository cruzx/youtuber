---
name: youtuber
description: Use to diagnose and grow a YouTube channel with creator-business operating principles, vidIQ keyword and competitor data, YouTube Studio metrics, YPP/copyright/AI risk checks, live-stream growth loops, upload-package optimization, title/thumbnail/description planning, default GPT img2 thumbnail rendering, publishing schedules, first-30-second retention audits from local video/editing files, and post-publish learning loops that turn video results into reusable channel knowledge. Trigger on YouTube运营, 频道诊断, 选题, 标题封面, vidIQ, 首30秒留存, Codex剪辑审计, 上传优化, 直播涨粉, 发布时间, 封标转化, 发布复盘, 自我学习, 账号经验库, YPP, 版权, Shorts/长视频策略, 日更, 起号计划.
---

# Youtuber Skill

Created by **Cruz Olli**

## Purpose

This skill is a Codex-ready YouTube operations system based on public, high-level creator-business YouTube themes and normalized into a reusable workflow for creators.

It combines ten layers:

1. **Creator-business operating principles**: YouTube as a long-term creator-business system, not a single-video lottery.
2. **Channel strategy**: positioning, niche selection, content pillars, publishing cadence, and monetization path.
3. **Data validation**: vidIQ keyword/competitor research before publishing, YouTube Studio metrics after publishing.
4. **First-30-second retention audit**: title/thumbnail promise versus opening delivery, timestamp-level editing recommendations.
5. **Policy safety**: YPP, copyright, reused content, AI disclosure, and originality risk checks.
6. **Upload-package optimization**: title, thumbnail, description, keywords/tags, chapters, pinned comment, end-screen, and playlist plan.
7. **Publishing schedule and live growth loops**: audience-time analysis, Premiere/live scheduling, Live Redirect, Shorts highlights, and subscriber-conversion CTAs.
8. **Packaging-to-retention forecasting**: pre-publish risk estimates for CTR, first-30-second retention, and packaging-to-30-second conversion.
9. **Default thumbnail rendering workflow**: when thumbnail assets are missing or weak, default to GPT img2 for cover generation from the chosen thumbnail brief.
10. **Post-publish learning loop**: turn each video's measured results into reusable channel rules, title patterns, thumbnail preferences, platform differences, and future packaging decisions.

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
- Review published-video performance and update the creator's reusable channel knowledge base.
- Compare YouTube, Bilibili, Shorts, long-form, live, and Premiere outcomes after publishing.

## Fast routing

Use this quick map before reading the full workflow:

| User need | Start here | Usually continue to |
|---|---|---|
| channel diagnosis or repositioning | Step 1-3 | Step 5, Step 14 |
| keyword validation or search-led topic selection | Step 3-4C | Step 6, Step 11 |
| title, thumbnail, description, or upload optimization | Step 6-8 | Step 10, Step 14 |
| first 30 seconds or retention problem | Step 7 | Step 8, Step 11 |
| live-stream growth or publishing schedule | Step 9-10 | Step 11, Step 14 |
| post-publish review or creator learning | Step 11-12 | Step 14 |
| YPP, copyright, reused content, or AI risk | Step 13 | Step 14 |

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

## Required input

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

## Standard project structure

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
    video_results.csv
    thumbnail_tests.csv
  /timeline
    timeline.fcpxml
    timeline.xml
    timeline.edl
  /thumbnails
    thumbnail_a.png
    thumbnail_b.png
    thumbnail_c.png
  /learning
    creator_style_guide.md
    platform_rules.md
    title_patterns.md
    video_results.csv
    thumbnail_tests.csv
    learning_log.md
  /reports
```

## Main workflow

### Workflow map

Use the workflow in four passes:

1. Strategy foundation: Step 1-5
2. Search, packaging, and retention: Step 6-8
3. Distribution, review, and learning: Step 9-12
4. Safety and action plan: Step 13-14

Start at the nearest relevant step when the user asks for a narrow task. Run the full sequence only when doing end-to-end channel or upload work.

### Phase 1: Strategy foundation

#### Step 1: Determine channel stage

| Stage | Typical state | Main job |
|---|---|---|
| 0-1 | no channel, no consistent uploads, or under 10 serious videos | build publishing system |
| 1-10 | some videos, weak data, inconsistent positioning | find working topic/viewer fit |
| 10-100 | some winning videos or repeatable signals | replicate successful patterns |
| 100-1000 | clear audience, stable content pillars | build operating system and monetization |
| 1000+ | brand asset exists | scale, delegate, productize, improve economics |

Do not judge only by subscriber count. Also inspect upload count, recent performance, best/worst spread, packaging, comments, cadence, and monetization fit.

#### Step 2: Rewrite positioning

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

#### Step 3: Score niche and topic opportunities

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

#### Step 4: Use vidIQ as data validation, not final strategy

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

Use the search workflow below in order when the topic depends on search discovery.

##### Search workflow A: Audit search relevance fields

Priority order for textual relevance:

| Field | Priority | How to use it |
|---|---|---|
| `title` | highest | put the core query and the click reason here |
| `keywords` / tags | high for query alignment, limited for overall growth | use to reinforce query intent and close obvious metadata gaps, not as a hack |
| `shortDescription` | high | use the first 1-3 lines to restate the topic naturally and cover adjacent phrasing |
| `author` / `ownerChannelName` | medium | channel naming can reinforce topic association over time |
| `category` | low | useful for context, but not a primary ranking lever |

Keep both rules true:

```text
Text relevance is not the same thing as guaranteed top ranking.
```

- metadata alignment matters for search understanding
- tags alone are still weak compared with title, description, retention, and viewer satisfaction

##### Search workflow B: Decompose the query into core concepts

Example:

```text
Search query: colorful condo kitchen design
Core concepts: colorful / condo / kitchen / design
```

For search-led videos, audit query coverage like this:

1. Split the target query into 3-6 core concepts.
2. Check which concepts appear in the title.
3. Check which concepts are reinforced in tags/keywords.
4. Check whether the first lines of the description naturally cover missing concepts or close variants.
5. If transcript, captions, or subtitles exist, verify that the spoken opening also supports the promised topic.
6. Mark the total hit rate as partial, strong, or near-complete.

Working rule:

```text
The more completely the core concepts are covered across title, description, keywords/tags, and spoken content, the stronger the video's textual relevance.
```

Example audit:

```text
Query: colorful condo kitchen design
Title hits: condo, color
Keyword hits: condo, colorful, kitchen, design
Description hits: color
Result: 4/4 core concepts represented across metadata surfaces
```

##### Search workflow C: Separate ranking signal groups

| Signal group | What it includes |
|---|---|
| Text relevance | title, description, tags/keywords, subtitles/transcript |
| Authority | subscriber base, channel history, external embeds/citations, topic trust |
| Engagement | plays, click-through rate, likes, comments, shares, watch time quality |
| Freshness | publish date, recent audience activity, timeliness of the topic |

If a video is highly relevant but still not ranking well, use this diagnosis:

| Situation | Likely explanation |
|---|---|
| high metadata alignment, weak ranking | low authority or weak engagement signals |
| high authority, weak ranking | poor title/topic fit or low freshness |
| high CTR, low sustained ranking | intro or full-video satisfaction is too weak |
| fresh upload, early lift then decay | freshness helped, but authority/engagement did not hold |

#### Step 5: Build content pillars

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

### Phase 2: Search, packaging, and retention

#### Step 6: Package titles and thumbnails

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

Search-led packaging rules:

- For search-led videos, define one primary query and 3-6 core concepts before writing metadata.
- Put the main query or its clearest natural-language version in the title whenever possible.
- Use the first lines of the description to restate the topic in human language, not keyword stuffing.
- Use tags/keywords to reinforce synonyms, variants, and adjacent terms that did not fit naturally in the title.
- If captions or transcript text are available, make sure the spoken opening reflects the same search promise.
- Do not force exact-match phrasing if it makes the title unreadable or weakens the click reason.
- Prefer natural-language query coverage over awkward SEO phrasing.

Default rendering rule:

- When the user asks for a thumbnail image, cover draft, or final cover render, default to GPT img2.
- Use the chosen thumbnail concept as the source brief and produce 2-3 materially different variants before picking one.
- If existing thumbnail files are provided, critique them first; if they are weak, still provide a GPT img2 redraw prompt.
- Keep the prompt operational: subject, framing, facial emotion, background simplicity, contrast, text-safe space, and mobile readability.
- Prefer the official phrasing `GPT Image / ChatGPT Images 2.0`, but you may refer to it in creator-facing language as `GPT img2`.
- When the user wants an actual output image, not just a brief, generate the file into `thumbnails/generated_thumbnail_*.png` by default.
- Use `scripts/generate_thumbnail_image.py` when `OPENAI_API_KEY` is available and a local output file is needed.

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

#### Step 7: Audit the first 30 seconds

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

#### Step 8: Optimize the full upload package

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
metadata/upload_package.json with thumbnail_render_model or thumbnail notes
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
- search relevance audit for the main query and its core concepts
- thumbnail brief plus 2-3 thumbnail concepts
- default GPT img2 thumbnail render prompt for the top concept, plus 1-2 alternate prompts
- if image generation is requested and credentials exist, generate at least 1 real thumbnail PNG into `thumbnails/`
- recommended publish window based on audience data when available
- live/Premiere/Shorts support plan when relevant
- pre-publish CTR, intro-retention, and packaging-to-30-second forecast

Upload-package decision tree:

| Signal | Diagnosis | Fix |
|---|---|---|
| Strong footage, weak topic promise | viewer does not know why to click | rewrite title/thumbnail around outcome, conflict, or rare access |
| Strong title, slow opening | click converts poorly into watch time | move proof/payoff into 0-8s |
| Good video, no subscriber reason | views do not become fans | add series promise, pinned comment, end screen, next-video path |
| Search topic, weak metadata | discovery is under-supported | tighten title/description/query coverage first; then use tags to reinforce missing concepts |
| Live topic, no replay plan | live spike disappears | clip Shorts, redirect to Premiere/VOD, pin next action |

### Phase 3: Distribution, review, and learning

#### Step 9: Use live streams as a growth loop

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

#### Step 10: Publish timing and distribution

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

#### Step 11: Review post-publish data

Never interpret one metric alone.

Use combinations:

| Pattern | Likely problem | First fix |
|---|---|---|
| high impressions, low CTR | title/thumbnail/topic packaging | rewrite packaging |
| high CTR, low 30s retention | intro promise mismatch | recut first 30s |
| high 30s retention, low average view duration | middle section weak | improve structure and pacing |
| high views, low subscribers | weak channel promise or creator identity | add series and follow reason |
| high comments, low views | narrow but engaged audience | deepen niche and test adjacent topics |

For search-led videos, also review:

| Pattern | Likely problem | First fix |
|---|---|---|
| impressions low, metadata match low | search system may not understand the topic clearly | rewrite title and first description lines around the primary query |
| metadata match high, impressions low | authority or freshness may be limiting discovery | compare against stronger channels and newer videos on the same query |
| impressions present, CTR low | search relevance exists but packaging is weak | improve click reason without breaking query alignment |
| CTR okay, watch time weak | metadata matched but viewer satisfaction failed | tighten the intro and structure to better fulfill the search promise |

#### Step 12: Update the channel learning loop

This skill can improve its recommendations for a specific creator by learning from measured results the user provides. It does not silently update itself. Only write or revise learning files when the user asks for post-publish review, learning, self-improvement, or channel memory.

Use these inputs when available:

```text
analytics/video_results.csv
analytics/thumbnail_tests.csv
reports/upload_package_optimization.json
learning/creator_style_guide.md
learning/platform_rules.md
learning/title_patterns.md
learning/learning_log.md
```

Learning rules:

- Treat YouTube Studio, Bilibili creator analytics, and platform dashboards as measured truth.
- Separate platform-specific behavior: YouTube packaging often rewards direct click reasons; Bilibili may reward freshness, authenticity, creator affinity, and less aggressive covers depending on niche.
- Learn from metric combinations, not single numbers.
- Store observations as hypotheses until repeated across at least 3 comparable videos.
- Never overfit one outlier video into a permanent rule.
- Keep personal creator taste separate from performance evidence.
- Do not claim the skill has autonomously evolved; say which files were updated and which data supported the update.

Run the learning updater:

```bash
python scripts/update_learning_profile.py \
  --project-dir . \
  --out-dir reports
```

Learning output must include:

- winning and losing title patterns
- thumbnail patterns by platform
- topic/category patterns
- publish timing signals
- intro-retention signals
- subscriber-conversion signals
- next 3 rules to test
- recommended edits to `learning/creator_style_guide.md`, `learning/platform_rules.md`, or `learning/title_patterns.md`

### Phase 4: Safety and action plan

#### Step 13: Apply YPP / copyright / AI risk review

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

#### Step 14: Produce action plan

Every output must end with concrete next steps:

- next 3 actions
- next 7-day publishing plan
- next 30-day testing plan
- metrics to review
- exact assets/files to change
- what to add to the learning log after publishing

## Output templates

### Template index

Use the closest template instead of improvising structure:

| Need | Template |
|---|---|
| channel diagnosis | Channel diagnosis |
| topic or keyword decision | Topic validation |
| intro or retention fix | First-30-second report |
| full upload optimization | Upload-package optimization report |
| post-publish review and creator learning | Post-publish learning report |

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

## Search Relevance Audit
- Primary query:
- Core concepts:
- Title hits:
- Description hits:
- Tag/keyword hits:
- Transcript/caption support:
- Coverage score:
- Relevance verdict:

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

## Thumbnail Render Default
- Default renderer: GPT img2
- Primary prompt:
- Alternate prompt A:
- Alternate prompt B:
- Default output path: `thumbnails/generated_thumbnail_primary.png`
- If local rendering is requested: run `scripts/generate_thumbnail_image.py`

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

## Learning Plan
- Metrics to record after publishing:
- Hypotheses being tested:
- What would count as a win:
- What to add to `learning/learning_log.md`:

## Next 3 actions
```

### Post-publish learning report

```markdown
# Post-Publish Learning Report

## Verdict
- What worked:
- What underperformed:
- What is still unclear:

## Measured Results
| Video | Platform | CTR | First 30s retention | Average view duration | Subscribers gained | Notes |
|---|---|---:|---:|---:|---:|---|

## Patterns Learned
- Title:
- Thumbnail:
- Opening:
- Topic:
- Publish timing:
- Platform differences:

## Rules To Keep Testing
1.
2.
3.

## Suggested Learning File Updates
- `learning/creator_style_guide.md`:
- `learning/platform_rules.md`:
- `learning/title_patterns.md`:
- `learning/learning_log.md`:
```

## Implementation

### Scripts

This skill includes:

```text
scripts/analyze_first30.py       # first-30s opening audit
scripts/youtube_ops_audit.py     # channel/topic/data diagnosis helper
scripts/optimize_upload_package.py # folder-based edit, packaging, schedule, and forecast helper
scripts/generate_thumbnail_image.py # direct OpenAI image generation to local PNG files
scripts/update_learning_profile.py # post-publish results review and channel learning helper
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

Render the thumbnail image:

```bash
OPENAI_API_KEY=your_key_here \
python scripts/generate_thumbnail_image.py \
  --metadata metadata/upload_package.json \
  --variant primary \
  --out thumbnails/generated_thumbnail_primary.png \
  --save-prompt reports/thumbnail_prompt_primary.txt \
  --save-metadata reports/thumbnail_generation_primary.json
```

Run the post-publish learning loop:

```bash
python scripts/update_learning_profile.py \
  --project-dir . \
  --out-dir reports
```

### Quality bar

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
- only update learning files when the user asks for learning, self-improvement, or post-publish review
- distinguish durable channel rules from one-video hypotheses

### Reference files

Load these only when needed:

- `references/creator_methodology.md`: normalized creator-business operating principles.
- `references/vidiq_data_layer.md`: how to use vidIQ data without over-trusting it.
- `references/first30_retention_conversion.md`: first-30-second retention audit model.
- `references/ypp_copyright_ai_safety.md`: monetization, copyright, reused-content, AI risk review.
- `references/codex_editor_workflow.md`: how to connect Codex to editing exports.
- `references/growth_playbook.md`: live, Shorts, schedule, packaging test, and distribution loop.
- `references/learning_loop.md`: post-publish learning, channel memory, and reusable creator-specific rules.
- `references/rubrics.md`: scoring tables.
