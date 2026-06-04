# Module 5 — Programmeren zonder computer

Code begrijp je niet door het te lezen. Je begrijpt het door het te *doen*.
In deze module speel je algoritmen uit — met kaartjes, rollen en je eigen lichaam.

---

## Materiaal

- Kaartjes of post-its (minimaal 20 stuks)
- Stiften
- Deelnemers: 3 tot 8 personen
- Optioneel: tape op de vloer voor "geheugenplaatsen"

---

## Spelrollen

| Rol | Taak |
|-----|------|
| **Processor** | Voert de instructies uit — letter voor letter |
| **Geheugen** | Houdt kaartjes vast met waarden (variabelen) |
| **Invoer** | Geeft nieuwe waarden aan als het programma ernaar vraagt |
| **Uitvoer** | Schrijft op wat het programma "print" |
| **Programma** | Leest de instructies voor, één voor één |

---

## Spel 1 — Variabelen en optelling

**Het programma:**
```
1. Sla de waarde 5 op als "x"
2. Sla de waarde 3 op als "y"
3. Bereken x + y
4. Sla het resultaat op als "som"
5. Druk "som" af
```

**Spelverloop:**
- Geheugen schrijft "x = 5" op een kaartje en houdt het vast
- Geheugen schrijft "y = 3" op een kaartje en houdt het vast
- Processor vraagt aan Geheugen: "Wat is x?" → Geheugen toont het kaartje
- Processor vraagt: "Wat is y?" → Geheugen toont het kaartje
- Processor berekent 5 + 3 = 8
- Geheugen schrijft "som = 8" op een nieuw kaartje
- Uitvoer schrijft "8" op het bord

**Nabespreking:** Wat gebeurt er als je in stap 1 "x = 5" verandert in "x = 10"? Wie past wat aan?

---

## Spel 2 — Conditie (if/else)

**Het programma:**
```
1. Vraag een getal aan de gebruiker → sla op als "getal"
2. Als getal groter dan 10 is:
       druk "groot" af
   Anders:
       druk "klein" af
```

**Spelverloop:**
- Invoer kiest een getal (bijv. 7) en schrijft het op een kaartje
- Geheugen slaat het op als "getal = 7"
- Processor vraagt: "Is 7 groter dan 10?" → Nee
- Processor gaat naar de "Anders"-tak
- Uitvoer schrijft "klein"

Speel het drie keer met verschillende getallen. Wat verandert er in het gedrag van de Processor?

---

## Spel 3 — Loop (herhaling)

**Het programma:**
```
1. Sla de waarde 1 op als "teller"
2. Zolang teller kleiner dan of gelijk aan 5 is:
       druk teller af
       verhoog teller met 1
3. Klaar
```

**Spelverloop:**
- Geheugen start met "teller = 1"
- Processor controleert: is 1 ≤ 5? Ja → uitvoer schrijft "1", teller wordt 2
- Processor controleert: is 2 ≤ 5? Ja → uitvoer schrijft "2", teller wordt 3
- ... (ga door totdat teller = 6)
- Processor controleert: is 6 ≤ 5? Nee → stop

**Nabespreking:** Wat zou er gebeuren als we stap 3 vergeten waren — "verhoog teller met 1"? Probeer het uit.

*(Dit is een **oneindige loop** — het programma stopt nooit. Dit is een veelgemaakte fout.)*

---

## Spel 4 — Sorteren (een algoritme uitspelen)

Dit is een klassieker: **Bubble Sort**.

**Voorbereiding:**
- Schrijf 5 willekeurige getallen op kaartjes: bijv. 4, 1, 7, 2, 9
- Leg ze in een rij op tafel

**Het algoritme:**
```
Herhaal totdat er niets meer verandert:
    Voor elk paar naast elkaar:
        Als het linker getal groter is dan het rechter:
            Wissel ze om
```

**Spelverloop:**
- Ronde 1: vergelijk 4 en 1 → 4 > 1, wissel → [1, 4, 7, 2, 9]
- Vergelijk 4 en 7 → 4 < 7, niet wisselen
- Vergelijk 7 en 2 → 7 > 2, wissel → [1, 4, 2, 7, 9]
- Vergelijk 7 en 9 → 7 < 9, niet wisselen
- Ronde 2: opnieuw van voor af aan...
- Ga door totdat er in een volledige ronde niets meer wisselt

**Nabespreking:**
- Hoeveel rondes had je nodig?
- Wat is het "slechtste geval" — welke volgorde vraagt de meeste stappen?
- Kun je een snellere aanpak bedenken?

---

## Verbinding met echte code

Na deze spellen herken je de begrippen als je ze tegenkomt in code:

| Wat je deed in het spel | In code |
|--------------------------|---------|
| Kaartje vasthouden met een waarde | `x = 5` (variabele) |
| "Als dit, dan dat" | `if / else` |
| Herhalen totdat een conditie niet meer geldt | `while`-loop |
| Door een rij gaan | `for`-loop |
| Een stap vergeten waardoor het niet stopt | oneindige loop (bug) |

In de volgende module schrijf je dit allemaal zelf — maar dan in een echte taal.
