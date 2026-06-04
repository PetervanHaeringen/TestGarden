# Module 3 – Testplan & Risicoanalyse

In deze module leer je de basis van een lichtgewicht testplan.

Geen dikke documenten, maar een praktische samenvatting van:

**wat gaan we testen, waarom, hoe en wanneer is het goed?**

---

## 1. Wat is een testplan?

Een testplan is een kort document dat richting geeft aan het testen.

Het beschrijft:

- wat er getest moet worden
- welke risico’s belangrijk zijn
- welke aanpak gekozen wordt

In moderne projecten, en zeker in TestGarden, maken we testplannen zo eenvoudig mogelijk.

Vaak is één pagina al voldoende.

### Een testplan bevat meestal

- Scope — wat testen we wel en wat niet?
- Belangrijkste risico’s
- Aanpak — smoke tests, testcases, exploratory testing
- Testomgeving
- Entry & Exit criteria
- Rollen — wie doet wat?

---

## 2. Wat is risicogestuurd testen?

Risico’s helpen je beslissen welke onderdelen het belangrijkst zijn om te testen.

Een risico ontstaat wanneer een **mogelijke fout** gecombineerd wordt met **impact**.

We gebruiken een simpele formule:

> **Risico = kans × impact**

Hoe hoger het risico, hoe meer aandacht een onderdeel nodig heeft in je testplan.

### Voorbeeld webshop

- Pagina “Product bekijken” → lage impact
- Pagina “Afrekenen” → hoge impact

Daarom krijgt het afrekenproces meer en diepere tests.

---

## 3. Voorbeeld van een 1-pagina testplan

Gebruik dit als basis wanneer je zelf een testplan maakt.

```text
Titel: Testplan voor [onderdeel/app]
Datum:
Auteur:

1. Scope:
   - Wat testen we wel?
   - Wat testen we niet?

2. Belangrijkste risico’s:
   - R1: [risico + reden]
   - R2: [risico + reden]

3. Aanpak:
   - Smoke tests
   - Testcases
   - Exploratory testing

4. Testomgeving:
   - URL, data, accounts

5. Entry criteria:
   - Build werkt
   - Testdata beschikbaar

6. Exit criteria:
   - Geen P1/P0 bugs open
   - Smoke test geslaagd

7. Rollen:
   - Tester(s)
   - Begeleider / Product owner
```

---

## 4. Praktijkopdracht: Maak je eigen mini-testplan

Je gaat nu voor het eerst zelf een testplan schrijven voor een klein onderdeel van de demo-app.

### Opdracht

1. Kies één onderdeel van de demo-app, bijvoorbeeld registratie.
2. Identificeer 3 risico’s met behulp van kans × impact.
3. Omschrijf wat je gaat testen (*scope*).
4. Kies je aanpak:
   - smoke testing
   - testcases
   - exploratory testing
5. Vul het 1-pagina testplansjabloon volledig in.

> **Tip:**  
> Hou het kort, overzichtelijk en praktisch.  
> Een testplan is geen verslag — het is je kompas.

---

## 5. Reflectie

Denk na over jouw testplan:

- Welke risico’s waren het belangrijkst?
- Wat heb je níet in scope gezet, en waarom?
- Zou je meer of minder detail willen toevoegen?

Probeer te bedenken:

- welke keuzes bewust waren
- welke onderdelen extra aandacht kregen
- en hoe jouw aanpak zou veranderen bij een grotere applicatie