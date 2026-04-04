#!/usr/bin/env python3
"""
=============================================================================
  TOKENIZACE -- Jak AI rozdeluje text na kousky
=============================================================================
  Tato ukazka pouziva SKUTECNY tokenizer (tiktoken, o200k_base),
  stejny jako modely GPT. Ukazuje, jak se anglicky a cesky text
  rozklada na tokeny a proc cestina stoji vic.

  Pozadavky: pip install tiktoken
  Spusteni:  python 01_tokenizace.py
=============================================================================
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import tiktoken


# Pouzivame encoding o200k_base (GPT-5 / GPT-4o)
# Slovnik ma ~200 000 tokenu -- cela anglicka slova jsou casto 1 token,
# ceske tvary se rozpadaji na vice kousku.
enc = tiktoken.get_encoding("o200k_base")


def tokenize(text: str) -> list[str]:
    """Tokenizuje text a vrati seznam dekodovanych tokenu."""
    token_ids = enc.encode(text)
    return [enc.decode([tid]) for tid in token_ids]


def visualize_tokens(tokens: list[str], label: str):
    """Vizualizuje tokeny s barvami v konzoli."""
    colors = [
        "\033[42m\033[30m",  # zelena
        "\033[44m\033[37m",  # modra
        "\033[43m\033[30m",  # zluta
        "\033[45m\033[37m",  # fialova
        "\033[46m\033[30m",  # cyan
        "\033[41m\033[37m",  # cervena
    ]
    reset = "\033[0m"

    print(f"\n  {label}")
    print("  ", end="")
    for i, token in enumerate(tokens):
        color = colors[i % len(colors)]
        display = token.replace(" ", "_")
        print(f"{color} {display} {reset}", end="")
    print()
    print(f"  Celkem tokenu: {len(tokens)}")


def compare(en_text: str, cs_text: str, label: str = ""):
    """Porovna tokenizaci anglickeho a ceskeho textu."""
    if label:
        print(f"\n  {label}")
        print(f"  {'-' * 60}")

    en_tokens = tokenize(en_text)
    cs_tokens = tokenize(cs_text)

    visualize_tokens(en_tokens, f'EN: "{en_text}"')
    visualize_tokens(cs_tokens, f'CS: "{cs_text}"')

    ratio = len(cs_tokens) / len(en_tokens) if en_tokens else 0
    print(f"  Pomer CS/EN: {ratio:.1f}x ({len(cs_tokens)} vs {len(en_tokens)} tokenu)")
    return len(en_tokens), len(cs_tokens)


def main():
    print(__doc__)

    # -- Priklad 1: Stejna veta ------------------------------------------------
    print("=" * 70)
    print("  PRIKLAD 1: Stejna veta -- realny tokenizer (o200k_base)")
    print("=" * 70)
    print("  Slovnik ma ~200 000 tokenu. Bezna anglicka slova = 1 token.")
    print("  Ceske tvary se casto rozpadaji na vice kousku.")

    compare(
        "The environmental contamination was investigated.",
        "Environmentalni kontaminace byla prozkoumana.",
    )

    # -- Priklad 2: Odborna terminologie (RECETOX) -----------------------------
    print("\n" + "=" * 70)
    print("  PRIKLAD 2: Odborna terminologie (RECETOX kontext)")
    print("=" * 70)

    terms = [
        ("polychlorinated biphenyls", "polychlorovane bifenyly"),
        ("persistent organic pollutants", "perzistentni organicke polutanty"),
        ("endocrine disruptors in drinking water", "endokrinni disruptory v pitne vode"),
        ("heavy metals in soil samples", "tezke kovy v pudnich vzorcich"),
        ("per- and polyfluoroalkyl substances", "per- a polyfluoralkylove latky"),
    ]

    total_en, total_cs = 0, 0
    for en, cs in terms:
        en_t, cs_t = compare(en, cs)
        total_en += en_t
        total_cs += cs_t

    print(f"\n  CELKEM: EN = {total_en} tokenu, CS = {total_cs} tokenu")
    print(f"  Prumerny pomer: {total_cs / total_en:.1f}x")

    # -- Priklad 3: Vlastni text -----------------------------------------------
    print("\n" + "=" * 70)
    print("  PRIKLAD 3: Jeden odstavec -- jak moc se to nasci?")
    print("=" * 70)

    en_para = (
        "The study investigated the occurrence of persistent organic pollutants "
        "in agricultural soil samples collected from three regions of the Czech Republic. "
        "Results indicate significant contamination levels exceeding EU regulatory limits."
    )
    cs_para = (
        "Studie zkoumala vyskyt perzistentnich organickych polutantu "
        "ve vzorcich zemedelske pudy odebranych ze tri regionu Ceske republiky. "
        "Vysledky ukazuji vyznamne urovne kontaminace prekracujici regulacni limity EU."
    )

    en_tokens = tokenize(en_para)
    cs_tokens = tokenize(cs_para)

    print(f"\n  EN ({len(en_tokens)} tokenu):")
    visualize_tokens(en_tokens, "")
    print(f"\n  CS ({len(cs_tokens)} tokenu):")
    visualize_tokens(cs_tokens, "")

    ratio = len(cs_tokens) / len(en_tokens)
    print(f"\n  Pomer: {ratio:.2f}x")
    print(f"  Cesky text je o {ratio - 1:.0%} drazsi na zpracovani.")

    # -- Priklad 4: Pocitani pismen --------------------------------------------
    print("\n" + "=" * 70)
    print("  PRIKLAD 4: Proc AI spatne pocita pismena")
    print("=" * 70)

    word = "strawberry"
    tokens = tokenize(word)
    visualize_tokens(tokens, f'Slovo: "{word}"')
    print(f"  Model vidi {len(tokens)} token(y), ne {len(word)} pismen!")
    print(f"  Tokeny: {tokens}")
    print("  Proto muze spatne odpovedet na 'Kolik r je ve slove strawberry?'")

    word2 = "jahoda"
    tokens2 = tokenize(word2)
    visualize_tokens(tokens2, f'Slovo: "{word2}"')
    print(f"  Tokeny: {tokens2}")

    # -- Proc na tom zalezi ----------------------------------------------------
    print("\n" + "=" * 70)
    print("  PROC NA TOKENIZACI ZALEZI?")
    print("=" * 70)
    print("""
  1. CENA -- Platite za tokeny, ne za slova.
     Stejny text v cestine stoji o ~50-80 % vic nez v anglictine.

  2. KONTEXT -- Kontextove okno modelu ma limit (napr. 200k-1M tokenu).
     Cesky text zabere v kontextu vice mista.

  3. KVALITA -- Model lepe rozumi tokenu, ktere videl casteji.
     "environmental" = 1 token (zna dobre), "environmentalni" = 2+ tokeny.

  4. ARITMETIKA -- Model nevidi pismena, vidi tokeny.
     Proto pocitani selhava.

  5. VYHLEDAVANI -- Ceske odborne terminy se rozpadaji na kousky,
     ktere mohou ztratet svuj specificky vyznam.
    """)


if __name__ == "__main__":
    main()
