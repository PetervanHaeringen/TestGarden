# Module 5 — Lokaal werken

Je hebt Git gezien, gevoeld en getekend.
Nu ga je het doen. In de terminal, op een echte repository.

---

## Voorbereiding: installatie en configuratie

**Installeer Git**
- Windows: [git-scm.com/download/win](https://git-scm.com/download/win)
- Mac: open Terminal, typ `git --version` (installeert automatisch of geeft instructie)
- Linux: `sudo apt install git`

**Stel je naam en e-mail in** (dit staat in elke commit die je maakt):

```bash
git config --global user.name "Jouw Naam"
git config --global user.email "jouw@email.nl"
```

Controleer je instellingen:

```bash
git config --list
```

---

## De oefenrepository

Voor dit leerpad gebruiken we een aparte oefenrepository:

**`git-garden-playground`**

Je docent geeft je de exacte URL.
Die begint met `https://github.com/...`

Deze repository is speciaal voor oefenen — je kunt er niets kapotmaken.

---

## Stap 1: Clonen

Clonen is het downloaden van een repository naar je eigen computer.

```bash
git clone https://github.com/...url.../git-garden-playground
```

Na het clonen:

```bash
cd git-garden-playground
ls
```

Je ziet de bestanden van de repo. En er is een verborgen `.git`-map — de tijdmachine.

---

## Stap 2: Status bekijken

`git status` is je kompas. Gebruik het vaak.

```bash
git status
```

Je ziet op welke branch je staat en of er bestanden zijn gewijzigd.

---

## Stap 3: Een wijziging maken

Open de map in je editor (of gebruik de terminal).
Maak een nieuw bestand aan in de map `deelnemers/`:

```bash
mkdir -p deelnemers
echo "Naam: [jouw naam]" > deelnemers/[jouw-naam].txt
```

Bekijk daarna de status:

```bash
git status
```

Git meldt het nieuwe bestand als "untracked" — het bestaat wel, maar Git volgt het nog niet.

---

## Stap 4: Stagen

Stagen is zeggen: "dit bestand wil ik meenemen in de volgende commit."

```bash
git add deelnemers/[jouw-naam].txt
```

Of voeg alles in één keer toe:

```bash
git add .
```

Bekijk de status opnieuw. Het bestand staat nu in de "staging area" — klaar voor commit.

![Werkstroom: working directory → staging area → repository](images/werkstroom.png)

---

## Stap 5: Committen

Nu maak je de momentopname.

```bash
git commit -m "Voeg [jouw naam] toe aan deelnemerslijst"
```

Een goede commit-message:
- begint met een werkwoord: "Voeg toe", "Fix", "Update", "Verwijder"
- beschrijft *wat* er veranderd is, niet *hoe*
- is kort (max ~72 tekens)

---

## Stap 6: Geschiedenis bekijken

```bash
git log
```

Je ziet alle commits: hash, auteur, datum, bericht.

Voor een compact overzicht:

```bash
git log --oneline
```

Voor een visueel overzicht met branches:

```bash
git log --oneline --graph --all
```

---

## Stap 7: Verschillen bekijken

Wil je zien wat er veranderd is vóór je commit?

```bash
git diff
```

Na stagen, maar vóór commit:

```bash
git diff --staged
```

---

## Samenvatting: de dagelijkse werkstroom

```
[wijziging maken]
      ↓
git add .
      ↓
git commit -m "..."
      ↓
git push   (volgt in module 6)
```

Herhaal dit patroon tientallen keren per dag.
Het wordt vanzelf routine.
