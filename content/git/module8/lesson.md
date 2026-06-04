# Module 8 — Git voor testers

Als tester gebruik je Git misschien anders dan een developer.
Jij werkt met testscripts, bugrapporten, bevindingen en documentatie.
In deze module zie je hoe Git en GitHub je werk als tester direct ondersteunen.

---

## 1. GitHub Issues: het hart van het werkproces

Een **issue** is een taak, bugmelding of vraag die in GitHub wordt bijgehouden.

Als tester maak je issues aan voor:
- gevonden bugs
- testvragen aan het team
- verzoeken om extra testdata
- verbetervoorstellen voor testscripts

**Een goed bugrapport als issue bevat:**

```markdown
## Omschrijving
Klikken op de "Opslaan"-knop in het formulier geeft een 500-fout.

## Stappen om te reproduceren
1. Ga naar /formulier
2. Vul alle velden in
3. Klik op "Opslaan"

## Verwacht gedrag
Het formulier wordt opgeslagen en je krijgt een bevestiging.

## Werkelijk gedrag
Foutmelding: Internal Server Error (500)

## Omgeving
- Browser: Chrome 124
- OS: Windows 11
- Testomgeving: staging
```

---

## 2. Labels: structuur aanbrengen

Labels categoriseren issues.
Standaard labels in GitHub:

| Label | Gebruik |
|-------|---------|
| `bug` | Iets werkt niet zoals verwacht |
| `enhancement` | Verbetervoorstel |
| `question` | Vraag aan het team |
| `documentation` | Documentatie mist of klopt niet |
| `duplicate` | Al eerder gemeld |
| `won't fix` | Bewuste keuze om niet op te lossen |

Je kunt ook eigen labels aanmaken:
- `prioriteit: hoog`
- `test: regressie`
- `omgeving: staging`

---

## 3. Milestones: koppelen aan een versie of sprint

Een **milestone** groepeert issues die bij een versie of sprint horen.

Voorbeeld:
- Milestone `Sprint 4 — Release 2.1`
- Issues: 12 bugs, 3 testverzoeken
- Voortgang: 7 van 15 gesloten

Als tester geeft een milestone je overzicht: wat moet er klaar zijn voor de release?

---

## 4. Testscripts in Git beheren

Testscripts zijn gewone bestanden (YAML, txt, Python, etc.).
Omdat ze in een Git-repository staan, heb je:

- **Geschiedenis**: wie heeft dit testscript wanneer aangepast?
- **Terugkeer**: een fout in een testscript? Terug naar de vorige versie.
- **Samenwerking**: collega kan testscripts reviewen via een pull request.
- **Traceerbaarheid**: je kunt een testscript koppelen aan een issue.

**Goede mapstructuur voor testscripts:**

```
testscripts/
  regressie/
    module1_login.yaml
    module2_formulieren.yaml
  smoke/
    dagelijkse_check.yaml
  exploratory/
    notities_sprint4.md
```

---

## 5. Een bugrapport koppelen aan een commit

In een commit-message kun je verwijzen naar een issue:

```bash
git commit -m "Fix login validatie (#42)"
```

GitHub herkent `#42` en maakt automatisch een koppeling naar issue 42.
Gebruik `Closes #42` om het issue automatisch te sluiten bij de merge:

```bash
git commit -m "Fix: kapotte opslaan-knop in formulier (Closes #58)"
```

---

## 6. De testworkflow in Git

Een typische cyclus voor een tester:

```
1. Testscript schrijven of aanpassen
       ↓
2. Branch aanmaken: test/sprint4-regressie
       ↓
3. Commits: kleine aanpassingen met duidelijke berichten
       ↓
4. Pull request → review door collega
       ↓
5. Bug gevonden? → Issue aanmaken met reproductiestappen
       ↓
6. Bug opgelost door developer → jij test opnieuw op de PR-branch
       ↓
7. PR gemerged → milestone bijgewerkt
```

Git is geen extra administratie.
Het is de plek waar jouw werk zichtbaar en traceerbaar wordt.
