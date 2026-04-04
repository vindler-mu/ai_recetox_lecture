#!/usr/bin/env python3
"""
=============================================================================
  SÉMANTICKÉ VYHLEDÁVÁNÍ — Proč AI rozumí významu, ne jen slovům
=============================================================================
  Tento skript ukazuje rozdíl mezi klasickým (keyword) a sémantickým
  vyhledáváním. Simuluje, jak vektorové embeddingy umožňují najít
  podobné dokumenty i bez přesné shody klíčových slov.

  Spuštění: python 03_semanticke_vyhledavani.py
=============================================================================
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import math
import random

random.seed(42)


# -- Simulovane embeddingy --------------------------------------------------
# Reálné embeddingy mají stovky dimenzí. Zde používáme 8 dimenzí pro ilustraci.
# Každá dimenze zachycuje určitý "aspekt významu":
#   [toxicita, životní_prostředí, chemie, zdraví, voda, půda, analýza, regulace]

DOCUMENTS = {
    "Kontaminace podzemních vod pesticidy v zemědělských oblastech":
        [0.6, 0.9, 0.7, 0.4, 0.95, 0.1, 0.5, 0.3],

    "Vliv polychlorovaných bifenylů na reprodukci ryb":
        [0.9, 0.8, 0.8, 0.6, 0.7, 0.1, 0.4, 0.5],

    "Metody stanovení těžkých kovů v půdních vzorcích":
        [0.5, 0.7, 0.9, 0.2, 0.1, 0.95, 0.9, 0.2],

    "Legislativní rámec pro REACH registraci chemických látek":
        [0.3, 0.5, 0.6, 0.3, 0.1, 0.1, 0.2, 0.95],

    "Biomonitoring persistentních organických polutantů v mateřském mléce":
        [0.8, 0.6, 0.7, 0.9, 0.1, 0.1, 0.7, 0.4],

    "Remediace brownfieldů pomocí fytotechnologií":
        [0.4, 0.9, 0.5, 0.3, 0.2, 0.8, 0.3, 0.3],

    "Endokrinní disruptory v pitné vodě a jejich zdravotní rizika":
        [0.8, 0.7, 0.7, 0.9, 0.9, 0.1, 0.5, 0.6],

    "Analytické postupy pro identifikaci nových kontaminantů":
        [0.5, 0.6, 0.8, 0.3, 0.3, 0.3, 0.95, 0.2],

    "Hodnocení ekotoxicity nanočástic stříbra":
        [0.9, 0.8, 0.6, 0.5, 0.4, 0.3, 0.6, 0.3],

    "Úprava kvality řek a chemické složení sedimentů":
        [0.4, 0.8, 0.7, 0.2, 0.8, 0.3, 0.5, 0.4],
}


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Kosinová podobnost dvou vektorů (0 = nepodobné, 1 = identické)."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def keyword_search(query: str, documents: dict) -> list[tuple[str, int]]:
    """Klasické klíčové vyhledávání — počet shodných slov."""
    query_words = set(query.lower().split())
    results = []
    for title in documents:
        title_words = set(title.lower().split())
        matches = len(query_words & title_words)
        results.append((title, matches))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def semantic_search(query_vec: list[float], documents: dict) -> list[tuple[str, float]]:
    """Sémantické vyhledávání — kosinová podobnost vektorů."""
    results = []
    for title, vec in documents.items():
        sim = cosine_similarity(query_vec, vec)
        results.append((title, sim))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def bar_chart(value: float, max_width: int = 30) -> str:
    filled = int(value * max_width)
    return "█" * filled + "░" * (max_width - filled)


def main():
    print(__doc__)

    queries = [
        {
            "text": "znečištění vody chemikáliemi",
            "vector": [0.7, 0.8, 0.7, 0.5, 0.9, 0.1, 0.3, 0.3],
            "explanation": "Hledáme dokumenty o chemickém znečištění vodních zdrojů.",
        },
        {
            "text": "analýza škodlivin v zemině",
            "vector": [0.5, 0.7, 0.8, 0.2, 0.1, 0.9, 0.8, 0.2],
            "explanation": "Hledáme metody analýzy kontaminantů v půdě.",
        },
        {
            "text": "health effects of toxic substances",
            "vector": [0.8, 0.5, 0.6, 0.9, 0.3, 0.2, 0.4, 0.4],
            "explanation": "Anglický dotaz — sémantické hledání najde i české dokumenty!",
        },
    ]

    for q_idx, query in enumerate(queries, 1):
        print("=" * 70)
        print(f"  DOTAZ {q_idx}: \"{query['text']}\"")
        print(f"  {query['explanation']}")
        print("=" * 70)

        # -- Keyword search ------------------------------------------------------
        print("\n  \033[94m> KLASICKÉ VYHLEDÁVÁNÍ (shoda klíčových slov)\033[0m")
        kw_results = keyword_search(query["text"], DOCUMENTS)
        has_any = False
        for rank, (title, matches) in enumerate(kw_results[:5], 1):
            if matches > 0:
                has_any = True
                print(f"    {rank}. [{matches} shod] {title}")
        if not has_any:
            print("    [!]  Žádná shoda! Dotaz neobsahuje přesná slova z dokumentů.")

        # -- Semantic search -----------------------------------------------------
        print(f"\n  \033[92m> SÉMANTICKÉ VYHLEDÁVÁNÍ (podobnost významu)\033[0m")
        sem_results = semantic_search(query["vector"], DOCUMENTS)
        for rank, (title, sim) in enumerate(sem_results[:5], 1):
            bar = bar_chart(sim)
            color = "\033[92m" if sim > 0.85 else "\033[93m" if sim > 0.75 else "\033[0m"
            print(f"    {rank}. {color}{sim:.1%}\033[0m {bar}  {title}")

        print()

    # -- Vizualizace vektoru ---------------------------------------------------
    print("=" * 70)
    print("  JAK VYPADÁ EMBEDDING? (zjednodušená ukázka)")
    print("=" * 70)

    dimensions = ["toxicita", "prostředí", "chemie", "zdraví", "voda", "půda", "analýza", "regulace"]
    example_title = "Endokrinní disruptory v pitné vodě a jejich zdravotní rizika"
    example_vec = DOCUMENTS[example_title]

    print(f"\n  Dokument: \"{example_title}\"")
    print(f"  Vektor:   {example_vec}\n")
    for dim, val in zip(dimensions, example_vec):
        bar = bar_chart(val, 25)
        print(f"    {dim:12s} {val:.1f} {bar}")

    # -- Shrnuti ---------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  CO Z TOHO PLYNE?")
    print("=" * 70)
    print("""
  KLASICKÉ VYHLEDÁVÁNÍ:
    + Přesné, deterministické, rychlé
    - "monitor" ≠ "screen", "zemina" ≠ "půda"
    - Hledá přesná slova, ne význam

  SÉMANTICKÉ VYHLEDÁVÁNÍ:
    + Rozumí významu, najde i synonyma
    + Funguje napříč jazyky (EN dotaz -> CS dokumenty)
    - Méně přesné u specifických termínů (chemické vzorce, zkratky)
    - Nedeterministické — výsledky se mohou lišit

  IDEÁLNÍ ŘEŠENÍ: Hybridní přístup (BM25 + sémantika)
    -> Přesně to dělají moderní nástroje jako Scopus AI, Semantic Scholar

  DŮLEŽITÉ PRO RECETOX:
    Chemické názvy (CAS čísla, IUPAC) -> klasické hledání je přesnější
    Konceptuální dotazy ("vliv na zdraví") -> sémantika je silnější
    """)


if __name__ == "__main__":
    main()
