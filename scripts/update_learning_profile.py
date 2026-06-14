#!/usr/bin/env python3
"""
Post-publish learning helper for the Youtuber skill.

Author: Cruz Olli

Inputs are discovered from a project folder:
- analytics/video_results.csv
- analytics/thumbnail_tests.csv
- learning/*.md

Outputs:
- post_publish_learning_report.md
- post_publish_learning_report.json

This helper turns measured results into cautious hypotheses. It does not
promise views, subscribers, or future performance.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Dict, List, Optional, Tuple


@dataclass
class VideoResult:
    video_id: str
    title: str
    platform: str
    publish_date: str
    topic_category: str
    views: float
    ctr_percent: Optional[float]
    average_view_duration_seconds: Optional[float]
    first30_retention_percent: Optional[float]
    subscribers_gained: float
    thumbnail_text: str
    title_angle: str
    opening_hook: str
    notes: str


def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _num(value: str) -> Optional[float]:
    value = (value or "").strip().replace("%", "")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_video_results(path: Path) -> List[VideoResult]:
    rows = _read_csv(path)
    results: List[VideoResult] = []
    for row in rows:
        results.append(
            VideoResult(
                video_id=row.get("video_id", "").strip(),
                title=row.get("video_title", "").strip(),
                platform=row.get("platform", "").strip() or "Unknown",
                publish_date=row.get("publish_date", "").strip(),
                topic_category=row.get("topic_category", "").strip(),
                views=_num(row.get("views", "")) or 0.0,
                ctr_percent=_num(row.get("ctr_percent", "")),
                average_view_duration_seconds=_num(row.get("average_view_duration_seconds", "")),
                first30_retention_percent=_num(row.get("first30_retention_percent", "")),
                subscribers_gained=_num(row.get("subscribers_gained", "")) or 0.0,
                thumbnail_text=row.get("thumbnail_text", "").strip(),
                title_angle=row.get("title_angle", "").strip(),
                opening_hook=row.get("opening_hook", "").strip(),
                notes=row.get("notes", "").strip(),
            )
        )
    return results


def group_by(items: List[VideoResult], attr: str) -> Dict[str, List[VideoResult]]:
    grouped: Dict[str, List[VideoResult]] = {}
    for item in items:
        key = getattr(item, attr) or "Unknown"
        grouped.setdefault(key, []).append(item)
    return grouped


def avg(values: List[Optional[float]]) -> Optional[float]:
    real = [v for v in values if v is not None]
    return round(mean(real), 2) if real else None


def platform_summary(results: List[VideoResult]) -> List[Dict[str, object]]:
    summaries: List[Dict[str, object]] = []
    for platform, rows in sorted(group_by(results, "platform").items()):
        summaries.append(
            {
                "platform": platform,
                "videos": len(rows),
                "avg_views": round(mean([r.views for r in rows]), 2) if rows else 0,
                "avg_ctr_percent": avg([r.ctr_percent for r in rows]),
                "avg_first30_retention_percent": avg([r.first30_retention_percent for r in rows]),
                "avg_view_duration_seconds": avg([r.average_view_duration_seconds for r in rows]),
                "total_subscribers_gained": round(sum(r.subscribers_gained for r in rows), 2),
            }
        )
    return summaries


def strongest(rows: List[VideoResult], metric: str) -> Optional[VideoResult]:
    scored: List[Tuple[float, VideoResult]] = []
    for row in rows:
        value = getattr(row, metric)
        if value is not None:
            scored.append((float(value), row))
    if not scored:
        return None
    return max(scored, key=lambda item: item[0])[1]


def build_hypotheses(results: List[VideoResult]) -> List[str]:
    hypotheses: List[str] = []
    if not results:
        return ["No video_results.csv data found yet. Add published-video metrics before drawing channel-specific rules."]

    best_ctr = strongest(results, "ctr_percent")
    if best_ctr:
        hypotheses.append(
            f"Highest CTR came from '{best_ctr.title}' on {best_ctr.platform} "
            f"({best_ctr.ctr_percent}%). Test whether title angle '{best_ctr.title_angle or 'unknown'}' "
            f"and thumbnail text '{best_ctr.thumbnail_text or 'unknown'}' can repeat."
        )

    best_retention = strongest(results, "first30_retention_percent")
    if best_retention:
        hypotheses.append(
            f"Best first-30-second retention came from '{best_retention.title}' "
            f"({best_retention.first30_retention_percent}%). Inspect opening hook: "
            f"{best_retention.opening_hook or 'not recorded'}."
        )

    platform_rows = platform_summary(results)
    if len(platform_rows) > 1:
        ordered = sorted(platform_rows, key=lambda row: row.get("avg_ctr_percent") or 0, reverse=True)
        hypotheses.append(
            f"Platform comparison: {ordered[0]['platform']} currently has the strongest average CTR signal. "
            "Keep platform-specific title and cover rules separate until more data repeats."
        )

    if len(results) < 3:
        hypotheses.append("Dataset has fewer than 3 comparable videos, so every insight should stay a hypothesis for now.")
    else:
        hypotheses.append("Promote a pattern to a working rule only if it repeats across at least 3 comparable videos.")

    return hypotheses


def render_markdown(results: List[VideoResult], thumbnail_rows: List[Dict[str, str]]) -> str:
    summaries = platform_summary(results)
    hypotheses = build_hypotheses(results)

    lines = [
        "# Post-Publish Learning Report",
        "",
        "Created by **Cruz Olli**",
        "",
        "## Verdict",
    ]
    if results:
        lines.extend([
            "- The report is based on measured post-publish data from `analytics/video_results.csv`.",
            "- Treat new findings as hypotheses until repeated across comparable uploads.",
            "- Keep YouTube, Bilibili, Shorts, and live results separated when forming rules.",
        ])
    else:
        lines.append("- No measured video-result data was found yet.")

    lines.extend([
        "",
        "## Platform Summary",
        "",
        "| Platform | Videos | Avg Views | Avg CTR | Avg First 30s | Avg View Duration | Subs Gained |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    if summaries:
        for row in summaries:
            lines.append(
                f"| {row['platform']} | {row['videos']} | {row['avg_views']} | "
                f"{row['avg_ctr_percent'] if row['avg_ctr_percent'] is not None else ''} | "
                f"{row['avg_first30_retention_percent'] if row['avg_first30_retention_percent'] is not None else ''} | "
                f"{row['avg_view_duration_seconds'] if row['avg_view_duration_seconds'] is not None else ''} | "
                f"{row['total_subscribers_gained']} |"
            )
    else:
        lines.append("| No data | 0 |  |  |  |  |  |")

    lines.extend([
        "",
        "## Patterns Learned",
    ])
    for item in hypotheses:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## Thumbnail Test Notes",
    ])
    if thumbnail_rows:
        for row in thumbnail_rows[:8]:
            lines.append(
                f"- {row.get('variant', 'Variant')}: {row.get('thumbnail_text', '')} "
                f"CTR {row.get('ctr_percent', '')}, AVD {row.get('average_view_duration_seconds', '')}. "
                f"{row.get('result_notes', '')}".strip()
            )
    else:
        lines.append("- No `analytics/thumbnail_tests.csv` data found yet.")

    lines.extend([
        "",
        "## Suggested Learning File Updates",
        "- `learning/creator_style_guide.md`: add creator taste and repeated visual rules only after evidence repeats.",
        "- `learning/platform_rules.md`: keep YouTube and Bilibili cover/title rules separate.",
        "- `learning/title_patterns.md`: record title formulas that win CTR without hurting watch time.",
        "- `learning/learning_log.md`: append a dated entry for this review.",
        "",
        "## Next 3 Tests",
        "1. Test one clear title promise against one softer diary-style promise.",
        "2. Test real-face thumbnail versus food-led thumbnail on the same topic type.",
        "3. Compare first-30-second retention when the opening starts with the best food shot versus location setup.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Update creator learning profile from post-publish metrics.")
    parser.add_argument("--project-dir", default=".", help="Project folder containing analytics/ and learning/.")
    parser.add_argument("--out-dir", default="reports", help="Output report directory.")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    out_dir = project_dir / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    results = load_video_results(project_dir / "analytics" / "video_results.csv")
    thumbnail_rows = _read_csv(project_dir / "analytics" / "thumbnail_tests.csv")
    md = render_markdown(results, thumbnail_rows)

    payload = {
        "video_results_count": len(results),
        "thumbnail_tests_count": len(thumbnail_rows),
        "platform_summary": platform_summary(results),
        "hypotheses": build_hypotheses(results),
    }

    (out_dir / "post_publish_learning_report.md").write_text(md, encoding="utf-8")
    (out_dir / "post_publish_learning_report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(str(out_dir / "post_publish_learning_report.md"))


if __name__ == "__main__":
    main()
