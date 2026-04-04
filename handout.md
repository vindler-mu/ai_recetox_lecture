# AI@RECETOX — Handout

**Opportunities and Limits of GenAI in Research**
7\. dubna 2026 | Vojtěch Velísek | velisek@sci.muni.cz

---

## 1. Klíčové pojmy

| Pojem | Co to je | Proč na tom záleží |
|-------|----------|---------------------|
| **Tokenizace** | Rozdělení textu na kousky (tokeny), které model zpracovává | Čeština = více tokenů = dražší a méně přesná práce |
| **Teplota** | Parametr ovlivňující "kreativitu" odpovědi (0 = deterministická, 1+ = kreativní) | Nenastavíte přímo, ale ovlivníte formulací promptu |
| **Embedding** | Převod textu na vektor čísel zachycující význam | Základ sémantického vyhledávání |
| **Halucinace** | Model generuje přesvědčivé, ale nepravdivé informace | Vždy ověřujte fakta, citace a čísla |
| **Bias** | Zkreslení dané nerovnoměrností trénovacích dat | Garbage in — garbage out |
| **RAG** | Retrieval-Augmented Generation — model hledá v externích zdrojích | Základ AI-powered vyhledávačů |
| **Kontext** | Vše, co model vidí v okamžiku generování odpovědi | Model nemá trvalou paměť |
| **Sycophant** | Model potvrzuje uživatele místo pravdivé odpovědi | Ztráta spolehlivosti |

---

## 2. AI na Masarykově univerzitě

| Nástroj | Pro koho | Model | Klíčové |
|---------|----------|-------|---------|
| **MS Copilot Chat** | Všichni na MU | GPT 5.3/5.4 | Práce s OneDrive a email |
| **MS Copilot for M365** | Rozšířená licence | GPT 5.3/5.4 | Integrace v Office apps |
| **Gemini** | Přes Google Workspace | Gemini 3/3.1 PRO | Integrace v Google apps |
| **AI as a Service** | Zaměstnanci (e-Infra.cz) | DeepSeek, GLM, Qwen | Data neopouští e-INFRA |

> Data u MS/Gemini jsou pod tenantem MU (zabezpečena, model se na nich netrénuje).

---

## 3. Infrastruktura AI — tři vrstvy

```
┌─────────────────────────────┐
│        APLIKACE             │  ← co vidíte (ChatGPT, Claude, Copilot)
│  UI, filtry, system prompt  │
├─────────────────────────────┤
│         SYSTÉM              │  ← pravidla, nástroje, RAG, API
│  konektory, feedback loops  │
├─────────────────────────────┤
│         MODEL               │  ← jádro (GPT, Claude, Gemini)
│  architektura + parametry   │
└─────────────────────────────┘
```

**Stejný model se chová jinak v různých aplikacích** — kvůli systémové vrstvě.

---

## 4. Přístupy k informacím v AI

| Aspekt | Symbolický | Sub-symbolický (dnešní AI) |
|--------|-----------|---------------------------|
| Reprezentace | Explicitní symboly a pravidla | Numerické parametry (váhy) |
| Logika | "Pokud A, pak B" | "Pravděpodobně B" |
| Transparentnost | Lze sledovat odvození | "Černá skříňka" |
| Znalosti | Pevně definované | Rozpuštěné v miliardách čísel |
| Příklad | Expert systémy, šachové enginy | LLM, rozpoznávání obrazu |

---

## 5. PROMPT Framework

| | Složka | Popis | Příklad |
|---|--------|-------|---------|
| **P** | Purpose | Co potřebuji | "Potřebuji analýzu metodických přístupů" |
| **R** | Role | Kdo má AI být | "Jsi analytický chemik se 15 lety zkušeností" |
| **O** | Objective | Konkrétní výstup | "Vytvoř srovnávací tabulku 4 metod" |
| **M** | Method | Jak postupovat | "Nejdřív definuj kritéria, pak porovnej" |
| **P** | Parameters | Formální požadavky | "Max 500 slov, tabulka, roky 2020-2026" |
| **T** | Tone | Styl komunikace | "Odborný, stručný, pro laboratorní zprávu" |

---

## 6. Promptovací techniky — rychlý přehled

| Technika | Kdy použít | Klíčový princip |
|----------|-----------|-----------------|
| **Zero-shot** | Jednoduché úlohy | Pouze instrukce, žádné příklady |
| **Chain of Thought** | Výpočty, logika | "Ukaž mezikroky" |
| **Tree of Thought** | Rozhodování | Paralelně více přístupů |
| **Self-consistency** | Kritické úlohy | Řeš vícekrát, porovnej |
| **Decomposition** | Komplexní úlohy | Rozlož na kroky |
| **Self-criticism** | Kvalitní texty | Vygeneruj → zkritizuj → přepiš |
| **Meta-prompting** | Nejistota | Nech AI navrhnout prompt |
| **Role/Persona** | Specifická perspektiva | "Jsi ..." |
| **Scaffolding** | Strukturované výstupy | Připrav kostru, AI doplní |

---

## 7. Instrument vs. Interpreter

```
INSTRUMENT                    ŠEDÁ ZÓNA                    INTERPRETER
     ←─────────────────────────────────────────────────────────→

Korektura gramatiky      AI navrhuje kód,          AI formuluje závěry
Formátování dat          já ho používám            z mých dat
Překlad textu            a zodpovídám za něj       Autorství nejasné
─────────────────────────────────────────────────────────────────
→ Není třeba deklarovat  → Uvést v metodice       → Uvést v metodice
                         → Reflektovat v limitech    a limitacích
                                                   → Zvážit, zda je to OK
```

**Klíčové otázky:**
- Kdo tu rozhoduje — já nebo AI?
- Umím výstup obhájit vlastními slovy?
- Kde na škále instrument–interpreter se právě nacházím?

---

## 8. Checklist pro kritické myšlení

- [ ] **SMELL TEST** — Zní to rozumně, nebo jako generická fráze?
- [ ] **NUMBER CHECK** — Jsou čísla realistická? Nejsou příliš specifická?
- [ ] **SOURCE HUNT** — Existují uvedené zdroje? Lze je najít?
- [ ] **LOGIC SCAN** — Následují argumenty logicky?
- [ ] **EXPERT GUT** — Co by řekl kolega z oboru?
- [ ] **CHALLENGE PROMPT** — Zeptejte se AI: "Jsi si jistá? Uveď zdroj."

---

## 9. AI-powered vyhledávání — nástroje

| Nástroj | Typ | Klíčová vlastnost |
|---------|-----|-------------------|
| **Perplexity** | AI vyhledávač | Vždy RAG, cituje zdroje |
| **Scite** | Akademický | Smart Citations — jak jsou články citovány |
| **Elicit** | Akademický | Extrakce dat z článků |
| **Consensus** | Akademický | Syntéza vědeckých závěrů |
| **Semantic Scholar** | Akademický | Sémantické hledání, open access |
| **NotebookLM** | Práce s texty | Nahrané dokumenty jako zdroj |
| **Scopus AI** | Databázový | RAG nad Scopus databází |
| **WOS Research Assis.** | Databázový | Generování dotazů z NL |

---

## 10. Fáze zapojení AI ve vyhledávání

| Fáze | Co se děje | Kdo rozhoduje |
|------|-----------|---------------|
| 1. Dotaz | Rozšíření a zpřesnění dotazu | Uživatel |
| 2. Retrieval | Hledání kandidátních dokumentů | Systém |
| 3. Ranking | Řazení podle relevance | Systém |
| 4. Enrichment | Sumarizace, extrakce klíčových bodů | Uživatel (ověření) |
| 5. Syntéza | Generování odpovědi (RAG) | AI |

> Čím dále ve fázích, tím více kontroly přebírá AI — a tím důležitější je kritické myšlení.

---

## 11. Python ukázky

V adresáři `ukazky/` najdete spustitelné Python skripty:

| Skript | Téma | Spuštění |
|--------|------|----------|
| `01_tokenizace.py` | Jak AI rozděluje text na tokeny | `python ukazky/01_tokenizace.py` |
| `02_teplota.py` | Vliv teploty na výběr dalšího slova | `python ukazky/02_teplota.py` |
| `03_semanticke_vyhledavani.py` | Keyword vs. sémantické hledání | `python ukazky/03_semanticke_vyhledavani.py` |
| `04_halucinace_cviceni.py` | Kvíz: rozpoznej halucinaci (interaktivní) | `python ukazky/04_halucinace_cviceni.py` |
| `05_prompt_srovnani.py` | Přehled promptovacích technik | `python ukazky/05_prompt_srovnani.py` |
| `06_bias_demo.py` | Bias v datech — garbage in, garbage out | `python ukazky/06_bias_demo.py` |

Požadavky: Python 3.10+ (skripty 01-06 nepotřebují žádné externí knihovny).

---

## 12. Co se nemění

- Potřeba definovat informační potřebu
- Kritický přístup k sobě i nástrojům
- Digitální kompetence
- Hodnota iterace
- Znalost vyhledávacích metodologií

---

## 13. Užitečné odkazy

- Artificial Intelligence | Central Library | MUNI SCI
- LMArena (srovnání modelů)
- Stockholmská úmluva (POPs)
- REACH registrace (ECHA)

---

*© 2026 Vojtěch Velísek | CC BY-NC 4.0*
*Vytvořeno s podporou Claude (Anthropic)*
