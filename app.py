#!/usr/bin/env python3
"""
AI@RECETOX -- Interactive lecture companion
Run: streamlit run app.py
"""

import streamlit as st
import math
import random
import tiktoken
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI@RECETOX",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═════════════════════════════════════════════════════════════════════════
#  TRANSLATIONS
# ═════════════════════════════════════════════════════════════════════════
T = {
    # ── Sidebar / navigation ─────────────────────────────────────────────
    "subtitle": {
        "cs": "Příležitosti a limity GenAI ve výzkumu",
        "en": "Opportunities and Limits of GenAI in Research",
    },
    "date_author": {
        "cs": "7. dubna 2026 | Vojtěch Velísek",
        "en": "7 April 2026 | Vojtěch Velísek",
    },
    "nav_label": {
        "cs": "Vyberte ukázku:",
        "en": "Select a demo:",
    },
    "pages": {
        "cs": [
            "Úvod",
            "1. Tokenizace",
            "2. Teplota",
            "3. Sémantické vyhledávání",
            "4. Halucinace — kvíz",
            "5. Prompting",
            "6. Bias v datech",
            "7. Kalkulačka ceny",
            "8. Kontextové okno",
            "📋 Cheat Sheet",
        ],
        "en": [
            "Introduction",
            "1. Tokenization",
            "2. Temperature",
            "3. Semantic Search",
            "4. Hallucination Quiz",
            "5. Prompting",
            "6. Bias in Data",
            "7. Cost Calculator",
            "8. Context Window",
            "📋 Cheat Sheet",
        ],
    },

    # ── Intro page ────────────────────────────────────────────────────────
    "intro_title": {
        "cs": "🧪 AI@RECETOX — Interaktivní ukázky",
        "en": "🧪 AI@RECETOX — Interactive Demos",
    },
    "intro_body": {
        "cs": """Vítejte v interaktivním doplňku k přednášce **Příležitosti a limity GenAI ve výzkumu**.

Vyberte ukázku v levém panelu a experimentujte s koncepty, o kterých mluvíme.

> ⚠️ **Důležité:** Všechny ukázky v této aplikaci jsou **zjednodušené ilustrace** principů AI.
> Skutečné modely jsou mnohem komplexnější. Cílem je budovat intuici, ne přesně replikovat chování AI.""",
        "en": """Welcome to the interactive companion for the lecture **Opportunities and Limits of GenAI in Research**.

Choose a demo in the left panel and experiment with the concepts we discuss.

> ⚠️ **Important:** All demos in this app are **simplified illustrations** of AI principles.
> Real models are far more complex. The goal is to build intuition, not to precisely replicate AI behavior.""",
    },
    "intro_cards": {
        "cs": [
            ("🔤 Tokenizace", "Jak AI rozděluje text a proč čeština stojí víc."),
            ("🌡️ Teplota", "Jak teplota ovlivňuje kreativitu vs. přesnost."),
            ("🔍 Sémantické vyhledávání", "Proč AI rozumí významu, ne jen slovům."),
            ("🎭 Halucinace", "Rozpoznáte, co je pravda a co si AI vymyslela?"),
            ("💬 Prompting", "Techniky a šablony pro výzkum na RECETOX."),
            ("⚖️ Bias v datech", "Garbage in — garbage out."),
            ("💰 Kalkulačka ceny", "Kolik stojí váš prompt v různých modelech?"),
            ("📏 Kontextové okno", "Kolik textu se vejde do paměti AI?"),
            ("📋 Cheat Sheet", "Vše podstatné na jednom místě."),
        ],
        "en": [
            ("🔤 Tokenization", "How AI splits text and why Czech costs more."),
            ("🌡️ Temperature", "How temperature affects creativity vs. precision."),
            ("🔍 Semantic Search", "Why AI understands meaning, not just words."),
            ("🎭 Hallucinations", "Can you tell what is true and what AI made up?"),
            ("💬 Prompting", "Techniques and templates for RECETOX research."),
            ("⚖️ Bias in Data", "Garbage in — garbage out."),
            ("💰 Cost Calculator", "How much does your prompt cost across models?"),
            ("📏 Context Window", "How much text fits in AI's memory?"),
            ("📋 Cheat Sheet", "Everything essential in one place."),
        ],
    },

    # ── Disclaimers ───────────────────────────────────────────────────────
    "disclaimer_illustration": {
        "cs": "⚠️ **Toto je zjednodušená ilustrace.** Skutečné AI modely fungují komplexněji. Cílem je ukázat princip.",
        "en": "⚠️ **This is a simplified illustration.** Real AI models work in more complex ways. The goal is to show the principle.",
    },
}


def t(key):
    """Get translated string for current language."""
    lang = st.session_state.get("lang", "cs")
    entry = T.get(key, {})
    return entry.get(lang, entry.get("cs", f"[{key}]"))


# ── Sidebar ──────────────────────────────────────────────────────────────
lang = st.sidebar.radio("🌐", ["🇨🇿 Čeština", "🇬🇧 English"], horizontal=True, label_visibility="collapsed")
st.session_state["lang"] = "cs" if "Čeština" in lang else "en"
L = st.session_state["lang"]

st.sidebar.title("AI@RECETOX")
st.sidebar.markdown(f"**{t('subtitle')}**")
st.sidebar.markdown(t("date_author"))
st.sidebar.markdown("---")

pages = t("pages")
page = st.sidebar.radio(t("nav_label"), pages)
page_idx = pages.index(page)


# ── Shared utilities ─────────────────────────────────────────────────────
COLORS = [
    "#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#00BCD4", "#F44336",
    "#8BC34A", "#3F51B5", "#FFEB3B", "#E91E63", "#009688", "#FF5722",
]

@st.cache_resource
def get_encoder():
    return tiktoken.get_encoding("o200k_base")

def real_tokenize(text):
    enc = get_encoder()
    token_ids = enc.encode(text)
    return [enc.decode([tid]) for tid in token_ids]

def render_tokens_html(tokens):
    html = '<div style="line-height: 2.4; margin: 10px 0;">'
    for i, token in enumerate(tokens):
        color = COLORS[i % len(COLORS)]
        display = token.replace(" ", "⎵").replace("\n", "↵").replace("<", "&lt;").replace(">", "&gt;")
        html += (
            f'<span style="background-color: {color}; color: white; '
            f'padding: 4px 8px; margin: 2px; border-radius: 4px; '
            f'font-family: monospace; font-size: 14px; display: inline-block;">'
            f'{display}</span>'
        )
    html += '</div>'
    return html

def softmax(logits, temperature):
    if temperature <= 0:
        temperature = 0.001
    scaled = [x / temperature for x in logits]
    max_val = max(scaled)
    exps = [math.exp(x - max_val) for x in scaled]
    total = sum(exps)
    return [e / total for e in exps]


# ═════════════════════════════════════════════════════════════════════════
#  PAGE: INTRO
# ═════════════════════════════════════════════════════════════════════════
if page_idx == 0:
    st.title(t("intro_title"))
    st.markdown(t("intro_body"))

    cards = t("intro_cards")
    cols = st.columns(3)
    for i, (title, desc) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"### {title}")
            st.markdown(desc)

    st.markdown("---")
    if L == "cs":
        st.info("💡 **Tip:** Každou ukázku si můžete vyzkoušet interaktivně — měňte parametry, zadávejte vlastní texty, zkoušejte různé varianty.")
    else:
        st.info("💡 **Tip:** Each demo is interactive — change parameters, enter your own text, try different variants.")


# ═════════════════════════════════════════════════════════════════════════
#  PAGE 1: TOKENIZATION
# ═════════════════════════════════════════════════════════════════════════
elif page_idx == 1:
    if L == "cs":
        st.title("🔤 Tokenizace — Jak AI rozděluje text")
        st.markdown("""
**Tokenizace** je proces rozdělení textu na menší kousky zvané **tokeny**. Model nevidí slova, věty, ani písmena — vidí tokeny.

**Jak to funguje?** Tokenizer má slovník (u GPT modelů ~200 000 položek). Běžná anglická slova jako "environmental" jsou v tomto slovníku jako **jeden token**. České slovo "environmentální" tam celé není — proto se rozloží na víc kousků.

Tato ukázka používá **skutečný tokenizer** (`o200k_base`) — stejný, jaký používají modely GPT.
        """)
        st.info(t("disclaimer_illustration"))
    else:
        st.title("🔤 Tokenization — How AI Splits Text")
        st.markdown("""
**Tokenization** splits text into smaller chunks called **tokens**. The model doesn't see words, sentences, or letters — it sees tokens.

**How does it work?** The tokenizer has a vocabulary (~200,000 entries for GPT models). Common English words like "environmental" exist as a **single token**. Czech "environmentální" is not in the vocabulary as a whole — so it gets split into multiple pieces.

This demo uses the **real tokenizer** (`o200k_base`) — the same one used by GPT models.
        """)
        st.info(t("disclaimer_illustration"))

    st.markdown(f"### {'Vyzkoušejte si to' if L == 'cs' else 'Try it yourself'}")
    col1, col2 = st.columns(2)
    with col1:
        en_text = st.text_input(
            "English text:" if L == "en" else "Anglický text:",
            "The environmental contamination was investigated.")
    with col2:
        cs_text = st.text_input(
            "Czech text:" if L == "en" else "Český text:",
            "Environmentální kontaminace byla prozkoumána.")

    en_tokens = real_tokenize(en_text)
    cs_tokens = real_tokenize(cs_text)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**EN** — {len(en_tokens)} {'tokens' if L == 'en' else 'tokenů'}")
        st.markdown(render_tokens_html(en_tokens), unsafe_allow_html=True)
    with col2:
        st.markdown(f"**CS** — {len(cs_tokens)} {'tokens' if L == 'en' else 'tokenů'}")
        st.markdown(render_tokens_html(cs_tokens), unsafe_allow_html=True)

    if en_tokens:
        ratio = len(cs_tokens) / len(en_tokens)
        delta = len(cs_tokens) - len(en_tokens)
        c1, c2, c3 = st.columns(3)
        c1.metric("EN", len(en_tokens))
        c2.metric("CS", len(cs_tokens), delta=f"+{delta}" if delta > 0 else str(delta))
        c3.metric("CS/EN", f"{ratio:.2f}x")

    st.markdown(f"### {'Odborné termíny (RECETOX)' if L == 'cs' else 'Scientific Terms (RECETOX)'}")
    terms = [
        ("polychlorinated biphenyls", "polychlorované bifenyly"),
        ("persistent organic pollutants", "perzistentní organické polutanty"),
        ("endocrine disruptors in drinking water", "endokrinní disruptory v pitné vodě"),
        ("heavy metals in soil samples", "těžké kovy v půdních vzorcích"),
        ("per- and polyfluoroalkyl substances", "per- a polyfluoralkylové látky"),
    ]
    data = []
    for en, cs in terms:
        en_t = len(real_tokenize(en))
        cs_t = len(real_tokenize(cs))
        r = cs_t / en_t if en_t else 0
        data.append({"EN": en, "EN tokens": en_t, "CS": cs, "CS tokens": cs_t, f"{'Poměr' if L == 'cs' else 'Ratio'}": f"{r:.1f}x"})
    st.dataframe(data, use_container_width=True)

    # Letter counting
    st.markdown(f"### {'Proč AI špatně počítá písmena' if L == 'cs' else 'Why AI Miscounts Letters'}")
    if L == "cs":
        st.markdown("Model nevidí jednotlivá písmena — vidí tokeny. Proto když se zeptáte \"Kolik písmen R je ve slově strawberry?\", model musí hádat z tokenů, ne z písmen.")
    else:
        st.markdown("The model doesn't see individual letters — it sees tokens. That's why when you ask \"How many R's are in strawberry?\", the model guesses from tokens, not letters.")

    word = st.text_input("Slovo / Word:", "strawberry")
    if word:
        tokens = real_tokenize(word)
        st.markdown(render_tokens_html(tokens), unsafe_allow_html=True)
        if L == "cs":
            st.markdown(f"Model vidí **{len(tokens)} token(y)**, ne **{len(word)} písmen**. Tokeny: `{tokens}`")
        else:
            st.markdown(f"Model sees **{len(tokens)} token(s)**, not **{len(word)} letters**. Tokens: `{tokens}`")

    if L == "cs":
        st.markdown("""
### Proč na tom záleží?
| Aspekt | Důsledek |
|--------|----------|
| **Cena** | Platíte za tokeny — čeština stojí o ~50-100 % víc než angličtina |
| **Kontext** | Kontextové okno má limit (200k–1M tokenů) — čeština zabere víc místa |
| **Kvalita** | `environmental` = 1 token (model zná dobře), `environmentální` = 2+ tokenů (méně přesné) |
| **Aritmetika** | Model nevidí písmena, vidí tokeny — proto špatně počítá |
| **Vyhledávání** | České odborné termíny se rozpadají na kousky a mohou ztratit specifický význam |
        """)
    else:
        st.markdown("""
### Why Does It Matter?
| Aspect | Consequence |
|--------|------------|
| **Cost** | You pay per token — Czech costs ~50-100% more than English |
| **Context** | Context window has a limit (200k–1M tokens) — Czech takes more space |
| **Quality** | `environmental` = 1 token (well-known), `environmentální` = 2+ tokens (less precise) |
| **Arithmetic** | Model sees tokens, not letters — that's why it miscounts |
| **Search** | Czech technical terms break into pieces and may lose specific meaning |
        """)


# ═════════════════════════════════════════════════════════════════════════
#  PAGE 2: TEMPERATURE
# ═════════════════════════════════════════════════════════════════════════
elif page_idx == 2:
    if L == "cs":
        st.title("🌡️ Teplota — Kreativita vs. přesnost")
        st.markdown("""
**Teplota** je parametr, který ovlivňuje, jak model vybírá další token (slovo).

**Nízká teplota** (0.1–0.3) = model téměř vždy vybere nejpravděpodobnější slovo. Výstup je **předvídatelný a konzistentní**.

**Vysoká teplota** (1.0+) = model častěji vybere i méně pravděpodobná slova. Výstup je **kreativnější, ale méně spolehlivý**.

Zkuste posunout slider a sledujte, jak se mění distribuce pravděpodobností.
        """)
        st.info(t("disclaimer_illustration"))
        context = "Kontaminace půdy byla"
    else:
        st.title("🌡️ Temperature — Creativity vs. Precision")
        st.markdown("""
**Temperature** is a parameter that controls how the model picks the next token (word).

**Low temperature** (0.1–0.3) = the model almost always picks the most probable word. Output is **predictable and consistent**.

**High temperature** (1.0+) = the model more often picks less probable words. Output is **more creative but less reliable**.

Try moving the slider and watch how the probability distribution changes.
        """)
        st.info(t("disclaimer_illustration"))
        context = "Soil contamination was"

    candidates_cs = [("zjištěna", 3.2), ("potvrzena", 2.8), ("analyzována", 2.1),
                     ("zkoumána", 1.5), ("ignorována", 0.3), ("oslavována", -1.0)]
    candidates_en = [("confirmed", 3.2), ("detected", 2.8), ("analyzed", 2.1),
                     ("studied", 1.5), ("ignored", 0.3), ("celebrated", -1.0)]
    candidates = candidates_cs if L == "cs" else candidates_en
    tokens = [c[0] for c in candidates]
    logits = [c[1] for c in candidates]

    st.markdown(f'### {"Kontext" if L == "cs" else "Context"}: *"{context} ___"*')

    temp = st.slider(
        "🌡️ Temperature:" if L == "en" else "🌡️ Teplota:",
        min_value=0.05, max_value=2.5, value=0.7, step=0.05)

    probs = softmax(logits, temp)

    if temp <= 0.3:
        label = "🔵 DETERMINISTICKÁ" if L == "cs" else "🔵 DETERMINISTIC"
    elif temp <= 0.7:
        label = "🟡 VYVÁŽENÁ" if L == "cs" else "🟡 BALANCED"
    else:
        label = "🔴 KREATIVNÍ" if L == "cs" else "🔴 CREATIVE"
    st.markdown(f"#### {label}")

    chart_data = pd.DataFrame({
        ("Slovo" if L == "cs" else "Word"): tokens,
        ("Pravděpodobnost (%)" if L == "cs" else "Probability (%)"): [p * 100 for p in probs],
    })
    y_col = "Pravděpodobnost (%)" if L == "cs" else "Probability (%)"
    x_col = "Slovo" if L == "cs" else "Word"
    st.bar_chart(chart_data, x=x_col, y=y_col, horizontal=True)

    for token, prob in zip(tokens, probs):
        cols = st.columns([2, 1, 4])
        cols[0].write(f"**{token}**")
        cols[1].write(f"{prob:.1%}")
        cols[2].progress(min(prob, 1.0))

    st.markdown(f"### {'Simulace: 10 generování' if L == 'cs' else 'Simulation: 10 generations'}")
    if st.button("🎲 " + ("Generovat" if L == "cs" else "Generate")):
        for i in range(10):
            r = random.random()
            cumulative = 0.0
            chosen = tokens[-1]
            for token, prob in zip(tokens, probs):
                cumulative += prob
                if r <= cumulative:
                    chosen = token
                    break
            color = "#4CAF50" if chosen == tokens[0] else "#FF9800" if chosen == tokens[1] else "#F44336"
            st.markdown(f'{i+1}. {context} <span style="color:{color};font-weight:bold">{chosen}</span>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════
#  PAGE 3: SEMANTIC SEARCH
# ═════════════════════════════════════════════════════════════════════════
elif page_idx == 3:
    if L == "cs":
        st.title("🔍 Sémantické vyhledávání")
        st.markdown("""
**Klasické vyhledávání** porovnává přesná slova — pokud hledáte "znečištění", nenajde dokumenty obsahující "kontaminace".

**Sémantické vyhledávání** převádí text na **vektory čísel** (embeddingy), které zachycují **význam**. Podobné významy mají podobné vektory — proto "znečištění" a "kontaminace" jsou si blízko.

Tato ukázka simuluje oba přístupy na zjednodušených příkladech z environmentálního výzkumu. Každý dokument je reprezentován 8-rozměrným vektorem (reálné embeddingy mají stovky dimenzí).
        """)
        st.info(t("disclaimer_illustration"))
    else:
        st.title("🔍 Semantic Search")
        st.markdown("""
**Classic search** compares exact words — if you search for "pollution", it won't find documents containing "contamination".

**Semantic search** converts text into **numerical vectors** (embeddings) that capture **meaning**. Similar meanings have similar vectors — so "pollution" and "contamination" are close together.

This demo simulates both approaches using simplified examples from environmental research. Each document is represented by an 8-dimensional vector (real embeddings have hundreds of dimensions).
        """)
        st.info(t("disclaimer_illustration"))

    DIMENSIONS = ["toxicity", "environment", "chemistry", "health", "water", "soil", "analysis", "regulation"] if L == "en" else ["toxicita", "prostředí", "chemie", "zdraví", "voda", "půda", "analýza", "regulace"]

    DOCUMENTS = {
        ("Kontaminace podzemních vod pesticidy" if L == "cs" else "Groundwater contamination by pesticides"): [0.6, 0.9, 0.7, 0.4, 0.95, 0.1, 0.5, 0.3],
        ("Vliv PCBs na reprodukci ryb" if L == "cs" else "Impact of PCBs on fish reproduction"): [0.9, 0.8, 0.8, 0.6, 0.7, 0.1, 0.4, 0.5],
        ("Stanovení těžkých kovů v půdě" if L == "cs" else "Determination of heavy metals in soil"): [0.5, 0.7, 0.9, 0.2, 0.1, 0.95, 0.9, 0.2],
        ("REACH registrace chemických látek" if L == "cs" else "REACH registration of chemicals"): [0.3, 0.5, 0.6, 0.3, 0.1, 0.1, 0.2, 0.95],
        ("Biomonitoring POPs v mateřském mléce" if L == "cs" else "Biomonitoring of POPs in breast milk"): [0.8, 0.6, 0.7, 0.9, 0.1, 0.1, 0.7, 0.4],
        ("Remediace brownfieldů fytotechnologiemi" if L == "cs" else "Brownfield remediation by phytotechnologies"): [0.4, 0.9, 0.5, 0.3, 0.2, 0.8, 0.3, 0.3],
        ("Endokrinní disruptory v pitné vodě" if L == "cs" else "Endocrine disruptors in drinking water"): [0.8, 0.7, 0.7, 0.9, 0.9, 0.1, 0.5, 0.6],
        ("Identifikace nových kontaminantů" if L == "cs" else "Identification of emerging contaminants"): [0.5, 0.6, 0.8, 0.3, 0.3, 0.3, 0.95, 0.2],
        ("Ekotoxicita nanočástic stříbra" if L == "cs" else "Ecotoxicity of silver nanoparticles"): [0.9, 0.8, 0.6, 0.5, 0.4, 0.3, 0.6, 0.3],
        ("Chemické složení říčních sedimentů" if L == "cs" else "Chemical composition of river sediments"): [0.4, 0.8, 0.7, 0.2, 0.8, 0.3, 0.5, 0.4],
    }

    PRESET_QUERIES = {
        ("znečištění vody chemikáliemi" if L == "cs" else "water pollution by chemicals"): [0.7, 0.8, 0.7, 0.5, 0.9, 0.1, 0.3, 0.3],
        ("analýza škodlivin v zemině" if L == "cs" else "analysis of pollutants in soil"): [0.5, 0.7, 0.8, 0.2, 0.1, 0.9, 0.8, 0.2],
        ("zdravotní dopady toxických látek" if L == "cs" else "health effects of toxic substances"): [0.8, 0.5, 0.6, 0.9, 0.3, 0.2, 0.4, 0.4],
        ("legislativa chemických látek EU" if L == "cs" else "EU chemicals legislation"): [0.2, 0.4, 0.5, 0.2, 0.1, 0.1, 0.2, 0.9],
    }

    def cosine_similarity(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def keyword_search(query, documents):
        query_words = set(query.lower().split())
        results = [(title, len(query_words & set(title.lower().split()))) for title in documents]
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    selected_query = st.selectbox("🔎 " + ("Vyberte dotaz:" if L == "cs" else "Select a query:"), list(PRESET_QUERIES.keys()))

    if L == "cs":
        st.markdown("#### Nebo si upravte vektor dotazu ručně:")
        st.caption("Každý slider představuje jednu dimenzi významu. Posuňte je a sledujte, jak se mění výsledky.")
    else:
        st.markdown("#### Or adjust the query vector manually:")
        st.caption("Each slider represents one dimension of meaning. Move them and watch the results change.")

    query_vec = PRESET_QUERIES[selected_query].copy()
    cols = st.columns(8)
    for i, dim in enumerate(DIMENSIONS):
        query_vec[i] = cols[i].slider(dim, 0.0, 1.0, query_vec[i], 0.05, key=f"dim_{i}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### 📋 {'Klasické vyhledávání' if L == 'cs' else 'Keyword Search'}")
        kw_results = keyword_search(selected_query, DOCUMENTS)
        has_any = False
        for title, matches in kw_results:
            if matches > 0:
                has_any = True
                st.markdown(f"- **{matches} {'shod' if L == 'cs' else 'matches'}** — {title}")
        if not has_any:
            if L == "cs":
                st.warning("Žádná shoda! Dotaz neobsahuje přesná slova z dokumentů.")
            else:
                st.warning("No matches! Query doesn't contain exact words from documents.")

    with col2:
        st.markdown(f"#### 🧠 {'Sémantické vyhledávání' if L == 'cs' else 'Semantic Search'}")
        sem_results = sorted([(t, cosine_similarity(query_vec, v)) for t, v in DOCUMENTS.items()], key=lambda x: x[1], reverse=True)
        for title, sim in sem_results[:5]:
            color = "green" if sim > 0.90 else "orange" if sim > 0.80 else "red"
            st.markdown(f"- :{color}[**{sim:.1%}**] — {title}")

    st.markdown("---")
    st.markdown(f"#### {'Jak vypadá embedding?' if L == 'cs' else 'What Does an Embedding Look Like?'}")
    if L == "cs":
        st.caption("Každý dokument je převeden na vektor čísel. Čím vyšší hodnota v dimenzi, tím silnější je souvislost dokumentu s tímto aspektem.")
    else:
        st.caption("Each document is converted to a vector of numbers. Higher values mean stronger association with that aspect.")
    selected_doc = st.selectbox("📄", list(DOCUMENTS.keys()), label_visibility="collapsed")
    embed_data = pd.DataFrame({"Dim": DIMENSIONS, "Value": DOCUMENTS[selected_doc]})
    st.bar_chart(embed_data, x="Dim", y="Value")


# ═════════════════════════════════════════════════════════════════════════
#  PAGE 4: HALLUCINATION QUIZ
# ═════════════════════════════════════════════════════════════════════════
elif page_idx == 4:
    if L == "cs":
        st.title("🎭 Halucinace — Rozpoznej, co AI vymyslela")
        st.markdown("""
**Halucinace** je situace, kdy AI generuje text, který **vypadá přesvědčivě a autoritativně**, ale je **fakticky nesprávný**. Problém je, že model nerozlišuje mezi tím, co "ví" a co "vymýšlí" — obojí generuje stejně sebevědomě.

Dokážete rozpoznat halucinaci od faktu? Následující texty vypadají jako typické AI odpovědi z oblasti environmentální chemie.
        """)
    else:
        st.title("🎭 Hallucinations — Spot What AI Made Up")
        st.markdown("""
**Hallucination** is when AI generates text that **looks convincing and authoritative** but is **factually incorrect**. The problem is that the model doesn't distinguish between what it "knows" and what it "makes up" — it generates both with equal confidence.

Can you tell hallucination from fact? The following texts look like typical AI responses from environmental chemistry.
        """)

    QUESTIONS = [
        {
            "text_cs": "Stockholmská úmluva o perzistentních organických polutantech byla přijata v roce 2001 a vstoupila v platnost v roce 2004.",
            "text_en": "The Stockholm Convention on Persistent Organic Pollutants was adopted in 2001 and entered into force in 2004.",
            "answer": False,
            "expl_cs": "**PRAVDA.** Stockholmská úmluva byla přijata 22. května 2001 a vstoupila v platnost 17. května 2004. Ověřitelný fakt.",
            "expl_en": "**TRUE.** The Stockholm Convention was adopted on May 22, 2001 and entered into force on May 17, 2004. Verifiable fact.",
            "indicators_cs": [], "indicators_en": [],
        },
        {
            "text_cs": "Podle studie Andersona et al. (2019) v Environmental Science & Technology koncentrace PFAS v pitné vodě v ČR překračují limit EU 0.1 µg/L ve 43.7 % zkoumaných vzorků.",
            "text_en": "According to Anderson et al. (2019) in Environmental Science & Technology, PFAS concentrations in Czech drinking water exceed the EU limit of 0.1 µg/L in 43.7% of examined samples.",
            "answer": True,
            "expl_cs": "**HALUCINACE.** Příliš specifické číslo (43.7 %), generické jméno autora, studii nelze dohledat.",
            "expl_en": "**HALLUCINATION.** Overly specific number (43.7%), generic author name, study cannot be found.",
            "indicators_cs": ["Příliš specifická čísla", "Generické jméno autora", "Nedohledatelný zdroj"],
            "indicators_en": ["Overly specific numbers", "Generic author name", "Source cannot be found"],
        },
        {
            "text_cs": "DDT byl poprvé syntetizován v roce 1874 Othmanem Zeidlerem. Paul Hermann Müller objevil jeho insekticidní vlastnosti v roce 1939 a získal za to Nobelovu cenu v roce 1948.",
            "text_en": "DDT was first synthesized in 1874 by Othmar Zeidler. Paul Hermann Müller discovered its insecticidal properties in 1939 and received the Nobel Prize in 1948.",
            "answer": False,
            "expl_cs": "**PRAVDA.** Všechna fakta jsou ověřitelná a správná.",
            "expl_en": "**TRUE.** All facts are verifiable and correct.",
            "indicators_cs": [], "indicators_en": [],
        },
        {
            "text_cs": "ECHA ve zprávě z roku 2023 identifikovala 2,847 látek klasifikovaných jako endokrinní disruptory kategorie 1A podle REACH. Zpráva: ECHA/RPT/2023/ED-1847.",
            "text_en": "ECHA in its 2023 report identified 2,847 substances classified as category 1A endocrine disruptors under REACH. Report: ECHA/RPT/2023/ED-1847.",
            "answer": True,
            "expl_cs": "**HALUCINACE.** Vymyšlené referenční číslo, neexistující klasifikační kategorie, příliš přesný počet.",
            "expl_en": "**HALLUCINATION.** Fabricated reference number, non-existent classification category, overly precise count.",
            "indicators_cs": ["Vymyšlené referenční číslo", "Neexistující kategorie", "Příliš přesná čísla"],
            "indicators_en": ["Fabricated reference number", "Non-existent category", "Overly precise numbers"],
        },
        {
            "text_cs": "Benzo[a]pyren je PAH klasifikovaný jako karcinogen skupiny 1 podle IARC. Vzniká neúplným spalováním a nachází se v cigaretovém kouři, grilovaném mase a výfukových plynech.",
            "text_en": "Benzo[a]pyrene is a PAH classified as a Group 1 carcinogen by IARC. It is produced by incomplete combustion and found in cigarette smoke, grilled meat, and exhaust fumes.",
            "answer": False,
            "expl_cs": "**PRAVDA.** Vše je správně — IARC skupina 1, PAH, vzniká neúplným spalováním.",
            "expl_en": "**TRUE.** Everything is correct — IARC Group 1, PAH, produced by incomplete combustion.",
            "indicators_cs": [], "indicators_en": [],
        },
        {
            "text_cs": "Metoda QuEChERS byla vyvinuta Robertem J. Blackwoodem na MIT v roce 1998 a je dnes zlatým standardem pro extrakci pesticidů.",
            "text_en": "The QuEChERS method was developed by Robert J. Blackwood at MIT in 1998 and is now the gold standard for pesticide extraction.",
            "answer": True,
            "expl_cs": "**ČÁSTEČNÁ HALUCINACE.** QuEChERS existuje a je standardem — ale vyvinuli ji Anastassiades, Lehotay a kol. v 2003, ne Blackwood na MIT. Typický mix faktů s fikcí.",
            "expl_en": "**PARTIAL HALLUCINATION.** QuEChERS exists and is a standard — but it was developed by Anastassiades, Lehotay et al. in 2003, not Blackwood at MIT. Typical mix of facts and fiction.",
            "indicators_cs": ["Vymyšlený autor", "Špatná instituce", "Nesprávný rok"],
            "indicators_en": ["Fabricated author", "Wrong institution", "Wrong year"],
        },
        {
            "text_cs": "Glyfosfát je nejpoužívanější herbicid na světě. V březnu 2015 jej IARC klasifikovala jako 'pravděpodobně karcinogenní' (skupina 2A).",
            "text_en": "Glyphosate is the most widely used herbicide in the world. In March 2015, IARC classified it as 'probably carcinogenic' (Group 2A).",
            "answer": False,
            "expl_cs": "**PRAVDA.** Vše správně a ověřitelně.",
            "expl_en": "**TRUE.** Everything is correct and verifiable.",
            "indicators_cs": [], "indicators_en": [],
        },
        {
            "text_cs": "Meta-analýza Wanga a Zhanga (2022) v Nature Reviews prokázala, že mikroplasty v pitné vodě způsobují 23% nárůst rizika kolorektálního karcinomu při expozici nad 150 částic/L.",
            "text_en": "A meta-analysis by Wang and Zhang (2022) in Nature Reviews demonstrated that microplastics in drinking water cause a 23% increase in colorectal cancer risk at exposures above 150 particles/L.",
            "answer": True,
            "expl_cs": "**HALUCINACE.** Příliš specifická čísla, generická jména, kauzální tvrzení bez podkladu. Takto silný závěr by byl světovou zprávou.",
            "expl_en": "**HALLUCINATION.** Overly specific numbers, generic names, causal claim without basis. Such a strong conclusion would be world news.",
            "indicators_cs": ["Příliš specifická čísla", "Generická jména", "Kauzální tvrzení", "Nedohledatelný zdroj"],
            "indicators_en": ["Overly specific numbers", "Generic names", "Causal claim", "Source cannot be found"],
        },
    ]

    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_order = list(range(len(QUESTIONS)))
        random.shuffle(st.session_state.quiz_order)

    idx = st.session_state.quiz_index
    order = st.session_state.quiz_order

    if idx < len(QUESTIONS):
        q = QUESTIONS[order[idx]]
        st.progress(idx / len(QUESTIONS), text=f"{'Otázka' if L == 'cs' else 'Question'} {idx + 1} / {len(QUESTIONS)}")

        text = q[f"text_{L}"]
        st.markdown(f"""<div style="background-color: #1e1e2e; padding: 20px; border-radius: 10px;
                    border-left: 4px solid #6C63FF; margin: 20px 0;">
            <p style="font-size: 16px; line-height: 1.6;">{text}</p></div>""", unsafe_allow_html=True)

        if not st.session_state.quiz_answered:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ " + ("Pravda" if L == "cs" else "True"), use_container_width=True):
                    st.session_state.quiz_answered = True
                    st.session_state.quiz_user_said_h = False
                    st.rerun()
            with c2:
                if st.button("🚨 " + ("Halucinace" if L == "cs" else "Hallucination"), use_container_width=True):
                    st.session_state.quiz_answered = True
                    st.session_state.quiz_user_said_h = True
                    st.rerun()
        else:
            is_correct = st.session_state.quiz_user_said_h == q["answer"]
            if is_correct:
                st.session_state.quiz_score += 1
                st.success(f"✅ {'Správně!' if L == 'cs' else 'Correct!'} {q[f'expl_{L}']}")
            else:
                st.error(f"❌ {'Špatně.' if L == 'cs' else 'Wrong.'} {q[f'expl_{L}']}")

            indicators = q[f"indicators_{L}"]
            if indicators:
                st.warning(f"**{'Varovné signály' if L == 'cs' else 'Warning signs'}:** " + " • ".join(indicators))

            if st.button("➡️ " + ("Další" if L == "cs" else "Next")):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.rerun()
    else:
        score = st.session_state.quiz_score
        total = len(QUESTIONS)
        pct = score / total * 100
        st.balloons()
        st.markdown(f"## {'Výsledek' if L == 'cs' else 'Result'}: {score}/{total} ({pct:.0f} %)")
        if pct >= 80:
            st.success("🎉 " + ("Výborně! Máte dobrý čich na halucinace." if L == "cs" else "Excellent! You have a good nose for hallucinations."))
        elif pct >= 50:
            st.warning("👍 " + ("Solidní základ, ale AI umí být přesvědčivá." if L == "cs" else "Solid base, but AI can be convincing."))
        else:
            st.info("💪 " + ("Nevadí — právě proto je kritické myšlení důležité!" if L == "cs" else "No worries — that's exactly why critical thinking matters!"))

        if st.button("🔄 " + ("Začít znovu" if L == "cs" else "Start over")):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = False
            random.shuffle(st.session_state.quiz_order)
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════
#  PAGE 5: PROMPTING
# ═════════════════════════════════════════════════════════════════════════
elif page_idx == 5:
    if L == "cs":
        st.title("💬 Prompting — Techniky a šablony")
        st.markdown("""
**Prompt** je vstup (text, otázka, instrukce), který zadáte modelu. **Prompt engineering** je systematický přístup k psaní promptů, který vede k lepším a spolehlivějším výstupům.

Neexistuje jeden "správný" způsob promptování — ale existují ověřené techniky, které fungují lépe než naivní dotazy. Níže najdete příklady relevantní pro výzkum na RECETOX.
        """)
    else:
        st.title("💬 Prompting — Techniques and Templates")
        st.markdown("""
A **prompt** is the input (text, question, instruction) you give to the model. **Prompt engineering** is a systematic approach to writing prompts that leads to better and more reliable outputs.

There is no single "correct" way to prompt — but there are proven techniques that work better than naive queries. Below you'll find examples relevant to RECETOX research.
        """)

    TECHNIQUES = [
        {"name": "Zero-shot", "icon": "🎯",
         "when_cs": "Jednoduché, jasně definované úlohy",
         "when_en": "Simple, well-defined tasks",
         "bad_cs": "Řekni mi něco o PFAS.",
         "bad_en": "Tell me something about PFAS.",
         "good_cs": "Vysvětli, co jsou PFAS (per- a polyfluoralkylové látky), jaké jsou jejich hlavní zdroje v životním prostředí a proč se jim říká 'forever chemicals'. Odpověz ve 3 odstavcích.",
         "good_en": "Explain what PFAS (per- and polyfluoroalkyl substances) are, their main environmental sources, and why they're called 'forever chemicals'. Answer in 3 paragraphs."},
        {"name": "Chain of Thought", "icon": "🔗",
         "when_cs": "Složité výpočty, logické odvozování, interpretace dat",
         "when_en": "Complex calculations, logical reasoning, data interpretation",
         "bad_cs": "Vyhodnoť toxicitu tohoto vzorku.",
         "bad_en": "Evaluate the toxicity of this sample.",
         "good_cs": "Mám vzorek vody:\n- Olovo: 15 µg/L\n- Kadmium: 3.5 µg/L\n- Arsen: 8 µg/L\n\nPorovnej s limity EU 2020/2184. U každé látky uveď: 1) naměřenou hodnotu, 2) limit, 3) poměr, 4) hodnocení.",
         "good_en": "I have a water sample:\n- Lead: 15 µg/L\n- Cadmium: 3.5 µg/L\n- Arsenic: 8 µg/L\n\nCompare with EU 2020/2184 limits. For each: 1) measured value, 2) limit, 3) ratio, 4) assessment."},
        {"name": "Tree of Thought", "icon": "🌳",
         "when_cs": "Rozhodování s více dobrými řešeními",
         "when_en": "Decisions with multiple good solutions",
         "bad_cs": "Jak analyzovat pesticidy?",
         "bad_en": "How to analyze pesticides?",
         "good_cs": "Analyzuji reziduá pesticidů v ovoci. Prozkoumej 3 přístupy:\nA: QuEChERS + GC-MS/MS\nB: QuEChERS + LC-MS/MS\nC: SFE + GC-MS\n\nPro každý: vhodnost, počet detekovatelných pesticidů, náročnost, skóre 1-10.",
         "good_en": "I'm analyzing pesticide residues in fruit. Explore 3 approaches:\nA: QuEChERS + GC-MS/MS\nB: QuEChERS + LC-MS/MS\nC: SFE + GC-MS\n\nFor each: suitability, number of detectable pesticides, complexity, score 1-10."},
        {"name": "Decomposition" if L == "en" else "Dekompozice", "icon": "📦",
         "when_cs": "Komplexní úlohy (rešerše, návrhy experimentů)",
         "when_en": "Complex tasks (literature reviews, experiment design)",
         "bad_cs": "Napiš rešerši o mikroplastech v půdě.",
         "bad_en": "Write a review about microplastics in soil.",
         "good_cs": "Připravíme rešerši o mikroplastech v půdě po krocích:\n1. Identifikuj 5 klíčových aspektů\n2. Navrhni vyhledávací strategii\n3. Shrň stav poznání\n4. Identifikuj mezery\n5. Navrhni strukturu\n\nZačni krokem 1. Další kroky po schválení.",
         "good_en": "Let's prepare a review on microplastics in soil step by step:\n1. Identify 5 key aspects\n2. Propose a search strategy\n3. Summarize current knowledge\n4. Identify gaps\n5. Propose structure\n\nStart with step 1. Next steps after approval."},
        {"name": "Self-criticism" if L == "en" else "Sebekritika", "icon": "🔄",
         "when_cs": "Když potřebujete vysokou kvalitu textu",
         "when_en": "When you need high-quality text",
         "bad_cs": "Napiš abstrakt pro můj článek.",
         "bad_en": "Write an abstract for my paper.",
         "good_cs": "Napiš abstrakt (max 250 slov) pro Environmental Pollution:\nTéma: Vliv mikroplastů na sorpci těžkých kovů v půdě\nMetodika: Batch sorpční experimenty, SEM-EDS\nVýsledek: PE a PP zvyšují mobilitu Cd o 15-30 %\n\nPak: 1) zkritizuj, 2) přepiš, 3) porovnej verze.",
         "good_en": "Write an abstract (max 250 words) for Environmental Pollution:\nTopic: Effect of microplastics on heavy metal sorption in soil\nMethods: Batch sorption experiments, SEM-EDS\nResult: PE and PP increase Cd mobility by 15-30%\n\nThen: 1) critique it, 2) rewrite, 3) compare versions."},
        {"name": "PROMPT Framework", "icon": "📐",
         "when_cs": "Maximální kvalita odpovědi",
         "when_en": "Maximum quality output",
         "bad_cs": "Pomoz mi s výzkumem.",
         "bad_en": "Help me with research.",
         "good_cs": "PURPOSE: Najít analytickou metodu pro emerging pollutants v odpadních vodách\nROLE: Analytický chemik, 15 let zkušeností, LC-MS\nOBJECTIVE: Srovnávací tabulka 4 metod (LOD, LOQ, opakovatelnost)\nMETHOD: Definuj kritéria, porovnej, doporuč\nPARAMETERS: Tabulka, PPCPs, roky 2020-2026\nTONE: Odborný, stručný",
         "good_en": "PURPOSE: Find analytical method for emerging pollutants in wastewater\nROLE: Analytical chemist, 15 years experience, LC-MS\nOBJECTIVE: Comparison table of 4 methods (LOD, LOQ, repeatability)\nMETHOD: Define criteria, compare, recommend\nPARAMETERS: Table, PPCPs, years 2020-2026\nTONE: Professional, concise"},
    ]

    for tech in TECHNIQUES:
        with st.expander(f"{tech['icon']} {tech['name']} — {tech[f'when_{L}']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**❌ {'Slabý prompt' if L == 'cs' else 'Weak prompt'}:**")
                st.code(tech[f"bad_{L}"], language=None)
            with c2:
                st.markdown(f"**✅ {'Silný prompt' if L == 'cs' else 'Strong prompt'}:**")
                st.code(tech[f"good_{L}"], language=None)

    st.markdown("---")
    st.markdown(f"### 🛠️ PROMPT Builder")
    if L == "cs":
        st.markdown("Sestavte si prompt pomocí PROMPT frameworku. Vyplněný prompt si zkopírujte do ChatGPT, Claude nebo Gemini.")
    else:
        st.markdown("Build your prompt using the PROMPT framework. Copy the result into ChatGPT, Claude, or Gemini.")

    labels = {
        "cs": ["**P**urpose — Co potřebujete:", "**R**ole — Kdo má AI být:", "**O**bjective — Konkrétní výstup:",
                "**M**ethod — Jak postupovat:", "**P**arameters — Formální požadavky:", "**T**one — Styl:"],
        "en": ["**P**urpose — What you need:", "**R**ole — Who AI should be:", "**O**bjective — Specific output:",
                "**M**ethod — How to proceed:", "**P**arameters — Formal requirements:", "**T**one — Style:"],
    }
    keys = ["PURPOSE", "ROLE", "OBJECTIVE", "METHOD", "PARAMETERS", "TONE"]
    vals = [st.text_input(labels[L][i], key=f"prompt_{i}") for i in range(6)]

    if any(vals):
        parts = [f"{k}: {v}" for k, v in zip(keys, vals) if v]
        st.markdown(f"#### {'Váš prompt' if L == 'cs' else 'Your prompt'}:")
        st.code("\n\n".join(parts), language=None)


# ═════════════════════════════════════════════════════════════════════════
#  PAGE 6: BIAS
# ═════════════════════════════════════════════════════════════════════════
elif page_idx == 6:
    if L == "cs":
        st.title("⚖️ Bias v datech — Garbage In, Garbage Out")
        st.markdown("Kvalita výstupu AI je přímo úměrná kvalitě trénovacích dat. Tyto simulace ukazují, **jak nerovnoměrnost dat zkresluje odpovědi** AI modelu.")
        st.info(t("disclaimer_illustration"))
    else:
        st.title("⚖️ Bias in Data — Garbage In, Garbage Out")
        st.markdown("AI output quality is directly proportional to training data quality. These simulations show **how data imbalance distorts AI responses**.")
        st.info(t("disclaimer_illustration"))

    tab_labels = {
        "cs": ["🌍 Geografický bias", "🗣️ Jazykový bias", "🔄 Model collapse", "📊 Korelace vs. kauzalita"],
        "en": ["🌍 Geographic Bias", "🗣️ Language Bias", "🔄 Model Collapse", "📊 Correlation vs. Causation"],
    }
    tab1, tab2, tab3, tab4 = st.tabs(tab_labels[L])

    with tab1:
        st.markdown(f"### {'Jak rozložení publikací zkresluje odpovědi AI' if L == 'cs' else 'How Publication Distribution Distorts AI Responses'}")
        if L == "cs":
            st.markdown("AI model \"ví\" tolik, kolik bylo napsáno. Pokud je o Africe 10x méně publikací než o Severní Americe, model bude o Africe vědět 10x méně — ne proto, že tam problémy nejsou.")
        else:
            st.markdown("The AI model \"knows\" as much as has been written. If there are 10x fewer publications about Africa than North America, the model knows 10x less about Africa — not because problems don't exist there.")

        regions = ["N. America", "W. Europe", "E. Asia", "Latin Am.", "E. Europe", "Africa", "S. Asia", "Oceania"] if L == "en" else ["Sev. Amerika", "Záp. Evropa", "Vých. Asie", "Lat. Amerika", "Vých. Evropa", "Afrika", "Jižní Asie", "Oceánie"]
        df = pd.DataFrame({
            "Region": regions,
            ("Publikace (%)" if L == "cs" else "Publications (%)"): [32, 28, 18, 8, 6, 4, 3, 1],
            ("Skutečné problémy (%)" if L == "cs" else "Actual Problems (%)"): [15, 12, 20, 15, 10, 15, 10, 3],
        })
        st.bar_chart(df, x="Region", y=[df.columns[1], df.columns[2]])

    with tab2:
        st.markdown(f"### {'Zastoupení jazyků v trénovacích datech' if L == 'cs' else 'Language Representation in Training Data'}")
        langs = ["English", "Chinese", "German", "French", "Spanish", "Russian", "Japanese", "Czech", "Slovak"] if L == "en" else ["Angličtina", "Čínština", "Němčina", "Francouz.", "Španělština", "Ruština", "Japonština", "Čeština", "Slovenšt."]
        df_lang = pd.DataFrame({("Jazyk" if L == "cs" else "Language"): langs, "%": [55, 8, 5, 5, 4, 3, 3, 0.5, 0.2]})
        st.bar_chart(df_lang, x=df_lang.columns[0], y="%")
        if L == "cs":
            st.warning("**Důsledky:** AI odpovídá v češtině, ale \"myslí\" anglicky. Odborná terminologie může být nepřesná. České zdroje (legislativa, instituce) model často nezná.")
        else:
            st.warning("**Consequences:** AI responds in Czech but \"thinks\" in English. Terminology may be imprecise. Czech sources (legislation, institutions) are often unknown to the model.")

    with tab3:
        st.markdown(f"### {'Co se stane, když AI trénujeme na AI-generovaných datech?' if L == 'cs' else 'What Happens When We Train AI on AI-Generated Data?'}")
        if L == "cs":
            st.markdown("S každou \"generací\" se hodnoty vzdalují od reality. Extrémní hodnoty se posouvají k průměru — AI normalizuje. Toto je zjednodušená simulace problému zvaného **model collapse**.")
        else:
            st.markdown("With each \"generation\", values drift from reality. Extreme values regress toward the mean — AI normalizes. This is a simplified simulation of **model collapse**.")

        random.seed(42)
        original = {"Benzo[a]pyrene": 85, "DDT": 72, ("Glyfosfát" if L == "cs" else "Glyphosate"): 35, ("Kofein" if L == "cs" else "Caffeine"): 8, ("Voda" if L == "cs" else "Water"): 0}
        gens = st.slider("Generations:" if L == "en" else "Počet generací:", 1, 10, 6)
        noise = st.slider("Noise factor:" if L == "en" else "Faktor šumu:", 0.05, 0.30, 0.15)

        results = []
        for sub, tv in original.items():
            row = {("Látka" if L == "cs" else "Substance"): sub, ("Skutečnost" if L == "cs" else "Reality"): tv}
            cur = float(tv)
            mean_v = sum(original.values()) / len(original)
            for g in range(1, gens + 1):
                cur = max(0, min(100, cur + random.gauss(0, tv * noise + 5) + (mean_v - cur) * 0.1))
                row[f"Gen {g}"] = round(cur)
            results.append(row)

        df_c = pd.DataFrame(results)
        st.dataframe(df_c, use_container_width=True)
        chart = {row[df_c.columns[0]]: [row[df_c.columns[1]]] + [row[f"Gen {g}"] for g in range(1, gens + 1)] for _, row in df_c.iterrows()}
        st.line_chart(pd.DataFrame(chart, index=[("Skutečnost" if L == "cs" else "Reality")] + [f"Gen {g}" for g in range(1, gens + 1)]))

    with tab4:
        title_corr = "AI najde korelace, ale nerozumí kauzalitě" if L == "cs" else "AI Finds Correlations But Does Not Understand Causation"
        st.markdown(f"### {title_corr}")
        corrs = [
            (("Spotřeba zmrzliny ↔ utonutí" if L == "cs" else "Ice cream sales ↔ drownings"), 0.87, False, ("Obojí způsobuje horko" if L == "cs" else "Both caused by hot weather")),
            (("Azbest ↔ mesotheliom" if L == "cs" else "Asbestos ↔ mesothelioma"), 0.92, True, ("Prokázaná kauzalita" if L == "cs" else "Proven causation")),
            (("Filmy N. Cage ↔ utonutí v bazénech" if L == "cs" else "N. Cage films ↔ pool drownings"), 0.67, False, ("Spurious" if L == "en" else "Náhodná korelace")),
            (("PM2.5 ↔ respirační nemoci" if L == "cs" else "PM2.5 ↔ respiratory disease"), 0.78, True, ("Prokázaná kauzalita" if L == "cs" else "Proven causation")),
            (("Bio potraviny ↔ autismus" if L == "cs" else "Organic food ↔ autism"), 0.95, False, ("Oba trendy rostou v čase" if L == "cs" else "Both trends grow over time")),
        ]
        for stmt, r, causal, expl in corrs:
            c1, c2, c3 = st.columns([4, 1, 3])
            c1.write(f"**{stmt}**")
            c2.write(f"r = {r:.2f}")
            if causal:
                c3.success(f"✅ {'Kauzální' if L == 'cs' else 'Causal'} — {expl}")
            else:
                c3.error(f"❌ {'Ne-kauzální' if L == 'cs' else 'Non-causal'} — {expl}")


# ═════════════════════════════════════════════════════════════════════════
#  PAGE 7: COST CALCULATOR
# ═════════════════════════════════════════════════════════════════════════
elif page_idx == 7:
    if L == "cs":
        st.title("💰 Kalkulačka ceny — Kolik stojí váš prompt?")
        st.markdown("""
Za AI platíte **za tokeny** — zvlášť za vstupní (co pošlete) a výstupní (co model vygeneruje). Ceny se liší podle modelu.

Zadejte text a podívejte se, kolik by stál v různých modelech. Nebo si zkuste přepsat text do angličtiny a porovnejte.
        """)
        st.info(t("disclaimer_illustration") + " Ceny jsou orientační a mohou se měnit.")
    else:
        st.title("💰 Cost Calculator — How Much Does Your Prompt Cost?")
        st.markdown("""
You pay for AI **per token** — separately for input (what you send) and output (what the model generates). Prices vary by model.

Enter text and see how much it would cost across models. Try rewriting in English to compare.
        """)
        st.info(t("disclaimer_illustration") + " Prices are approximate and may change.")

    # Approximate prices per 1M tokens (input / output) as of March 2026
    MODELS = {
        "GPT-5.4": (2.50, 10.00),
        "GPT-5.3 Instant": (0.50, 2.00),
        "Claude Opus 4.6": (15.00, 75.00),
        "Claude Sonnet 4.6": (3.00, 15.00),
        "Gemini 3.1 PRO": (1.25, 5.00),
        "Gemini 3.1 Flash": (0.075, 0.30),
    }

    user_text = st.text_area(
        "Váš text / Your text:",
        "Studie zkoumala výskyt perzistentních organických polutantů ve vzorcích zemědělské půdy odebraných ze tří regionů České republiky. Výsledky ukazují významné úrovně kontaminace překračující regulační limity EU.",
        height=120)

    tokens = real_tokenize(user_text)
    n_tokens = len(tokens)

    st.markdown(render_tokens_html(tokens), unsafe_allow_html=True)
    st.metric("Tokens", n_tokens)

    est_output = st.slider(
        ("Odhadovaný výstup (tokenů):" if L == "cs" else "Estimated output (tokens):"),
        100, 4000, 500, 100)

    st.markdown(f"### {'Cena podle modelu' if L == 'cs' else 'Cost by Model'}")
    rows = []
    for model, (inp_price, out_price) in MODELS.items():
        inp_cost = n_tokens / 1_000_000 * inp_price
        out_cost = est_output / 1_000_000 * out_price
        total = inp_cost + out_cost
        rows.append({
            "Model": model,
            f"{'Vstup' if L == 'cs' else 'Input'} ($/1M tok)": f"${inp_price:.2f}",
            f"{'Výstup' if L == 'cs' else 'Output'} ($/1M tok)": f"${out_price:.2f}",
            f"{'Celkem' if L == 'cs' else 'Total'}": f"${total:.6f}",
        })
    st.dataframe(rows, use_container_width=True)

    if L == "cs":
        st.caption("Ceny jsou přibližné, platné k březnu 2026. Skutečné ceny závisí na konkrétním API plánu.")
    else:
        st.caption("Prices are approximate as of March 2026. Actual prices depend on your API plan.")


# ═════════════════════════════════════════════════════════════════════════
#  PAGE 8: CONTEXT WINDOW
# ═════════════════════════════════════════════════════════════════════════
elif page_idx == 8:
    if L == "cs":
        st.title("📏 Kontextové okno — Kolik se vejde do paměti AI?")
        st.markdown("""
**Kontextové okno** je vše, co model \"vidí\" v daném okamžiku — váš prompt, historie konverzace, systémové instrukce, nahrané dokumenty. Model nemá trvalou paměť — každá konverzace začíná prázdná.

Kontextové okno má **limit v tokenech**. Jakmile ho překročíte, starší části konverzace se \"zapomínají\".
        """)
        st.info(t("disclaimer_illustration"))
    else:
        st.title("📏 Context Window — How Much Fits in AI's Memory?")
        st.markdown("""
The **context window** is everything the model \"sees\" at a given moment — your prompt, conversation history, system instructions, uploaded documents. The model has no persistent memory — each conversation starts empty.

The context window has a **token limit**. Once exceeded, older parts of the conversation get \"forgotten\".
        """)
        st.info(t("disclaimer_illustration"))

    models_ctx = {
        "GPT-5.4": 1_000_000,
        "Claude Opus 4.6": 1_000_000,
        "Claude Sonnet 4.6": 1_000_000,
        "Gemini 3.1 PRO": 1_000_000,
        "Copilot (GPT-5.3)": 400_000,
    }

    # Approximate token counts for reference texts
    if L == "cs":
        references = [
            ("Jedna strana A4 (česky)", 700),
            ("Jedna strana A4 (anglicky)", 400),
            ("Bakalářská práce (~40 stran, česky)", 28_000),
            ("Vědecký článek (~8 stran, anglicky)", 5_000),
            ("Diplomová práce (~80 stran, česky)", 56_000),
            ("Disertační práce (~200 stran, česky)", 140_000),
            ("Kniha (300 stran, anglicky)", 90_000),
            ("Kniha (300 stran, česky)", 160_000),
        ]
    else:
        references = [
            ("One A4 page (English)", 400),
            ("One A4 page (Czech)", 700),
            ("Bachelor thesis (~40pp, Czech)", 28_000),
            ("Scientific article (~8pp, English)", 5_000),
            ("Master thesis (~80pp, Czech)", 56_000),
            ("Doctoral thesis (~200pp, Czech)", 140_000),
            ("Book (300pp, English)", 90_000),
            ("Book (300pp, Czech)", 160_000),
        ]

    st.markdown(f"### {'Co se vejde do kontextu?' if L == 'cs' else 'What Fits in the Context?'}")

    selected_model = st.selectbox("Model:", list(models_ctx.keys()))
    ctx_size = models_ctx[selected_model]

    ref_data = []
    for name, tokens in references:
        fits = ctx_size // tokens
        pct = tokens / ctx_size * 100
        ref_data.append({
            ("Text" if L == "en" else "Text"): name,
            ("Tokenů" if L == "cs" else "Tokens"): f"{tokens:,}",
            (f"Vejde se {fits}x" if L == "cs" else f"Fits {fits}x"): fits,
            ("% kontextu" if L == "cs" else "% of context"): f"{pct:.1f}%",
        })
    st.dataframe(ref_data, use_container_width=True)

    st.markdown(f"### {'Vizualizace' if L == 'cs' else 'Visualization'}")
    viz_ref = st.selectbox(
        ("Vyberte referenční text:" if L == "cs" else "Select reference text:"),
        [r[0] for r in references])
    ref_tokens = [r[1] for r in references if r[0] == viz_ref][0]
    fill = min(ref_tokens / ctx_size, 1.0)
    st.progress(fill, text=f"{ref_tokens:,} / {ctx_size:,} tokens ({fill:.1%})")

    if L == "cs":
        st.markdown(f"""
### Klíčové poznatky
- **1M tokenů** ≈ 2 500 stran anglicky nebo ≈ 1 400 stran česky
- **Český text zabere ~1.5-2x víc tokenů** než anglický se stejným obsahem
- Kontextové okno zahrnuje **vše**: systémový prompt + historie + váš vstup + výstup modelu
- Pokud nahrajete 200stránkový dokument, zbude méně místa na konverzaci
        """)
    else:
        st.markdown(f"""
### Key Takeaways
- **1M tokens** ≈ 2,500 pages in English or ≈ 1,400 pages in Czech
- **Czech text takes ~1.5-2x more tokens** than English with the same content
- Context window includes **everything**: system prompt + history + your input + model output
- If you upload a 200-page document, less room remains for conversation
        """)


# ═════════════════════════════════════════════════════════════════════════
#  PAGE: CHEAT SHEET
# ═════════════════════════════════════════════════════════════════════════
elif page_idx == 9:
    if L == "cs":
        st.title("📋 Cheat Sheet — Praktická reference")
        st.markdown("Tuto stránku si **uložte do záložek** — obsahuje vše podstatné na jednom místě.")
    else:
        st.title("📋 Cheat Sheet — Practical Reference")
        st.markdown("**Bookmark this page** — it contains everything essential in one place.")

    tab_labels_cs = ["🛠️ Nástroje", "📐 PROMPT", "✅ Checklist", "📝 Deklarace AI", "⚠️ Časté chyby"]
    tab_labels_en = ["🛠️ Tools", "📐 PROMPT", "✅ Checklist", "📝 AI Declaration", "⚠️ Common Mistakes"]
    tabs = st.tabs(tab_labels_cs if L == "cs" else tab_labels_en)

    with tabs[0]:
        if L == "cs":
            st.markdown("""
### Konverzační AI

| Nástroj | Model | Kontext | Silné stránky |
|---------|-------|---------|---------------|
| **ChatGPT** | GPT-5.4 | až 1M tokenů | Univerzální, kód, multimodální |
| **Claude** | Opus/Sonnet 4.6 | až 1M tokenů | Dlouhé texty, etika, kód |
| **Gemini** | Gemini 3.1 PRO | až 1M tokenů | Google integrace, video |
| **Copilot** | GPT-5.2/5.3 | 128k-400k | Office 365 integrace |

### AI vyhledávání (akademické)

| Nástroj | Klíčová vlastnost | Zdarma? |
|---------|-------------------|---------|
| **Perplexity** | Vždy RAG, cituje zdroje | Limitovaně |
| **Scite** | Smart Citations — jak jsou články citovány | Limitovaně |
| **Elicit** | Extrakce dat z článků | Limitovaně |
| **Consensus** | Syntéza vědeckých závěrů | Limitovaně |
| **Semantic Scholar** | Sémantické hledání, open access | Ano |
| **NotebookLM** | Nahrané dokumenty jako zdroj | Ano |

### Na MU máte k dispozici

| Nástroj | Přístup | Více informací |
|---------|---------|----------------|
| **MS Copilot Chat** | Všichni na MU (GPT 5.3/5.4) | [it.muni.cz](https://it.muni.cz/sluzby/microsoft-copilot) |
| **Gemini** | Přes Google Workspace | [it.muni.cz](https://it.muni.cz/sluzby/google-workspace) |
| **AI as a Service** | Zaměstnanci přes e-Infra.cz | [docs.e-infra.cz/ai](https://docs.e-infra.cz) |

> ⚠️ Data u MS Copilot jsou pod tenantem MU — model se na nich netrénuje. U Gemini to nebylo potvrzeno.

> ⚠️ Scopus AI a WOS Research Assistant **nejsou** aktuálně na MU k dispozici.
            """)
        else:
            st.markdown("""
### Conversational AI

| Tool | Model | Context | Strengths |
|------|-------|---------|-----------|
| **ChatGPT** | GPT-5.4 | up to 1M tokens | Universal, code, multimodal |
| **Claude** | Opus/Sonnet 4.6 | up to 1M tokens | Long texts, ethics, code |
| **Gemini** | Gemini 3.1 PRO | up to 1M tokens | Google integration, video |
| **Copilot** | GPT-5.2/5.3 | 128k-400k | Office 365 integration |

### Academic AI Search

| Tool | Key Feature | Free? |
|------|-------------|-------|
| **Perplexity** | Always RAG, cites sources | Limited |
| **Scite** | Smart Citations | Limited |
| **Elicit** | Data extraction from papers | Limited |
| **Consensus** | Scientific consensus synthesis | Limited |
| **Semantic Scholar** | Semantic search, open access | Yes |
| **NotebookLM** | Uploaded docs as source | Yes |

### Available at Masaryk University

| Tool | Access | More info |
|------|--------|-----------|
| **MS Copilot Chat** | All MU members (GPT 5.3/5.4) | [it.muni.cz](https://it.muni.cz/sluzby/microsoft-copilot) |
| **Gemini** | Via Google Workspace | [it.muni.cz](https://it.muni.cz/sluzby/google-workspace) |
| **AI as a Service** | Employees via e-Infra.cz | [docs.e-infra.cz](https://docs.e-infra.cz) |

> ⚠️ MS Copilot data is under MU tenant — the model is not trained on it. Not confirmed for Gemini.

> ⚠️ Scopus AI and WOS Research Assistant are **not** currently available at MU.
            """)

    with tabs[1]:
        if L == "cs":
            st.markdown("### PROMPT Framework — šablona ke kopírování")
        else:
            st.markdown("### PROMPT Framework — copy-paste template")
        st.code(("PURPOSE: [Co potřebujete]\nROLE: [Kdo má AI být]\nOBJECTIVE: [Konkrétní výstup]\nMETHOD: [Jak postupovat]\nPARAMETERS: [Formální požadavky]\nTONE: [Styl komunikace]" if L == "cs" else "PURPOSE: [What you need]\nROLE: [Who AI should be]\nOBJECTIVE: [Specific output]\nMETHOD: [How to proceed]\nPARAMETERS: [Formal requirements]\nTONE: [Communication style]"), language=None)

        if L == "cs":
            st.markdown("""
### Kdy co použít

| Situace | Technika | Klíčová fráze |
|---------|----------|---------------|
| Jednoduchý dotaz | **Zero-shot** | Prostě se zeptejte |
| Výpočet / logika | **Chain of Thought** | "Ukaž mezikroky" |
| Rozhodování | **Tree of Thought** | "Prozkoumej 3 přístupy" |
| Komplexní úloha | **Dekompozice** | "Začni krokem 1" |
| Kvalitní text | **Sebekritika** | "Zkritizuj a přepiš" |
| Nejistota | **Meta-prompting** | "Navrhni optimální prompt" |
            """)
        else:
            st.markdown("""
### When to Use What

| Situation | Technique | Key Phrase |
|-----------|----------|------------|
| Simple query | **Zero-shot** | Just ask |
| Calculation / logic | **Chain of Thought** | "Show intermediate steps" |
| Decision-making | **Tree of Thought** | "Explore 3 approaches" |
| Complex task | **Decomposition** | "Start with step 1" |
| Quality text | **Self-criticism** | "Critique and rewrite" |
| Uncertainty | **Meta-prompting** | "Design an optimal prompt" |
            """)

    with tabs[2]:
        if L == "cs":
            st.markdown("""
### Před použitím AI

- [ ] **Co potřebuji?** — Definujte informační potřebu
- [ ] **Co už vím?** — Oddělte vlastní znalost od AI asistence
- [ ] **Jaký nástroj?** — Konverzační AI, AI vyhledávání, nebo specializovaný nástroj?
- [ ] **Jsou data citlivá?** — Nepublikovaná data, pacienti → e-Infra / lokální AI

### Po obdržení odpovědi (SMELL)

| Test | Otázka |
|------|--------|
| **S** — Smell test | Zní to rozumně, nebo jako generická fráze? |
| **M** — Math | Jsou čísla realistická? Souhlasí jednotky? |
| **E** — Evidence | Existují zdroje? Sedí DOI? |
| **L** — Logic | Následují argumenty logicky? |
| **L** — Limits | Je to v rámci znalostí modelu? |

### Další kontroly

- [ ] **Expert gut** — Co by řekl kolega z oboru?
- [ ] **Challenge** — "Jsi si jistá? Uveď konkrétní zdroj."
- [ ] **Cross-check** — Ověřte v jiném modelu nebo primárním zdroji
            """)
        else:
            st.markdown("""
### Before Using AI

- [ ] **What do I need?** — Define your information need
- [ ] **What do I know?** — Separate your own knowledge from AI assistance
- [ ] **Which tool?** — Conversational AI, AI search, or specialized tool?
- [ ] **Is data sensitive?** — Unpublished data, patients → e-Infra / local AI

### After Getting a Response (SMELL)

| Test | Question |
|------|----------|
| **S** — Smell test | Does it sound reasonable or like a generic phrase? |
| **M** — Math | Are numbers realistic? Do units match? |
| **E** — Evidence | Do sources exist? Does the DOI check out? |
| **L** — Logic | Do arguments follow logically? |
| **L** — Limits | Is this within the model's knowledge? |

### Additional Checks

- [ ] **Expert gut** — What would a colleague say?
- [ ] **Challenge** — "Are you sure? Provide a specific source."
- [ ] **Cross-check** — Verify in another model or primary source
            """)

    with tabs[3]:
        if L == "cs":
            st.markdown("""
### Instrument vs. Interpreter

| Úroveň | Příklad | Co uvést |
|--------|---------|----------|
| **Instrument** | Korektura, formátování, překlad | Není třeba deklarovat |
| **Instrument (výzkum)** | Kódování dat, výběr metody | Poznámka v metodice |
| **Šedá zóna** | AI navrhuje, já zodpovídám | Metodika + limitace |
| **Interpreter** | AI formuluje závěry z dat | Metodika + limitace + zvážit přijatelnost |

### Vzorová formulace
            """)
            st.code("AI-assisted analysis was conducted using [model, version].\nThe tool was used for [specific tasks].\nAll outputs were independently verified by the authors.\nThe authors take full responsibility for the accuracy of results.", language=None)
            st.markdown("""
### MUNI politika

Masarykova univerzita vyžaduje **transparentní deklaraci** použití AI.
Nezveřejněné použití AI se posuzuje jako plagiát.

🔗 [Prohlášení MU k aplikaci AI](https://www.muni.cz/o-univerzite/uredni-deska/prohlaseni-k-aplikaci-ai)
            """)
        else:
            st.markdown("""
### Instrument vs. Interpreter

| Level | Example | What to declare |
|-------|---------|-----------------|
| **Instrument** | Proofreading, formatting, translation | No declaration needed |
| **Instrument (research)** | Data coding, method selection | Note in methods |
| **Grey zone** | AI suggests, I take responsibility | Methods + limitations |
| **Interpreter** | AI formulates conclusions from data | Methods + limitations + consider acceptability |

### Template for Methods Section
            """)
            st.code("AI-assisted analysis was conducted using [model, version].\nThe tool was used for [specific tasks].\nAll outputs were independently verified by the authors.\nThe authors take full responsibility for the accuracy of results.", language=None)
            st.markdown("""
### MUNI Policy

Masaryk University requires **transparent declaration** of AI use.
Undisclosed AI use is treated as plagiarism.

🔗 [MU Statement on AI Application](https://www.muni.cz/en/about-us/official-notice-board/statement-on-the-application-of-ai)
            """)

    with tabs[4]:
        if L == "cs":
            st.markdown("""
### Top 10 chyb výzkumníků s AI

| # | Chyba | Jak se bránit |
|---|-------|---------------|
| 1 | **Citování AI jako zdroje** | AI není zdroj — dohledejte primární literaturu |
| 2 | **Vymyšlené reference** | Ověřte KAŽDÝ DOI, autora, časopis |
| 3 | **Chybné jednotky** | AI míchá µg/L vs. mg/kg, ppm vs. ppb |
| 4 | **Vymyšlená statistika** | Nedůvěřujte p-hodnotám a CI z AI |
| 5 | **Knowledge cutoff** | Model nezná nedávné publikace |
| 6 | **Automation bias** | Nekontrolujete AI-generovaný kód |
| 7 | **Ztráta porozumění** | Používáte statistiku, které nerozumíte |
| 8 | **Nereprodukovatelnost** | Stejný prompt = jiná odpověď jindy |
| 9 | **Únik dat** | Nepublikovaná data v komerčním API |
| 10 | **Homogenizace** | "AI hlas" — recenzenti to poznají |

### Specificky pro environmentální výzkum

- **Chemické názvy**: AI může zaměnit IUPAC názvy, CAS čísla
- **Regulatorní limity**: Liší se podle jurisdikce a matrice — AI je míchá
- **Kauzální tvrzení**: "X způsobuje Y" z AI = korelace, ne mechanismus
- **Data subjektů**: Nikdy nevkládejte osobní data do komerčních AI
            """)
        else:
            st.markdown("""
### Top 10 Researcher Mistakes with AI

| # | Mistake | How to Prevent |
|---|---------|----------------|
| 1 | **Citing AI as a source** | AI is not a source — find primary literature |
| 2 | **Fabricated references** | Verify EVERY DOI, author, journal |
| 3 | **Wrong units** | AI mixes µg/L vs. mg/kg, ppm vs. ppb |
| 4 | **Fabricated statistics** | Don't trust p-values and CIs from AI |
| 5 | **Knowledge cutoff** | Model doesn't know recent publications |
| 6 | **Automation bias** | Not reviewing AI-generated code |
| 7 | **Loss of understanding** | Using statistics you don't understand |
| 8 | **Non-reproducibility** | Same prompt = different answer next time |
| 9 | **Data leakage** | Unpublished data in commercial APIs |
| 10 | **Homogenization** | "AI voice" — reviewers can tell |

### Specific to Environmental Research

- **Chemical names**: AI may confuse IUPAC names, CAS numbers
- **Regulatory limits**: Differ by jurisdiction and matrix — AI mixes them
- **Causal claims**: "X causes Y" from AI = correlation, not mechanism
- **Subject data**: Never input personal data into commercial AI
            """)
