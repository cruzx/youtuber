# Post-Publish Learning Loop

Created by **Cruz Olli**

This reference turns published-video results into reusable channel knowledge. It helps the skill become more useful for one creator over time, while staying honest about what is measured and what is still only a hypothesis.

## Core principle

The skill does not autonomously evolve in the background. It learns only when the user provides results or asks for a review, and it should say which files or recommendations changed.

Use this loop:

```text
publish -> collect metrics -> compare against forecast -> identify patterns -> write hypotheses -> test again -> promote repeated wins into rules
```

## Minimum data to collect

For every published video, collect:

- platform
- publish date and time
- title
- thumbnail text
- topic/category
- video length
- impressions
- views
- CTR
- average view duration
- average percentage viewed
- first 30s retention if available
- subscribers gained
- comments
- likes
- traffic source notes
- what was tested
- what changed after publishing

## Learning hierarchy

Use this order when deciding what to trust:

1. Platform analytics from YouTube Studio, Bilibili, or equivalent dashboards.
2. A/B test results where the only meaningful difference was title or thumbnail.
3. Repeated patterns across at least 3 comparable videos.
4. Viewer comments and qualitative feedback.
5. Creator intuition and taste.
6. Generic best practices.

## Pattern rules

Store observations as:

```text
Hypothesis: observed once or twice; useful but unproven.
Working rule: repeated across at least 3 comparable videos.
Strong rule: repeated across formats, platforms, or time periods.
Retired rule: no longer supported by newer results.
```

Never convert one high-performing video into a permanent rule without comparable evidence.

## Platform learning

Track platforms separately.

YouTube often needs:

- immediate click reason
- clear title promise
- strong thumbnail readability
- fast proof in the first 30 seconds
- topic and packaging match

Bilibili may need:

- less aggressive cover design for travel and lifestyle niches
- more creator authenticity
- more natural faces
- clearer episode diary feeling
- stronger community language

Shorts and short-form platforms may need:

- first 1-2 seconds as the hook
- a visual surprise before explanation
- faster caption rhythm
- one idea per clip

## Learning outputs

Every post-publish review should output:

- What worked
- What underperformed
- What is uncertain
- What to test next
- Which learning files should be updated

Prefer this format:

```markdown
## New Hypothesis
- Evidence:
- Applies to:
- Risk:
- Next test:

## Rule Candidate
- Evidence:
- Applies to:
- How to use next time:
```

## Recommended files

Use the project-level `learning/` folder:

```text
learning/creator_style_guide.md
learning/platform_rules.md
learning/title_patterns.md
learning/learning_log.md
```

Do not overwrite a creator's existing style rules casually. Append dated notes unless the user explicitly asks for cleanup.
