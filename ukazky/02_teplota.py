#!/usr/bin/env python3
"""
=============================================================================
  TEPLOTA (Temperature) — Jak AI volí další slovo
=============================================================================
  Teplota je parametr, který ovlivňuje, jak "kreativní" nebo "deterministická"
  je odpověď AI. Tento skript simuluje, jak softmax funkce s různými
  teplotami mění pravděpodobnostní distribuci dalšího tokenu.

  Spuštění: python 02_teplota.py
=============================================================================
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import math
import random


def softmax(logits: list[float], temperature: float) -> list[float]:
    """Softmax funkce s teplotou. Nižší teplota = ostřejší distribuce."""
    if temperature <= 0:
        temperature = 0.001  # ochrana proti dělení nulou

    scaled = [x / temperature for x in logits]
    max_val = max(scaled)
    exps = [math.exp(x - max_val) for x in scaled]  # numerická stabilita
    total = sum(exps)
    return [e / total for e in exps]


def sample_token(tokens: list[str], probs: list[float]) -> str:
    """Vzorkuje token na základě pravděpodobností."""
    r = random.random()
    cumulative = 0.0
    for token, prob in zip(tokens, probs):
        cumulative += prob
        if r <= cumulative:
            return token
    return tokens[-1]


def bar_chart(value: float, max_width: int = 40) -> str:
    """Vytvoří textový sloupcový graf."""
    filled = int(value * max_width)
    return "█" * filled + "░" * (max_width - filled)


def main():
    print(__doc__)

    # -- Scenar: Model prave vygeneroval "Kontaminace pudy byla" -----------
    # a nyní volí další slovo. Logity jsou "surové skóre" z modelu.

    context = "Kontaminace půdy byla"
    candidates = [
        ("zjištěna",    3.2),   # nejvyšší skóre
        ("potvrzena",   2.8),
        ("analyzována", 2.1),
        ("zkoumána",    1.5),
        ("ignorována",  0.3),
        ("oslavována", -1.0),   # nesmyslné, ale nenulové skóre
    ]

    tokens = [c[0] for c in candidates]
    logits = [c[1] for c in candidates]

    temperatures = [0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]

    print("=" * 70)
    print(f"  Kontext: \"{context} ___\"")
    print(f"  Model zvažuje {len(tokens)} kandidátů na další slovo.")
    print("=" * 70)

    # -- Surove logity -----------------------------------------------------
    print("\n  SUROVÉ LOGITY (skóre z modelu):")
    for token, logit in candidates:
        print(f"    {token:15s}  logit = {logit:+.1f}")

    # -- Vliv teploty ------------------------------------------------------
    for temp in temperatures:
        probs = softmax(logits, temp)
        top_idx = probs.index(max(probs))

        if temp <= 0.3:
            label = "DETERMINISTICKÁ"
            color = "\033[94m"  # modrá
        elif temp <= 0.7:
            label = "VYVÁŽENÁ"
            color = "\033[93m"  # žlutá
        else:
            label = "KREATIVNÍ"
            color = "\033[91m"  # červená
        reset = "\033[0m"

        print(f"\n  {color}{'-' * 60}")
        print(f"  Teplota = {temp:.1f}  ({label})")
        print(f"  {'-' * 60}{reset}")

        for i, (token, prob) in enumerate(zip(tokens, probs)):
            marker = " <-" if i == top_idx else ""
            bar = bar_chart(prob)
            print(f"    {token:15s} {prob:6.1%}  {bar}{marker}")

    # -- Simulace generovani -----------------------------------------------
    print("\n" + "=" * 70)
    print("  SIMULACE: 10x generování při různých teplotách")
    print("=" * 70)

    for temp in [0.1, 0.7, 1.5]:
        probs = softmax(logits, temp)
        samples = [sample_token(tokens, probs) for _ in range(10)]

        if temp <= 0.3:
            color = "\033[94m"
        elif temp <= 0.7:
            color = "\033[93m"
        else:
            color = "\033[91m"
        reset = "\033[0m"

        print(f"\n  {color}Teplota {temp:.1f}:{reset}")
        for i, s in enumerate(samples, 1):
            print(f"    {i:2d}. {context} {color}{s}{reset}")

        unique = len(set(samples))
        print(f"    -> Unikátních odpovědí: {unique}/10")

    # -- Shrnuti ------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  CO Z TOHO PLYNE?")
    print("=" * 70)
    print("""
  Nízká teplota (0.1-0.3):
    -> Model téměř vždy vybere nejpravděpodobnější token.
    -> Vhodné pro: faktické odpovědi, překlady, sumarizace.

  Střední teplota (0.5-0.7):
    -> Vyváženost mezi přesností a variabilitou.
    -> Vhodné pro: většinu běžných úloh.

  Vysoká teplota (1.0+):
    -> Model častěji vybírá méně pravděpodobné tokeny.
    -> Vhodné pro: kreativní psaní, brainstorming.

  DŮLEŽITÉ: Uživatel většinou teplotu přímo nastavit nemůže.
  Ale může její efekt napodobit formulací promptu:
    "Buď přesný a konzistentní" ≈ nižší teplota
    "Buď kreativní, překvap mě" ≈ vyšší teplota
    """)


if __name__ == "__main__":
    main()
