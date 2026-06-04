# Module 4 — Talen vergeleken

Er zijn honderden programmeertalen. Je hoeft ze niet allemaal te kennen.
Maar je moet begrijpen waarom er zoveel zijn — en hoe je kiest.

---

## 1. Hetzelfde probleem, drie talen

We beginnen met een simpel algoritme: bepaal of een getal even of oneven is.

**Pseudocode** — geen echte taal, gewoon de gedachte opschrijven:
```
als getal deelbaar door 2 is:
    print "even"
anders:
    print "oneven"
```

**Python:**
```python
getal = 7
if getal % 2 == 0:
    print("even")
else:
    print("oneven")
```

**JavaScript:**
```javascript
let getal = 7;
if (getal % 2 === 0) {
    console.log("even");
} else {
    console.log("oneven");
}
```

De gedachte is identiek. De spelling verschilt.

Merk op: Python gebruikt inspringing (witruimte) om blokken af te bakenen. JavaScript gebruikt accolades `{}`. Beide werken — het zijn gewoon verschillende keuzes van de taalontwerpers.

---

## 2. De grote namen en waar ze voor dienen

| Taal | Sterk in | Typisch gebruikt voor |
|------|----------|-----------------------|
| Python | leesbaarheid, data, AI | scripts, data-analyse, backend, onderwijs |
| JavaScript | browser, interactiviteit | websites, frontend, ook backend (Node.js) |
| Java | stabiliteit, grote systemen | bedrijfssoftware, Android |
| C / C++ | snelheid, hardware-controle | besturingssystemen, spelengines, embedded |
| SQL | databases bevragen | elke toepassing met een database |
| HTML/CSS | structuur en stijl | webpagina's (geen programmeertaal, maar wel code) |
| PHP | webservers | WordPress, veel bestaande websites |
| Swift / Kotlin | mobiel | iOS (Swift), Android (Kotlin) |

Er is geen "beste" taal. Elke taal is een gereedschap. Je kiest op basis van het probleem.

---

## 3. Hoe lees je onbekende code?

Je zult in je carrière voortdurend code tegenkomen die je nog nooit hebt gezien.
Dat is normaal. De vaardigheid is niet alles kennen — het is de hoofdlijn kunnen lezen.

**Strategie:**
1. Zoek de structuur: waar beginnen blokken? Waar eindigen ze?
2. Zoek de intentie: wat probeert deze code te doen?
3. Zoek de invoer en uitvoer: wat gaat erin, wat komt eruit?
4. Zoek bekende patronen: if/else, loops, functies — die zien er in elke taal vergelijkbaar uit

**Voorbeeld — onbekende taal (Ruby):**
```ruby
getal = 7
if getal % 2 == 0
  puts "even"
else
  puts "oneven"
end
```

Je kent Ruby misschien niet. Maar je herkent `if`, `else`, `% 2`, en het idee van uitvoer.
Je begrijpt wat dit doet zonder ooit Ruby te hebben geleerd.

---

## 4. JavaScript in de browser — probeer het zelf

JavaScript heeft een bijzonder voordeel: elke computer met een browser heeft al een JavaScript-omgeving ingebouwd.

**Zo open je die:**
1. Open Chrome, Firefox of Edge
2. Druk op F12 (of rechtermuisklik → "Inspecteren")
3. Klik op het tabblad "Console"
4. Type hier JavaScript en druk op Enter

Probeer:
```javascript
console.log("Hallo wereld");
```

En dan:
```javascript
let x = 5;
let y = 3;
console.log(x + y);
```

De browser voert het meteen uit. Geen installatie, geen configuratie.

---

## 5. Python — de taal die leest als Engels

Python is ontworpen met één duidelijk doel: **leesbaarheid**.

De maker, Guido van Rossum, schreef in 1991 een taal waarbij witruimte betekenis heeft, waarbij je geen puntkomma's nodig hebt, en waarbij code bijna als proza leest.

```python
namen = ["Ali", "Fatima", "Jonas"]

for naam in namen:
    print("Hallo, " + naam)
```

Dit doet wat er staat: voor elke naam in de lijst, druk een begroeting af.

Python is populair in onderwijs, data-analyse, AI en scripting. Het is de taal die je kiest als je snel iets wil bouwen en leesbaarheid belangrijk is.

---

## 6. Welke taal leer je als eerste?

Het eerlijke antwoord: het maakt minder uit dan je denkt.

Als je JavaScript leert, begrijp je daarna Python sneller. Als je Python leert, begrijp je daarna JavaScript sneller. De kernconcepten — variabelen, condities, loops, functies — zijn in elke taal aanwezig.

Kies op basis van:
- **Wat je wil bouwen** — een website? JavaScript. Data analyseren? Python. Een app? Swift of Kotlin.
- **Wat je omgeving gebruikt** — als je collega's Python schrijven, begin met Python.
- **Wat je motiveert** — de taal die je enthousiast maakt, leer je sneller.

In deze cursus gebruiken we JavaScript voor browser-oefeningen (geen installatie) en Python voor backend-concepten.
