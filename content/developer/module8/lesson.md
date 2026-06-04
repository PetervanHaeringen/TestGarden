# Module 8 — Iets echts bouwen

Je kent de bouwstenen. Nu bouw je iets.

In deze module kies je een van vier projecten en werk je het af. Niet perfect — maar werkend. En werkend is de enige maatstaf die telt.

---

## Kies je project

Kies het project dat jou het meest aanspreekt.

---

### Project A — Quiz

Een quiz die vragen stelt en bijhoudt hoeveel je er goed hebt.

**Wat het doet:**
- Stelt 3 of meer vragen
- Accepteert een antwoord van de gebruiker
- Geeft terug of het goed of fout was
- Geeft aan het einde de totale score

**Startpunt:**
```javascript
let score = 0;

function stelVraag(vraag, juistAntwoord) {
    let antwoord = prompt(vraag);
    if (antwoord.toLowerCase() === juistAntwoord.toLowerCase()) {
        alert("Goed!");
        score++;
    } else {
        alert("Helaas. Het juiste antwoord was: " + juistAntwoord);
    }
}

stelVraag("Wat is de hoofdstad van Nederland?", "Amsterdam");
stelVraag("Hoeveel is 7 maal 8?", "56");
stelVraag("Wie schreef het eerste algoritme voor een machine?", "Ada Lovelace");

alert("Je score: " + score + " van de 3");
```

**Uitbreiden:**
- Voeg meer vragen toe
- Geef feedback per vraag
- Maak de vragen willekeurig met `Math.random()`

---

### Project B — Calculator

Een calculator die rekent met twee getallen en een bewerking.

**Wat het doet:**
- Vraagt twee getallen
- Vraagt welke bewerking (+, -, *, /)
- Geeft het resultaat

**Startpunt:**
```javascript
function bereken(a, b, bewerking) {
    if (bewerking === "+") return a + b;
    if (bewerking === "-") return a - b;
    if (bewerking === "*") return a * b;
    if (bewerking === "/") {
        if (b === 0) return "Kan niet delen door nul";
        return a / b;
    }
    return "Onbekende bewerking";
}

let getal1 = Number(prompt("Eerste getal:"));
let getal2 = Number(prompt("Tweede getal:"));
let bewerking = prompt("Bewerking (+, -, *, /):");

let resultaat = bereken(getal1, getal2, bewerking);
alert(getal1 + " " + bewerking + " " + getal2 + " = " + resultaat);
```

**Uitbreiden:**
- Laat de gebruiker meerdere berekeningen achter elkaar doen
- Voeg de wortel toe (`Math.sqrt()`)
- Sla een geschiedenis bij van alle berekeningen

---

### Project C — Tekstverwerker

Een programma dat iets doet met tekst die je invoert.

**Wat het doet:**
- Telt het aantal woorden in een tekst
- Telt het aantal keer dat een bepaald woord voorkomt
- Zet de tekst om naar hoofdletters of kleine letters

**Startpunt:**
```javascript
let tekst = prompt("Voer een tekst in:");

let woorden = tekst.split(" ");
alert("Aantal woorden: " + woorden.length);

let zoekwoord = prompt("Welk woord wil je zoeken?");
let teller = 0;
for (let i = 0; i < woorden.length; i++) {
    if (woorden[i].toLowerCase() === zoekwoord.toLowerCase()) {
        teller++;
    }
}
alert("'" + zoekwoord + "' komt " + teller + " keer voor");
```

**Uitbreiden:**
- Vervang een woord door een ander woord
- Keer de volgorde van de woorden om
- Tel het aantal zinnen (hint: zoek naar punten)

---

### Project D — Raad het getal

Een spel waarbij de computer een getal kiest en jij het moet raden.

**Wat het doet:**
- De computer kiest een willekeurig getal tussen 1 en 100
- De speler gokt
- Het programma zegt "te hoog", "te laag" of "goed geraden"
- Het telt hoeveel pogingen de speler nodig had

**Startpunt:**
```javascript
let geheim = Math.floor(Math.random() * 100) + 1;
let pogingen = 0;
let geraden = false;

while (!geraden) {
    let gok = Number(prompt("Raad een getal tussen 1 en 100:"));
    pogingen++;

    if (gok < geheim) {
        alert("Te laag! Probeer hoger.");
    } else if (gok > geheim) {
        alert("Te hoog! Probeer lager.");
    } else {
        alert("Goed geraden! Je had " + pogingen + " pogingen nodig.");
        geraden = true;
    }
}
```

**Uitbreiden:**
- Voeg een maximumaantal pogingen toe
- Geef een beoordeling op basis van het aantal pogingen
- Laat de speler opnieuw spelen zonder de pagina te herladen

---

## Hoe je dit aanpakt

**Stap 1 — Kies en begrijp het startpunt**
Lees de code regel voor regel. Kun je uitleggen wat elke regel doet?

**Stap 2 — Laat het werken zoals het is**
Kopieer het startpunt naar de browserconsole en voer het uit. Werkt het?

**Stap 3 — Pas één ding aan**
Verander één kleine waarde of voeg één regel toe. Voer opnieuw uit.

**Stap 4 — Breid stap voor stap uit**
Voeg één uitbreiding toe tegelijk. Test na elke toevoeging.

**Stap 5 — Breek het bewust**
Verander iets wat het fout laat gaan. Lees de foutmelding. Herstel.

---

## Wat maakt een goed programma?

- Het doet wat het moet doen
- Het geeft duidelijke feedback aan de gebruiker
- Het crasht niet bij onverwachte invoer
- Je kunt aan anderen uitleggen hoe het werkt

Perfectionisme is de vijand van af. Maak het werkend — dan kun je het verbeteren.
