#!/usr/bin/env python3
"""Hybrid grader for video presentation assignments (A3-style).

Pipeline:
  Python (this file): ffprobe duration, ffmpeg audio extraction + frame sampling,
                      faster-whisper transcription with speaker-change heuristics.
  Agent (LLM):        reads transcript + sampled frames, judges:
                      - Dominio del contenido (depth & accuracy)
                      - Participación equitativa (each member spoke)
                      - Ejemplos prácticos (demos/code shown)
                      - Habilidad de presentación (reading vs paraphrasing)

Time management is purely deterministic from ffprobe duration.

Usage:
    python3 grade_presentacion_template.py <video.mp4> --out <dir>
    # or batch:
    python3 grade_presentacion_template.py <folder-with-videos>
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Deterministic signals
# ─────────────────────────────────────────────────────────────────────────────

def ffprobe_duration(video: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())


def extract_audio(video: Path, out_wav: Path) -> Path:
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-i", str(video), "-ac", "1", "-ar", "16000", "-vn", str(out_wav)],
        check=True,
    )
    return out_wav


def sample_frames(video: Path, out_dir: Path, n: int = 6) -> list[Path]:
    """Sample n evenly-spaced frames from the video."""
    out_dir.mkdir(parents=True, exist_ok=True)
    duration = ffprobe_duration(video)
    interval = max(1, int(duration / n))
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-i", str(video), "-vf", f"fps=1/{interval}",
         "-frames:v", str(n), str(out_dir / "frame_%02d.jpg")],
        check=True,
    )
    return sorted(out_dir.glob("frame_*.jpg"))


def transcribe(audio: Path, model_size: str = "small", language: str = "es") -> dict:
    """Use faster-whisper to transcribe. Returns {language, duration, segments}."""
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio), language=language, vad_filter=True)
    out = []
    for s in segments:
        out.append({"start": round(s.start, 2), "end": round(s.end, 2),
                    "text": s.text.strip()})
    return {"language": info.language, "duration": info.duration,
            "language_probability": info.language_probability, "segments": out}


# ─────────────────────────────────────────────────────────────────────────────
# Heuristic speaker-change detection from transcript pauses
# ─────────────────────────────────────────────────────────────────────────────

def detect_speaker_segments(segments: list[dict], pause_threshold: float = 4.0) -> list[dict]:
    """Group transcript segments into turns by pause threshold.

    Returns list of `{start, end, text, segment_count}` per estimated turn.
    Not real diarization — just detects natural breaks. Useful as a signal
    that turns alternated (multiple turns ⇒ multiple speakers likely).
    """
    if not segments:
        return []
    turns = [{"start": segments[0]["start"], "end": segments[0]["end"],
              "text": segments[0]["text"], "segment_count": 1}]
    for s in segments[1:]:
        prev = turns[-1]
        if s["start"] - prev["end"] >= pause_threshold:
            turns.append({"start": s["start"], "end": s["end"],
                          "text": s["text"], "segment_count": 1})
        else:
            prev["end"] = s["end"]
            prev["text"] += " " + s["text"]
            prev["segment_count"] += 1
    return turns


# ─────────────────────────────────────────────────────────────────────────────
# Structural scoring
# ─────────────────────────────────────────────────────────────────────────────

def score_time(duration_sec: float) -> tuple[int, str]:
    """Gestión del tiempo: 8-12 min ⇒ 4, etc. Returns (level, note)."""
    m = duration_sec / 60.0
    if 8 <= m <= 12:
        return 4, f"{m:.1f} min — dentro del rango ideal (8-12)"
    if 6 <= m < 8 or 12 < m <= 14:
        return 3, f"{m:.1f} min — fuera del ideal por poco (6-8 o 12-14)"
    if 5 <= m < 6 or 14 < m <= 15:
        return 2, f"{m:.1f} min — corto/largo (5-6 o 14-15)"
    return 1, f"{m:.1f} min — fuera de rango (<5 o >15)"


# ─────────────────────────────────────────────────────────────────────────────
# Rubric metadata
# ─────────────────────────────────────────────────────────────────────────────

CRITERIA = [
    ("dominio", "Dominio del contenido", 20, "llm"),
    ("participacion", "Participación equitativa", 20, "hybrid"),  # turns + LLM confirm
    ("ejemplos", "Ejemplos prácticos", 20, "llm"),  # LLM judges slides+transcript
    ("habilidad", "Habilidad de presentación", 20, "llm"),
    ("tiempo", "Gestión del tiempo", 20, "structural"),
]


def build_findings(signals: dict, llm_scores: dict, recovered_from: str | None = None) -> dict:
    """signals must include: duration_sec, turns_estimate, language, frames_paths
       llm_scores must include: dominio, participacion, ejemplos, habilidad."""
    time_level, time_note = score_time(signals["duration_sec"])
    levels = {
        "dominio": llm_scores["dominio"],
        "participacion": llm_scores["participacion"],
        "ejemplos": llm_scores["ejemplos"],
        "habilidad": llm_scores["habilidad"],
        "tiempo": time_level,
    }
    notes = {
        "dominio": llm_scores.get("dominio_note", ""),
        "participacion": llm_scores.get("participacion_note", ""),
        "ejemplos": llm_scores.get("ejemplos_note", ""),
        "habilidad": llm_scores.get("habilidad_note", ""),
        "tiempo": time_note,
    }
    rubric = []
    total = 0
    for key, label, weight, _ in CRITERIA:
        lvl = levels[key]
        rubric.append({
            "criterion": label,
            "level": lvl,
            "max": 4,
            "weight_pct": weight,
            "note": notes[key] or {4: "Excelente", 3: "Bueno", 2: "Normal", 1: "Deficiente"}.get(lvl, "?"),
        })
        total += lvl * (weight / 4)
    score = round(total)
    missing = [r["criterion"] for r in rubric if r["level"] <= 2]
    return {
        "score": score,
        "rubric": rubric,
        "signals": {k: v for k, v in signals.items() if k != "frames_paths"},
        "missing": missing,
        "recovered_from": recovered_from,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline orchestrator (Python-side)
# ─────────────────────────────────────────────────────────────────────────────

def process_video(video: Path, out_dir: Path | None = None,
                  model_size: str = "small", frame_count: int = 6) -> dict:
    out_dir = out_dir or video.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    duration = ffprobe_duration(video)
    audio = extract_audio(video, out_dir / "audio.wav")
    frames = sample_frames(video, out_dir / "frames", n=frame_count)
    transcript = transcribe(audio, model_size=model_size)
    turns = detect_speaker_segments(transcript["segments"])

    # Persist
    (out_dir / "transcript.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=2))
    (out_dir / "transcript.txt").write_text("\n".join(s["text"] for s in transcript["segments"]))
    (out_dir / "turns.json").write_text(json.dumps(turns, ensure_ascii=False, indent=2))

    signals = {
        "duration_sec": duration,
        "duration_min": round(duration / 60, 2),
        "transcript_segments": len(transcript["segments"]),
        "turns_estimate": len(turns),
        "language": transcript["language"],
        "language_probability": transcript["language_probability"],
        "word_count": len(transcript["segments"]) and sum(len(s["text"].split()) for s in transcript["segments"]),
        "frames_paths": [str(f) for f in frames],
    }
    structural = {"tiempo": score_time(duration)}
    payload = {
        "video": str(video),
        "signals": signals,
        "structural": {"tiempo_level": structural["tiempo"][0], "tiempo_note": structural["tiempo"][1]},
        "ready_for_llm": True,
    }
    (out_dir / "STRUCTURAL.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


def main():
    if len(sys.argv) < 2:
        print("Usage: grade_presentacion_template.py <video.mp4|folder>")
        sys.exit(1)
    target = Path(sys.argv[1])
    if target.is_file():
        result = process_video(target)
        print(json.dumps(result["signals"], indent=2, ensure_ascii=False))
    else:
        for v in target.rglob("*.mp4"):
            print(f"Processing {v.name}...")
            try:
                r = process_video(v, out_dir=v.parent)
                sig = r["signals"]
                print(f"  duration={sig['duration_min']}min turns={sig['turns_estimate']} segs={sig['transcript_segments']}")
            except Exception as e:
                print(f"  ERROR: {e}")


if __name__ == "__main__":
    main()
