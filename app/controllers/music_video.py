from __future__ import annotations

import os

import requests
from fastapi import APIRouter

router = APIRouter(prefix="/api/music-video", tags=["music-video"])

DEFAULT_CONTROL_URL = (
    "https://ai-music-video-studio-three.vercel.app/api/control/health"
)
DEFAULT_WORKER_URL = (
    "https://freelance-michigan-losses-depending.trycloudflare.com"
)


@router.get("/worker")
def get_music_video_worker():
    """Resolve the current AI Music Video Studio worker for the browser UI.

    The heavy render process stays on the user's Mac. Vercel only serves the
    control UI, so uploads and generation do not consume serverless runtime.
    """
    configured = os.getenv("MUSIC_VIDEO_WORKER_URL", "").strip()
    if configured:
        return {
            "ok": True,
            "worker_url": configured.rstrip("/"),
            "source": "env",
        }

    control_url = os.getenv("MUSIC_VIDEO_CONTROL_URL", DEFAULT_CONTROL_URL).strip()
    try:
        response = requests.get(control_url, timeout=8)
        response.raise_for_status()
        payload = response.json()
        worker_url = str(payload.get("worker_url", "") or "").strip()
        online = bool(payload.get("online"))
        if worker_url:
            return {
                "ok": online,
                "worker_url": worker_url.rstrip("/"),
                "source": "control-plane",
                "worker": payload.get("worker"),
            }
    except Exception as exc:
        return {
            "ok": False,
            "worker_url": DEFAULT_WORKER_URL,
            "source": "fallback",
            "error": str(exc),
        }

    return {
        "ok": False,
        "worker_url": DEFAULT_WORKER_URL,
        "source": "fallback",
    }
