#!/usr/bin/env python3
"""
=============================================================================
  BIAS V DATECH — Garbage In, Garbage Out
=============================================================================
  Simulace toho, jak nerovnoměrné zastoupení v trénovacích datech
  ovlivňuje výstupy AI modelu. Ukazuje, proč kvalita dat je klíčová.

  Spuštění: python 06_bias_demo.py
=============================================================================
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import random
import math

random.seed(42)


def bar_chart(value: float, max_width: int = 35, char: str = "█") -> str:
    filled = int(value * max_width)
    return char * filled + "░" * (max_width - filled)


# ═══════════════════════════════════════════════════════════════════════════
#  SIMULACE 1: Geografický bias v environmentálních datech
# ═══════════════════════════════════════════════════════════════════════════

def geographic_bias():
    """Ukazuje, jak geografické rozložení dat ovlivňuje odpovědi AI."""
    print("=" * 70)
    print("  SIMULACE 1: Geografický bias v trénovacích datech")
    print("=" * 70)

    # Simulovaná distribuce vědeckých článků o kontaminaci podle regionu
    # (odráží skutečný bias v publikacích)
    training_data = {
        "Severní Amerika": 0.32,
        "Západní Evropa":  0.28,
        "Východní Asie":   0.18,
        "Latinská Amerika": 0.08,
        "Východní Evropa":  0.06,
        "Afrika":           0.04,
        "Jižní Asie":       0.03,
        "Oceánie":          0.01,
    }

    # Skutečná distribuce environmentálních problémů (hypotetická)
    actual_problems = {
        "Severní Amerika": 0.15,
        "Západní Evropa":  0.12,
        "Východní Asie":   0.20,
        "Latinská Amerika": 0.15,
        "Východní Evropa":  0.10,
        "Afrika":           0.15,
        "Jižní Asie":       0.10,
        "Oceánie":          0.03,
    }

    print("\n  Distribuce trénovacích dat (vědecké publikace):")
    for region, pct in training_data.items():
        bar = bar_chart(pct)
        print(f"    {region:20s} {pct:5.0%}  {bar}")

    print("\n  Skutečné rozložení environmentálních problémů (odhad):")
    for region, pct in actual_problems.items():
        bar = bar_chart(pct, char="#")
        print(f"    {region:20s} {pct:5.0%}  {bar}")

    print("\n  \033[93m-> Bias: AI \"ví\" víc o kontaminaci v USA a Evropě,")
    print("    protože o nich bylo napsáno víc článků.")
    print("    O Africe a Jižní Asii \"ví\" minimum — ne proto, že tam")
    print("    problémy nejsou, ale proto, že data chybí.\033[0m")

    # Simulace: Co model odpoví na dotaz o kontaminaci
    print(f"\n  {'-' * 60}")
    print("  Dotaz: \"Které regiony světa jsou nejvíce zasaženy kontaminací\"")
    print(f"  {'-' * 60}")

    # Model generuje na základě dat, ne reality
    print("\n  \033[91mModel pravděpodobně odpoví:\033[0m")
    sorted_by_data = sorted(training_data.items(), key=lambda x: x[1], reverse=True)
    for i, (region, _) in enumerate(sorted_by_data[:3], 1):
        print(f"    {i}. {region}")

    print("\n  \033[92mAle skutečnost může být jiná:\033[0m")
    sorted_by_real = sorted(actual_problems.items(), key=lambda x: x[1], reverse=True)
    for i, (region, _) in enumerate(sorted_by_real[:3], 1):
        print(f"    {i}. {region}")


# ═══════════════════════════════════════════════════════════════════════════
#  SIMULACE 2: Jazykový bias
# ═══════════════════════════════════════════════════════════════════════════

def language_bias():
    """Ukazuje, jak jazykový bias ovlivňuje kvalitu odpovědí."""
    print("\n\n" + "=" * 70)
    print("  SIMULACE 2: Jazykový bias — kvalita odpovědí podle jazyka")
    print("=" * 70)

    # Odhadované zastoupení jazyků v trénovacích datech typického LLM
    languages = {
        "Angličtina":   0.55,
        "Čínština":     0.08,
        "Němčina":      0.05,
        "Francouzština": 0.05,
        "Španělština":   0.04,
        "Ruština":       0.03,
        "Japonština":    0.03,
        "Čeština":       0.005,
        "Slovenština":   0.002,
    }

    print("\n  Odhadované zastoupení jazyků v trénovacích datech LLM:")
    for lang, pct in languages.items():
        bar = bar_chart(min(pct * 2, 1.0))  # škálujeme pro vizualizaci
        color = "\033[92m" if pct > 0.05 else "\033[93m" if pct > 0.01 else "\033[91m"
        print(f"    {color}{lang:16s} {pct:6.1%}  {bar}\033[0m")

    print("""
  \033[93m-> Důsledky pro česky mluvící výzkumníky:\033[0m
    • AI odpovídá v češtině, ale "myslí" anglicky
    • Odborná terminologie může být nepřesně přeložena
    • Kulturní a právní kontext často neodpovídá české realitě
    • Specificky české zdroje (legislativa, instituce) model nezná

  \033[92m-> Doporučení:\033[0m
    • Zadávejte prompty v angličtině, pokud potřebujete odborný text
    • Český výstup vždy zkontrolujte z hlediska terminologie
    • U legislativy nikdy nespoléhejte na AI — ověřte v oficiálních zdrojích
    """)


# ═══════════════════════════════════════════════════════════════════════════
#  SIMULACE 3: Zpětnovazební smyčka (Data Drift)
# ═══════════════════════════════════════════════════════════════════════════

def feedback_loop():
    """Simuluje degradaci kvality dat přes generace AI-generovaného obsahu."""
    print("=" * 70)
    print("  SIMULACE 3: Zpětnovazební smyčka (Model Collapse)")
    print("=" * 70)
    print("""
  Co se stane, když AI trénujeme na datech, která sama vygenerovala?
  Simulujeme 'hru na telefon' — každá generace přidává šum.
    """)

    # Simulace: začneme s distribucí "skutečných" dat
    # a sledujeme, jak se mění přes generace AI-generovaného obsahu

    # Původní distribuce toxicity pro 5 látek (škála 0-100)
    original = {
        "Benzo[a]pyren":  85,
        "DDT":            72,
        "Glyfosfát":      35,
        "Kofein":         8,
        "Voda":           0,
    }

    generations = 6
    noise_factor = 0.15  # každá generace přidá ~15% šum

    print(f"  {'Látka':20s}", end="")
    print(f"  {'Skutečnost':>10s}", end="")
    for g in range(1, generations + 1):
        print(f"  {'Gen ' + str(g):>8s}", end="")
    print()
    print("  " + "-" * (20 + 10 + generations * 10))

    all_values = {}
    for substance, true_value in original.items():
        all_values[substance] = [true_value]
        current = float(true_value)

        print(f"  {substance:20s}  {true_value:8d}  ", end="")

        for g in range(generations):
            # Každá generace přidá šum + regrese k průměru
            mean_value = sum(original.values()) / len(original)
            noise = random.gauss(0, true_value * noise_factor + 5)
            regression = (mean_value - current) * 0.1  # regrese k průměru
            current = max(0, min(100, current + noise + regression))
            all_values[substance].append(round(current))

            # Barva podle odchylky od originálu
            deviation = abs(current - true_value) / max(true_value, 1)
            if deviation < 0.15:
                color = "\033[92m"  # zelená
            elif deviation < 0.3:
                color = "\033[93m"  # žlutá
            else:
                color = "\033[91m"  # červená
            print(f"{color}{current:8.0f}\033[0m", end="")

        print()

    # Shrnutí
    print(f"""
  \033[93m-> Co vidíme:\033[0m
    • S každou generací se hodnoty vzdalují od skutečnosti
    • Extrémní hodnoty se posouvají k průměru (AI "normalizuje")
    • Nízké hodnoty se uměle zvyšují, vysoké snižují
    • Po několika generacích jsou všechny látky "podobně toxické"

  \033[91m-> Toto je zjednodušená simulace problému zvaného 'model collapse':\033[0m
    Internet se plní AI-generovaným obsahem -> nové modely se trénují
    na tomto obsahu -> kvalita klesá -> a tak dokola.
    """)


# ═══════════════════════════════════════════════════════════════════════════
#  SIMULACE 4: Korelace vs. kauzalita
# ═══════════════════════════════════════════════════════════════════════════

def correlation_causation():
    """Ukazuje, že AI nalezne korelace, ale nerozumí kauzalitě."""
    print("=" * 70)
    print("  SIMULACE 4: Korelace ≠ Kauzalita")
    print("=" * 70)

    print("""
  AI model se naučil z dat následující statistické korelace.
  Ale které z nich jsou kauzální?
    """)

    correlations = [
        {
            "statement": "Vyšší spotřeba zmrzliny koreluje s vyšším počtem utonutí.",
            "r": 0.87,
            "causal": False,
            "explanation": "Obojí způsobuje horké počasí (confounding variable).",
        },
        {
            "statement": "Expozice azbestu koreluje s výskytem mesoteliomu.",
            "r": 0.92,
            "causal": True,
            "explanation": "Prokázaná kauzalita — azbest přímo způsobuje mesotheliom.",
        },
        {
            "statement": "Počet filmů Nicolase Cage koreluje s počtem utopení v bazénech.",
            "r": 0.67,
            "causal": False,
            "explanation": "Náhodná korelace (spurious correlation). Žádný mechanismus.",
        },
        {
            "statement": "Koncentrace PM2.5 koreluje s incidencí respiračních onemocnění.",
            "r": 0.78,
            "causal": True,
            "explanation": "Prokázaná kauzalita — drobné částice poškozují plíce.",
        },
        {
            "statement": "Prodej bio potravin koreluje s počtem případů autismu.",
            "r": 0.95,
            "causal": False,
            "explanation": "Oba trendy rostou v čase, ale nemají společný mechanismus.",
        },
    ]

    for i, corr in enumerate(correlations, 1):
        r = corr["r"]
        bar = bar_chart(r / 1.0, 20)

        print(f"  {i}. {corr['statement']}")
        print(f"     Korelace: r = {r:.2f}  {bar}")

        if corr["causal"]:
            print(f"     \033[92m[OK] KAUZÁLNÍ -- {corr['explanation']}\033[0m")
        else:
            print(f"     \033[91m[X] NE-KAUZÁLNÍ -- {corr['explanation']}\033[0m")
        print()

    print("""
  \033[93m-> Pro AI je korelace i kauzalita jen "co se vyskytuje spolu v datech".\033[0m
    Model nerozumí mechanismům. Když řekne "A způsobuje B", ve skutečnosti
    říká "v mých datech se A a B často vyskytují společně".

  \033[92m-> Důsledek pro výzkum:\033[0m
    NIKDY nepřijímejte kauzální tvrzení AI bez ověření mechanismu.
    AI je skvělá na hledání korelací — ale kauzalitu musíte posoudit vy.
    """)


def main():
    print(__doc__)

    geographic_bias()
    language_bias()
    feedback_loop()
    correlation_causation()

    # -- Celkove shrnuti -------------------------------------------------------
    print("=" * 70)
    print("  SHRNUTÍ: GARBAGE IN — GARBAGE OUT")
    print("=" * 70)
    print("""
  Kvalita výstupu AI je přímo úměrná kvalitě trénovacích dat.

  HLAVNÍ ZDROJE BIASU:
    1. Geografický — nadreprezentace západního světa
    2. Jazykový    — dominance angličtiny
    3. Temporální  — zastaralá data (knowledge cutoff)
    4. Kulturní    — západní normy jako "default"
    5. Publikační  — pozitivní výsledky převažují

  JAK SE BRÁNIT:
    • Ptejte se: "Odkud pocházejí data pro toto tvrzení?"
    • Ověřujte čísla v primárních zdrojích
    • Doplňujte kontext, který AI nemá (lokální data, legislativa)
    • Buďte si vědomi vlastních biasů — AI je potvrdí, ne opraví
    """)


if __name__ == "__main__":
    main()
