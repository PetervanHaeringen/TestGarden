# Module 7 — Conflicten & kwaliteit

Samenwerken gaat niet altijd vanzelf.
Soms wil je iets samenvoegen en zegt Git: "dit lukt me niet alleen."
Dat is geen fout — dat is een vraag aan jou.

---

## 1. Wat is een merge conflict?

Een merge conflict ontstaat als twee branches **dezelfde regel op een andere manier hebben gewijzigd**.

Git kan niet zelf beslissen welke versie de juiste is.
Het markeert de conflicterende regels en wacht op jou.

Voorbeeld: op `main` is de eerste regel van `README.md`:
```
Versie: 1.0
```

Op jouw branch heb jij er van gemaakt:
```
Versie: 2.0
```

En op de andere branch staat:
```
Versie: 1.5
```

Wie heeft gelijk? Git weet het niet. Jij wel.

---

## 2. Hoe ziet een conflict eruit?

Git opent het bestand en voegt markeringen in:

```
<<<<<<< HEAD
Versie: 2.0
=======
Versie: 1.5
>>>>>>> andere-branch
```

- Alles tussen `<<<<<<< HEAD` en `=======` is jouw versie
- Alles tussen `=======` en `>>>>>>>` is de andere branch
- Jij kiest wat er blijft staan

---

## 3. Een conflict oplossen: stap voor stap

```bash
# Je probeert te mergen
git merge andere-branch

# Git meldt: CONFLICT (content) in README.md
# Open het bestand in je editor
```

**In de editor:**
1. Zoek de conflictmarkeringen (`<<<<<<<`, `=======`, `>>>>>>>`)
2. Besluit welke versie klopt — of combineer ze
3. Verwijder alle markeringen
4. Sla het bestand op

**Terug in de terminal:**
```bash
git add README.md
git commit -m "Conflict opgelost: versienummer naar 2.0"
```

Het conflict is opgelost. De merge-commit is gemaakt.

---

## 4. Conflicten voorkomen

De beste manier om conflicten te vermijden: **kleine, frequente commits en merges**.

Hoe langer je wacht met mergen, hoe groter de kans dat iemand anders dezelfde regels heeft aangepast.

Goede gewoonten:
- Houd branches kort — werk in dagen, niet weken
- Pull regelmatig: `git pull origin main` op je branch om bij te blijven
- Bespreek wie aan welk deel werkt

---

## 5. Code review: kwaliteit voor de merge

Een **code review** is het bekijken van andermans werk vóórdat het wordt gemerged.

Als reviewer let je op:
- Is de wijziging begrijpelijk?
- Heeft het onverwachte gevolgen?
- Zijn commit messages duidelijk?
- Zijn er typefouten of inconsistenties?

Als tester ben je uitstekend in reviewen — je denkt al in randgevallen en risico's.

**Goede review-etiquette:**
- Stel vragen in plaats van eisen te stellen: "Heb je nagedacht over...?" i.p.v. "Dit is fout."
- Benoem ook wat er goed is
- Laat je ego buiten de review — het gaat om het product

![Pull request review op GitHub](images/code_review.png)

---

## 6. Tags en releases

Een **tag** is een naam die je aan een specifieke commit geeft.
Handig voor versienummers: `v1.0`, `v2.3.1`.

```bash
# Maak een lichte tag
git tag v1.0

# Maak een annotated tag (met beschrijving)
git tag -a v1.0 -m "Eerste stabiele versie"

# Push de tag naar GitHub
git push origin v1.0
```

Op GitHub kun je een **release** maken van een tag.
Een release bevat:
- de code op dat moment
- release notes (wat is nieuw, wat is opgelost)
- eventueel bijlagen (installatiebestanden)

Voor een tester is een release het startpunt van een testronde.
