# Module 6 – Bug Reporting

Bugreporting is één van de belangrijkste vaardigheden van een tester.

Een goed bugreport is:
- duidelijk
- reproduceerbaar
- volledig
- bruikbaar voor ontwikkelaars

In deze module leer je hoe je professionele bugreports schrijft.

---

## 1. Wat is een bug?

Een **bug** is een situatie waarin software niet doet wat verwacht wordt.

Dat kan gaan om:

- functionele fouten
- layoutproblemen
- verkeerde foutmeldingen
- onverwacht gedrag
- beveiligingsproblemen
- prestatieproblemen

Een bug is dus het verschil tussen:

> verwacht gedrag ↔ werkelijk gedrag

---

## 2. Wat is een goed bugreport?

Een goed bugreport is:

- **Duidelijk** — iedereen begrijpt het probleem
- **Reproduceerbaar** — iemand anders kan het opnieuw veroorzaken
- **Volledig** — alle relevante informatie staat erin
- **Neutraal** — feitelijk zonder verwijt of emotie

### Voorbeeld

#### Slecht bugreport

> “De site doet het niet. Fix plz.”

#### Goed bugreport

> “Bij het klikken op ‘Opslaan’ verschijnt foutmelding 500 en wordt het formulier niet opgeslagen.”

---

## 3. Severity en Priority

Testers geven vaak labels mee aan bugs.

### Severity

Hoe ernstig is het probleem voor het systeem?

### Priority

Hoe snel moet het opgelost worden?

### Voorbeelden

#### Hoge severity, lage priority
Een crash in een functie die bijna niemand gebruikt.

#### Lage severity, hoge priority
Een spelfout op de homepage van een belangrijke klant.

---

## 4. Bugreport Template

Gebruik dit template bij het schrijven van bugreports.

```text
Titel:
  Korte en duidelijke omschrijving

Omgeving:
  Browser, OS, versie, device

Severity:
Priority:

Stappen om te reproduceren:
  1. ...
  2. ...
  3. ...

Verwacht resultaat:
  Wat zou er moeten gebeuren?

Werkelijk resultaat:
  Wat gebeurde er in plaats daarvan?

Screenshot / log:
  (optioneel maar aanbevolen)

Extra opmerkingen:
  frequentie, impact, bijzonderheden
```

---

## 5. Praktijkopdracht: schrijf 3 bugreports

Je gaat nu drie bugreports schrijven op basis van fouten die je eerder vond tijdens exploratory testing.

### Opdracht

1. Kies drie issues uit je session report.
2. Schrijf voor elk issue een volledig bugreport.
3. Gebruik het template hierboven.
4. Controleer of de bug reproduceerbaar is.
5. Laat een klasgenoot jouw report testen.

> Een bugreport is pas goed als iemand anders exact hetzelfde probleem kan reproduceren.

---

## 6. Reflectie

Denk terug aan jouw bugreports:

- Welke was het duidelijkst?
- Welke informatie miste je eerst?
- Hoe reageerde je klasgenoot?
- Wat zou je volgende keer anders doen?