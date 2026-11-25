# instagen

Pipeline di analisi, selezione/montaggio di ritagli video per **Instagram Reel** (`9:16`) con strategia di **Caption SEO + hashtag a coda lunga** (*Millennium's Bug tail effect*).

> **Architettura & Decisioni:** Consulta [`docs/adr/README.md`](./docs/adr/README.md) e [`docs/adr/0001-core-architecture.md`](./docs/adr/0001-core-architecture.md) prima di modificare la pipeline.

## Prerequisiti di Sistema

- **Python 3.11+**
- **`ffmpeg` e `ffprobe`** installati e disponibili nel `PATH` (su macOS: `brew install ffmpeg`).

## Setup Rapido

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Compila `VLM_API_KEY` nel file `.env` locale (non tracciato da Git).

## Output MVP (Fase 1: Export Assistito)

Per ogni Reel selezionato, `instagen` genera una cartella bundle pronta per la pubblicazione manuale (e compatibile con il futuro adapter Instagram Graph API):

- `reel.mp4` — video verticale `606×1080` (da sorgenti `1080p`), H.264 `yuv420p`, `-movflags +faststart`, audio AAC `>=128 kbps`.
- `cover.jpg` — copertina `9:16` estratta dal ritaglio.
- `caption_ready.txt` — Caption SEO (primi 125 caratteri ottimizzati) + 3–5 hashtag CamelCase.
- `metadata.json` — score delle 5 dimensioni, timestamp e metadati pronti per Fase 2.

## Verifica & Test

```bash
pytest
python3 ~/.gemini/config/skills/adr-github-methodology/scripts/pre_release_check.py
```
