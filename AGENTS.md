# AGENTS.md — Contesto & Linee Guida per Agenti AI e Sviluppatori

> **REGOLA AUREA (MANDATORY):**
> Prima di modificare l'architettura, toccare il modello dati, aggiungere endpoint o sviluppare nuove feature, **DEVI leggere [`docs/adr/README.md`](./docs/adr/README.md)** e gli ADR specifici nella cartella [`docs/adr/`](./docs/adr/).

---

## 1. Panoramica del Progetto

- **Nome Progetto:** `instagen`
- **Repository:** `Noobucodonosor/instagen`
- **Descrizione Sintetica:** Pipeline di analisi, selezione/montaggio di ritagli video per Instagram Reel con iniezione strategica di hashtag (*Millennium's Bug tail effect*).
- **Stack Tecnologico:** *(In definizione in [ADR-0001](./docs/adr/0001-core-architecture.md))*
  - **Core / Pipeline:** Da definire (es. Python + FFmpeg / MoviePy per ritagli e montaggio Reel)
  - **Analisi & Hashtag Engine:** Da definire (analisi trend/coda lunga hashtag)
  - **Interfaccia Instagram:** Da decidere in `TASK-CORE-01` (Export assistito vs Instagram Graph API ufficiale)

---

## 2. Mappa dei File Principali

| File / Cartella | Ruolo |
| :--- | :--- |
| [`docs/adr/README.md`](./docs/adr/README.md) | **Indice degli ADR**, diagramma architetturale Mermaid e **Master Task Backlog**. |
| [`docs/adr/0001-core-architecture.md`](./docs/adr/0001-core-architecture.md) | Architettura Core, pipeline ritagli Reel e strategia hashtag (*Proposto*). |
| `.github/ISSUE_TEMPLATE/` | Template standard per l'apertura di GitHub Issues (`adr_task.yml`, `bug_report.yml`). |
| `.github/PULL_REQUEST_TEMPLATE.md` | Checklist di PR allineata a ADR, Verification Step e modalità `Show` / `Ask`. |
| `.github/workflows/adr-pre-release.yml` | Gate CI automatico (file >50 MB, segreti, conformità `AGENTS.md` e `docs/adr/`). |

---

## 3. Metodologia di Lavoro (ADR + GitHub Issues)

1. **Ogni decisione architetturale o di sicurezza** è documentata in un file `docs/adr/NNNN-titolo.md`.
2. **Ogni task operativo** ha un codice univoco (`TASK-<MODULO>-XX`) censito sia nell'ADR di origine, sia in `docs/adr/README.md`, sia come **GitHub Issue**.
3. **Priorità Standard:**
   - `P0-critical`: Sicurezza, bug bloccanti di produzione, protezione credenziali/dati.
   - `P1-high`: Feature core, moduli verticali prioritari, integrazioni essenziali.
   - `P2-medium`: Evoluzioni pianificate, ottimizzazioni, moduli secondari.
4. **Sviluppo & Flusso GitHub (Vibe Coding Sicuro):**
   - **Bivio `Issue` vs `Branch`:** per task esplorativi/architetturali salva prima il piano in una Issue (*Plan-to-Issue*); apri un branch (`feat/TASK-XXX-01` o `vibe/<slug>`, con `git worktree` se lavori in parallelo) solo su task perimetrati. Scoperte fuori scope → nuova Issue separata, mai *scope drift*.
   - **Draft PR & Rollback sicuro:** apri presto una Draft PR (`gh pr create --draft`); usa micro-PR e **Squash Merge** su `main`. **Mai `git rebase -i`** (usa `git reset --soft` per salvare parti valide; `--force-with-lease` solo prima di review umane, altrimenti `git revert`). Se la sessione degrada, genera `handoff.md` (con i tentativi falliti) e riparti pulito.
   - **Flusso graduato (`Show` vs `Ask`):** modifiche `P0-critical`, sicurezza o cambi a `docs/adr/`, `AGENTS.md` e `.github/**` richiedono sempre review umana (**Ask**). L'agente non approva né fa auto-merge del proprio codice.
   - **Verification Step reale:** esegui sempre il test previsto nella Issue verificando il comportamento sul diff (non solo `%` di coverage), ispeziona `gh pr diff` e usa commit atomici:
     ```bash
     git commit -m "feat(TASK-XXX-01): descrizione sintetica della modifica (closes #N)"
     ```

---

## 4. Sicurezza & Regole Critiche

- **Mai committare segreti:** Il file `.env` e i database locali (`*.db`, `*.sqlite`) devono restare sempre in `.gitignore`. Ogni sviluppatore usa la propria chiave API locale in `.env`.
- **Conformità Piattaforma:** Nessuna automazione non autorizzata o scraping aggressivo su Instagram; valutare solo export assistito o Instagram Graph API ufficiale.
- **Verifica Pre-Release:** Prima di generare pacchetti di deploy o fare push di rilascio, esegui:
  ```bash
  python3 ~/.gemini/config/skills/adr-github-methodology/scripts/pre_release_check.py
  ```

---

## 5. Comandi Rapidi di Sviluppo e Test

```bash
# Lista GitHub Issues attive per priorità
gh issue list --limit 30

# Verifica pre-release locale
python3 ~/.gemini/config/skills/adr-github-methodology/scripts/pre_release_check.py
```
