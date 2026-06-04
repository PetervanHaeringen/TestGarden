# Eindopdracht — Volledige Git-workflow

Je hebt de theorie, de visualisaties en de praktische stappen doorlopen.
Nu voer je alles samen uit: een complete professionele workflow op de oefenrepository.

---

## Wat je gaat doen

Je doorloopt de stappen die een tester dagelijks uitvoert in een echt team:

```
Issue aanmaken
      ↓
Branch aanmaken
      ↓
Testbestand schrijven + committen
      ↓
Push naar GitHub
      ↓
Pull request openen
      ↓
Review ontvangen en verwerken
      ↓
Merge (door docent of peer)
      ↓
Issue sluiten
```

---

## De opdracht

### Stap 1 — Issue aanmaken

Maak een issue aan in de repository `git-garden-playground`.

Het scenario: je hebt ontdekt dat de instructies in de map `handleidingen/` ontbreken voor het onderwerp dat jij hebt geleerd.

Schrijf een issue met:
- een duidelijke titel
- omschrijving van wat er ontbreekt
- label: `documentation`
- milestone: `Git Garden v1.0` (als die bestaat, anders laat je dit leeg)

Noteer het issue-nummer — dat heb je later nodig.

---

### Stap 2 — Branch aanmaken

```bash
git switch main
git pull
git switch -c docs/handleiding-[jouw-naam]
```

Gebruik een beschrijvende branchnaam die begint met `docs/`.

---

### Stap 3 — Bestand schrijven

Maak een bestand aan in de map `handleidingen/`:

**`handleidingen/[jouw-naam]-samenvatting.md`**

Schrijf daarin een korte samenvatting van wat jij hebt geleerd in dit Git-leerpad.
Minimaal:
- 3 dingen die je nu snapt die je eerst niet snapte
- 1 commando dat je het meest nuttig vindt
- 1 situatie uit je eigen werk waar je Git zou willen gebruiken

---

### Stap 4 — Committen

```bash
git add handleidingen/[jouw-naam]-samenvatting.md
git commit -m "Voeg Git-samenvatting toe voor [jouw naam] (Closes #[issue-nummer])"
```

---

### Stap 5 — Pushen

```bash
git push origin docs/handleiding-[jouw-naam]
```

---

### Stap 6 — Pull request openen

Ga naar GitHub en open een pull request.

**Vereisten voor de PR-beschrijving:**
- Wat heb je toegevoegd?
- Waarom is dit nuttig voor anderen?
- Verwijzing naar het issue: `Closes #[nummer]`
- Eén punt dat een reviewer specifiek moet controleren

---

### Stap 7 — Review verwerken

Je docent of een medestudent reviewt je PR.
Als er feedback is:
1. Pas het bestand aan op je lokale branch
2. Commit de aanpassing met een duidelijke boodschap
3. Push de wijziging — de PR wordt automatisch bijgewerkt

---

### Stap 8 — Merge

Na goedkeuring wordt de PR gemerged door de docent of door jou (als de rechten dat toestaan).

Controleer daarna:
```bash
git switch main
git pull
ls handleidingen/
```

Jouw bestand staat nu in `main`. Het is onderdeel van de officiële repository.

---

## Beoordelingscriteria

| Onderdeel | Goed |
|-----------|------|
| Issue | Duidelijke titel, omschrijving, correct label |
| Branchnaam | Beschrijvend, begint met `docs/` |
| Commit-message | Beschrijvend, verwijst naar issue-nummer |
| Bestand | Voldoet aan de vereisten, eigen tekst |
| PR-beschrijving | Compleet, bevat Closes #nummer |
| Verwerken feedback | Nieuwe commit met duidelijke boodschap |

---

## Klaar?

Als alles gemerged is, heb je aangetoond dat je:
- zelfstandig een volledige Git-workflow kunt uitvoeren
- professioneel kunt communiceren in issues en pull requests
- weet hoe je feedback verwerkt zonder de workflow te verstoren

Dat is geen trukje met vier commando's — dat is werken zoals een professional.
