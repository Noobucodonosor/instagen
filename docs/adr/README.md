# Architecture Decision Records (ADR) & Master Task Backlog — instagen

Questa cartella raccoglie gli **Architecture Decision Records (ADR)** e il **Backlog Operativo** del progetto **instagen** (`Noobucodonosor/instagen`), consolidando le decisioni architetturali, di sicurezza e di prodotto.

---

## Indice degli ADR

| ID | Titolo | Stato | Priorità | Autori / Fonti |
| :--- | :--- | :--- | :--- | :--- |
| **[ADR-0001](./0001-core-architecture.md)** | Architettura Core: Analisi, Montaggio Ritagli Reel e Strategia Hashtag | **Accettato** | **P1 — Alta** | `@Noobucodonosor` |

---

## Diagramma Architetturale del Sistema

```mermaid
flowchart LR
  subgraph Input["1. Sorgenti Locali (1080p)"]
    SRC["Video Sorgente"]
    SEG["PySceneDetect\n(Tagli & Scene)"]
    AUD["faster-whisper + FFmpeg astats\n(Trascritto & Energia RMS)"]
  end

  subgraph Core["2. Engine instagen"]
    VLM["VLM Scoring (Gemini 2.5 Pro)\nTop-K Ritagli"]
    HASH["Millennium's Bug Tail-Effect\nCaption SEO (125c) + 3-5 Tag CamelCase"]
    EDIT["Reel Assembler\nReframing 9:16 (606x1080) + faststart"]
  end

  subgraph Output["3. PublisherPort"]
    EXP["Fase 1: Export Assistito\n(reel.mp4, cover.jpg, caption_ready.txt, metadata.json)"]
    API["Fase 2: Instagram Graph API\n(Opzionale)"]
  end

  SRC --> SEG --> AUD --> VLM
  VLM --> EDIT
  VLM --> HASH
  HASH --> EXP
  EDIT --> EXP
  EXP -.->|"Adapter futuro"| API
```

---

## Master Task Backlog (Tutti i Task Censiti)

> **Nota:** Lo stato live (`Open` / `Closed`) di ciascun task è tracciato sulle **GitHub Issues** del repository. Usa `closes #<NumeroIssue>` nei commit per chiuderle automaticamente.

| Task ID | Issue | ADR | Titolo Task | File Coinvolti | Priorità | Assegnatari |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TASK-CORE-01** | `#1` *(Chiusa)* | [ADR-0001](./0001-core-architecture.md) | Discovery e decisione canale Instagram (Export assistito vs Graph API) | `docs/adr/0001-core-architecture.md` | **P1 — Alta** | `@Noobucodonosor` |
| **TASK-CORE-02** | `#2` | [ADR-0001](./0001-core-architecture.md) | Setup scheletro progetto, dipendenze e `.env.example` | `README.md`, `.env.example`, `pyproject.toml`, `src/instagen/` | **P1 — Alta** | `@Noobucodonosor` |
