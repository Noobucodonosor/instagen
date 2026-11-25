"""Core domain models and ports for instagen (ADR-0001)."""

from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, Field, field_validator


class ReelScoreBreakdown(BaseModel):
    """Heuristic 5-dimension scoring aligned with Reels 2026 signals."""

    hook_strength: float = Field(..., ge=0.0, le=100.0)
    sendability: float = Field(..., ge=0.0, le=100.0)
    narrative_loop: float = Field(..., ge=0.0, le=100.0)
    audio_dynamics: float = Field(..., ge=0.0, le=100.0)
    vertical_framing: float = Field(..., ge=0.0, le=100.0)

    @property
    def weighted_total(self) -> float:
        """Compute weighted score (35/25/20/10/10)."""
        return round(
            self.hook_strength * 0.35
            + self.sendability * 0.25
            + self.narrative_loop * 0.20
            + self.audio_dynamics * 0.10
            + self.vertical_framing * 0.10,
            2,
        )


class HashtagBundle(BaseModel):
    """Caption SEO + 3-5 CamelCase long-tail hashtags (Millennium's Bug tail effect)."""

    seo_caption: str = Field(..., min_length=1)
    hashtags: list[str] = Field(..., min_length=1, max_length=5)

    @field_validator("hashtags")
    @classmethod
    def validate_hashtags(cls, tags: list[str]) -> list[str]:
        cleaned: list[str] = []
        for tag in tags:
            normalized = tag.strip()
            if not normalized.startswith("#"):
                normalized = f"#{normalized}"
            cleaned.append(normalized)
        return cleaned


class ReelCandidate(BaseModel):
    """Candidate clip extracted from local source video."""

    source_path: Path
    start_sec: float = Field(..., ge=0.0)
    end_sec: float = Field(..., gt=0.0)
    transcript: str = ""
    scores: ReelScoreBreakdown
    hashtag_bundle: HashtagBundle


class PublisherPort(Protocol):
    """Decoupled output port (Phase 1: local assisted export; Phase 2: Graph API)."""

    def publish(self, candidate: ReelCandidate, output_dir: Path) -> Path:
        """Export or publish a Reel bundle and return the target path/URI."""
        ...
