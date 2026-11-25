# ADR-0001: Architettura Core — Analisi, Montaggio Ritagli Reel e Strategia Hashtag

- **Stato:** Proposto (`Proposed`)
- **Priorità:** P1 — Alta
- **Data:** 2026-11-25
- **Autori:** `@Noobucodonosor`
- **Fonti:** Discovery iniziale (`instagen`)

---

## 1. Contesto e Problema

L'obiettivo di **instagen** è analizzare contenuti/trend e **iniettare ritagli mirati all'interno di Reel** (montaggi di ritagli) abbinati a una strategia di hashtag con effetto a coda lunga (*"Millennium's Bug tail effect"*).

Prima di scrivere codice applicativo, è necessario risolvere due punti architetturali chiave:
1. **Canale di interfacciamento con Instagram:** pubblicazione diretta via Instagram Graph API ufficiale (richiede account Business/Creator collegato a pagina Meta e token OAuth) oppure pipeline di export assistito (generazione locale di Reel montato + caption/hashtag pronti per la pubblicazione).
2. **Modello di analisi e composizione:** come vengono selezionati i ritagli, su quali metriche/segnali si basa l'analisi e come viene costruita la sequenza di hashtag (*tail effect*).

---

## 2. Decisione Architetturale (Proposta Iniziale)

1. **Modulo Analisi & Hashtag Engine:**
   - Analizza gli input/trend configurati per determinare quali ritagli selezionare e quali hashtag a coda lunga associare (*Millennium's Bug tail effect*).
2. **Modulo Reel Assembler (Iniezione Ritagli):**
   - Compone il Reel finale combinando i ritagli selezionati e integrando gli overlay/metadati/hashtag previsti.
3. **Modulo Output / Delivery (Da confermare in `TASK-CORE-01`):**
   - **Opzione A (Consigliata per MVP):** Export locale strutturato (video `.mp4` verticale 9:16 + file testo/JSON con caption e set hashtag) per pubblicazione sicura senza rischi di ban o blocchi Meta App Review.
   - **Opzione B:** Integrazione Instagram Graph API ufficiale (Media Container + Publish) per account Business/Creator.

---

## 3. Conseguenze

- **Positive:** Separazione netta tra logica di analisi, generazione video e canale di pubblicazione; l'Opzione A permette di validare subito l'algoritmo di montaggio e hashtag senza blocchi burocratici delle API Meta.
- **Trade-off / Vincoli:** Finché `TASK-CORE-01` non è chiuso e l'ADR non passa ad `Accettato`, non si implementano connettori Instagram né scraping non autorizzato.

---

## 4. Task Operativi Collegati (con Definition of Done)

- [ ] **TASK-CORE-01**: **Discovery e decisione canale Instagram (Export assistito vs Graph API)**
  - *File coinvolti*: `docs/adr/0001-core-architecture.md`, `docs/adr/README.md`
  - *Acceptance Criteria*: Definiti i criteri di analisi dei ritagli, la struttura del "Millennium's Bug tail effect" sugli hashtag e scelto il canale di output (Opzione A o B), portando `ADR-0001` in stato `Accettato`.
  - *Verification Step*: Verifica della completezza di `ADR-0001` e aggiornamento di `docs/adr/README.md`.
- [ ] **TASK-CORE-02**: **Setup scheletro progetto, dipendenze e `.env.example`**
  - *File coinvolti*: `README.md`, `.env.example`
  - *Acceptance Criteria*: Struttura directory e stack confermato inizializzati, `.env.example` documentato senza segreti reali.
  - *Verification Step*: `python3 ~/.gemini/config/skills/adr-github-methodology/scripts/pre_release_check.py` supera tutti i controlli.
