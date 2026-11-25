# ADR-0001: Architettura Core — Analisi, Montaggio Ritagli Reel e Strategia Hashtag

- **Stato:** Accettato (`Accepted`)
- **Priorità:** P1 — Alta
- **Data:** 2026-11-25
- **Autori:** `@Noobucodonosor`
- **Fonti:** Discovery `TASK-CORE-01` (`instagen`), specifiche piattaforma Instagram (novembre 2026)

---

## 1. Contesto e Problema

L'obiettivo di **instagen** è analizzare video sorgente locali (prevalentemente `1080p`: interviste, tutorial, talking-head) e **iniettare i ritagli più efficaci in formato Reel 9:16**, abbinati a un blocco testo ottimizzato per la ricerca interna di Instagram.

La progettazione deve rispettare i vincoli reali della piattaforma a novembre 2026:
1. **Segnali del ranker Reels 2026:** superamento dei primi 3 secondi (hook), tempo di visione/replay, *likes per reach* e soprattutto *sends per reach* (condivisioni in DM), oltre ai filtri di originalità e qualità tecnica (niente watermark, niente audio muto).
2. **Nuove regole hashtag (dicembre 2024 – dicembre 2025):** rimozione del follow sugli hashtag e limite ufficiale a **massimo 5 hashtag** per post/Reel, con indicizzazione centrata su NLP della caption (primi 125 caratteri), OCR e parlato.
3. **Conformità e time-to-MVP:** evitare i colli di bottiglia iniziali della Instagram Graph API (hosting pubblico per Instagram Login, refresh token 60 giorni, App Review, assenza accesso alla libreria musicale nativa) e vietare categoricamente librerie non ufficiali ad alto rischio ban.

---

## 2. Decisione Architetturale

### 2.1 Pipeline ibrida di analisi e scoring dei ritagli
1. **Segmentazione strutturale (`PySceneDetect`):** rilevamento cambi scena tramite `AdaptiveDetector` (con `downscale_factor=2` per velocità) e dissolvenze con `ThresholdDetector`.
2. **Analisi audio e trascrizione (`faster-whisper` + `FFmpeg astats`):** trascrizione con VAD e timestamp a livello di parola, più estrazione RMS/picchi audio per individuare energia vocale ed enfasi.
3. **Scoring multimodale (`Gemini 2.5 Pro` via `google-genai`):** campionamento fotogrammi equidistanti + trascritto + metriche `astats` con output JSON deterministico (`pydantic`). La pipeline produce una **graduatoria top-k** (senza scartare irreversibilmente il girato) basata su pesi euristici iniziali da calibrare empiricamente:
   - **Forza dell'hook iniziale (35%)**: domanda, affermazione netta o cambio ritmo nei primi 1,7–3,0 s.
   - **Potenziale di invio DM / Sendability (25%)**: utilità pratica, sintesi memorabile o identificazione.
   - **Compattezza narrativa e loop (20%)**: struttura autonoma e chiusura ricollegabile all'inizio.
   - **Dinamica audio (10%)**: RMS medio e picchi da `astats`, assenza di silenzi morti.
   - **Idoneità al taglio verticale 9:16 (10%)**: soggetti stabili e centrabili senza testo tagliato ai bordi.

### 2.2 Reel Assembler & Reframing verticale 9:16
- **Tracciamento soggetto:** `PySceneDetect` + `MediaPipe` (ancoraggio volto) con fallback su `YOLO + ByteTrack` o *blurred padding* nelle scene senza volti.
- **Anti-tremolio:** banda morta (*deadband*) del 5% della larghezza frame, velocità massima di pan ~60 px/s oppure posizione statica media per singola inquadratura.
- **Risoluzione nativa:** per sorgenti `1080p`, export nativo **`606×1080`** (multiplo pari per H.264, superiore al minimo `540×960`, evitando upscaling distruttivi a `1080×1920`).
- **Specifiche `.mp4` Graph-API-ready:** contenitore MP4 con `-movflags +faststart`, H.264/HEVC progressivo `yuv420p`, GOP chiuso, 9:16, durata 5–90 s (<=100 MB), audio AAC `>=128 kbps` (max 48 kHz, <=8 MB).

### 2.3 Definizione formale: "Millennium's Bug tail effect" (Caption SEO + 5 Hashtag)
Con **"Millennium's Bug tail effect"** si definisce formalmente l'etichetta progettuale interna del motore testuale di `instagen`: invece dei vecchi 30 hashtag generici, il sistema combina **Caption SEO** (parole chiave mirate nei primi **125 caratteri** estratte da `faster-whisper` e VLM) con **3–5 hashtag a coda lunga in CamelCase** con rotazione automatica da tassonomia locale pre-curata:
- **Slot 1–2:** nicchia specifica / *long-tail* (argomento esatto del ritaglio).
- **Slot 3:** scenario o intento dell'utente.
- **Slot 4:** categoria media o tag geografico (vietati tag generici `#reels`, `#explore`, `#viral`, `#instagood`).
- **Slot 5:** tag di serie o brand (per collegare episodi ricorrenti dopo la rimozione delle serie native).

### 2.4 Canale di uscita: Opzione A (Export assistito locale) + `PublisherPort`
- **Fase 1 (MVP):** Export assistito locale dietro interfaccia disaccoppiata `PublisherPort`. Ogni Reel generato produce una cartella bundle contenente:
  - `reel.mp4` (conforme alle specifiche Graph API);
  - `cover.jpg` (frame 9:16 selezionato);
  - `caption_ready.txt` (Caption SEO + 3–5 hashtag pronti per copia/incolla);
  - `metadata.json` (score, timestamp, tag usati e metadati pronti per Fase 2).
- **Fase 2 (Opzionale):** Adapter `Instagram Graph API` ufficiale (preferibilmente flusso Facebook Login con `rupload.facebook.com` per upload locali o Instagram Login con URL pubblico).
- **Divieto esplicito:** è **categoricamente vietato** integrare librerie non ufficiali (`instagrapi`, emulation mobile o automazione browser non autorizzata).

---

## 3. Conseguenze

- **Positive:** MVP funzionante subito senza blocchi di App Review o token Meta; compatibilità con account Personal, Creator e Business; possibilità di aggiungere audio nativi in-app; file `.mp4` e `metadata.json` già pronti per la Fase 2 Graph API.
- **Trade-off / Vincoli:** L'analisi VLM cloud (`Gemini 2.5 Pro`) richiede connettività e chiave API (`VLM_API_KEY`); la pubblicazione in Fase 1 richiede un passaggio manuale da smartphone.

---

## 4. Task Operativi Collegati (con Definition of Done)

- [x] **TASK-CORE-01**: **Discovery e decisione canale Instagram (Export assistito vs Graph API)**
  - *File coinvolti*: `docs/adr/0001-core-architecture.md`, `docs/adr/README.md`, `AGENTS.md`
  - *Acceptance Criteria*: Definiti i criteri di analisi dei ritagli, la definizione formale di "Millennium's Bug tail effect" e scelto il canale di output (Opzione A MVP + `PublisherPort`), portando `ADR-0001` in stato `Accettato`.
  - *Verification Step*: `python3 ~/.gemini/config/skills/adr-github-methodology/scripts/pre_release_check.py`
- [ ] **TASK-CORE-02**: **Setup scheletro progetto, dipendenze e `.env.example`**
  - *File coinvolti*: `README.md`, `.env.example`, `pyproject.toml`, `src/instagen/`
  - *Acceptance Criteria*: Struttura directory core creata (`src/instagen/`), dipendenze dichiarate, `.env.example` documentato senza segreti reali e `README.md` allineato.
  - *Verification Step*: `python3 ~/.gemini/config/skills/adr-github-methodology/scripts/pre_release_check.py`
