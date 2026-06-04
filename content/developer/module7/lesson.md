# Module 7 — Fouten maken en lezen

Elk programma dat je schrijft gaat een keer fout.
Dat is niet erg — het is onvermijdelijk. De vraag is niet *of* je fouten maakt, maar hoe snel je ze vindt en oplost.

Goede developers zijn niet mensen die geen fouten maken. Het zijn mensen die fouten snel lezen.

---

## 1. Drie soorten fouten

**Syntaxfout (SyntaxError)**
De code is grammaticaal incorrect — de taal begrijpt het niet.

```javascript
console.log("Hallo"   // haakje vergeten
```
```
Uncaught SyntaxError: Unexpected end of input
```

De interpreter kan de code niet eens starten. Zoek naar ontbrekende haakjes, aanhalingstekens of accolades.

---

**Runtimefout**
De code is grammaticaal correct, maar gaat fout tijdens uitvoering.

```javascript
let getal = null;
console.log(getal.toString());
```
```
Uncaught TypeError: Cannot read properties of null
```

De code ziet er geldig uit maar probeert iets te doen wat niet kan — in dit geval een methode aanroepen op `null`.

---

**Logische fout**
De code draait zonder foutmelding, maar doet niet wat je bedoelt.

```javascript
function gemiddelde(a, b) {
    return a + b / 2;   // fout: deelt alleen b door 2
}

console.log(gemiddelde(4, 6));  // geeft 7, niet 5
```

Dit is de lastigste fout — de computer klaagt niet. Jij moet zelf ontdekken wat er mis is.

---

## 2. Foutmeldingen lezen

Een foutmelding is geen aanval. Het is informatie.

```
Uncaught TypeError: namen.push is not a function
    at <anonymous>:3:7
```

Lees het in drie stappen:

1. **Type fout** — `TypeError`: iets heeft het verkeerde type
2. **Beschrijving** — `namen.push is not a function`: de variabele `namen` heeft geen methode `push`
3. **Locatie** — `at <anonymous>:3:7`: regel 3, karakter 7

Begin altijd bij de eerste foutmelding. Soms veroorzaakt één fout een cascade van andere meldingen.

---

## 3. Debuggen als denkproces

Debuggen is wetenschappelijk denken: hypothese opstellen, testen, conclusie trekken.

**Stap 1 — Reproduceer het probleem**
Kun je het probleem betrouwbaar laten optreden? Als je niet weet wanneer het fout gaat, kun je het niet oplossen.

**Stap 2 — Isoleer het probleem**
Verklein de code totdat je de kleinste versie hebt die nog steeds fout gaat. Hoe minder code, hoe makkelijker te begrijpen.

**Stap 3 — Stel een hypothese op**
"Ik denk dat het fout gaat omdat variabele x op dit punt leeg is."

**Stap 4 — Test de hypothese**
Voeg `console.log` toe om te zien wat de waarden zijn:

```javascript
function berekenKorting(prijs, percentage) {
    console.log("prijs:", prijs);           // controleer invoer
    console.log("percentage:", percentage);  // controleer invoer
    let korting = prijs * percentage / 100;
    console.log("korting:", korting);        // controleer berekening
    return prijs - korting;
}
```

**Stap 5 — Pas aan en test opnieuw**
Was je hypothese correct? Zo niet, stel een nieuwe op.

---

## 4. Veelgemaakte fouten en hoe je ze oplost

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| `is not defined` | Variabele bestaat niet of naam verkeerd gespeld | Controleer de naam en of `let` is gebruikt |
| `is not a function` | Aanroep op iets wat geen functie is | Controleer het type van de variabele |
| `Cannot read properties of null` | Methode aanroepen op null/undefined | Controleer of de variabele een waarde heeft |
| `SyntaxError` | Ontbrekend haakje, aanhalingsteken of accolade | Tel de haakjes — zijn ze gesloten? |
| Oneindige loop | Stopconditie wordt nooit vals | Controleer of de variabele in de conditie verandert |

---

## 5. Kapotte programma's repareren

Hieronder staan drie stukjes kapotte code. Zoek de fout en herstel hem.

**Kapot programma 1:**
```javascript
function groet(naam) {
    console.log("Hallo, " + naam)
}

groet("Ali"
```

**Kapot programma 2:**
```javascript
let score = "95";

if (score >= 90) {
    console.log("Geslaagd");
}
```
*(Hint: `score` is een string, geen getal. Wat doet `>=` met een string?)*

**Kapot programma 3:**
```javascript
function vermenigvuldig(a, b) {
    return a + b;
}

console.log(vermenigvuldig(3, 4));  // verwacht 12, geeft 7
```

---

## 6. De mindset van een debugger

De beste developers worden niet chagrijnig van fouten — ze worden nieuwsgierig.

Een fout betekent: *de computer vertelt je iets wat je nog niet wist over je eigen code.*

Dat is waardevol. Elke fout die je oplost maakt je beter in het voorkomen van diezelfde fout de volgende keer.

> "Debugging is als een detectiveverhaal waarbij jij tegelijk de detective én de dader bent."
