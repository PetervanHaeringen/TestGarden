# Module 2 — Testlevels & Smoke Testing

In deze module ontdek je hoe software testen in verschillende lagen gebeurt, en wat de rol is van de bekende **smoke test**.

We gaan van overzicht naar praktijk, zodat jij begrijpt hoe jouw testwerk onderdeel is van het grotere geheel.

---

## 1. Wat zijn testlevels?

Software wordt niet in één keer getest. Elk onderdeel wordt op een ander niveau gecontroleerd.

Deze niveaus noemen we **testlevels**.

- **Unit Testing** — kleine stukjes code, getest door ontwikkelaars
- **Integratietests** — werkt alles samen zoals bedoeld?
- **Systeemtests** — werkt de hele applicatie als geheel?
- **Acceptatietests** — werkt het voor de gebruiker en de opdrachtgever?

### Voorbeeld

In een webshop:

- unit test → werkt de berekening van korting?
- integratietest → werkt winkelwagen + voorraad samen?
- systeemtest → werkt het bestelproces end-to-end?
- acceptatietest → vindt de klant de flow logisch en bruikbaar?

---

## 2. Testtypes: functioneel & niet-functioneel

Naast testlevels heb je ook **testtypes**.

Dit beschrijft wat je test.

- **Functioneel testen** — doet de functie wat hij moet doen?
- **Niet-functioneel testen** — snelheid, veiligheid, gebruiksgemak, stabiliteit

In TestGarden richten we ons vooral op functioneel testen, zoals smoke tests en exploratory testing.

---

## 3. Wat is een Smoke Test?

Een smoke test is een **korte, snelle check** om te zien of het systeem “ongeveer gezond” is na een nieuwe release, update of deploy.

Het is de digitale variant van:

> “gaat de rookmelder af?”

Als iets fundamenteels stuk is, wil je dat meteen weten.

### Waarom smoke tests?

- Ze zijn snel en geven direct duidelijkheid
- Ze voorkomen verspilling van tijd op kapotte builds
- Ze geven een GO / NO-GO voor verdere testen

### Voorbeeld van een smoke test

- Laadt de applicatie?
- Kan de gebruiker inloggen?
- Werkt de belangrijkste flow?
- Zijn er geen 404- of 500-fouten?

---

## 4. Voorbeeld Smoke Test Checklist

- [ ] Is de website bereikbaar?
- [ ] Kan een testgebruiker inloggen?
- [ ] Werkt de belangrijkste functionaliteit?
- [ ] Werken de belangrijkste links en knoppen?
- [ ] Zijn er geen grote fouten zichtbaar?
- [ ] Werkt het ook op mobiel of andere browser?

Je sluit een smoke test af met:

**GO / NO-GO**

---

## 5. Praktijkopdracht

1. Kies een demo-webapp
2. Maak een smoke checklist
3. Voer de checklist uit
4. Noteer Pass / Fail
5. Schrijf een conclusie

> Een smoke test is geen volledige test.
> Het is een snelle gezondheidsscan.

---

## 6. Reflectie

Denk na over:

- Welke check was het belangrijkst?
- Welk probleem was het grootste risico?
- Hoe zou je checklist verbeteren?