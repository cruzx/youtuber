#!/usr/bin/env python3
"""
YouTube First 30s Retention Conversion Audit

Local heuristic analyzer for Codex workflows.

Inputs:
- --video: exported video file, ideally first 30 seconds or full video
- --transcript: .srt / .vtt / .txt transcript
- --metadata: JSON file with title, thumbnail_text, target_viewer, video_promise
- --analytics: YouTube Studio CSV with ctr_percent and intro_retention_30s_percent
- --timeline: optional FCPXML/XML/EDL timeline export
- --out-dir: output directory

The script produces:
- first30_retention_report.md
- first30_retention_report.json

Notes:
- This is a pre-publish risk estimator unless YouTube Studio data is provided.
- Real Intro retention is a YouTube Studio post-publish metric.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET


CJK_WORD_RE = re.compile(r"[\u4e00-\u9fff]{1}|[A-Za-z0-9_]+")
TIMESTAMP_RE = re.compile(
    r"(?P<h>\d{1,2}):(?P<m>\d{2}):(?P<s>\d{2})(?:[,.](?P<ms>\d{1,3}))?"
)

VALUE_MARKERS = [
    "原因", "方法", "关键", "核心", "结论", "重点", "第一", "三个", "步骤", "怎么", "为什么",
    "真相", "误区", "解决", "提高", "避免", "不要", "必须", "马上", "直接", "数据", "案例",
    "because", "how", "why", "first", "step", "mistake", "fix", "secret", "data", "case",
]

DEAD_ZONE_MARKERS = [
    "大家好", "欢迎来到", "我是", "今天我们来聊", "今天跟大家聊", "废话不多说",
    "hello", "welcome back", "in this video", "today we are going to talk",
]

PROMISE_MARKERS = [
    "提高", "增长", "赚钱", "变现", "留存", "点击", "流量", "爆款", "账号", "选题", "封面", "标题",
    "增长", "新手", "避免", "风险", "为什么", "如何", "怎么", "方法", "问题", "错误",
]


@dataclass
class SubtitleLine:
    start: float
    end: float
    text: str


@dataclass
class VideoProbe:
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    has_audio: Optional[bool] = None
    ffprobe_available: bool = False
    ffmpeg_available: bool = False


@dataclass
class SceneAudit:
    cut_count: Optional[int] = None
    cuts_per_30s: Optional[float] = None
    scene_threshold: float = 0.30
    warning: Optional[str] = None


@dataclass
class SilenceAudit:
    silence_seconds: Optional[float] = None
    silence_ratio: Optional[float] = None
    warning: Optional[str] = None


@dataclass
class TimelineAudit:
    path: Optional[str] = None
    format: Optional[str] = None
    event_count_30s: Optional[int] = None
    title_or_caption_events_30s: Optional[int] = None
    likely_cut_density_30s: Optional[float] = None
    warning: Optional[str] = None


@dataclass
class MetricAudit:
    ctr_percent: Optional[float] = None
    intro_retention_30s_percent: Optional[float] = None
    views: Optional[float] = None
    views_from_impressions: Optional[float] = None
    impressions: Optional[float] = None
    average_view_duration_seconds: Optional[float] = None
    packaging_to_30s_conversion_percent: Optional[float] = None
    retained_30_per_1000_impressions: Optional[float] = None
    retained_30_views_estimate: Optional[float] = None


@dataclass
class ScoreBreakdown:
    hook_clarity: int
    promise_match: int
    first_value_time: int
    curiosity_loop: int
    pacing: int
    visual_change: int
    specificity: int
    target_viewer_fit: int
    total_score: int
    risk_level: str


@dataclass
class AuditResult:
    metadata: Dict[str, Any]
    video_probe: VideoProbe
    transcript_text_30s: str
    first_value_time: Optional[float]
    scene_audit: SceneAudit
    silence_audit: SilenceAudit
    timeline_audit: TimelineAudit
    metric_audit: MetricAudit
    score: ScoreBreakdown
    timestamp_diagnosis: List[Dict[str, str]]
    edit_list: List[str]
    rewrite: Dict[str, str]


def run_cmd(cmd: List[str], timeout: int = 20) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", exc.stderr or "timeout"
    except FileNotFoundError:
        return 127, "", f"not found: {cmd[0]}"


def parse_time(ts: str) -> float:
    m = TIMESTAMP_RE.search(ts)
    if not m:
        return 0.0
    h = int(m.group("h"))
    minute = int(m.group("m"))
    sec = int(m.group("s"))
    ms = m.group("ms") or "0"
    ms_float = int(ms.ljust(3, "0")[:3]) / 1000.0
    return h * 3600 + minute * 60 + sec + ms_float


def parse_transcript(path: Optional[Path]) -> List[SubtitleLine]:
    if not path or not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    subs: List[SubtitleLine] = []

    # SRT/VTT path
    for i, line in enumerate(lines):
        if "-->" in line:
            parts = line.split("-->")
            start = parse_time(parts[0].strip())
            end = parse_time(parts[1].strip())
            payload: List[str] = []
            j = i + 1
            while j < len(lines) and lines[j].strip():
                if not re.fullmatch(r"\d+", lines[j].strip()):
                    payload.append(lines[j].strip())
                j += 1
            if payload:
                subs.append(SubtitleLine(start, end, " ".join(payload)))

    if subs:
        return subs

    # Plain text fallback. Treat all text as first 30 seconds.
    clean = " ".join([line.strip() for line in lines if line.strip()])
    return [SubtitleLine(0, 30, clean)] if clean else []


def transcript_first_30s(subs: List[SubtitleLine]) -> str:
    return " ".join(s.text for s in subs if s.start < 30).strip()


def tokenize(text: str) -> List[str]:
    return [m.group(0).lower() for m in CJK_WORD_RE.finditer(text or "")]


def keyword_overlap(a: str, b: str) -> float:
    toks_a = set(tokenize(a))
    toks_b = set(tokenize(b))
    if not toks_a or not toks_b:
        return 0.0
    return len(toks_a & toks_b) / max(1, len(toks_a | toks_b))


def first_value_time(subs: List[SubtitleLine]) -> Optional[float]:
    if not subs:
        return None
    for sub in subs:
        if sub.start >= 30:
            continue
        low = sub.text.lower()
        if any(marker.lower() in low for marker in VALUE_MARKERS):
            return sub.start
    # fallback: first non-trivial line after title/greeting
    for sub in subs:
        if sub.start >= 30:
            continue
        if len(tokenize(sub.text)) >= 8 and not any(m in sub.text.lower() for m in DEAD_ZONE_MARKERS):
            return sub.start
    return None


def load_metadata(path: Optional[Path]) -> Dict[str, Any]:
    if not path or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_metadata_error": str(exc)}


def probe_video(path: Optional[Path]) -> VideoProbe:
    probe = VideoProbe(
        ffprobe_available=shutil.which("ffprobe") is not None,
        ffmpeg_available=shutil.which("ffmpeg") is not None,
    )
    if not path or not path.exists() or not probe.ffprobe_available:
        return probe
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_streams", "-show_format", str(path)
    ]
    code, stdout, _ = run_cmd(cmd)
    if code != 0 or not stdout.strip():
        return probe
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return probe
    fmt = data.get("format", {})
    try:
        probe.duration = float(fmt.get("duration")) if fmt.get("duration") else None
    except ValueError:
        pass
    streams = data.get("streams", [])
    for st in streams:
        if st.get("codec_type") == "video":
            probe.width = st.get("width")
            probe.height = st.get("height")
            rate = st.get("avg_frame_rate") or st.get("r_frame_rate")
            if rate and "/" in rate:
                num, den = rate.split("/", 1)
                try:
                    probe.fps = float(num) / float(den) if float(den) else None
                except ValueError:
                    pass
        if st.get("codec_type") == "audio":
            probe.has_audio = True
    if probe.has_audio is None:
        probe.has_audio = False
    return probe


def audit_scenes(video: Optional[Path], threshold: float = 0.30) -> SceneAudit:
    if not video or not video.exists():
        return SceneAudit(warning="No video file supplied.")
    if shutil.which("ffmpeg") is None:
        return SceneAudit(warning="FFmpeg not found; scene-change analysis skipped.")
    # Use scene detection. Metadata print lines often include lavfi.scene_score.
    cmd = [
        "ffmpeg", "-hide_banner", "-ss", "0", "-t", "30", "-i", str(video),
        "-filter:v", f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"
    ]
    code, _, stderr = run_cmd(cmd, timeout=30)
    if code not in (0, 1):
        # ffmpeg may return nonzero for some files; still parse if possible.
        pass
    # Count selected frames by showinfo lines.
    cut_count = len(re.findall(r"showinfo.* n:\s*\d+", stderr))
    return SceneAudit(cut_count=cut_count, cuts_per_30s=float(cut_count), scene_threshold=threshold)


def audit_silence(video: Optional[Path]) -> SilenceAudit:
    if not video or not video.exists():
        return SilenceAudit(warning="No video file supplied.")
    if shutil.which("ffmpeg") is None:
        return SilenceAudit(warning="FFmpeg not found; silence analysis skipped.")
    cmd = [
        "ffmpeg", "-hide_banner", "-ss", "0", "-t", "30", "-i", str(video),
        "-af", "silencedetect=n=-35dB:d=0.4", "-f", "null", "-"
    ]
    code, _, stderr = run_cmd(cmd, timeout=30)
    if code not in (0, 1):
        pass
    starts = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", stderr)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", stderr)]
    total = 0.0
    for idx, start in enumerate(starts):
        end = ends[idx] if idx < len(ends) else 30.0
        total += max(0.0, min(30.0, end) - max(0.0, start))
    ratio = total / 30.0 if total else 0.0
    return SilenceAudit(silence_seconds=round(total, 2), silence_ratio=round(ratio, 3))



def _parse_fcpx_time(value: str) -> Optional[float]:
    """Parse a subset of FCPXML time strings such as 300/30s, 12.5s, or 00:00:12.5."""
    if not value:
        return None
    value = value.strip()
    if value.endswith('s'):
        raw = value[:-1]
        if '/' in raw:
            num, den = raw.split('/', 1)
            try:
                return float(num) / float(den)
            except ValueError:
                return None
        try:
            return float(raw)
        except ValueError:
            return None
    if ':' in value:
        return parse_time(value)
    try:
        return float(value)
    except ValueError:
        return None


def audit_timeline(path: Optional[Path]) -> TimelineAudit:
    if not path or not path.exists():
        return TimelineAudit(warning="No editing timeline file supplied.")
    ext = path.suffix.lower().lstrip('.')
    audit = TimelineAudit(path=str(path), format=ext or None)
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as exc:
        audit.warning = f"Could not read timeline: {exc}"
        return audit

    if ext == 'edl':
        # Rough EDL heuristic: numbered event lines frequently begin with 001, 002, etc.
        events = re.findall(r"(?m)^\s*\d{3,}\s+", text)
        audit.event_count_30s = len(events)
        audit.title_or_caption_events_30s = len(re.findall(r"(?i)title|caption|text|subtitle", text))
        audit.likely_cut_density_30s = float(audit.event_count_30s or 0)
        return audit

    if ext in {'fcpxml', 'xml'}:
        try:
            root = ET.fromstring(text)
        except ET.ParseError:
            # Fallback regex count for malformed XML exports.
            events = re.findall(r"<(asset-clip|clip|title|gap|video|audio|mc-clip)\b", text)
            titles = re.findall(r"<(title)\b|caption|subtitle|text", text, flags=re.I)
            audit.event_count_30s = len(events)
            audit.title_or_caption_events_30s = len(titles)
            audit.likely_cut_density_30s = float(audit.event_count_30s or 0)
            audit.warning = "Timeline XML could not be parsed cleanly; used regex fallback."
            return audit

        events = 0
        titles = 0
        for el in root.iter():
            tag = el.tag.split('}', 1)[-1].lower()
            if tag in {'asset-clip', 'clip', 'title', 'gap', 'video', 'audio', 'mc-clip', 'sync-clip'}:
                start = _parse_fcpx_time(el.attrib.get('start', ''))
                offset = _parse_fcpx_time(el.attrib.get('offset', ''))
                candidate = offset if offset is not None else start
                # Include unknown timestamps rather than excluding useful timeline signals.
                if candidate is None or candidate < 30:
                    events += 1
                    if tag == 'title' or any(k in str(el.attrib).lower() for k in ['title', 'caption', 'subtitle', 'text']):
                        titles += 1
        audit.event_count_30s = events
        audit.title_or_caption_events_30s = titles
        audit.likely_cut_density_30s = float(events)
        return audit

    audit.warning = f"Unsupported timeline format: .{ext}. Supported: .fcpxml, .xml, .edl"
    return audit


def read_first_csv_row(path: Optional[Path]) -> Dict[str, str]:
    if not path or not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            return {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
    return {}


def parse_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace("%", "").replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def audit_metrics(path: Optional[Path]) -> MetricAudit:
    row = read_first_csv_row(path)
    audit = MetricAudit()
    if not row:
        return audit

    def get(*names: str) -> Optional[float]:
        normalized = {k.lower().strip(): v for k, v in row.items()}
        for name in names:
            if name.lower() in normalized:
                return parse_float(normalized[name.lower()])
        return None

    audit.ctr_percent = get("ctr_percent", "impressions_ctr", "click_through_rate", "ctr")
    audit.intro_retention_30s_percent = get(
        "intro_retention_30s_percent", "intro_retention", "30s_retention", "retention_30s_percent"
    )
    audit.views = get("views")
    audit.views_from_impressions = get("views_from_impressions")
    audit.impressions = get("impressions")
    audit.average_view_duration_seconds = get("average_view_duration_seconds", "avg_view_duration_seconds")

    if audit.ctr_percent is not None and audit.intro_retention_30s_percent is not None:
        conv = (audit.ctr_percent / 100.0) * (audit.intro_retention_30s_percent / 100.0)
        audit.packaging_to_30s_conversion_percent = round(conv * 100.0, 3)
        audit.retained_30_per_1000_impressions = round(conv * 1000.0, 2)

    base_views = audit.views_from_impressions or audit.views
    if base_views is not None and audit.intro_retention_30s_percent is not None:
        audit.retained_30_views_estimate = round(base_views * audit.intro_retention_30s_percent / 100.0, 2)

    return audit


def clamp_score(x: float) -> int:
    return int(max(0, min(10, round(x))))


def compute_score(
    metadata: Dict[str, Any],
    transcript_30: str,
    first_value: Optional[float],
    scene: SceneAudit,
    silence: SilenceAudit,
) -> ScoreBreakdown:
    title = str(metadata.get("title", ""))
    thumb = str(metadata.get("thumbnail_text", ""))
    promise = str(metadata.get("video_promise", ""))
    target = str(metadata.get("target_viewer", ""))
    package_text = " ".join([title, thumb, promise])

    first_5 = " ".join(tokenize(transcript_30)[:30])
    opening_overlap = keyword_overlap(package_text, transcript_30)
    first5_overlap = keyword_overlap(package_text, first_5)

    hook = 3 + 7 * min(1.0, first5_overlap * 5)
    if any(marker in transcript_30[:80].lower() for marker in DEAD_ZONE_MARKERS):
        hook -= 2

    promise_match = 2 + 8 * min(1.0, opening_overlap * 4)

    if first_value is None:
        fvt = 3
    elif first_value <= 8:
        fvt = 10
    elif first_value <= 15:
        fvt = 8
    elif first_value <= 30:
        fvt = 5
    else:
        fvt = 2

    curiosity = 5
    if any(x in transcript_30 for x in ["最后", "接下来", "第一个", "三个", "但", "真正", "不是", "而是"]):
        curiosity += 3
    if "?" in transcript_30 or "？" in transcript_30 or "为什么" in transcript_30:
        curiosity += 1

    pacing = 7
    if silence.silence_ratio is not None:
        pacing -= silence.silence_ratio * 10
    if any(marker in transcript_30[:100].lower() for marker in DEAD_ZONE_MARKERS):
        pacing -= 2
    if len(tokenize(transcript_30)) < 35:
        pacing -= 2

    if scene.cut_count is None:
        visual = 6
    elif scene.cut_count == 0:
        visual = 4
    elif 1 <= scene.cut_count <= 3:
        visual = 6
    elif 4 <= scene.cut_count <= 10:
        visual = 8
    else:
        visual = 7

    specificity = 4
    if re.search(r"\d", transcript_30):
        specificity += 2
    if any(marker in transcript_30 for marker in PROMISE_MARKERS):
        specificity += 2
    if len(tokenize(transcript_30)) > 70:
        specificity += 1

    target_fit = 5
    if target and keyword_overlap(target, transcript_30 + " " + package_text) > 0:
        target_fit = 8
    if any(x in transcript_30 for x in ["你", "新手", "创作者", "账号", "频道", "观众"]):
        target_fit = max(target_fit, 7)

    dims = {
        "hook_clarity": clamp_score(hook),
        "promise_match": clamp_score(promise_match),
        "first_value_time": clamp_score(fvt),
        "curiosity_loop": clamp_score(curiosity),
        "pacing": clamp_score(pacing),
        "visual_change": clamp_score(visual),
        "specificity": clamp_score(specificity),
        "target_viewer_fit": clamp_score(target_fit),
    }
    weights = {
        "hook_clarity": 0.15,
        "promise_match": 0.20,
        "first_value_time": 0.15,
        "curiosity_loop": 0.10,
        "pacing": 0.15,
        "visual_change": 0.10,
        "specificity": 0.10,
        "target_viewer_fit": 0.05,
    }
    total = round(sum(dims[k] * weights[k] for k in dims) * 10)
    if total < 50:
        risk = "High drop risk"
    elif total < 70:
        risk = "Medium drop risk"
    elif total < 85:
        risk = "Usable, needs targeted edits"
    else:
        risk = "Strong opening"
    return ScoreBreakdown(total_score=total, risk_level=risk, **dims)


def timestamp_diagnosis(
    transcript_30: str,
    subs: List[SubtitleLine],
    first_value: Optional[float],
    scene: SceneAudit,
    silence: SilenceAudit,
    score: ScoreBreakdown,
) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    first_text = transcript_30[:120]
    if any(marker in first_text.lower() for marker in DEAD_ZONE_MARKERS):
        issues.append({
            "time": "0-5s",
            "issue": "Opening starts with greeting/meta setup instead of viewer pain or payoff.",
            "fix": "Cut the greeting. Start with the specific problem, result, or contradiction promised by the title."
        })
    if first_value is None:
        issues.append({
            "time": "0-30s",
            "issue": "No clear first value detected in the first 30 seconds.",
            "fix": "Add one concrete insight, number, mistake, or answer before 15 seconds."
        })
    elif first_value > 15:
        issues.append({
            "time": f"{first_value:.1f}s",
            "issue": "First concrete value arrives too late.",
            "fix": "Move this value into the first 8-12 seconds."
        })
    if silence.silence_ratio is not None and silence.silence_ratio > 0.10:
        issues.append({
            "time": "0-30s",
            "issue": f"Detected silence ratio is about {silence.silence_ratio:.0%}.",
            "fix": "Tighten pauses, remove dead air, or add purposeful visual/audio transition."
        })
    if scene.cut_count is not None and scene.cut_count == 0:
        issues.append({
            "time": "0-30s",
            "issue": "No significant scene change detected.",
            "fix": "Add a visual change, crop, screenshot, B-roll, caption emphasis, or cutaway if performance alone is not strong."
        })
    if score.promise_match < 6:
        issues.append({
            "time": "0-10s",
            "issue": "Weak title/thumbnail-to-opening promise match.",
            "fix": "Say the title promise explicitly in the first sentence. Do not force viewers to infer the connection."
        })
    return issues


def default_edit_list(score: ScoreBreakdown, first_value: Optional[float]) -> List[str]:
    edits: List[str] = []
    if score.hook_clarity < 7:
        edits.append("Rewrite the first sentence so the viewer pain/result is obvious within 3 seconds.")
    if score.promise_match < 7:
        edits.append("Make the opening repeat or directly answer the title/thumbnail promise.")
    if first_value is None or first_value > 15:
        edits.append("Move the first concrete value into 0-15 seconds; ideally 0-8 seconds.")
    if score.pacing < 7:
        edits.append("Remove slow setup, greeting, repeated context, silence, and low-information pauses.")
    if score.visual_change < 7:
        edits.append("Add at least one meaningful visual change before 10 seconds and another before 25 seconds.")
    if not edits:
        edits.append("Keep the opening structure. Test title/thumbnail variants before changing the edit heavily.")
    return edits


def make_rewrite(metadata: Dict[str, Any], transcript_30: str) -> Dict[str, str]:
    title = metadata.get("title", "这个视频")
    target = metadata.get("target_viewer", "你")
    promise = metadata.get("video_promise", "解决这个问题")
    return {
        "0-3s": f"你点进来不是为了听铺垫，而是想知道：{title}",
        "3-8s": f"真正影响留存的，不是开头够不够炫，而是前几秒有没有兑现标题承诺。",
        "8-15s": f"我会用三个指标判断：承诺匹配、第一价值时间、节奏断点。",
        "15-25s": f"只要这三项有一个失控，观众很可能在30秒前离开。",
        "25-30s": f"先看第一个问题：你的开头有没有让{target}立刻确认这条视频值得继续看。",
    }


def make_markdown(result: AuditResult) -> str:
    m = result.metric_audit
    score = result.score
    metadata = result.metadata

    def fmt(x: Any, suffix: str = "") -> str:
        if x is None:
            return "N/A"
        if isinstance(x, float):
            return f"{x:.2f}{suffix}"
        return f"{x}{suffix}"

    diag_rows = "\n".join(
        f"| {d['time']} | {d['issue']} | {d['fix']} |" for d in result.timestamp_diagnosis
    ) or "| N/A | No major timestamp issue detected by heuristic script. | Validate with human review. |"

    edit_items = "\n".join(f"{i+1}. {item}" for i, item in enumerate(result.edit_list))
    rewrite_items = "\n".join(f"- **{k}**: {v}" for k, v in result.rewrite.items())

    return f"""# First 30s Retention Audit

## Verdict

- **Risk level**: {score.risk_level}
- **Score**: {score.total_score}/100
- **Main issue**: {main_issue(score)}

## Metadata

- **Title**: {metadata.get('title', 'N/A')}
- **Thumbnail text**: {metadata.get('thumbnail_text', 'N/A')}
- **Target viewer**: {metadata.get('target_viewer', 'N/A')}
- **Video promise**: {metadata.get('video_promise', 'N/A')}

## Metrics

- **CTR**: {fmt(m.ctr_percent, '%')}
- **Intro retention after 30s**: {fmt(m.intro_retention_30s_percent, '%')}
- **Packaging-to-30s conversion**: {fmt(m.packaging_to_30s_conversion_percent, '%')}
- **Retained viewers per 1,000 impressions**: {fmt(m.retained_30_per_1000_impressions)}
- **Estimated 30s retained views**: {fmt(m.retained_30_views_estimate)}
- **First value time**: {fmt(result.first_value_time, 's')}

## Score breakdown

| Dimension | Score |
|---|---:|
| Hook clarity | {score.hook_clarity}/10 |
| Promise match | {score.promise_match}/10 |
| First value time | {score.first_value_time}/10 |
| Curiosity loop | {score.curiosity_loop}/10 |
| Pacing | {score.pacing}/10 |
| Visual change | {score.visual_change}/10 |
| Specificity | {score.specificity}/10 |
| Target viewer fit | {score.target_viewer_fit}/10 |

## Video/Audio heuristic

- **Duration**: {fmt(result.video_probe.duration, 's')}
- **Resolution**: {result.video_probe.width or 'N/A'} × {result.video_probe.height or 'N/A'}
- **Scene changes in first 30s**: {fmt(result.scene_audit.cut_count)}
- **Silence seconds in first 30s**: {fmt(result.silence_audit.silence_seconds, 's')}
- **Silence ratio**: {fmt(result.silence_audit.silence_ratio)}
- **Timeline format**: {result.timeline_audit.format or 'N/A'}
- **Timeline events, estimated first 30s**: {fmt(result.timeline_audit.event_count_30s)}
- **Title/caption events, estimated first 30s**: {fmt(result.timeline_audit.title_or_caption_events_30s)}

## Timestamp diagnosis

| Time | Issue | Fix |
|---|---|---|
{diag_rows}

## Transcript excerpt, first 30s

```text
{result.transcript_text_30s[:1600] or 'N/A'}
```

## Edit list

{edit_items}

## Rewrite

{rewrite_items}

## Next test

- **A version**: Keep current topic, rebuild the first 15 seconds around the exact title promise.
- **B version**: Start with the strongest result/proof/conflict, then explain context after 15 seconds.
- **Measure**: CTR, Intro retention after 30s, average view duration, traffic source, and comments mentioning confusion or payoff.

## Boundary

This report is a heuristic pre-publish estimate unless YouTube Studio data was provided. Real first-30-second retention must be validated after publication.
"""


def main_issue(score: ScoreBreakdown) -> str:
    dims = {
        "hook clarity": score.hook_clarity,
        "promise match": score.promise_match,
        "first value time": score.first_value_time,
        "curiosity loop": score.curiosity_loop,
        "pacing": score.pacing,
        "visual change": score.visual_change,
        "specificity": score.specificity,
        "target viewer fit": score.target_viewer_fit,
    }
    worst = min(dims, key=dims.get)
    return f"Weakest area is {worst} ({dims[worst]}/10)."


def audit(args: argparse.Namespace) -> AuditResult:
    video = Path(args.video) if args.video else None
    transcript = Path(args.transcript) if args.transcript else None
    metadata_path = Path(args.metadata) if args.metadata else None
    analytics_path = Path(args.analytics) if args.analytics else None
    timeline_path = Path(args.timeline) if args.timeline else None

    metadata = load_metadata(metadata_path)
    subs = parse_transcript(transcript)
    txt30 = transcript_first_30s(subs)
    fvt = first_value_time(subs)
    probe = probe_video(video)
    scene = audit_scenes(video, threshold=args.scene_threshold)
    silence = audit_silence(video)
    timeline = audit_timeline(timeline_path)
    metrics = audit_metrics(analytics_path)
    score = compute_score(metadata, txt30, fvt, scene, silence)
    diags = timestamp_diagnosis(txt30, subs, fvt, scene, silence, score)
    edits = default_edit_list(score, fvt)
    rewrite = make_rewrite(metadata, txt30)
    return AuditResult(
        metadata=metadata,
        video_probe=probe,
        transcript_text_30s=txt30,
        first_value_time=fvt,
        scene_audit=scene,
        silence_audit=silence,
        timeline_audit=timeline,
        metric_audit=metrics,
        score=score,
        timestamp_diagnosis=diags,
        edit_list=edits,
        rewrite=rewrite,
    )


def to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, list):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    return obj


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit first 30 seconds for YouTube retention risk.")
    parser.add_argument("--video", help="Path to first30.mp4 or full video export.")
    parser.add_argument("--transcript", help="Path to .srt, .vtt, or .txt transcript.")
    parser.add_argument("--metadata", help="Path to metadata JSON.")
    parser.add_argument("--analytics", help="Path to YouTube Studio CSV.")
    parser.add_argument("--timeline", help="Path to FCPXML/XML/EDL editing timeline export.")
    parser.add_argument("--out-dir", default="reports", help="Output directory.")
    parser.add_argument("--scene-threshold", type=float, default=0.30, help="FFmpeg scene threshold.")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    result = audit(args)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "first30_retention_report.md"
    json_path = out_dir / "first30_retention_report.json"
    md_path.write_text(make_markdown(result), encoding="utf-8")
    json_path.write_text(json.dumps(to_jsonable(result), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    print(f"Score: {result.score.total_score}/100 | {result.score.risk_level}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
