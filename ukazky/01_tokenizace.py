#!/usr/bin/env python3
"""
=============================================================================
  TOKENIZACE — Jak AI rozděluje text na kousky
=============================================================================
  Tato ukázka simuluje, jak jazykové modely (LLM) rozkládají text na tokeny.
  Ukazuje rozdíl mezi angličtinou a češtinou (flektivní jazyk = více tokenů).

  Spuštění: python 01_tokenizace.py
=============================================================================
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import re
import math


# -- Jednoduchy BPE-like tokenizer (simulace) -------------------------------
# Reálné tokenizery (tiktoken, sentencepiece) jsou mnohem složitější,
# ale princip je stejný: rozděl text na co nejmenší známé kousky.

# Simulovaný slovník — časté kousky angličtiny a češtiny
VOCAB_EN = [
    "the", "ing", "tion", "er", "ed", "al", "an", "or", "en", "es",
    "re", "on", "at", "is", "it", "in", "to", "of", "th", "he",
    "ar", "ou", "st", "nd", "ion", "ment", "ness", "able", "ful",
    "un", "pre", "dis", "ly", "ous", "ive", "ity", " ", ".", ",",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
]

VOCAB_CS = [
    "ní", "ov", "ost", "ná", "ně", "ský", "ská", "ské", "ho", "ch",
    "je", "se", "na", "po", "za", "př", "pro", "pre", "ne", "do",
    "od", "ve", "ko", "ro", "lo", "to", "no", "mo", "vo", "st",
    "ek", "ík", "ám", "ém", "ím", "ům", "ou", "ej", "aj",
    " ", ".", ",", "á", "é", "í", "ó", "ú", "ý", "ě", "ř", "ž",
    "š", "č", "ť", "ď", "ň",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
]


def simple_tokenize(text: str, vocab: list[str]) -> list[str]:
    """Greedy longest-match tokenizace (zjednodušená simulace BPE)."""
    tokens = []
    text_lower = text.lower()
    i = 0
    while i < len(text_lower):
        best_match = None
        best_len = 0
        for token in vocab:
            if text_lower[i:i+len(token)] == token and len(token) > best_len:
                best_match = token
                best_len = len(token)
        if best_match:
            tokens.append(text[i:i+best_len])  # zachovej originální velikost písmen
            i += best_len
        else:
            tokens.append(text[i])  # neznámý znak = samostatný token
            i += 1
    return tokens


def visualize_tokens(tokens: list[str], label: str):
    """Vizualizuje tokeny s barvami v konzoli."""
    colors = [
        "\033[42m\033[30m",  # zelená
        "\033[44m\033[37m",  # modrá
        "\033[43m\033[30m",  # žlutá
        "\033[45m\033[37m",  # fialová
        "\033[46m\033[30m",  # cyan
        "\033[41m\033[37m",  # červená
    ]
    reset = "\033[0m"

    print(f"\n  {label}")
    print("  ", end="")
    for i, token in enumerate(tokens):
        color = colors[i % len(colors)]
        display = token.replace(" ", "_")
        print(f"{color} {display} {reset}", end="")
    print()
    print(f"  Celkem tokenů: {len(tokens)}")


def main():
    print(__doc__)

    # -- Příklad 1: Stejná věta v angličtině a češtině ----------------------
    print("=" * 70)
    print("  PŘÍKLAD 1: Stejný význam, různý počet tokenů")
    print("=" * 70)

    en_text = "The environmental contamination was investigated."
    cs_text = "Environmentální kontaminace byla prozkoumána."

    en_tokens = simple_tokenize(en_text, VOCAB_EN)
    cs_tokens = simple_tokenize(cs_text, VOCAB_CS)

    visualize_tokens(en_tokens, f"EN: \"{en_text}\"")
    visualize_tokens(cs_tokens, f"CS: \"{cs_text}\"")

    ratio = len(cs_tokens) / len(en_tokens) if en_tokens else 0
    print(f"\n  Poměr CS/EN tokenů: {ratio:.1f}x")
    print("  -> Flektivní jazyky (čeština) typicky potřebují VÍCE tokenů")
    print("    než analytické jazyky (angličtina).")

    # -- Příklad 2: Odborná terminologie -------------------------------------
    print("\n" + "=" * 70)
    print("  PŘÍKLAD 2: Odborné termíny (RECETOX kontext)")
    print("=" * 70)

    terms = [
        ("polychlorinated biphenyls", VOCAB_EN, "EN"),
        ("polychlorované bifenyly", VOCAB_CS, "CS"),
        ("persistent organic pollutants", VOCAB_EN, "EN"),
        ("perzistentní organické polutanty", VOCAB_CS, "CS"),
    ]

    for text, vocab, lang in terms:
        tokens = simple_tokenize(text, vocab)
        visualize_tokens(tokens, f"{lang}: \"{text}\"")

    # -- Příklad 3: Proč na tokenizaci záleží --------------------------------
    print("\n" + "=" * 70)
    print("  PROČ NA TOKENIZACI ZÁLEŽÍ?")
    print("=" * 70)
    print("""
  1. CENA — Platíte za tokeny, ne za slova.
     Stejný text v češtině stojí víc než v angličtině.

  2. KONTEXT — Kontextové okno modelu má limit (např. 200k tokenů).
     Český text zabere v kontextu více místa.

  3. KVALITA — Model lépe rozumí tokenům, které viděl častěji.
     Anglické tokeny měl v trénovacích datech mnohem víc.

  4. ARITMETIKA — "Kolik písmen má slovo jahoda?"
     Model nevidí písmena, vidí tokeny. Proto počítání selhává.
    """)

    # -- Příklad 4: Počítání písmen -------------------------------------------
    print("=" * 70)
    print("  PŘÍKLAD 4: Proč AI špatně počítá písmena")
    print("=" * 70)

    word = "strawberry"
    tokens = simple_tokenize(word, VOCAB_EN)
    visualize_tokens(tokens, f"Slovo: \"{word}\"")
    print(f"  Model vidí {len(tokens)} tokenů, ne {len(word)} písmen!")
    print("  Proto často špatně odpoví na 'Kolik r je ve slově strawberry?'")


if __name__ == "__main__":
    main()
