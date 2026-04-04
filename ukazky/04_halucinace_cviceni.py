#!/usr/bin/env python3
"""
=============================================================================
  HALUCINACE — Rozpoznej, co AI vymyslela
=============================================================================
  Interaktivní kvíz: ukáže vám texty, které vypadají jako AI výstup.
  Vaším úkolem je rozhodnout, zda je tvrzení pravdivé nebo halucinované.

  Spuštění: python 04_halucinace_cviceni.py
=============================================================================
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import random


QUESTIONS = [
    {
        "text": (
            "Stockholmská úmluva o perzistentních organických polutantech "
            "byla přijata v roce 2001 a vstoupila v platnost v roce 2004. "
            "Jejím cílem je eliminace nebo omezení výroby a použití POPs."
        ),
        "is_hallucination": False,
        "explanation": (
            "PRAVDA. Stockholmská úmluva byla skutečně přijata 22. května 2001 "
            "a vstoupila v platnost 17. května 2004. Toto je ověřitelný fakt."
        ),
        "indicators": [],
    },
    {
        "text": (
            "Podle studie Andersona et al. (2019) publikované v Environmental "
            "Science & Technology bylo zjištěno, že koncentrace PFAS v pitné "
            "vodě v České republice překračují limit EU 0.1 µg/L "
            "ve 43.7 % zkoumaných vzorků."
        ),
        "is_hallucination": True,
        "explanation": (
            "HALUCINACE. Několik varovných signálů:\n"
            "    • Příliš specifické číslo (43.7 %) bez ověřitelného zdroje.\n"
            "    • 'Anderson et al.' — generický anglický příjmení pro studii o ČR.\n"
            "    • Kombinace přesných detailů naznačuje, že AI 'vyplňuje mezery'\n"
            "      statisticky pravděpodobnými hodnotami."
        ),
        "indicators": [
            "Příliš specifická čísla",
            "Generické jméno autora",
            "Studii nelze dohledat",
        ],
    },
    {
        "text": (
            "DDT (dichlordifenyltrichlorethan) byl poprvé syntetizován "
            "v roce 1874 Othmanem Zeidlerem. Jeho insekticidní vlastnosti "
            "objevil Paul Hermann Müller v roce 1939, za což získal "
            "Nobelovu cenu za fyziologii a lékařství v roce 1948."
        ),
        "is_hallucination": False,
        "explanation": (
            "PRAVDA. Všechna fakta jsou ověřitelná:\n"
            "    • Syntéza 1874 — Othmar Zeidler.\n"
            "    • Insekticidní vlastnosti 1939 — Paul H. Müller.\n"
            "    • Nobelova cena 1948 — správně."
        ),
        "indicators": [],
    },
    {
        "text": (
            "European Chemicals Agency (ECHA) ve své zprávě z roku 2023 "
            "identifikovala celkem 2,847 látek klasifikovaných jako endokrinní "
            "disruptory kategorie 1A podle nařízení REACH. Zpráva je dostupná "
            "pod referenčním číslem ECHA/RPT/2023/ED-1847."
        ),
        "is_hallucination": True,
        "explanation": (
            "HALUCINACE. Varovné signály:\n"
            "    • Referenční číslo ECHA/RPT/2023/ED-1847 — AI vymýšlí kódy.\n"
            "    • Přesný počet 2,847 — příliš specifické, nedohledatelné.\n"
            "    • 'Kategorie 1A' endokrinních disruptorů — taková klasifikace\n"
            "      v REACH neexistuje v této formě.\n"
            "    • Typický vzorec: AI generuje autoritativně znějící detaily."
        ),
        "indicators": [
            "Vymyšlené referenční číslo",
            "Neexistující klasifikační kategorie",
            "Příliš přesná čísla",
        ],
    },
    {
        "text": (
            "Benzo[a]pyren je polycyklický aromatický uhlovodík (PAH) "
            "klasifikovaný jako karcinogen skupiny 1 podle IARC. Je běžným "
            "produktem neúplného spalování organických materiálů a nachází "
            "se v cigaretovém kouři, grilovaném mase a výfukových plynech."
        ),
        "is_hallucination": False,
        "explanation": (
            "PRAVDA. Benzo[a]pyren je skutečně:\n"
            "    • PAH — správně.\n"
            "    • IARC skupina 1 (karcinogenní pro člověka) — správně.\n"
            "    • Vzniká neúplným spalováním — správně.\n"
            "    • Zdroje (kouř, maso, výfuky) — správně."
        ),
        "indicators": [],
    },
    {
        "text": (
            "Metoda QuEChERS (Quick, Easy, Cheap, Effective, Rugged, Safe) "
            "byla vyvinuta Robertem J. Blackwoodem na MIT v roce 1998 "
            "a je dnes zlatým standardem pro extrakci pesticidů "
            "z potravinových matric."
        ),
        "is_hallucination": True,
        "explanation": (
            "ČÁSTEČNÁ HALUCINACE:\n"
            "    • QuEChERS je skutečná metoda a skutečně je standardem — PRAVDA.\n"
            "    • Rozvinutí zkratky je správné — PRAVDA.\n"
            "    • Ale vyvinuli ji Anastassiades, Lehotay a kol. v roce 2003,\n"
            "      ne Blackwood na MIT v 1998 — HALUCINACE.\n"
            "    • Typický vzorec: AI smíchá pravdivé a vymyšlené informace."
        ),
        "indicators": [
            "Vymyšlený autor",
            "Špatná instituce",
            "Nesprávný rok",
            "Mixuje fakta s fikcí",
        ],
    },
    {
        "text": (
            "Glyfosfát je nejpoužívanější herbicid na světě. V březnu 2015 "
            "jej IARC klasifikovala jako 'pravděpodobně karcinogenní pro "
            "člověka' (skupina 2A). Tato klasifikace vyvolala celosvětovou "
            "debatu o jeho bezpečnosti."
        ),
        "is_hallucination": False,
        "explanation": (
            "PRAVDA. Všechna fakta jsou správná a ověřitelná:\n"
            "    • Nejpoužívanější herbicid — správně.\n"
            "    • IARC klasifikace 2A (březen 2015) — správně.\n"
            "    • Celosvětová debata — správně."
        ),
        "indicators": [],
    },
    {
        "text": (
            "Podle meta-analýzy Wanga a Zhanga (2022) v Nature Reviews "
            "Environmental Science bylo prokázáno, že mikro-plasty v pitné "
            "vodě způsobují 23% nárůst rizika kolorektálního karcinomu "
            "při expozici nad 150 částic/L po dobu 10 let."
        ),
        "is_hallucination": True,
        "explanation": (
            "HALUCINACE. Varovné signály:\n"
            "    • Příliš specifické kvantitativní závěry (23 %, 150 částic/L).\n"
            "    • Generická čínská příjmení (Wang, Zhang) — nejčastější v AI citacích.\n"
            "    • Kauzální tvrzení ('způsobují') — výzkum mikroplastů je stále v rané fázi.\n"
            "    • Takto silný závěr by byl světovou zprávou."
        ),
        "indicators": [
            "Příliš specifická čísla",
            "Generická jména autorů",
            "Kauzální tvrzení bez podkladu",
            "Nedohledatelný zdroj",
        ],
    },
]


def main():
    print(__doc__)

    questions = QUESTIONS.copy()
    random.shuffle(questions)

    score = 0
    total = len(questions)

    print("=" * 70)
    print("  KVÍZ: Rozpoznej halucinaci!")
    print("  U každého textu rozhodněte: je to PRAVDA (p) nebo HALUCINACE (h)?")
    print("=" * 70)

    for i, q in enumerate(questions, 1):
        print(f"\n{'-' * 70}")
        print(f"  OTÁZKA {i}/{total}")
        print(f"{'-' * 70}")
        print()

        # Zobraz text zalamovaný na ~70 znaků
        words = q["text"].split()
        line = "  "
        for word in words:
            if len(line) + len(word) + 1 > 68:
                print(line)
                line = "  " + word
            else:
                line += " " + word if line.strip() else "  " + word
        if line.strip():
            print(line)

        print()

        # Uživatelský vstup
        while True:
            answer = input("  Vaše odpověď [p = pravda / h = halucinace / q = konec]: ").strip().lower()
            if answer in ("p", "h", "q"):
                break
            print("  Zadejte 'p', 'h', nebo 'q'.")

        if answer == "q":
            print("\n  Kvíz ukončen předčasně.")
            total = i - 1
            break

        is_correct = (answer == "h") == q["is_hallucination"]

        if is_correct:
            score += 1
            print(f"\n  \033[92m[OK] SPRÁVNĚ!\033[0m")
        else:
            print(f"\n  \033[91m[X] ŠPATNĚ!\033[0m")

        print(f"\n  {q['explanation']}")

        if q["indicators"]:
            print("\n  \033[93mVarovné signály:\033[0m")
            for ind in q["indicators"]:
                print(f"    [!] {ind}")

    # -- Vysledky --------------------------------------------------------------
    if total > 0:
        pct = score / total * 100
        print(f"\n{'=' * 70}")
        print(f"  VÝSLEDEK: {score}/{total} ({pct:.0f} %)")
        print(f"{'=' * 70}")

        if pct >= 80:
            print("  Výborně! Máte dobrý čich na halucinace.")
        elif pct >= 50:
            print("  Solidní základ, ale pozor — AI umí být velmi přesvědčivá.")
        else:
            print("  Nevadí — právě proto je kritické myšlení tak důležité!")

    print(f"""
{'=' * 70}
  CHECKLIST PRO ROZPOZNÁNÍ HALUCINACÍ
{'=' * 70}

  SMELL TEST    — Zní to rozumně, nebo jako generická fráze?
  NUMBER CHECK  — Jsou čísla realistická? Nejsou příliš specifická?
  SOURCE HUNT   — Existují uvedené zdroje? Lze je dohledat?
  LOGIC SCAN    — Následují argumenty logicky?
  EXPERT GUT    — Co by řekl kolega z oboru?
  CHALLENGE     — Zeptejte se AI: "Jsi si jistá? Uveď zdroj."

  TYPICKÉ VZORCE HALUCINACÍ:
  • Vymyšlené citace s realisticky znějícími autory a čísly
  • Mix pravdivých a nepravdivých informací v jedné odpovědi
  • Příliš specifická čísla bez ověřitelného zdroje
  • Neexistující referenční kódy, ISBN, DOI
  • Kauzální tvrzení kde existuje jen korelace
    """)


if __name__ == "__main__":
    main()
