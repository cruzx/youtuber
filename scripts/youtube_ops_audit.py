#!/usr/bin/env python3
"""YouTube operations audit helper for youtuber skill.

Author: Cruz Olli

Reads optional channel profile JSON, topic/keyword CSV, and YouTube Studio CSV.
Produces a Markdown and JSON report.

This script is intentionally conservative: it helps structure analysis; it does not
claim to predict virality or replace YouTube Studio/vidIQ dashboards.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _num(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return default
        return float(value)
    s = str(value).strip().replace(',', '')
    if not s:
        return default
    if s.endswith('%'):
        try:
            return float(s[:-1]) / 100.0
        except ValueError:
            return default
    try:
        return float(s)
    except ValueError:
        return default


def _pct(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    if value <= 1:
        return f"{value * 100:.2f}%"
    return f"{value:.2f}%"


def _read_json(path: Optional[str]) -> Dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    with p.open('r', encoding='utf-8') as f:
        return json.load(f)


def _read_csv(path: Optional[str]) -> List[Dict[str, Any]]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    with p.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def _find(row: Dict[str, Any], names: List[str], default: Any = None) -> Any:
    norm = {k.lower().strip().replace(' ', '_'): v for k, v in row.items()}
    for n in names:
        key = n.lower().strip().replace(' ', '_')
        if key in norm:
            return norm[key]
    return default


def stage_from_profile(profile: Dict[str, Any]) -> Tuple[str, str]:
    subs = _num(profile.get('subscriber_count') or profile.get('subscribers'), 0) or 0
    videos = _num(profile.get('video_count') or profile.get('videos'), 0) or 0
    avg_views = _num(profile.get('recent_30_video_average_views') or profile.get('avg_recent_views'), None)

    if videos < 10 or subs < 100:
        return '0-1', 'Build the basic publishing and review system.'
    if subs < 1000:
        return '1-10', 'Find topic-viewer fit and stabilize positioning.'
    if subs < 10000:
        return '10-100', 'Replicate working topics and packaging patterns.'
    if subs < 100000:
        return '100-1000', 'Systematize series, monetization, and production.'
    return '1000+', 'Scale brand assets, team workflow, and business economics.'


@dataclass
class TopicScore:
    topic: str
    score: float
    verdict: str
    pain_strength: float
    audience_size: float
    search_demand: float
    competition_opportunity: float
    channel_fit: float
    commercial_value: float
    sustainability: float
    notes: str = ''


def score_topics(rows: List[Dict[str, Any]]) -> List[TopicScore]:
    scored: List[TopicScore] = []
    for i, row in enumerate(rows, start=1):
        topic = str(_find(row, ['topic', 'keyword', 'title', '选题', '关键词'], f'Topic {i}')).strip()
        search_volume = _num(_find(row, ['search_volume', 'volume', '搜索量']), None)
        competition = _num(_find(row, ['competition', 'competition_score', '竞争', '竞争分数']), None)

        pain = _num(_find(row, ['pain_strength', 'pain', '痛点强度']), 5) or 5
        audience = _num(_find(row, ['audience_size', 'audience', '受众规模']), None)
        search = _num(_find(row, ['search_demand', '搜索需求']), None)
        comp_opp = _num(_find(row, ['competition_opportunity', '竞争机会']), None)
        fit = _num(_find(row, ['channel_fit', 'fit', '频道匹配度']), 5) or 5
        commercial = _num(_find(row, ['commercial_value', '商业价值']), 5) or 5
        sustain = _num(_find(row, ['sustainability', '可持续性']), 5) or 5
        notes = str(_find(row, ['notes', '备注'], '') or '')

        # Convert common vidIQ-like scale if values are available.
        if search is None:
            if search_volume is None:
                search = 5
            else:
                # Log scale so huge volumes do not dominate.
                search = min(10, max(1, 1 + math.log10(max(1, search_volume)) * 2))
        if audience is None:
            audience = search
        if comp_opp is None:
            if competition is None:
                comp_opp = 5
            else:
                # Accept competition either 0-1, 0-100, or 1-10.
                c = competition
                if c <= 1:
                    c = c * 10
                elif c > 10:
                    c = c / 10
                comp_opp = max(1, min(10, 11 - c))

        dims = [pain, audience, search, comp_opp, fit, commercial, sustain]
        dims = [max(1, min(10, float(d))) for d in dims]
        # Geometric mean punishes one critical weakness without making score zero.
        gm = math.prod(dims) ** (1 / len(dims))
        score = gm * 10
        if score >= 75:
            verdict = 'Recommended'
        elif score >= 55:
            verdict = 'Cautious'
        else:
            verdict = 'Not recommended'
        scored.append(TopicScore(topic, round(score, 1), verdict, *[round(d, 1) for d in dims], notes=notes))
    scored.sort(key=lambda x: x.score, reverse=True)
    return scored


def analytics_summary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {'available': False}

    ctrs: List[float] = []
    intros: List[float] = []
    views: List[float] = []
    rows_out: List[Dict[str, Any]] = []

    for row in rows:
        title = str(_find(row, ['title', 'video_title', '视频标题'], '') or '')
        ctr = _num(_find(row, ['ctr', 'impressions_ctr', 'click_through_rate', '点击率']), None)
        intro = _num(_find(row, ['intro_retention', '30s_retention', 'first_30s_retention', '首30秒留存'], None), None)
        view = _num(_find(row, ['views', '播放量'], None), None)
        impressions = _num(_find(row, ['impressions', '展示量'], None), None)
        vfi = _num(_find(row, ['views_from_impressions', 'impressions_views', '来自展示的观看次数'], None), None)

        if ctr is not None and ctr > 1:
            ctr = ctr / 100.0
        if intro is not None and intro > 1:
            intro = intro / 100.0
        if ctr is not None:
            ctrs.append(ctr)
        if intro is not None:
            intros.append(intro)
        if view is not None:
            views.append(view)

        packaging_to_30 = ctr * intro if ctr is not None and intro is not None else None
        rows_out.append({
            'title': title,
            'views': view,
            'impressions': impressions,
            'ctr': ctr,
            'intro_retention': intro,
            'packaging_to_30s': packaging_to_30,
            'retained_30s_views': (view * intro if view is not None and intro is not None else None),
            'retained_30s_from_impressions': (vfi * intro if vfi is not None and intro is not None else None),
        })

    def avg(xs: List[float]) -> Optional[float]:
        return statistics.mean(xs) if xs else None

    return {
        'available': True,
        'row_count': len(rows),
        'avg_ctr': avg(ctrs),
        'avg_intro_retention': avg(intros),
        'avg_views': avg(views),
        'videos': rows_out,
    }


def priority_diagnosis(profile: Dict[str, Any], topics: List[TopicScore], analytics: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    if not profile.get('target_viewer'):
        issues.append('Target viewer is not explicit. Rewrite positioning before scaling output.')
    if not profile.get('business_goal'):
        issues.append('Business goal is missing. Clarify whether the channel optimizes for AdSense, consulting, courses, affiliate, membership, or brand demand.')
    if topics and topics[0].score < 55:
        issues.append('Current topic candidates are weak. Rebuild topic pool around stronger pain/search/channel-fit overlap.')
    if analytics.get('available'):
        avg_ctr = analytics.get('avg_ctr')
        avg_intro = analytics.get('avg_intro_retention')
        if avg_ctr is not None and avg_intro is not None:
            if avg_ctr < 0.035 and avg_intro < 0.55:
                issues.append('Packaging and first 30 seconds are both weak. Fix topic/title/thumbnail before deep editing polish.')
            elif avg_ctr >= 0.05 and avg_intro < 0.55:
                issues.append('Packaging attracts clicks but opening under-delivers. Recut first 30 seconds.')
            elif avg_ctr < 0.035 and avg_intro >= 0.60:
                issues.append('Content retains viewers but packaging is under-selling it. Rewrite title/thumbnail.')
    if not issues:
        issues.append('No single bottleneck is obvious from provided data. Review recent top/bottom videos manually and test controlled topic/title variations.')
    return issues[:5]


def make_markdown(profile: Dict[str, Any], topics: List[TopicScore], analytics: Dict[str, Any]) -> str:
    stage, stage_job = stage_from_profile(profile)
    lines: List[str] = []
    lines.append('# YouTube Ops Audit')
    lines.append('')
    lines.append('## Channel stage')
    lines.append(f'- Stage: **{stage}**')
    lines.append(f'- Main job: {stage_job}')
    lines.append('')
    lines.append('## Positioning')
    lines.append(f'- Channel: {profile.get("channel_name", "n/a")}')
    lines.append(f'- Target viewer: {profile.get("target_viewer", "n/a")}')
    lines.append(f'- Niche: {profile.get("niche", "n/a")}')
    lines.append(f'- Business goal: {profile.get("business_goal", "n/a")}')
    lines.append('')
    lines.append('## Priority diagnosis')
    for issue in priority_diagnosis(profile, topics, analytics):
        lines.append(f'- {issue}')
    lines.append('')

    if topics:
        lines.append('## Topic / keyword opportunities')
        lines.append('| Rank | Topic | Score | Verdict | Pain | Search | Competition opportunity | Fit | Commercial | Sustainability |')
        lines.append('|---:|---|---:|---|---:|---:|---:|---:|---:|---:|')
        for idx, t in enumerate(topics[:15], start=1):
            lines.append(
                f'| {idx} | {t.topic} | {t.score:.1f} | {t.verdict} | {t.pain_strength:.1f} | {t.search_demand:.1f} | {t.competition_opportunity:.1f} | {t.channel_fit:.1f} | {t.commercial_value:.1f} | {t.sustainability:.1f} |'
            )
        lines.append('')
    else:
        lines.append('## Topic / keyword opportunities')
        lines.append('No topic/vidIQ CSV provided.')
        lines.append('')

    if analytics.get('available'):
        lines.append('## YouTube Studio summary')
        lines.append(f'- Videos analyzed: {analytics.get("row_count")}')
        lines.append(f'- Average CTR: {_pct(analytics.get("avg_ctr"))}')
        lines.append(f'- Average Intro Retention: {_pct(analytics.get("avg_intro_retention"))}')
        avgv = analytics.get('avg_views')
        lines.append(f'- Average views: {avgv:.0f}' if avgv is not None else '- Average views: n/a')
        lines.append('')
        lines.append('| Video | CTR | Intro retention | Packaging-to-30s | 30s retained views |')
        lines.append('|---|---:|---:|---:|---:|')
        for v in analytics.get('videos', [])[:15]:
            title = (v.get('title') or 'Untitled')[:80].replace('|', '/')
            rv = v.get('retained_30s_views')
            lines.append(f'| {title} | {_pct(v.get("ctr"))} | {_pct(v.get("intro_retention"))} | {_pct(v.get("packaging_to_30s"))} | {rv:.0f} |' if rv is not None else f'| {title} | {_pct(v.get("ctr"))} | {_pct(v.get("intro_retention"))} | {_pct(v.get("packaging_to_30s"))} | n/a |')
        lines.append('')
    else:
        lines.append('## YouTube Studio summary')
        lines.append('No YouTube Studio CSV provided.')
        lines.append('')

    lines.append('## Next 7 days')
    lines.append('1. Rewrite the channel promise in one sentence and align the next 5 topics to it.')
    lines.append('2. Validate at least 10 topic candidates using pain, search, competition, channel fit, commercial value, and sustainability.')
    lines.append('3. For the next upload, export `first30.mp4` and run `scripts/analyze_first30.py` before publishing.')
    lines.append('4. After publishing, record CTR, Intro Retention, average view duration, subscribers gained, and comment demand.')
    lines.append('')
    lines.append('## Policy note')
    lines.append('This report is an operations aid. Verify current YouTube/YPP/copyright/AI policies before making policy-sensitive channel decisions.')
    lines.append('')
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate a YouTube operations audit report.')
    parser.add_argument('--channel', help='Path to channel_profile.json', default=None)
    parser.add_argument('--topics', help='Path to topic or vidIQ keyword CSV', default=None)
    parser.add_argument('--analytics', help='Path to YouTube Studio CSV', default=None)
    parser.add_argument('--out-dir', default='reports', help='Output directory')
    args = parser.parse_args()

    profile = _read_json(args.channel)
    topic_rows = _read_csv(args.topics)
    analytics_rows = _read_csv(args.analytics)

    topics = score_topics(topic_rows)
    analytics = analytics_summary(analytics_rows)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    md = make_markdown(profile, topics, analytics)
    (out_dir / 'youtube_ops_audit.md').write_text(md, encoding='utf-8')
    payload = {
        'profile': profile,
        'stage': stage_from_profile(profile),
        'topics': [asdict(t) for t in topics],
        'analytics': analytics,
        'priority_diagnosis': priority_diagnosis(profile, topics, analytics),
    }
    (out_dir / 'youtube_ops_audit.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'Wrote {out_dir / "youtube_ops_audit.md"}')
    print(f'Wrote {out_dir / "youtube_ops_audit.json"}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
