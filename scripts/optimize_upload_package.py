#!/usr/bin/env python3
"""
Folder-based YouTube upload package optimizer.

Inputs are discovered from a project folder:
- exports/full_video.mp4 or exports/first30.mp4
- transcripts/transcript.srt, .vtt, or .txt
- metadata/upload_package.json
- analytics/vidiq_keywords.csv
- analytics/audience_times.csv
- timeline/timeline.fcpxml, .xml, or .edl
- thumbnails/*

Outputs:
- upload_package_optimization.md
- upload_package_optimization.json

This is a pre-publish planning helper. It gives ranges and assumptions, not
guarantees about views, subscribers, or CTR.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


TIMESTAMP_RE = re.compile(r"(?P<h>\d{1,2}):(?P<m>\d{2}):(?P<s>\d{2})(?:[,.](?P<ms>\d{1,3}))?")
CJK_WORD_RE = re.compile(r"[\u4e00-\u9fff]{1}|[A-Za-z0-9_]+")

VALUE_MARKERS = [
    "为什么", "怎么", "如何", "方法", "结果", "结论", "关键", "重点", "避坑", "真相", "对比",
    "最", "第一", "三个", "数据", "实测", "值得", "后悔", "发现", "涨粉", "播放", "流量",
    "why", "how", "result", "mistake", "best", "worst", "tested", "data", "secret",
]

GENERIC_TITLE_WORDS = ["vlog", "日常", "记录", "分享", "随便", "杂谈", "生活", "旅行", "美食"]


@dataclass
class PackageInputs:
    project_dir: str
    video_path: Optional[str]
    transcript_path: Optional[str]
    metadata_path: Optional[str]
    keyword_path: Optional[str]
    audience_times_path: Optional[str]
    timeline_path: Optional[str]
    thumbnail_paths: List[str]


@dataclass
class Forecast:
    ctr_conservative: float
    ctr_target: float
    first30_conservative: float
    first30_target: float
    packaging_to_30_conservative: float
    packaging_to_30_target: float
    notes: List[str]


def _read_json(path: Optional[Path]) -> Dict[str, Any]:
    if not path or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_error": str(exc)}


def _read_csv(path: Optional[Path]) -> List[Dict[str, str]]:
    if not path or not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _find_file(base: Path, candidates: List[str]) -> Optional[Path]:
    for rel in candidates:
        p = base / rel
        if p.exists():
            return p
    return None


def _find_first(base: Path, patterns: List[str]) -> Optional[Path]:
    for pattern in patterns:
        matches = sorted(base.glob(pattern))
        if matches:
            return matches[0]
    return None


def discover(project_dir: Path) -> PackageInputs:
    video = _find_file(project_dir, ["exports/full_video.mp4", "exports/first30.mp4"])
    if video is None:
        video = _find_first(project_dir, ["exports/*.mp4", "exports/*.mov", "*.mp4", "*.mov"])
    transcript = _find_first(project_dir, ["transcripts/*.srt", "transcripts/*.vtt", "transcripts/*.txt", "*.srt", "*.txt"])
    metadata = _find_file(project_dir, ["metadata/upload_package.json", "metadata/first30_metadata.json", "metadata/metadata.json"])
    keyword = _find_file(project_dir, ["analytics/vidiq_keywords.csv", "analytics/keywords.csv"])
    audience_times = _find_file(project_dir, ["analytics/audience_times.csv"])
    timeline = _find_first(project_dir, ["timeline/*.fcpxml", "timeline/*.xml", "timeline/*.edl"])
    thumbnails = [str(p) for p in sorted((project_dir / "thumbnails").glob("*")) if p.is_file()] if (project_dir / "thumbnails").exists() else []
    return PackageInputs(
        project_dir=str(project_dir),
        video_path=str(video) if video else None,
        transcript_path=str(transcript) if transcript else None,
        metadata_path=str(metadata) if metadata else None,
        keyword_path=str(keyword) if keyword else None,
        audience_times_path=str(audience_times) if audience_times else None,
        timeline_path=str(timeline) if timeline else None,
        thumbnail_paths=thumbnails,
    )


def parse_time(ts: str) -> float:
    m = TIMESTAMP_RE.search(ts)
    if not m:
        return 0.0
    ms = int((m.group("ms") or "0").ljust(3, "0")[:3])
    return int(m.group("h")) * 3600 + int(m.group("m")) * 60 + int(m.group("s")) + ms / 1000


def read_transcript(path: Optional[Path]) -> List[Tuple[float, float, str]]:
    if not path or not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    rows: List[Tuple[float, float, str]] = []
    for i, line in enumerate(lines):
        if "-->" not in line:
            continue
        start_s, end_s = [part.strip() for part in line.split("-->", 1)]
        payload: List[str] = []
        j = i + 1
        while j < len(lines) and lines[j].strip():
            if not lines[j].strip().isdigit():
                payload.append(lines[j].strip())
            j += 1
        if payload:
            rows.append((parse_time(start_s), parse_time(end_s), " ".join(payload)))
    if rows:
        return rows
    clean = " ".join(line.strip() for line in lines if line.strip())
    return [(0, 30, clean)] if clean else []


def tokenize(text: str) -> List[str]:
    return [m.group(0).lower() for m in CJK_WORD_RE.finditer(text or "")]


def first_value_time(rows: List[Tuple[float, float, str]]) -> Optional[float]:
    for start, _, text in rows:
        if start > 30:
            continue
        low = text.lower()
        if any(marker.lower() in low for marker in VALUE_MARKERS):
            return start
    for start, _, text in rows:
        if start <= 30 and len(tokenize(text)) >= 8:
            return start
    return None


def probe_duration(video_path: Optional[Path]) -> Optional[float]:
    if not video_path or not video_path.exists() or shutil.which("ffprobe") is None:
        return None
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nokey=1:noprint_wrappers=1", str(video_path)
    ]
    try:
        out = subprocess.check_output(cmd, text=True, timeout=12).strip()
        return float(out)
    except Exception:
        return None


def best_publish_window(rows: List[Dict[str, str]], fallback: str) -> Tuple[str, str]:
    if not rows:
        return fallback, "No audience_times.csv provided; use the channel's normal audience window and review after 4 weeks."
    best_row: Optional[Dict[str, str]] = None
    best_score = -1.0
    for row in rows:
        values = list(row.values())
        score = None
        for v in values:
            try:
                score = float(str(v).replace("%", "").strip())
            except ValueError:
                continue
        if score is not None and score > best_score:
            best_score = score
            best_row = row
    if not best_row:
        return fallback, "Audience file was present but no numeric activity score was found."
    day = best_row.get("day") or best_row.get("weekday") or best_row.get("日期") or "best audience day"
    time = best_row.get("time") or best_row.get("hour") or best_row.get("时间") or "best audience hour"
    return f"{day} {time}", "Chosen from analytics/audience_times.csv. For normal uploads, publish 1-3 hours before this window; for live/Premiere, schedule at the window."


def top_keywords(rows: List[Dict[str, str]], limit: int = 12) -> List[str]:
    scored: List[Tuple[float, str]] = []
    for idx, row in enumerate(rows):
        keyword = row.get("keyword") or row.get("topic") or row.get("关键词") or row.get("title") or ""
        keyword = keyword.strip()
        if not keyword:
            continue
        score = 1000 - idx
        for key in ["score", "overall_score", "volume", "search_volume", "搜索量"]:
            if key in row:
                try:
                    score = float(str(row[key]).replace(",", ""))
                    break
                except ValueError:
                    pass
        scored.append((score, keyword))
    scored.sort(reverse=True)
    return [k for _, k in scored[:limit]]


def title_options(metadata: Dict[str, Any], transcript_text: str, keywords: List[str]) -> List[Dict[str, str]]:
    topic = metadata.get("topic") or metadata.get("video_topic") or metadata.get("title") or (keywords[0] if keywords else "这个视频")
    viewer = metadata.get("target_viewer") or "目标观众"
    payoff = metadata.get("video_promise") or metadata.get("promise") or metadata.get("payoff") or "为什么值得看"
    pain = metadata.get("viewer_pain") or metadata.get("pain") or "最容易忽略的问题"
    topic = str(topic).strip()
    payoff = str(payoff).strip()
    pain = str(pain).strip()
    return [
        {"title": f"{topic}：{payoff}", "angle": "结果/收益", "risk": "需要开头立刻证明这个收益"},
        {"title": f"{pain}？{viewer}先看这一步", "angle": "目标人群 + 痛点", "risk": "标题要避免太宽泛"},
        {"title": f"我实测了{topic}，结论和想的不一样", "angle": "反差/实测", "risk": "视频里必须有真实反差或证据"},
    ]


def thumbnail_concepts(metadata: Dict[str, Any]) -> List[Dict[str, str]]:
    topic = metadata.get("topic") or metadata.get("video_topic") or "核心画面"
    emotion = metadata.get("thumbnail_emotion") or "惊讶/判断"
    return [
        {"visual": f"一个清晰主体 + {topic} 的最高价值画面", "text": "别先错过", "why": "把稀缺点前置，适合旅行/体验/测评类"},
        {"visual": "人物表情或动作 + 结果画面对比", "text": "差很多", "why": "制造反差，适合有前后变化的视频"},
        {"visual": "大特写 + 极简背景 + 明确方向箭头/圈选", "text": "就看这里", "why": "手机端更容易读，适合信息密度高的内容"},
    ]


def forecast(metadata: Dict[str, Any], first_value: Optional[float], thumbnail_count: int, keywords: List[str]) -> Forecast:
    title = str(metadata.get("title") or "")
    promise = str(metadata.get("video_promise") or metadata.get("promise") or "")
    thumb_text = str(metadata.get("thumbnail_text") or "")
    base_ctr = 0.035
    notes: List[str] = []
    if promise:
        base_ctr += 0.008
    else:
        notes.append("No explicit video_promise found; CTR forecast stays conservative.")
    if thumb_text and len(tokenize(thumb_text)) <= 8:
        base_ctr += 0.005
    if any(w.lower() in title.lower() for w in GENERIC_TITLE_WORDS):
        base_ctr -= 0.006
        notes.append("Title contains generic wording; sharpen the click reason.")
    if thumbnail_count >= 2:
        base_ctr += 0.004
        notes.append("Multiple thumbnail candidates exist; choose the strongest promise-match or test if available.")
    if keywords:
        base_ctr += 0.002

    if first_value is None:
        first30 = 0.48
        notes.append("No clear first value detected in the first 30 seconds.")
    elif first_value <= 5:
        first30 = 0.68
    elif first_value <= 12:
        first30 = 0.60
    else:
        first30 = 0.52
        notes.append("First clear value appears late; move proof/payoff earlier.")

    ctr_con = max(0.015, base_ctr - 0.01)
    ctr_target = min(0.12, base_ctr + 0.02)
    f30_con = max(0.35, first30 - 0.08)
    f30_target = min(0.82, first30 + 0.08)
    return Forecast(
        ctr_conservative=round(ctr_con, 4),
        ctr_target=round(ctr_target, 4),
        first30_conservative=round(f30_con, 4),
        first30_target=round(f30_target, 4),
        packaging_to_30_conservative=round(ctr_con * f30_con, 4),
        packaging_to_30_target=round(ctr_target * f30_target, 4),
        notes=notes,
    )


def pct(v: float) -> str:
    return f"{v * 100:.1f}%"


def make_report(inputs: PackageInputs, metadata: Dict[str, Any], transcript_rows: List[Tuple[float, float, str]], keywords: List[str], publish_window: Tuple[str, str], fc: Forecast, duration: Optional[float]) -> str:
    first30_text = " ".join(t for s, _, t in transcript_rows if s < 30)
    first_value = first_value_time(transcript_rows)
    titles = title_options(metadata, first30_text, keywords)
    thumbs = thumbnail_concepts(metadata)
    readiness = "Cautious"
    if inputs.video_path and (metadata.get("video_promise") or metadata.get("promise")) and first_value is not None and first_value <= 12:
        readiness = "Ready after packaging polish"
    if not inputs.video_path:
        readiness = "Needs video export"

    lines: List[str] = []
    lines.append("# Upload Package Optimization")
    lines.append("")
    lines.append("## Verdict")
    lines.append(f"- Publish readiness: {readiness}")
    lines.append(f"- Biggest bottleneck: {'opening proof arrives late' if first_value is None or first_value > 12 else 'package clarity and thumbnail selection'}")
    lines.append("- Highest-leverage fix: make the title/thumbnail promise visible in the first 3-8 seconds")
    lines.append("")
    lines.append("## Inputs Found")
    lines.append(f"- Video: {inputs.video_path or 'missing'}")
    lines.append(f"- Duration: {duration:.1f}s" if duration else "- Duration: unknown")
    lines.append(f"- Transcript: {inputs.transcript_path or 'missing'}")
    lines.append(f"- Metadata: {inputs.metadata_path or 'missing'}")
    lines.append(f"- Keyword CSV: {inputs.keyword_path or 'missing'}")
    lines.append(f"- Audience time CSV: {inputs.audience_times_path or 'missing'}")
    lines.append(f"- Timeline: {inputs.timeline_path or 'missing'}")
    lines.append(f"- Thumbnail candidates: {len(inputs.thumbnail_paths)}")
    lines.append("")
    lines.append("## Edit Plan")
    lines.append("| Time | Keep / Cut / Move | Reason | Exact edit |")
    lines.append("|---|---|---|---|")
    lines.append("| 0-3s | Move | Viewers need immediate confirmation | Show strongest proof shot + overlay the core promise |")
    lines.append("| 3-8s | Keep if specific | This is where the viewer decides whether the click was right | State the result, conflict, or rare access in one sentence |")
    lines.append("| 8-15s | Move earlier if needed | First value should arrive before setup fatigue | Put the first concrete payoff, not background |")
    lines.append("| 15-30s | Tighten | Build forward momentum | Give a mini-roadmap or start the first segment |")
    lines.append("")
    lines.append("## Opening Rewrite")
    lines.append("- 0-3s: strongest visual proof + one-line promise")
    lines.append("- 3-8s: state the viewer problem or surprising result")
    lines.append("- 8-15s: first concrete value/proof")
    lines.append("- 15-30s: tease the next payoff and enter the main story")
    lines.append("")
    lines.append("## Title Options")
    lines.append("| Option | Title | Angle | Risk |")
    lines.append("|---|---|---|---|")
    for i, t in enumerate(titles, 1):
        lines.append(f"| {i} | {t['title']} | {t['angle']} | {t['risk']} |")
    lines.append("")
    lines.append("## Thumbnail Concepts")
    lines.append("| Concept | Visual | Text | Why it may work |")
    lines.append("|---|---|---|---|")
    for i, t in enumerate(thumbs, 1):
        lines.append(f"| {i} | {t['visual']} | {t['text']} | {t['why']} |")
    lines.append("")
    lines.append("## Description Draft")
    first_title = titles[0]["title"]
    lines.append(f"{first_title}")
    lines.append("")
    lines.append("本期先给你最关键的结论，再进入完整过程。适合想快速判断这个视频主题是否值得投入时间的观众。")
    lines.append("")
    lines.append("Chapters:")
    lines.append("00:00 Key moment")
    lines.append("00:30 Context")
    lines.append("01:30 Main segment")
    lines.append("")
    lines.append("## Keywords / Tags")
    tag_line = ", ".join(keywords[:12]) if keywords else "Add 8-12 topical tags from vidIQ/search, but treat tags as secondary."
    lines.append(tag_line)
    lines.append("")
    lines.append("## Publish Schedule")
    lines.append(f"- Recommended window: {publish_window[0]}")
    lines.append(f"- Reason: {publish_window[1]}")
    lines.append("- Backup window: same audience window on the next strongest day")
    lines.append("")
    lines.append("## Live / Shorts / Premiere Support")
    lines.append("- If this topic has live discussion potential, schedule a live Q&A or Premiere and pin the next action.")
    lines.append("- Cut 3-7 Shorts from the highest-emotion or highest-proof moments.")
    lines.append("- Use the live replay or Shorts comments to choose the next long-video angle.")
    lines.append("")
    lines.append("## Packaging Forecast")
    lines.append("| Metric | Conservative | Target | Notes |")
    lines.append("|---|---:|---:|---|")
    lines.append(f"| CTR | {pct(fc.ctr_conservative)} | {pct(fc.ctr_target)} | Estimate only; compare against channel baseline |")
    lines.append(f"| First 30s retention | {pct(fc.first30_conservative)} | {pct(fc.first30_target)} | Depends on promise delivery speed |")
    lines.append(f"| Packaging-to-30s conversion | {pct(fc.packaging_to_30_conservative)} | {pct(fc.packaging_to_30_target)} | CTR x first-30s retention |")
    if fc.notes:
        lines.append("")
        lines.append("Forecast notes:")
        for note in fc.notes:
            lines.append(f"- {note}")
    lines.append("")
    lines.append("## Next 3 actions")
    lines.append("1. Lock one title/thumbnail promise and make it visible in the first 8 seconds.")
    lines.append("2. Export a fresh first30.mp4 after recutting and rerun the first-30-second audit.")
    lines.append("3. Publish with a pinned comment, playlist, end screen, and 2h/24h/72h metric review.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimize a YouTube upload package from a local project folder.")
    parser.add_argument("--project-dir", default=".", help="Project folder containing exports/, transcripts/, metadata/, analytics/, thumbnails/.")
    parser.add_argument("--out-dir", default="reports", help="Output directory, relative to project-dir unless absolute.")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    inputs = discover(project_dir)
    metadata = _read_json(Path(inputs.metadata_path) if inputs.metadata_path else None)
    transcript_rows = read_transcript(Path(inputs.transcript_path) if inputs.transcript_path else None)
    keyword_rows = _read_csv(Path(inputs.keyword_path) if inputs.keyword_path else None)
    keywords = top_keywords(keyword_rows)
    audience_rows = _read_csv(Path(inputs.audience_times_path) if inputs.audience_times_path else None)
    fallback_window = str(metadata.get("preferred_publish_window") or "channel-local evening or weekend test window")
    publish_window = best_publish_window(audience_rows, fallback_window)
    duration = probe_duration(Path(inputs.video_path) if inputs.video_path else None)
    fc = forecast(metadata, first_value_time(transcript_rows), len(inputs.thumbnail_paths), keywords)

    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = project_dir / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    report = make_report(inputs, metadata, transcript_rows, keywords, publish_window, fc, duration)
    (out_dir / "upload_package_optimization.md").write_text(report, encoding="utf-8")
    payload = {
        "inputs": asdict(inputs),
        "metadata": metadata,
        "keywords": keywords,
        "publish_window": publish_window,
        "duration": duration,
        "forecast": asdict(fc),
    }
    (out_dir / "upload_package_optimization.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_dir / 'upload_package_optimization.md'}")
    print(f"Wrote {out_dir / 'upload_package_optimization.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
