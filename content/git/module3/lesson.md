# Module 3 — Versiebeheer in beeld

Voordat je een commando typt, moet je het kunnen *zien*.
In deze module bouwen we het mentale model: hoe ziet Git eruit als je het tekent?

---

## 1. De tijdlijn: commits in een rij

De eenvoudigste Git-situatie is een rechte lijn van commits.
Elke commit is een momentopname. Elke commit wijst terug naar zijn voorganger.

```
○ — ○ — ○ — ○ — ○
A   B   C   D   E
```

- **A** is de eerste commit (de oorsprong)
- **E** is de laatste commit (de huidige stand)
- De pijlen wijzen naar het verleden

Lees de tijdlijn van links naar rechts: zo is de geschiedenis gegroeid.

![Git tijdlijn — commits in een rij](images/tijdlijn_lineair.png)

---

## 2. Een branch: een zijtak

Stel je voor: je wilt iets uitproberen zonder de hoofdlijn te raken.
Je maakt een **branch** — een zijtak die begint bij een bestaande commit.

```
○ — ○ — ○ — ○ — ○       (main)
              |
              ○ — ○       (experiment)
```

- `main` gaat gewoon door
- `experiment` begint bij commit D en groeit onafhankelijk
- Beide bestaan tegelijk, zonder elkaar te beïnvloeden

Een branch is in Git niets meer dan een naam die wijst naar een commit.
Dat is het. Geen kopie van bestanden, geen dubbele map — gewoon een label.

![Branch als zijtak van de tijdlijn](images/branch_zijtak.png)

---

## 3. Mergen: twee takken samenvoegen

Als het experiment klaar is, wil je het terugvoegen in `main`.
Dat heet een **merge**.

```
○ — ○ — ○ — ○ — ○ — ○   (main, na merge)
              |       |
              ○ — ○ ——   (experiment, gemerged)
```

Git kijkt naar de gemeenschappelijke voorouder (commit D) en de twee uiteinden.
Het combineert de wijzigingen en maakt een nieuwe **merge-commit** (de laatste ○ op main).

Als dezelfde regels op beide takken zijn veranderd → conflict.
Als dat niet zo is → automatische merge.

![Merge van twee branches](images/merge_visueel.png)

---

## 4. HEAD: jij bent hier

`HEAD` is een sticker die aangeeft waar jij nu bent in de graaf.

```
○ — ○ — ○ — ○ — ○
                 ↑
                HEAD (main)
```

Als je naar een andere branch gaat (`git switch experiment`), schuift de sticker mee:

```
○ — ○ — ○ — ○ — ○       (main)
              |
              ○ — ○
                   ↑
                  HEAD (experiment)
```

Alles wat je nu committet, gaat naar de branch waar HEAD op staat.

---

## 5. Terug in de tijd

Stel dat commit C een fout bevatte die je nu wil onderzoeken.
Je kunt HEAD tijdelijk naar C verplaatsen (`git checkout C`).

```
○ — ○ — ○ — ○ — ○
         ↑
        HEAD (detached)
```

Je bestanden zien er dan uit zoals ze op dat moment waren.
Git noemt dit "detached HEAD" — je staat niet op een branch, maar direct op een commit.

Nuttig om te kijken. Gevaarlijk om te committen zonder nieuwe branch.

---

## 6. Oefening: teken het zelf

Pak een pen en papier.

1. Teken een rechte lijn met vijf cirkels (commits A t/m E).
2. Teken een branch die begint bij C, met twee extra commits.
3. Teken een merge terug naar de hoofdlijn na E.
4. Zet de HEAD-sticker op de juiste plek.

Deze tekening is precies wat Git van binnen bijhoudt.
In de volgende module speel je dit na met kaartjes.
