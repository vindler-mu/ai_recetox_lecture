#!/usr/bin/env python3
"""
AI@RECETOX — Interaktivní ukázky pro přednášku
Spuštění: streamlit run app.py
"""

import streamlit as st
import math
import random
import tiktoken

# ── Konfigurace stránky ──────────────────────────────────────────────────
st.set_page_config(
    page_title="AI@RECETOX — Interaktivní ukázky",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar navigace ─────────────────────────────────────────────────────
st.sidebar.title("AI@RECETOX")
st.sidebar.markdown("**Opportunities and Limits of GenAI in Research**")
st.sidebar.markdown("7. dubna 2026 | Vojtěch Velísek")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Vyberte ukázku:",
    [
        "Úvod",
        "1. Tokenizace",
        "2. Teplota",
        "3. Sémantické vyhledávání",
        "4. Halucinace — kvíz",
        "5. Prompting",
        "6. Bias v datech",
        "📋 Cheat Sheet",
    ],
)


# ═════════════════════════════════════════════════════════════════════════
#  ÚVOD
# ═════════════════════════════════════════════════════════════════════════
if page == "Úvod":
    st.title("🧪 AI@RECETOX — Interaktivní ukázky")
    st.markdown("""
    Vítejte v interaktivním doplňku k přednášce **Opportunities and Limits of GenAI in Research**.

    Vyberte ukázku v levém panelu a experimentujte s koncepty, o kterých mluvíme.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 🔤 Tokenizace
        Jak AI rozděluje text na kousky
        a proč čeština stojí víc.

        ### 🌡️ Teplota
        Jak parametr teploty ovlivňuje
        kreativitu vs. přesnost odpovědí.
        """)
    with col2:
        st.markdown("""
        ### 🔍 Sémantické vyhledávání
        Proč AI rozumí významu,
        ne jen klíčovým slovům.

        ### 🎭 Halucinace — kvíz
        Rozpoznáte, co je pravda
        a co si AI vymyslela?
        """)
    with col3:
        st.markdown("""
        ### 💬 Prompting
        Srovnání technik a šablony
        pro výzkum na RECETOX.

        ### ⚖️ Bias v datech
        Garbage in — garbage out.
        Jak data ovlivňují výstupy.
        """)

    st.markdown("---")
    st.info("💡 **Tip:** Každou ukázku si můžete vyzkoušet interaktivně — měňte parametry, zadávejte vlastní texty, zkoušejte různé varianty.")


# ═════════════════════════════════════════════════════════════════════════
#  1. TOKENIZACE
# ═════════════════════════════════════════════════════════════════════════
elif page == "1. Tokenizace":
    st.title("🔤 Tokenizace — Jak AI rozděluje text")

    st.markdown("""
    **Tokenizace** je proces rozdělení textu na menší kousky (tokeny),
    které model zpracovává. Model nevidí slova ani písmena — vidí tokeny.

    Tato ukázka používá **skutečný tokenizer** (`o200k_base`) — stejný,
    jaký používají modely GPT. Slovník obsahuje ~200 000 tokenů.
    Běžná anglická slova jsou často **1 token**, české tvary se rozpadají na více kousků.
    """)

    COLORS = [
        "#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#00BCD4", "#F44336",
        "#8BC34A", "#3F51B5", "#FFEB3B", "#E91E63", "#009688", "#FF5722",
    ]

    @st.cache_resource
    def get_encoder():
        return tiktoken.get_encoding("o200k_base")

    enc = get_encoder()

    def real_tokenize(text):
        token_ids = enc.encode(text)
        return [enc.decode([tid]) for tid in token_ids]

    def render_tokens(tokens):
        html = '<div style="line-height: 2.4; margin: 10px 0;">'
        for i, token in enumerate(tokens):
            color = COLORS[i % len(COLORS)]
            display = token.replace(" ", "⎵").replace("\n", "↵")
            html += (
                f'<span style="background-color: {color}; color: white; '
                f'padding: 4px 8px; margin: 2px; border-radius: 4px; '
                f'font-family: monospace; font-size: 14px; display: inline-block;">'
                f'{display}</span>'
            )
        html += '</div>'
        return html

    # Interaktivní vstup
    st.markdown("### Vyzkoušejte si to")
    col1, col2 = st.columns(2)

    with col1:
        en_text = st.text_input("Anglický text:", "The environmental contamination was investigated.")
    with col2:
        cs_text = st.text_input("Český text:", "Environmentální kontaminace byla prozkoumána.")

    en_tokens = real_tokenize(en_text)
    cs_tokens = real_tokenize(cs_text)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**EN** — {len(en_tokens)} tokenů")
        st.markdown(render_tokens(en_tokens), unsafe_allow_html=True)
    with col2:
        st.markdown(f"**CS** — {len(cs_tokens)} tokenů")
        st.markdown(render_tokens(cs_tokens), unsafe_allow_html=True)

    if en_tokens:
        ratio = len(cs_tokens) / len(en_tokens)
        delta = len(cs_tokens) - len(en_tokens)
        col1, col2, col3 = st.columns(3)
        col1.metric("EN tokeny", len(en_tokens))
        col2.metric("CS tokeny", len(cs_tokens), delta=f"+{delta}" if delta > 0 else str(delta))
        col3.metric("Poměr CS/EN", f"{ratio:.2f}x")

    # Odborné termíny
    st.markdown("### Odborné termíny (RECETOX)")
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
        data.append({"Termín EN": en, "Tokeny EN": en_t, "Termín CS": cs, "Tokeny CS": cs_t, "Poměr": f"{cs_t/en_t:.1f}x"})

    st.dataframe(data, use_container_width=True)

    # Počítání písmen
    st.markdown("### Proč AI špatně počítá písmena")
    word = st.text_input("Zadejte slovo:", "strawberry")
    if word:
        tokens = real_tokenize(word)
        st.markdown(render_tokens(tokens), unsafe_allow_html=True)
        st.markdown(f"Model vidí **{len(tokens)} token(y)**, ne **{len(word)} písmen**. Tokeny: `{tokens}`")

    st.markdown("""
    ### Proč na tom záleží?
    | Aspekt | Důsledek |
    |--------|----------|
    | **Cena** | Platíte za tokeny — čeština stojí o ~50-100 % víc |
    | **Kontext** | Kontextové okno má limit — čeština zabere víc místa |
    | **Kvalita** | `environmental` = 1 token (model zná dobře), `environmentální` = 2+ tokenů |
    | **Aritmetika** | Model nevidí písmena, vidí tokeny — proto špatně počítá |
    | **Vyhledávání** | České odborné termíny se rozpadají na kousky, mohou ztratit specifický význam |
    """)


# ═════════════════════════════════════════════════════════════════════════
#  2. TEPLOTA
# ═════════════════════════════════════════════════════════════════════════
elif page == "2. Teplota":
    st.title("🌡️ Teplota — Kreativita vs. přesnost")

    st.markdown("""
    **Teplota** je parametr, který ovlivňuje pravděpodobnostní distribuci
    dalšího tokenu. Nízká teplota = deterministická odpověď, vysoká = kreativní.
    """)

    def softmax(logits, temperature):
        if temperature <= 0:
            temperature = 0.001
        scaled = [x / temperature for x in logits]
        max_val = max(scaled)
        exps = [math.exp(x - max_val) for x in scaled]
        total = sum(exps)
        return [e / total for e in exps]

    context = "Kontaminace půdy byla"
    candidates = [
        ("zjištěna", 3.2),
        ("potvrzena", 2.8),
        ("analyzována", 2.1),
        ("zkoumána", 1.5),
        ("ignorována", 0.3),
        ("oslavována", -1.0),
    ]
    tokens = [c[0] for c in candidates]
    logits = [c[1] for c in candidates]

    st.markdown(f'### Kontext: *"{context} ___"*')
    st.markdown("Model zvažuje 6 kandidátů na další slovo.")

    # Slider pro teplotu
    temp = st.slider(
        "Nastavte teplotu:",
        min_value=0.05, max_value=2.5, value=0.7, step=0.05,
        help="Nízká = deterministická, Vysoká = kreativní"
    )

    probs = softmax(logits, temp)

    if temp <= 0.3:
        label = "🔵 DETERMINISTICKÁ"
        desc = "Model téměř vždy vybere nejpravděpodobnější token."
    elif temp <= 0.7:
        label = "🟡 VYVÁŽENÁ"
        desc = "Vyváženost mezi přesností a variabilitou."
    else:
        label = "🔴 KREATIVNÍ"
        desc = "Model častěji vybírá méně pravděpodobné tokeny."

    st.markdown(f"#### {label}")
    st.caption(desc)

    # Vizualizace distribuce
    import pandas as pd
    chart_data = pd.DataFrame({
        "Slovo": tokens,
        "Pravděpodobnost": [p * 100 for p in probs],
    })
    st.bar_chart(chart_data, x="Slovo", y="Pravděpodobnost", horizontal=True)

    # Tabulka s přesnými hodnotami
    for token, prob, logit in zip(tokens, probs, logits):
        cols = st.columns([2, 1, 4])
        cols[0].write(f"**{token}**")
        cols[1].write(f"{prob:.1%}")
        cols[2].progress(min(prob, 1.0))

    # Simulace generování
    st.markdown("### Simulace: 10 generování")
    if st.button("Generovat 10 odpovědí"):
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
            st.markdown(
                f'{i+1}. {context} <span style="color: {color}; font-weight: bold;">{chosen}</span>',
                unsafe_allow_html=True,
            )

    st.markdown("""
    ---
    ### Co z toho plyne?
    - **Nízká teplota (0.1-0.3):** Vhodné pro faktické odpovědi, překlady, sumarizace
    - **Střední teplota (0.5-0.7):** Většina běžných úloh
    - **Vysoká teplota (1.0+):** Kreativní psaní, brainstorming

    > ⚠️ Uživatel teplotu přímo nenastavuje — ale může její efekt napodobit formulací promptu.
    """)


# ═════════════════════════════════════════════════════════════════════════
#  3. SÉMANTICKÉ VYHLEDÁVÁNÍ
# ═════════════════════════════════════════════════════════════════════════
elif page == "3. Sémantické vyhledávání":
    st.title("🔍 Sémantické vyhledávání")

    st.markdown("""
    Klasické vyhledávání hledá **přesná slova**. Sémantické vyhledávání rozumí **významu**.
    """)

    DIMENSIONS = ["toxicita", "prostředí", "chemie", "zdraví", "voda", "půda", "analýza", "regulace"]

    DOCUMENTS = {
        "Kontaminace podzemních vod pesticidy": [0.6, 0.9, 0.7, 0.4, 0.95, 0.1, 0.5, 0.3],
        "Vliv PCBs na reprodukci ryb": [0.9, 0.8, 0.8, 0.6, 0.7, 0.1, 0.4, 0.5],
        "Stanovení těžkých kovů v půdě": [0.5, 0.7, 0.9, 0.2, 0.1, 0.95, 0.9, 0.2],
        "REACH registrace chemických látek": [0.3, 0.5, 0.6, 0.3, 0.1, 0.1, 0.2, 0.95],
        "Biomonitoring POPs v mateřském mléce": [0.8, 0.6, 0.7, 0.9, 0.1, 0.1, 0.7, 0.4],
        "Remediace brownfieldů fytotechnologiemi": [0.4, 0.9, 0.5, 0.3, 0.2, 0.8, 0.3, 0.3],
        "Endokrinní disruptory v pitné vodě": [0.8, 0.7, 0.7, 0.9, 0.9, 0.1, 0.5, 0.6],
        "Identifikace nových kontaminantů": [0.5, 0.6, 0.8, 0.3, 0.3, 0.3, 0.95, 0.2],
        "Ekotoxicita nanočástic stříbra": [0.9, 0.8, 0.6, 0.5, 0.4, 0.3, 0.6, 0.3],
        "Chemické složení říčních sedimentů": [0.4, 0.8, 0.7, 0.2, 0.8, 0.3, 0.5, 0.4],
    }

    PRESET_QUERIES = {
        "znečištění vody chemikáliemi": [0.7, 0.8, 0.7, 0.5, 0.9, 0.1, 0.3, 0.3],
        "analýza škodlivin v zemině": [0.5, 0.7, 0.8, 0.2, 0.1, 0.9, 0.8, 0.2],
        "zdravotní dopady toxických látek": [0.8, 0.5, 0.6, 0.9, 0.3, 0.2, 0.4, 0.4],
        "legislativa chemických látek EU": [0.2, 0.4, 0.5, 0.2, 0.1, 0.1, 0.2, 0.9],
    }

    def cosine_similarity(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def keyword_search(query, documents):
        query_words = set(query.lower().split())
        results = []
        for title in documents:
            title_words = set(title.lower().split())
            matches = len(query_words & title_words)
            results.append((title, matches))
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    # Volba dotazu
    selected_query = st.selectbox("Vyberte dotaz:", list(PRESET_QUERIES.keys()))

    st.markdown("#### Nebo si upravte vektor dotazu ručně:")
    query_vec = PRESET_QUERIES[selected_query].copy()
    cols = st.columns(8)
    for i, dim in enumerate(DIMENSIONS):
        query_vec[i] = cols[i].slider(dim, 0.0, 1.0, query_vec[i], 0.05, key=f"dim_{i}")

    # Výsledky
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📋 Klasické vyhledávání")
        kw_results = keyword_search(selected_query, DOCUMENTS)
        has_any = False
        for title, matches in kw_results:
            if matches > 0:
                has_any = True
                st.markdown(f"- **{matches} shod** — {title}")
        if not has_any:
            st.warning("Žádná shoda! Dotaz neobsahuje přesná slova z dokumentů.")

    with col2:
        st.markdown("#### 🧠 Sémantické vyhledávání")
        sem_results = []
        for title, vec in DOCUMENTS.items():
            sim = cosine_similarity(query_vec, vec)
            sem_results.append((title, sim))
        sem_results.sort(key=lambda x: x[1], reverse=True)

        for title, sim in sem_results[:5]:
            color = "green" if sim > 0.90 else "orange" if sim > 0.80 else "red"
            st.markdown(f"- :{color}[**{sim:.1%}**] — {title}")

    # Vizualizace embeddingu
    st.markdown("---")
    st.markdown("#### Jak vypadá embedding?")
    selected_doc = st.selectbox("Vyberte dokument:", list(DOCUMENTS.keys()))
    import pandas as pd
    embed_data = pd.DataFrame({
        "Dimenze": DIMENSIONS,
        "Hodnota": DOCUMENTS[selected_doc],
    })
    st.bar_chart(embed_data, x="Dimenze", y="Hodnota")


# ═════════════════════════════════════════════════════════════════════════
#  4. HALUCINACE KVÍZ
# ═════════════════════════════════════════════════════════════════════════
elif page == "4. Halucinace — kvíz":
    st.title("🎭 Halucinace — Rozpoznej, co AI vymyslela")

    st.markdown("""
    AI generuje text, který **vypadá přesvědčivě**, ale nemusí být pravdivý.
    Dokážete rozpoznat halucinaci od faktu?
    """)

    QUESTIONS = [
        {
            "text": (
                "Stockholmská úmluva o perzistentních organických polutantech "
                "byla přijata v roce 2001 a vstoupila v platnost v roce 2004."
            ),
            "answer": False,
            "explanation": "**PRAVDA.** Stockholmská úmluva byla přijata 22. května 2001 a vstoupila v platnost 17. května 2004.",
            "indicators": [],
        },
        {
            "text": (
                "Podle studie Andersona et al. (2019) v Environmental Science & Technology "
                "koncentrace PFAS v pitné vodě v ČR překračují limit EU 0.1 µg/L "
                "ve 43.7 % zkoumaných vzorků."
            ),
            "answer": True,
            "explanation": "**HALUCINACE.** Příliš specifické číslo (43.7 %), generické jméno autora, studii nelze dohledat.",
            "indicators": ["Příliš specifická čísla", "Generické jméno autora", "Nedohledatelný zdroj"],
        },
        {
            "text": (
                "DDT byl poprvé syntetizován v roce 1874 Othmanem Zeidlerem. "
                "Paul Hermann Müller objevil jeho insekticidní vlastnosti v roce 1939 "
                "a získal za to Nobelovu cenu v roce 1948."
            ),
            "answer": False,
            "explanation": "**PRAVDA.** Všechna fakta jsou ověřitelná a správná.",
            "indicators": [],
        },
        {
            "text": (
                "ECHA ve zprávě z roku 2023 identifikovala 2,847 látek klasifikovaných "
                "jako endokrinní disruptory kategorie 1A podle REACH. "
                "Zpráva: ECHA/RPT/2023/ED-1847."
            ),
            "answer": True,
            "explanation": "**HALUCINACE.** Vymyšlené referenční číslo, neexistující klasifikační kategorie, příliš přesný počet.",
            "indicators": ["Vymyšlené referenční číslo", "Neexistující kategorie", "Příliš přesná čísla"],
        },
        {
            "text": (
                "Benzo[a]pyren je PAH klasifikovaný jako karcinogen skupiny 1 podle IARC. "
                "Vzniká neúplným spalováním a nachází se v cigaretovém kouři, "
                "grilovaném mase a výfukových plynech."
            ),
            "answer": False,
            "explanation": "**PRAVDA.** Benzo[a]pyren je skutečně IARC skupina 1, PAH, vzniká neúplným spalováním.",
            "indicators": [],
        },
        {
            "text": (
                "Metoda QuEChERS byla vyvinuta Robertem J. Blackwoodem na MIT "
                "v roce 1998 a je dnes zlatým standardem pro extrakci pesticidů."
            ),
            "answer": True,
            "explanation": "**ČÁSTEČNÁ HALUCINACE.** QuEChERS existuje, ale vyvinuli ji Anastassiades, Lehotay a kol. v 2003, ne Blackwood na MIT.",
            "indicators": ["Vymyšlený autor", "Špatná instituce", "Nesprávný rok", "Mix faktů s fikcí"],
        },
        {
            "text": (
                "Glyfosfát je nejpoužívanější herbicid na světě. V březnu 2015 "
                "jej IARC klasifikovala jako 'pravděpodobně karcinogenní' (skupina 2A)."
            ),
            "answer": False,
            "explanation": "**PRAVDA.** Nejpoužívanější herbicid, IARC 2A (březen 2015) — vše správně.",
            "indicators": [],
        },
        {
            "text": (
                "Meta-analýza Wanga a Zhanga (2022) v Nature Reviews prokázala, "
                "že mikroplasty v pitné vodě způsobují 23% nárůst rizika "
                "kolorektálního karcinomu při expozici nad 150 částic/L."
            ),
            "answer": True,
            "explanation": "**HALUCINACE.** Příliš specifická čísla, generická jména, kauzální tvrzení bez podkladu.",
            "indicators": ["Příliš specifická čísla", "Generická jména", "Kauzální tvrzení", "Nedohledatelný zdroj"],
        },
    ]

    # Session state pro kvíz
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
        st.progress((idx) / len(QUESTIONS), text=f"Otázka {idx + 1} / {len(QUESTIONS)}")

        st.markdown(f"""
        <div style="background-color: #1e1e2e; padding: 20px; border-radius: 10px;
                    border-left: 4px solid #6C63FF; margin: 20px 0;">
            <p style="font-size: 16px; line-height: 1.6;">{q['text']}</p>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.quiz_answered:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Pravda", use_container_width=True):
                    st.session_state.quiz_answered = True
                    st.session_state.quiz_user_said_hallucination = False
                    st.rerun()
            with col2:
                if st.button("🚨 Halucinace", use_container_width=True):
                    st.session_state.quiz_answered = True
                    st.session_state.quiz_user_said_hallucination = True
                    st.rerun()
        else:
            user_said_h = st.session_state.quiz_user_said_hallucination
            is_correct = user_said_h == q["answer"]

            if is_correct:
                st.session_state.quiz_score += 1
                st.success(f"✅ Správně! {q['explanation']}")
            else:
                st.error(f"❌ Špatně. {q['explanation']}")

            if q["indicators"]:
                st.warning("**Varovné signály:** " + " • ".join(q["indicators"]))

            if st.button("Další otázka →"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.rerun()
    else:
        score = st.session_state.quiz_score
        total = len(QUESTIONS)
        pct = score / total * 100

        st.balloons()
        st.markdown(f"## Výsledek: {score}/{total} ({pct:.0f} %)")

        if pct >= 80:
            st.success("Výborně! Máte dobrý čich na halucinace.")
        elif pct >= 50:
            st.warning("Solidní základ, ale AI umí být přesvědčivá.")
        else:
            st.info("Nevadí — právě proto je kritické myšlení tak důležité!")

        st.markdown("""
        ### Checklist pro rozpoznání halucinací
        | Test | Co kontrolovat |
        |------|---------------|
        | **SMELL TEST** | Zní to rozumně, nebo jako generická fráze? |
        | **NUMBER CHECK** | Jsou čísla realistická? Nejsou příliš specifická? |
        | **SOURCE HUNT** | Existují zdroje? Lze je dohledat? |
        | **LOGIC SCAN** | Následují argumenty logicky? |
        | **EXPERT GUT** | Co by řekl kolega z oboru? |
        | **CHALLENGE** | Zeptejte se AI: "Jsi si jistá?" |
        """)

        if st.button("Začít znovu"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = False
            random.shuffle(st.session_state.quiz_order)
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════
#  5. PROMPTING
# ═════════════════════════════════════════════════════════════════════════
elif page == "5. Prompting":
    st.title("💬 Prompting — Techniky a šablony")

    st.markdown("Srovnání promptovacích technik s příklady pro výzkum na RECETOX.")

    TECHNIQUES = [
        {
            "name": "Zero-shot",
            "icon": "🎯",
            "when": "Jednoduché, jasně definované úlohy",
            "bad": "Řekni mi něco o PFAS.",
            "good": "Vysvětli, co jsou PFAS (per- a polyfluoralkylové látky), jaké jsou jejich hlavní zdroje v životním prostředí a proč se jim říká 'forever chemicals'. Odpověz ve 3 odstavcích.",
        },
        {
            "name": "Chain of Thought",
            "icon": "🔗",
            "when": "Složité výpočty, logické odvozování",
            "bad": "Vyhodnoť toxicitu tohoto vzorku.",
            "good": "Mám vzorek vody:\n- Olovo: 15 µg/L\n- Kadmium: 3.5 µg/L\n- Arsen: 8 µg/L\n\nPorovnej s limity EU 2020/2184. U každé látky uveď: 1) naměřenou hodnotu, 2) limit EU, 3) poměr, 4) hodnocení. Na závěr shrň.",
        },
        {
            "name": "Tree of Thought",
            "icon": "🌳",
            "when": "Rozhodování s více dobrými řešeními",
            "bad": "Jak analyzovat pesticidy?",
            "good": "Analyzuji reziduá pesticidů v ovoci. Prozkoumej 3 přístupy:\nA: QuEChERS + GC-MS/MS\nB: QuEChERS + LC-MS/MS\nC: SFE + GC-MS\n\nPro každý uveď vhodnost, počet detekovatelných pesticidů, náročnost, skóre 1-10.",
        },
        {
            "name": "Dekompozice",
            "icon": "📦",
            "when": "Komplexní úlohy (rešerše, návrhy experimentů)",
            "bad": "Napiš rešerši o mikroplastech v půdě.",
            "good": "Připravíme rešerši o mikroplastech v půdě po krocích:\n1. Identifikuj 5 klíčových aspektů\n2. Navrhni vyhledávací strategii\n3. Shrň stav poznání\n4. Identifikuj mezery\n5. Navrhni strukturu\n\nZačni krokem 1.",
        },
        {
            "name": "Sebekritika",
            "icon": "🔄",
            "when": "Když potřebujete vysokou kvalitu textu",
            "bad": "Napiš abstrakt pro můj článek.",
            "good": "Napiš abstrakt (max 250 slov) pro Environmental Pollution:\nTéma: Vliv mikroplastů na sorpci těžkých kovů v půdě\nMetodika: Batch sorpční experimenty, SEM-EDS\nVýsledek: PE a PP zvyšují mobilitu Cd o 15-30 %\n\nPak: 1) zkritizuj, 2) přepiš, 3) porovnej verze.",
        },
        {
            "name": "PROMPT Framework",
            "icon": "📐",
            "when": "Maximální kvalita odpovědi",
            "bad": "Pomoz mi s výzkumem.",
            "good": "PURPOSE: Najít analytickou metodu pro emerging pollutants v odpadních vodách\nROLE: Analytický chemik, 15 let zkušeností, LC-MS\nOBJECTIVE: Srovnávací tabulka 4 metod (LOD, LOQ, opakovatelnost)\nMETHOD: Definuj kritéria → porovnej → doporuč\nPARAMETERS: Tabulka, PPCPs, roky 2020-2026\nTONE: Odborný, stručný",
        },
    ]

    for tech in TECHNIQUES:
        with st.expander(f"{tech['icon']} {tech['name']} — {tech['when']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**❌ Slabý prompt:**")
                st.code(tech["bad"], language=None)
            with col2:
                st.markdown("**✅ Silný prompt:**")
                st.code(tech["good"], language=None)

    # PROMPT builder
    st.markdown("---")
    st.markdown("### 🛠️ PROMPT Builder")
    st.markdown("Sestavte si prompt pomocí PROMPT frameworku:")

    p = st.text_input("**P**urpose — Co potřebujete:", placeholder="Najít vhodnou analytickou metodu...")
    r = st.text_input("**R**ole — Kdo má AI být:", placeholder="Analytický chemik se specializací na...")
    o = st.text_input("**O**bjective — Konkrétní výstup:", placeholder="Srovnávací tabulka 4 metod...")
    m = st.text_input("**M**ethod — Jak postupovat:", placeholder="Nejdřív definuj kritéria, pak porovnej...")
    pa = st.text_input("**P**arameters — Formální požadavky:", placeholder="Max 500 slov, tabulka, roky 2020-2026...")
    t = st.text_input("**T**one — Styl komunikace:", placeholder="Odborný, stručný, pro laboratorní zprávu...")

    if any([p, r, o, m, pa, t]):
        prompt_parts = []
        if p: prompt_parts.append(f"PURPOSE: {p}")
        if r: prompt_parts.append(f"ROLE: {r}")
        if o: prompt_parts.append(f"OBJECTIVE: {o}")
        if m: prompt_parts.append(f"METHOD: {m}")
        if pa: prompt_parts.append(f"PARAMETERS: {pa}")
        if t: prompt_parts.append(f"TONE: {t}")
        full_prompt = "\n\n".join(prompt_parts)

        st.markdown("#### Váš prompt:")
        st.code(full_prompt, language=None)
        st.caption("Zkopírujte a vložte do ChatGPT, Claude nebo Gemini.")


# ═════════════════════════════════════════════════════════════════════════
#  6. BIAS V DATECH
# ═════════════════════════════════════════════════════════════════════════
elif page == "6. Bias v datech":
    st.title("⚖️ Bias v datech — Garbage In, Garbage Out")

    import pandas as pd

    tab1, tab2, tab3, tab4 = st.tabs([
        "🌍 Geografický bias",
        "🗣️ Jazykový bias",
        "🔄 Model collapse",
        "📊 Korelace vs. kauzalita",
    ])

    # ── Tab 1: Geografický bias ───────────────────────────────────────────
    with tab1:
        st.markdown("### Jak rozložení publikací zkresluje odpovědi AI")

        data = {
            "Region": ["Severní Amerika", "Západní Evropa", "Východní Asie",
                       "Latinská Amerika", "Východní Evropa", "Afrika",
                       "Jižní Asie", "Oceánie"],
            "Publikace (%)": [32, 28, 18, 8, 6, 4, 3, 1],
            "Skutečné problémy (%)": [15, 12, 20, 15, 10, 15, 10, 3],
        }
        df = pd.DataFrame(data)

        st.bar_chart(df, x="Region", y=["Publikace (%)", "Skutečné problémy (%)"])

        st.warning("""
        **Bias:** AI "ví" víc o kontaminaci v USA a Evropě, protože o nich bylo
        napsáno víc článků. O Africe "ví" minimum — ne proto, že tam problémy
        nejsou, ale proto, že data chybí.
        """)

    # ── Tab 2: Jazykový bias ─────────────────────────────────────────────
    with tab2:
        st.markdown("### Zastoupení jazyků v trénovacích datech LLM")

        lang_data = {
            "Jazyk": ["Angličtina", "Čínština", "Němčina", "Francouzština",
                      "Španělština", "Ruština", "Japonština", "Čeština", "Slovenština"],
            "Podíl (%)": [55.0, 8.0, 5.0, 5.0, 4.0, 3.0, 3.0, 0.5, 0.2],
        }
        df_lang = pd.DataFrame(lang_data)
        st.bar_chart(df_lang, x="Jazyk", y="Podíl (%)")

        st.markdown("""
        **Důsledky pro česky mluvící výzkumníky:**
        - AI odpovídá v češtině, ale "myslí" anglicky
        - Odborná terminologie může být nepřesně přeložena
        - Kulturní a právní kontext neodpovídá české realitě
        - České zdroje (legislativa, instituce) model nezná

        **Doporučení:** Zadávejte prompty v angličtině pro odborný text.
        Český výstup vždy zkontrolujte z hlediska terminologie.
        """)

    # ── Tab 3: Model collapse ────────────────────────────────────────────
    with tab3:
        st.markdown("### Co se stane, když AI trénujeme na AI-generovaných datech?")

        random.seed(42)
        original = {"Benzo[a]pyren": 85, "DDT": 72, "Glyfosfát": 35, "Kofein": 8, "Voda": 0}
        generations = st.slider("Počet generací:", 1, 10, 6)
        noise = st.slider("Faktor šumu:", 0.05, 0.30, 0.15)

        results = []
        for substance, true_val in original.items():
            row = {"Látka": substance, "Skutečnost": true_val}
            current = float(true_val)
            mean_val = sum(original.values()) / len(original)
            for g in range(1, generations + 1):
                n = random.gauss(0, true_val * noise + 5)
                regression = (mean_val - current) * 0.1
                current = max(0, min(100, current + n + regression))
                row[f"Gen {g}"] = round(current)
            results.append(row)

        df_collapse = pd.DataFrame(results)
        st.dataframe(df_collapse, use_container_width=True)

        # Vizualizace
        chart_data = {}
        for _, row in df_collapse.iterrows():
            vals = [row["Skutečnost"]] + [row[f"Gen {g}"] for g in range(1, generations + 1)]
            chart_data[row["Látka"]] = vals

        chart_df = pd.DataFrame(chart_data, index=["Skutečnost"] + [f"Gen {g}" for g in range(1, generations + 1)])
        st.line_chart(chart_df)

        st.error("""
        **Model collapse:** S každou generací se hodnoty vzdalují od skutečnosti.
        Extrémní hodnoty se posouvají k průměru — AI "normalizuje".
        Internet se plní AI obsahem → nové modely se trénují na tomto obsahu → kvalita klesá.
        """)

    # ── Tab 4: Korelace vs. kauzalita ────────────────────────────────────
    with tab4:
        st.markdown("### AI najde korelace, ale nerozumí kauzalitě")

        correlations = [
            ("Spotřeba zmrzliny ↔ počet utonutí", 0.87, False, "Obojí způsobuje horké počasí"),
            ("Expozice azbestu ↔ mesotheliom", 0.92, True, "Azbest přímo způsobuje mesotheliom"),
            ("Filmy N. Cage ↔ utonutí v bazénech", 0.67, False, "Náhodná korelace"),
            ("PM2.5 ↔ respirační onemocnění", 0.78, True, "Částice poškozují plíce"),
            ("Bio potraviny ↔ autismus", 0.95, False, "Oba trendy rostou v čase"),
        ]

        for statement, r, causal, explanation in correlations:
            col1, col2, col3 = st.columns([4, 1, 3])
            col1.write(f"**{statement}**")
            col2.write(f"r = {r:.2f}")
            if causal:
                col3.success(f"✅ Kauzální — {explanation}")
            else:
                col3.error(f"❌ Ne-kauzální — {explanation}")

        st.info("""
        **Pro AI je korelace i kauzalita jen "co se vyskytuje spolu v datech".**
        Model nerozumí mechanismům. NIKDY nepřijímejte kauzální tvrzení AI bez ověření.
        """)


# =====================================================================
#  CHEAT SHEET
# =====================================================================
elif page == "\U0001f4cb Cheat Sheet":
    st.title("\U0001f4cb Cheat Sheet -- Praktická reference")
    st.markdown("Tuto stránku si **uložte do záložek** -- obsahuje vše podstatné na jednom místě.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "\U0001f6e0\ufe0f Nástroje",
        "\U0001f4d0 PROMPT Framework",
        "\u2705 Checklist",
        "\U0001f4dd Jak deklarovat AI",
        "\u26a0\ufe0f Časté chyby",
    ])

    with tab1:
        st.markdown("""
        ### Konverzační AI

        | Nástroj | Model | Kontext | Silné stránky |
        |---------|-------|---------|---------------|
        | **ChatGPT** | GPT-5.4 | až 1M tokenů | Univerzální, kód, multimodální |
        | **Claude** | Opus/Sonnet 4.6 | až 1M tokenů | Dlouhé texty, etika, kód |
        | **Gemini** | Gemini 3.1 PRO | až 1M tokenů | Google integrace, video |
        | **Copilot** | GPT-5.2/5.3 | 128k-400k | Office 365 integrace |

        ### AI vyhledávání (akademické)

        | Nástroj | Typ | Klíčová vlastnost | Zdarma? |
        |---------|-----|-------------------|---------|
        | **Perplexity** | AI vyhledávač | Vždy RAG, cituje zdroje | Limitovaně |
        | **Scite** | Akademický | Smart Citations | Limitovaně |
        | **Elicit** | Akademický | Extrakce dat z článků | Limitovaně |
        | **Consensus** | Akademický | Syntéza vědeckých závěrů | Limitovaně |
        | **Semantic Scholar** | Akademický | Sémantické hledání, open access | Ano |
        | **NotebookLM** | Práce s texty | Nahrané dokumenty jako zdroj | Ano |
        | **Scopus AI** | Databázový | RAG nad Scopus | Přes MU |
        | **WOS Research Assis.** | Databázový | Generování dotazů z NL | Přes MU |

        ### Na MU máte k dispozici

        | Nástroj | Přístup | Poznámka |
        |---------|---------|----------|
        | **MS Copilot Chat** | Všichni na MU | GPT 5.3/5.4, OneDrive + email |
        | **Gemini** | Google Workspace | Gemini 3/3.1 PRO |
        | **AI as a Service** | e-Infra.cz (zaměstnanci) | Data neopouští e-INFRA |
        """)

    with tab2:
        st.markdown("### PROMPT Framework -- šablona ke kopírování")
        st.code("""PURPOSE: [Co potřebujete -- konkrétní úloha]

ROLE: [Kdo má AI být -- odbornost, perspektiva]

OBJECTIVE: [Konkrétní, měřitelný výstup]

METHOD: [Jak postupovat -- krok po kroku]

PARAMETERS: [Formální požadavky -- délka, formát, omezení]

TONE: [Styl komunikace -- akademický, stručný, pro koho]""", language=None)

        st.markdown("""
        ### Promptovací techniky -- kdy co použít

        | Situace | Technika | Klíčová fráze |
        |---------|----------|---------------|
        | Jednoduchý dotaz | **Zero-shot** | Prostě se zeptejte |
        | Výpočet / logika | **Chain of Thought** | "Ukaž mezikroky" |
        | Rozhodování | **Tree of Thought** | "Prozkoumej 3 přístupy" |
        | Komplexní úloha | **Dekompozice** | "Rozlož na kroky, začni krokem 1" |
        | Kvalitní text | **Sebekritika** | "Zkritizuj a přepiš" |
        | Nejistota | **Meta-prompting** | "Navrhni optimální prompt pro..." |
        | Specifická perspektiva | **Role/Persona** | "Jsi [expert] s [X lety zkušeností]" |
        | Strukturovaný výstup | **Scaffolding** | Připravte kostru, AI doplní |
        | Kritické úlohy | **Self-consistency** | "Vyřeš 3 různými způsoby" |
        """)

        st.markdown("### Custom instructions -- šablona pro výzkumníka")
        st.code("""Jsem výzkumník v oblasti [obor] na RECETOX, Masarykova univerzita.
Pracuji s [specifikace].

Pravidla:
- Když cituješ zdroj, uveď DOI. Pokud si nejsi jistý, řekni.
- Nebuď servilní. Neříkej "skvělá otázka".
- Když tvrdím něco chybného, oprav mě.
- U číselných dat vždy uveď jednotky a nejistotu.
- Preferuj peer-reviewed zdroje.

Tagy:
<academic> -- přesnost, citace, APA formát
<critic>   -- buď kritický a zpochybňuj
<source>   -- ke každému tvrzení uveď zdroj
<explain>  -- vysvětli jednoduše jako nejlepší učitel""", language=None)

    with tab3:
        st.markdown("""
        ### Před použitím AI se zeptejte

        - [ ] **Co potřebuji?** -- Definujte informační potřebu
        - [ ] **Co už vím?** -- Oddělte vlastní znalost od AI asistence
        - [ ] **Jaký nástroj?** -- Konverzační AI, AI vyhledávání, nebo specializovaný nástroj?
        - [ ] **Jsou data citlivá?** -- Nepublikovaná data, pacienti -> e-Infra / lokální AI

        ### Po obdržení odpovědi (SMELL checklist)

        | Test | Otázka |
        |------|--------|
        | **S** -- Smell test | Zní to rozumně, nebo jako generická fráze? |
        | **M** -- Math / Numbers | Jsou čísla realistická? Dávají smysl v kontextu? |
        | **E** -- Evidence | Existují uvedené zdroje? Lze je dohledat? Sedí DOI? |
        | **L** -- Logic | Následují argumenty logicky? Nejsou tam protimluvy? |
        | **L** -- Limits | Spadá to do znalostí modelu? Není to za knowledge cutoff? |

        ### Další kontroly

        - [ ] **Expert gut** -- Co by řekl kolega z oboru?
        - [ ] **Challenge** -- Zeptejte se AI: "Jsi si jistá? Uveď konkrétní zdroj."
        - [ ] **Cross-check** -- Ověřte klíčová tvrzení v jiném modelu nebo primárním zdroji
        - [ ] **Unit check** -- Souhlasí jednotky? (ug/L vs. mg/kg, ppm vs. ppb)
        """)

    with tab4:
        st.markdown("""
        ### Instrument vs. Interpreter -- co deklarovat

        | Úroveň | Příklad | Co uvést |
        |--------|---------|----------|
        | **Instrument** | Korektura, formátování, překlad | Není třeba deklarovat |
        | **Instrument (výzkum)** | Kódování dat, výběr metody, rešerše | Poznámka v metodice |
        | **Šedá zóna** | AI navrhuje, já přijímám a zodpovídám | Uvést v metodice + limitacích |
        | **Interpreter** | AI formuluje závěry z dat | Metodika + limitace + zvážit přijatelnost |

        ### Vzorová formulace pro metody
        """)

        st.code("""AI-assisted analysis was conducted using [model name, version].
The tool was used for [specific tasks: e.g., literature screening,
code generation, data visualization]. All AI-generated outputs
were independently verified by the authors against [primary sources /
original data / established methods]. The authors take full
responsibility for the accuracy of the final results.""", language=None)

        st.markdown("""
        ### Klíčové otázky

        > *Kdo tu rozhoduje -- já nebo AI?*

        > *Umím výstup obhájit vlastními slovy?*

        > *Byl/a bych v pohodě, kdyby kolegové věděli přesně jak jsem AI použil/a?*

        ### MUNI politika

        Masarykova univerzita vyžaduje **transparentní deklaraci** použití AI.
        Nezveřejněné použití AI se posuzuje jako plagiát.
        """)

    with tab5:
        st.markdown("""
        ### Top 10 chyb výzkumníků s AI

        | # | Chyba | Jak se bránit |
        |---|-------|---------------|
        | 1 | **Citování AI jako zdroje** | AI není zdroj -- dohledejte primární literaturu |
        | 2 | **Vymyšlené reference** | Ověřte KAŽDÝ DOI, autora, časopis |
        | 3 | **Chybné jednotky** | AI míchá ug/L vs. mg/kg, ppm vs. ppb |
        | 4 | **Vymyšlená statistika** | Nedůvěřujte p-hodnotám a CI z AI |
        | 5 | **Knowledge cutoff** | Model nezná nedávné publikace a legislativu |
        | 6 | **Automation bias** | Nekontrolujete AI-generovaný kód |
        | 7 | **Ztráta porozumění** | Používáte statistiku, které nerozumíte |
        | 8 | **Nereprodukovatelnost** | Stejný prompt = jiná odpověď jindy |
        | 9 | **Únik dat** | Nepublikovaná data v komerčním API |
        | 10 | **Homogenizace** | "AI hlas" -- recenzenti to poznají |

        ### Specificky pro environmentální výzkum

        - **Chemické názvy**: AI může zaměnit IUPAC názvy, CAS čísla nebo sm��si
        - **Regulatorní limity**: Limity se liší podle jurisdikce a matrice -- AI je míchá
        - **Kauzální tvrzení**: "X způsobuje Y" z AI = korelace v datech, ne mechanismus
        - **Záznamy o expozici**: Nikdy nevkládejte osobní data subjektů do komerčních AI
        """)
