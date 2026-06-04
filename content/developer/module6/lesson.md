# Module 6 — Bouwstenen van een programma

Je hebt algoritmen gevoeld met je handen. Nu schrijf je ze op.
Open de browserconsole (F12 → Console) en typ mee terwijl je leest.

---

## 1. Variabelen — waarden een naam geven

Een variabele is een naam die een waarde vasthoudt.

```javascript
let naam = "Ali";
let leeftijd = 23;
let actief = true;
```

- `let` maakt een nieuwe variabele aan
- `naam`, `leeftijd`, `actief` zijn de namen
- De waarden rechts van `=` worden opgeslagen

Typ dit in de console en druk op Enter na elke regel.
Dan typ je `naam` en druk je op Enter — de console toont "Ali".

**Drie soorten waarden:**
- Tekst (string): `"Ali"` — altijd tussen aanhalingstekens
- Getal (number): `23` — geen aanhalingstekens
- Waar/niet-waar (boolean): `true` of `false`

---

## 2. Condities — beslissingen nemen

```javascript
let temperatuur = 22;

if (temperatuur > 25) {
    console.log("Warm — neem water mee");
} else {
    console.log("Koel — een jas is handig");
}
```

Typ dit in de console. Verander dan `22` in `30` en voer het opnieuw uit.

De structuur is altijd:
```javascript
if (conditie) {
    // doe dit als de conditie waar is
} else {
    // doe dit als de conditie niet waar is
}
```

**Vergelijkingsoperatoren:**
| Operator | Betekenis |
|----------|-----------|
| `>` | groter dan |
| `<` | kleiner dan |
| `>=` | groter dan of gelijk aan |
| `<=` | kleiner dan of gelijk aan |
| `===` | precies gelijk aan |
| `!==` | niet gelijk aan |

---

## 3. Loops — herhalen

**For-loop** — als je weet hoeveel keer je iets wil herhalen:

```javascript
for (let i = 1; i <= 5; i++) {
    console.log("Stap " + i);
}
```

Dit drukt "Stap 1" t/m "Stap 5" af.

De drie delen tussen de haakjes:
1. `let i = 1` — begin bij 1
2. `i <= 5` — ga door zolang i kleiner dan of gelijk aan 5 is
3. `i++` — verhoog i met 1 na elke stap

**While-loop** — als je niet weet hoeveel keer:

```javascript
let teller = 1;

while (teller <= 5) {
    console.log("Teller is nu: " + teller);
    teller++;
}
```

Hetzelfde resultaat, andere schrijfwijze. Gebruik `while` als de stopconditie afhankelijk is van iets wat tijdens het programma verandert.

---

## 4. Functies — herbruikbare blokken

Een functie is een blok code met een naam. Je schrijft het één keer en gebruikt het meerdere keren.

```javascript
function groet(naam) {
    console.log("Hallo, " + naam + "!");
}

groet("Ali");
groet("Fatima");
groet("Jonas");
```

De functie `groet` verwacht een **parameter** — `naam`.
Elke keer dat je de functie aanroept, geef je een andere waarde mee.

**Functies die een waarde teruggeven:**

```javascript
function kwadraat(getal) {
    return getal * getal;
}

let resultaat = kwadraat(4);
console.log(resultaat);
```

`return` stuurt een waarde terug. Die kun je opslaan of direct gebruiken.

---

## 5. Alles samen — een mini-programma

```javascript
function beoordeel(score) {
    if (score >= 90) {
        return "Uitstekend";
    } else if (score >= 70) {
        return "Goed";
    } else if (score >= 55) {
        return "Voldoende";
    } else {
        return "Onvoldoende";
    }
}

let scores = [88, 42, 95, 67, 55];

for (let i = 0; i < scores.length; i++) {
    let oordeel = beoordeel(scores[i]);
    console.log("Score " + scores[i] + ": " + oordeel);
}
```

Typ dit over in de console. Kijk wat er gebeurt.
Verander dan één score en voer het opnieuw uit.

Dit is een echt programma: het heeft invoer, verwerking en uitvoer.

---

## 6. Oefeningen

Probeer deze opdrachten in de browserconsole:

**Opdracht 1:** Schrijf een functie `isEven` die `true` teruggeeft als een getal even is, en `false` als het oneven is. Test hem met de getallen 4, 7, 12 en 9.

**Opdracht 2:** Schrijf een loop die de tafel van 3 afdrukt (3, 6, 9, ... tot en met 30).

**Opdracht 3:** Maak een lijst met vijf namen. Loop door de lijst en druk elke naam af met "Welkom, [naam]!".

*Tip: Gebruik `let namen = ["naam1", "naam2", ...]` voor een lijst (array).*
