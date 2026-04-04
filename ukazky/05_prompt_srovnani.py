#!/usr/bin/env python3
"""
=============================================================================
  PROMPTING — Srovnání technik a šablony pro výzkum
=============================================================================
  Tento skript ukazuje různé promptovací techniky z přednášky na
  konkrétních příkladech relevantních pro RECETOX. Vygenerované prompty
  si můžete zkopírovat a vyzkoušet v ChatGPT, Claude nebo Gemini.

  Spuštění: python 05_prompt_srovnani.py
=============================================================================
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


TECHNIQUES = [
    {
        "name": "ZERO-SHOT",
        "description": "Model řeší úlohu bez příkladů, pouze na základě instrukce.",
        "when": "Jednoduché, jasně definované úlohy.",
        "bad_prompt": "Řekni mi něco o PFAS.",
        "good_prompt": (
            "Vysvětli, co jsou PFAS (per- a polyfluoralkylové látky), "
            "jaké jsou jejich hlavní zdroje v životním prostředí a proč "
            "se jim říká 'forever chemicals'. Odpověz ve 3 odstavcích."
        ),
        "why_better": (
            "Specifický dotaz, jasný rozsah (3 odstavce), konkrétní aspekty "
            "(zdroje, přezdívka). Model nemusí hádat, co chcete."
        ),
    },
    {
        "name": "CHAIN OF THOUGHT (Řetězec myšlení)",
        "description": "Model ukazuje mezikroky svého uvažování.",
        "when": "Složité výpočty, logické odvozování, interpretace dat.",
        "bad_prompt": "Vyhodnoť toxicitu tohoto vzorku.",
        "good_prompt": (
            "Mám vzorek vody s těmito koncentracemi:\n"
            "  - Olovo: 15 µg/L\n"
            "  - Kadmium: 3.5 µg/L\n"
            "  - Arsen: 8 µg/L\n\n"
            "Porovnej každou hodnotu s limitem pro pitnou vodu podle "
            "směrnice EU 2020/2184. U každé látky uveď:\n"
            "  1. Naměřenou hodnotu\n"
            "  2. Limit EU\n"
            "  3. Poměr naměřená/limit\n"
            "  4. Hodnocení (vyhovuje / překračuje)\n\n"
            "Na závěr shrň celkové hodnocení vzorku."
        ),
        "why_better": (
            "Explicitní mezikroky (1-4) nutí model ukázat postup. "
            "Konkrétní data umožňují ověření. Odkaz na legislativu zajistí "
            "použití správných limitů."
        ),
    },
    {
        "name": "TREE OF THOUGHT (Strom myšlení)",
        "description": "Model prozkoumá více přístupů paralelně a porovná je.",
        "when": "Rozhodování, kde existuje více dobrých řešení.",
        "bad_prompt": "Jak analyzovat pesticidy ve vzorcích?",
        "good_prompt": (
            "Potřebuji analyzovat reziduá pesticidů v ovoci.\n"
            "Prozkoumej 3 analytické přístupy:\n\n"
            "  Přístup A: QuEChERS + GC-MS/MS\n"
            "  Přístup B: QuEChERS + LC-MS/MS\n"
            "  Přístup C: SFE (superkritická fluidní extrakce) + GC-MS\n\n"
            "Pro každý uveď:\n"
            "  - Vhodnost pro danou matrici\n"
            "  - Počet detekovatelných pesticidů\n"
            "  - Časová a finanční náročnost\n"
            "  - Skóre vhodnosti (1-10)\n\n"
            "Doporuč nejlepší přístup a zdůvodni."
        ),
        "why_better": (
            "Paralelní porovnání nutí model zvážit trade-offs. "
            "Strukturovaná kritéria umožňují objektivní srovnání."
        ),
    },
    {
        "name": "DECOMPOSITION (Dekompozice)",
        "description": "Složitý úkol rozložíte na kroky, každý potvrdíte zvlášť.",
        "when": "Komplexní úlohy (rešerše, analýzy, návrhy experimentů).",
        "bad_prompt": "Napiš mi literární rešerši o mikroplastech v půdě.",
        "good_prompt": (
            "Pomohu ti připravit literární rešerši o mikroplastech v půdě.\n"
            "Budeme postupovat po krocích. Začni krokem 1.\n\n"
            "  Krok 1: Identifikuj 5 klíčových aspektů tématu.\n"
            "  Krok 2: Pro každý aspekt navrhni vyhledávací strategii.\n"
            "  Krok 3: Shrň současný stav poznání.\n"
            "  Krok 4: Identifikuj mezery ve výzkumu.\n"
            "  Krok 5: Navrhni strukturu rešerše.\n\n"
            "Začni krokem 1. Další kroky provedeme po schválení."
        ),
        "why_better": (
            "Kontrola po každém kroku. Můžete korigovat směr dřív, "
            "než AI vytvoří celý text na špatných základech."
        ),
    },
    {
        "name": "SELF-CRITICISM (Sebekritika)",
        "description": "Model vytvoří odpověď, pak ji sám zkritizuje a vylepší.",
        "when": "Když potřebujete vysokou kvalitu textu.",
        "bad_prompt": "Napiš abstrakt pro můj článek.",
        "good_prompt": (
            "Napiš abstrakt (max 250 slov) pro vědecký článek:\n"
            "  Téma: Vliv mikroplastů na sorpci těžkých kovů v půdě\n"
            "  Metodika: Batch sorpční experimenty, SEM-EDS analýza\n"
            "  Klíčový výsledek: PE a PP zvyšují mobilitu Cd o 15-30 %\n"
            "  Časopis: Environmental Pollution (styl IMRAD)\n\n"
            "Poté:\n"
            "  1. Zkritizuj svůj abstrakt — co chybí, co je slabé?\n"
            "  2. Přepiš abstrakt na základě kritiky.\n"
            "  3. Porovnej verzi 1 a verzi 2."
        ),
        "why_better": (
            "Iterativní vylepšování. Model sám najde slabiny. "
            "Srovnání verzí ukáže, co se zlepšilo."
        ),
    },
    {
        "name": "PROMPT FRAMEWORK (P-R-O-M-P-T)",
        "description": "Strukturovaný přístup: Purpose, Role, Objective, Method, Parameters, Tone.",
        "when": "Vždy, když chcete maximální kvalitu odpovědi.",
        "bad_prompt": "Pomoz mi s výzkumem.",
        "good_prompt": (
            "PURPOSE: Potřebuji identifikovat vhodnou analytickou metodu "
            "pro stanovení nových kontaminantů (emerging pollutants) "
            "ve vzorcích odpadních vod.\n\n"
            "ROLE: Jsi zkušený analytický chemik se specializací na "
            "environmentální analýzu a LC-MS techniky.\n\n"
            "OBJECTIVE: Vytvoř srovnávací tabulku 4 metod s hodnocením "
            "LOD, LOQ, opakovatelnosti a matričních efektů.\n\n"
            "METHOD: Postupuj systematicky — nejdřív definuj kritéria, "
            "pak porovnej metody, nakonec doporuč.\n\n"
            "PARAMETERS: Tabulka, max 1 strana, zaměření na léčiva "
            "a osobní hygienu (PPCPs), roky 2020-2026.\n\n"
            "TONE: Odborný, stručný, vhodný pro interní laboratorní zprávu."
        ),
        "why_better": (
            "Kompletní kontext: model přesně ví CO, JAK, PRO KOHO a V JAKÉM "
            "FORMÁTU odpovědět. Minimální prostor pro halucinace."
        ),
    },
]

CUSTOM_INSTRUCTIONS_EXAMPLE = """
  +======================================================================+
  |  PŘÍKLAD CUSTOM INSTRUCTIONS PRO VÝZKUMNÍKA NA RECETOX             |
  +======================================================================+
  |                                                                    |
  |  Jsem výzkumník v oblasti environmentální chemie na RECETOX,       |
  |  Masarykova univerzita. Pracuji s perzistentními organickými       |
  |  polutanty (POPs) a emerging contaminants.                         |
  |                                                                    |
  |  Pravidla:                                                         |
  |  - Když cituješ zdroj, uveď DOI. Pokud si nejsi jistý, řekni.    |
  |  - Nebuď servilní (sycophant). Neříkej "skvělá otázka".           |
  |  - Když tvrdím něco chybného, oprav mě.                           |
  |  - U číselných dat vždy uveď jednotky a nejistotu.                |
  |  - Preferuj peer-reviewed zdroje.                                  |
  |  - Při práci s kódem: jsem začátečník v Pythonu.                  |
  |                                                                    |
  |  Tagy:                                                             |
  |  <academic> -- priorita: přesnost, citace, APA formát              |
  |  <critic>   -- buď kritický a zpochybňuj                           |
  |  <source>   -- ke každému tvrzení uveď zdroj                       |
  |  <explain>  -- vysvětli jednoduše jako nejlepší učitel              |
  |                                                                    |
  +======================================================================+"""


def main():
    print(__doc__)

    print("=" * 70)
    print("  PROMPTOVACÍ TECHNIKY — PŘEHLED A PŘÍKLADY PRO RECETOX")
    print("=" * 70)

    for i, tech in enumerate(TECHNIQUES, 1):
        print(f"\n{'=' * 70}")
        print(f"  {i}. {tech['name']}")
        print(f"{'=' * 70}")
        print(f"\n  \033[90m{tech['description']}\033[0m")
        print(f"  Kdy použít: {tech['when']}")

        print(f"\n  \033[91m[X] SLABÝ PROMPT:\033[0m")
        print(f"    \"{tech['bad_prompt']}\"")

        print(f"\n  \033[92m[OK] SILNÝ PROMPT:\033[0m")
        for line in tech["good_prompt"].split("\n"):
            print(f"    {line}")

        print(f"\n  \033[93mProč je lepší:\033[0m {tech['why_better']}")

    # -- Custom instructions ---------------------------------------------------
    print(f"\n{'=' * 70}")
    print(f"  BONUS: CUSTOM INSTRUCTIONS")
    print(f"{'=' * 70}")
    print(CUSTOM_INSTRUCTIONS_EXAMPLE)

    # -- Shrnuti ---------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print(f"  PRAKTICKÉ TIPY")
    print(f"{'=' * 70}")
    print("""
  1. ZAČNĚTE JEDNODUŠE — zero-shot stačí na 80 % úloh.
     Složitější techniky použijte, až když výstup nestačí.

  2. ITERUJTE — Neočekávejte perfektní odpověď napoprvé.
     Konverzace s AI je dialog, ne jednorázový dotaz.

  3. OVĚŘUJTE — Žádná promptovací technika neodstraní halucinace.
     Vždy kontrolujte fakta, citace a čísla.

  4. UKLÁDEJTE — Prompty, které fungují, si uložte.
     AI nemá trvalou paměť, ale vy ano.

  5. EXPERIMENTUJTE — Stejný prompt vyzkoušejte v ChatGPT, Claude
     i Gemini. Různé modely = různé výsledky.

  6. KONTEXT JE KRÁL — Čím víc relevantního kontextu poskytnete,
     tím lepší odpověď dostanete. Nahrajte soubory, dejte příklady.
    """)


if __name__ == "__main__":
    main()
