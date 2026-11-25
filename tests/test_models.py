"""Behavioral tests for instagen core domain models."""

from pathlib import Path
import pytest
from pydantic import ValidationError

from instagen.models import HashtagBundle, ReelCandidate, ReelScoreBreakdown


def test_weighted_score_calculation() -> None:
    scores = ReelScoreBreakdown(
        hook_strength=80.0,
        sendability=60.0,
        narrative_loop=50.0,
        audio_dynamics=100.0,
        vertical_framing=90.0,
    )
    # 80*0.35 + 60*0.25 + 50*0.20 + 100*0.10 + 90*0.10 = 28 + 15 + 10 + 10 + 9 = 72.0
    assert scores.weighted_total == 72.0


def test_hashtag_bundle_enforces_five_tag_limit() -> None:
    with pytest.raises(ValidationError):
        HashtagBundle(
            seo_caption="Come ottimizzare il taglio video in 15 secondi",
            hashtags=["#a", "#b", "#c", "#d", "#e", "#f"],
        )


def test_hashtag_bundle_normalizes_hash_prefix() -> None:
    bundle = HashtagBundle(
        seo_caption="Guida pratica al montaggio verticale",
        hashtags=["MontaggioVideo", "#ReelItalia", "CreatorTips"],
    )
    assert bundle.hashtags == ["#MontaggioVideo", "#ReelItalia", "#CreatorTips"]


def test_reel_candidate_instantiation() -> None:
    candidate = ReelCandidate(
        source_path=Path("input/demo.mp4"),
        start_sec=12.5,
        end_sec=34.0,
        transcript="Ecco il punto chiave del video.",
        scores=ReelScoreBreakdown(
            hook_strength=90.0,
            sendability=80.0,
            narrative_loop=75.0,
            audio_dynamics=85.0,
            vertical_framing=95.0,
        ),
        hashtag_bundle=HashtagBundle(
            seo_caption="Il punto chiave per mantenere l'attenzione nei primi 3 secondi",
            hashtags=["#VideoEditing", "#HookStrategico", "#InstagenSeries"],
        ),
    )
    assert candidate.end_sec > candidate.start_sec
