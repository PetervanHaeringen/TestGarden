# Module 4 — Het Git Spel

Git begrijp je pas écht als je het hebt *gevoeld*.
In dit spel wordt de groep zelf een versiebeheersysteem.
Geen terminal. Geen commando's. Wel een echte ervaring van wat er in Git gebeurt.

---

## Materiaal

- Post-its of kaartjes (minimaal 30 stuks)
- Stiften (minimaal 2 kleuren)
- Een tafel of muur als "tijdlijn"
- 1 rol plakband of maskingtape voor de lijnen
- Deelnemers: 3 tot 8 personen

---

## Rollen

| Rol | Taak |
|-----|------|
| **Maintainer** | Beheert de `main`-branch. Keurt merges goed. |
| **Developer A** | Werkt op een eigen branch. |
| **Developer B** | Werkt op een andere branch (tegelijk met A). |
| **Reviewer** | Bekijkt branches voordat ze worden gemerged. |

Bij kleine groepen kan één persoon meerdere rollen hebben.

---

## Het "project"

Het project is een fictief tekstbestand: `README.txt`
De beginversie heeft drie regels:

```
Projectnaam: Git Garden
Versie: 1.0
Beschrijving: Een oefenproject.
```

Schrijf deze beginversie op een post-it. Dit is **commit A** — de oorsprong.
Plak hem links op de tijdlijn.

---

## Ronde 1 — Rechte tijdlijn

**Doel:** ervaren hoe commits achter elkaar komen.

1. Developer A schrijft een kleine wijziging op een nieuwe post-it.
   Voorbeeld: `Versie: 1.1`
   Schrijf bovenaan: `Commit B — Developer A — "versie bijgewerkt"`
2. Plak commit B rechts van A, verbonden met een pijl.
3. Developer A maakt nog een wijziging → commit C.
4. Developer B doet hetzelfde → commit D, E.

Na vijf commits heb je een tijdlijn. Bespreek:
- Wie heeft wat veranderd?
- Kun je teruggaan naar commit B?

---

## Ronde 2 — Branchen

**Doel:** ervaren dat twee mensen tegelijk aan hetzelfde project kunnen werken.

1. Trek met plakband twee lijnen vanuit commit C — één omhoog, één recht door.
2. Developer A werkt verder op de bovenste lijn: commit D (zijn versie van het bestand).
3. Developer B werkt op de onderste lijn: commit D' (zijn versie — andere wijzigingen).
4. Beide schrijven hun post-its, plakken ze op hun eigen lijn.

Nu hebben jullie twee branches. Bespreek:
- Wat staat er op de A-lijn? Wat op de B-lijn?
- Zijn ze allebei geldig? Ja. Git houdt ze allebei bij.

---

## Ronde 3 — Mergen

**Doel:** ervaren wat een merge is — en wanneer het mis kan gaan.

**Scenario A: geen conflict**
Developer A heeft de beschrijving veranderd.
Developer B heeft de versie veranderd.
→ Geen conflict. De Reviewer combineert beide wijzigingen op een nieuwe post-it: **merge-commit M**.
Plak M rechts van de twee lijnen, met twee pijlen ernaartoe.

**Scenario B: conflict**
Developer A schrijft: `Versie: 2.0`
Developer B schrijft ook: `Versie: 1.5`
→ Conflict! Dezelfde regel, twee verschillende waarden.
De Reviewer stopt. Bespreek: wie heeft gelijk? Wat kiezen jullie?
Schrijf de beslissing op de merge-commit.

Dit is precies wat Git doet: automatisch samenvoegen als het kan, en stoppen als het niet kan.

---

## Ronde 4 — Terug in de tijd

**Doel:** begrijpen dat Git nooit iets vergeet.

1. Kijk naar de tijdlijn.
2. Maintainer vraagt: "Hoe zag het bestand eruit bij commit B?"
3. Iedereen kijkt naar de post-it van commit B — en kan het antwoord geven.

Git doet precies dit: elke commit bevat de volledige staat van het project.
Je kunt altijd terug.

---

## Nabespreking

Bespreek met de groep:

1. Wat was het moeilijkste moment in het spel?
2. Wanneer ontstond het conflict — en hoe loste jullie het op?
3. Wat had een betere commit-message kunnen zijn?
4. Hoe verhoudt dit zich tot jullie dagelijkse werk met bestanden?

---

## Verbinding met de echte terminal

Na dit spel ken je de begrippen van binnenuit:

| Wat je deed in het spel | Git-commando |
|--------------------------|--------------|
| Post-it schrijven (wijziging vastleggen) | `git commit -m "..."` |
| Nieuwe lijn trekken (branch maken) | `git branch naam` |
| Wisselen naar een andere lijn | `git switch naam` |
| Twee lijnen samenvoegen | `git merge naam` |
| Terugkijken naar een eerdere post-it | `git log` / `git checkout` |

In de volgende module ga je precies dit doen — maar dan in de terminal.
