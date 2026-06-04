# Module 2 — Onder de motorkap

Je weet nu *waarom* Git bestaat.
Deze module gaat een stap dieper: *hoe werkt het van binnen?*

Je hoeft geen programmeur te zijn om dit te begrijpen.
Maar als je het begrijpt, snap je nooit meer per ongeluk wat er misgaat.

---

## 1. De .git-folder: het geheugen van het project

Wanneer je `git init` uitvoert in een map, maakt Git één verborgen map aan: `.git`

Die map bevat alles wat Git weet over jouw project:
- alle commits
- alle branches
- alle instellingen
- de volledige geschiedenis

Als je de `.git`-folder verwijdert, is het een gewone map zonder geschiedenis.
De `.git`-folder *is* Git, voor dat project.

> **Probeer het (optioneel):** Open een terminal in een Git-repo en typ `ls -la`.
> Je ziet de `.git`-map. Typ daarna `ls .git` om de inhoud te zien.

---

## 2. Alles is een object

Git bewaart geen "bestanden" zoals een harde schijf.
Git bewaart **objecten**. Er zijn vier soorten:

| Type | Wat het is |
|------|-----------|
| **blob** | de inhoud van één bestand |
| **tree** | een map: welke blobs en trees zitten erin |
| **commit** | een momentopname: welke tree, wie, wanneer, bericht |
| **tag** | een naam die naar een commit wijst |

Elk object krijgt een unieke naam: een **hash**.

---

## 3. Wat is een hash?

Een hash is een code die Git berekent op basis van de *inhoud* van een object.

Voorbeeld: de tekst `Hello, Git!` geeft altijd dezelfde hash.
Verander één letter, en de hash verandert volledig.

```
echo "Hello, Git!" | git hash-object --stdin
# Geeft iets als: a8c9f4b2d3...
```

Git gebruikt hashes (SHA-1) om:
- objecten uniek te identificeren
- te detecteren of er iets is veranderd of beschadigd
- te verwijzen van de ene commit naar de andere

![Hash-principe: kleine wijziging, volledig andere hash](/instructions/content-images/git/module2//hash_principe.svg)

---

## 4. Snapshots, geen diffs

Veel mensen denken dat Git de *verschillen* tussen versies bewaart.
Dat klopt niet helemaal.

Git bewaart **snapshots** — volledige momentopnamen van hoe de bestanden eruitzien.

Maar het is slim: als een bestand niet is veranderd, bewaart Git alleen een verwijzing naar de vorige versie van dat bestand. Geen duplicaat.

Resultaat: compleet én efficiënt.

![Snapshots vs diffs](/instructions/content-images/git/module2/snapshots_vs_diffs.svg)

---

## 5. De commit-graaf

Elke commit weet van welke commit hij afstamt — zijn "ouder" (parent).
Zo ontstaat een keten van commits.

```
A ← B ← C ← D   (main)
```

Wanneer je een branch maakt, vertakkt die keten:

```
A ← B ← C ← D         (main)
          ↖
            E ← F     (feature-branch)
```

Dit noemen we een **DAG**: een Directed Acyclic Graph.
Gericht (richting van oud naar nieuw), niet cyclisch (geen lussen).

HEAD is een verwijzing die zegt: *"hier ben jij nu"*.
Gewoonlijk wijst HEAD naar de tip van een branch.

![Commit-graaf met branches en HEAD](/instructions/content-images/git/module2/commit_graaf.svg)

---

## 6. Waarom is dit nuttig om te weten?

Je gebruikt deze kennis niet elke dag actief.
Maar als je begrijpt hoe Git intern werkt, begrijp je:

- waarom twee branches veilig naast elkaar kunnen bestaan
- waarom Git zo snel is (alles is lokaal en gehasht)
- waarom een commit onveranderlijk is (de hash bevestigt de inhoud)
- wat er bedoeld wordt als iemand zegt "teruggaan naar een eerdere commit"

Git is geen magie. Het is een slim systeem van objecten en verwijzingen.
