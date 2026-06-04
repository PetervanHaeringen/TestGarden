# Module 6 — Branches & samenwerken

Je kent de basiswerkstroom. Nu voeg je samenwerking toe.
Samenwerken in Git draait om branches en pull requests — de twee instrumenten waarmee teams tegelijk aan hetzelfde project werken zonder chaos.

---

## 1. Een branch aanmaken

Maak altijd een branch voor een nieuwe taak.
Nooit direct op `main` werken.

```bash
git branch mijn-branch
git switch mijn-branch
```

Of in één stap:

```bash
git switch -c mijn-branch
```

Controleer op welke branch je staat:

```bash
git branch
```

De branch met `*` ervoor is de huidige branch.

Goede branchnamen zijn beschrijvend en kort:
- `voeg-readme-toe`
- `fix-typo-introductie`
- `update-versienummer`

---

## 2. Wijzigingen committen op de branch

Werk gewoon zoals in module 5:

```bash
# wijziging maken in een bestand
git add .
git commit -m "Beschrijving van de wijziging"
```

Je commits staan nu op jouw branch — niet op `main`.
`main` is onveranderd.

---

## 3. Pushen naar GitHub

Nu stuur je jouw branch naar GitHub:

```bash
git push origin mijn-branch
```

De eerste keer vraagt Git je om je GitHub-account te bevestigen.
Na het pushen staat de branch op GitHub — zichtbaar voor anderen.

---

## 4. Een pull request openen

Een **pull request (PR)** is een voorstel: "ik wil mijn branch samenvoegen met main."

Op GitHub:
1. Ga naar de repository `git-garden-playground`
2. Je ziet een gele balk: "mijn-branch — Compare & pull request"
3. Klik daarop
4. Schrijf een beschrijving:
   - Wat heb je veranderd?
   - Waarom?
   - Is er iets dat de reviewer moet weten?
5. Klik op **"Create pull request"**

![Pull request aanmaken op GitHub](images/pull_request_aanmaken.png)

Een pull request is een gesprek, geen formulier.
Hoe beter de beschrijving, hoe soepeler de review.

---

## 5. De werkstroom van samenwerking

```
main (stable)
 |
 ├── branch A (Developer A werkt hier)
 |        → commits → push → PR → review → merge
 |
 ├── branch B (Developer B werkt hier)
 |        → commits → push → PR → review → merge
 |
main (bijgewerkt na merges)
```

Iedereen werkt op een eigen branch.
`main` wordt alleen bijgewerkt via goedgekeurde pull requests.
Zo blijft `main` altijd stabiel.

---

## 6. Wijzigingen van anderen ophalen

Als iemand anders een branch heeft gemerged, wil je die wijzigingen ook hebben.

```bash
git switch main
git pull
```

`git pull` haalt de nieuwste versie van `main` op van GitHub.

Wil je weten wat er op GitHub staat zonder je lokale bestanden te veranderen?

```bash
git fetch
git status
```

`git fetch` haalt de informatie op. `git pull` haalt de informatie op én past je bestanden aan.

---

## 7. Praktijkopdracht

1. Clone de `git-garden-playground` repository (als je dat nog niet gedaan hebt).
2. Maak een branch met je naam: `bijdrage-[jouw-naam]`
3. Maak een bestand aan in de map `bijdragen/`: `[jouw-naam].md`
4. Schrijf daarin:
   - Wat je verwacht te leren van Git
   - Één vraag die je nog hebt
5. Commit het bestand met een duidelijke boodschap.
6. Push de branch naar GitHub.
7. Open een pull request met een korte beschrijving.

Na de opdracht: je docent of een medestudent reviewt de PR.
