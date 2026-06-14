#!/usr/bin/env python3
"""
Generate a YouTube thumbnail image with the OpenAI Images API.

Author: Cruz Olli

Creator-facing default workflow label: GPT img2
API model: configurable with --model or OPENAI_IMAGE_MODEL
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Tuple


def read_json(path: Path | None) -> Dict[str, Any]:
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def thumbnail_concepts(metadata: Dict[str, Any]) -> List[Dict[str, str]]:
    topic = metadata.get("topic") or metadata.get("video_topic") or "YouTube thumbnail"
    emotion = metadata.get("thumbnail_emotion") or "surprised, decisive"
    return [
        {
            "visual": f"one dominant subject plus the strongest payoff shot for {topic}",
            "text": metadata.get("thumbnail_text") or "Do not miss this",
            "why": f"best default for a direct promise; emotion={emotion}",
        },
        {
            "visual": "before/after contrast with one obvious result gap",
            "text": "Big difference",
            "why": "good when the video contains measurable change or transformation",
        },
        {
            "visual": "tight close-up, simple background, one strong marker or circle",
            "text": "Look here",
            "why": "good for mobile readability and feed-size legibility",
        },
    ]


def build_prompts(metadata: Dict[str, Any]) -> Tuple[str, List[str]]:
    viewer = str(metadata.get("target_viewer") or "YouTube viewer").strip()
    topic = str(metadata.get("topic") or metadata.get("video_topic") or "the video topic").strip()
    emotion = str(metadata.get("thumbnail_emotion") or "surprised, decisive").strip()
    style = str(
        metadata.get("thumbnail_style_notes")
        or "high contrast, clean background, one clear focal subject, mobile readable, no clutter"
    ).strip()
    concepts = thumbnail_concepts(metadata)
    primary = (
        f"Create a YouTube thumbnail for {viewer}. Topic: {topic}. "
        f"Use {concepts[0]['visual']}. Emotional tone: {emotion}. "
        f"Include text-safe space for '{concepts[0]['text']}'. "
        f"Style: {style}. Make it bold, clickable, and easy to read on a phone feed."
    )
    alternates = [
        (
            f"Create a YouTube thumbnail focused on contrast. Topic: {topic}. "
            f"Use {concepts[1]['visual']}. Emotional tone: {emotion}. "
            f"Keep the composition simple and highly legible on mobile."
        ),
        (
            f"Create a clean, high-readability YouTube thumbnail. Topic: {topic}. "
            f"Use {concepts[2]['visual']}. Emotional tone: {emotion}. "
            f"Make one subject dominate the frame and preserve obvious text-safe space."
        ),
    ]
    return primary, alternates


def request_image(api_key: str, model: str, prompt: str, size: str, background: str) -> bytes:
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "background": background,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Images API request failed: {exc.code} {body}") from exc

    data = result.get("data") or []
    if not data:
        raise RuntimeError(f"Images API returned no image data: {result}")
    b64 = data[0].get("b64_json")
    if not b64:
        raise RuntimeError(f"Images API response missing b64_json: {result}")
    return base64.b64decode(b64)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a thumbnail image from metadata with the OpenAI Images API.")
    parser.add_argument("--metadata", default="metadata/upload_package.json", help="Path to upload-package metadata JSON.")
    parser.add_argument("--prompt", default="", help="Optional explicit prompt. If omitted, build from metadata.")
    parser.add_argument("--variant", choices=["primary", "alt-a", "alt-b"], default="primary", help="Which built-in prompt variant to use.")
    parser.add_argument("--model", default=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1"), help="Images API model. Workflow label remains GPT img2.")
    parser.add_argument("--size", default="1536x1024", help="Image size for generation.")
    parser.add_argument("--background", default="opaque", help="Background mode sent to the Images API.")
    parser.add_argument("--out", default="thumbnails/generated_thumbnail_primary.png", help="Output PNG path.")
    parser.add_argument("--save-prompt", default="", help="Optional path to save the final prompt text.")
    parser.add_argument("--save-metadata", default="", help="Optional path to save generation metadata JSON.")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required to generate thumbnail images.")

    metadata_path = Path(args.metadata).resolve()
    metadata = read_json(metadata_path)
    primary, alts = build_prompts(metadata)
    built_prompt = primary if args.variant == "primary" else alts[0] if args.variant == "alt-a" else alts[1]
    prompt = args.prompt.strip() or built_prompt

    image_bytes = request_image(api_key, args.model, prompt, args.size, args.background)

    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(image_bytes)

    if args.save_prompt:
        prompt_path = Path(args.save_prompt).resolve()
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(prompt, encoding="utf-8")

    if args.save_metadata:
        meta_out = Path(args.save_metadata).resolve()
        meta_out.parent.mkdir(parents=True, exist_ok=True)
        meta_out.write_text(
            json.dumps(
                {
                    "workflow_model_label": "gpt img2",
                    "api_model": args.model,
                    "size": args.size,
                    "background": args.background,
                    "prompt": prompt,
                    "output_path": str(out_path),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    print(f"Generated thumbnail: {out_path}")
    print("Workflow default: GPT img2")
    print(f"API model used: {args.model}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
