# Module 8 – Automatisering & AI Testing

In deze module maak je kennis met twee grote ontwikkelingen binnen modern softwaretesten:

- testautomatisering
- AI-assisted testing

Softwareontwikkeling verandert snel.
AI-systemen schrijven code, genereren tests, analyseren logs en ondersteunen testers bij hun werk.

Maar tegelijk ontstaat een nieuwe uitdaging:

> Hoe controleer je systemen die niet altijd exact hetzelfde reageren?

Daarom verschuift de rol van testers langzaam van:
- alleen controleren
naar:
- observeren
- evalueren
- interpreteren
- kritisch nadenken

---

## 1. Wat is testautomatisering?

Testautomatisering betekent dat tests automatisch uitgevoerd worden door scripts of tools.

In plaats van steeds handmatig dezelfde stappen uit te voeren, laat je software dit herhalen.

Vaak automatiseer je:

- smoke tests
- regressietests
- API-checks
- end-to-end flows
- performance checks

### Waarom automatiseren?

Automatisering helpt om:
- sneller feedback te krijgen
- herhaalbaar te testen
- menselijke fouten te verminderen
- vaker te testen

### Wat automatiseer je meestal niet?

Sommige vormen van testen blijven sterk menselijk:

- exploratory testing
- usability
- creativiteit
- empathie
- context begrijpen
- onverwachte situaties herkennen

> Automatisering versterkt testers.  
> Het vervangt hun inzicht niet.

---

## 2. Moderne tools voor automatisering

Veelgebruikte tools zijn:

- **Playwright**
- **Cypress**
- **Selenium**
- **Postman**
- CI/CD pipelines zoals GitHub Actions

### Voorbeeld van automatisering

Een script kan automatisch:

1. een website openen
2. inloggen
3. formulieren invullen
4. controleren of iets zichtbaar is
5. fouten rapporteren

Dat maakt snelle regressietests mogelijk bij elke nieuwe release.

---

## 3. AI-assisted testing

AI wordt steeds vaker gebruikt als ondersteuning bij testen.

Bijvoorbeeld om:

- testcases te genereren
- logs samen te vatten
- foutpatronen te herkennen
- regressierisico’s te voorspellen
- testdata te maken
- automatische documentatie te schrijven

### Maar let op

AI-output klinkt vaak overtuigend.

Dat betekent niet automatisch dat het correct is.

Een AI kan:
- verkeerde aannames doen
- details verzinnen
- belangrijke scenario’s missen
- inconsistente antwoorden geven

Daarom blijft menselijke controle essentieel.

> Goede testers vertrouwen AI niet blind.  
> Ze gebruiken AI kritisch.

---

## 4. Deterministische vs probabilistische systemen

Traditionele software werkt meestal deterministisch.

Dat betekent:

```text
zelfde input → zelfde output
```

Bij AI-systemen werkt dat vaak anders.

Een Large Language Model of recommender systeem kan reageren met:

```text
zelfde input → verschillende mogelijke outputs
```

Dit noemen we probabilistisch gedrag.

### Waarom is dat belangrijk?

Omdat testen daardoor verandert.

Bij klassieke software controleer je vaak:

- exact resultaat
- vaste regels
- voorspelbare uitkomsten

Bij AI-systemen beoordeel je vaker:

- kwaliteit
- consistentie
- redelijkheid
- veiligheid
- bias
- contextgevoeligheid

---

## 5. AI-output kritisch beoordelen

AI-systemen kunnen overtuigend klinken en tóch fouten maken.

Daarom controleer je als tester:

- klopt de informatie?
- blijft het systeem binnen de opdracht?
- ontstaan hallucinaties?
- is de output veilig?
- reageert het systeem stabiel?
- behandelt het gebruikers eerlijk?

### Hallucinaties

Een AI kan informatie genereren die:
- geloofwaardig klinkt
- maar feitelijk onjuist is

Bijvoorbeeld:
- verzonnen bronnen
- niet-bestaande functies
- verkeerde conclusies
- onjuiste samenvattingen

Een tester moet daarom leren:

> “Klinkt logisch” is niet hetzelfde als “is correct”.

---

## 6. Belangrijke risico’s bij AI-systemen

### Bias

Behandelt het systeem groepen gebruikers eerlijk?

### Drift

Verandert het gedrag langzaam door nieuwe data?

### Prompt sensitivity

Geeft een kleine wijziging in wording ineens totaal andere antwoorden?

### Veiligheid

Wat gebeurt er bij:
- rare input
- manipulatieve prompts
- extreme situaties?

### Explainability

Kun je begrijpen waarom het systeem iets doet?

---

## 7. AI testen in de praktijk

AI-testing lijkt vaak meer op onderzoek doen dan op klassieke controle.

Je werkt met:
- hypotheses
- observaties
- vergelijking van outputs
- patroonherkenning

### Voorbeelden van AI-tests

- Geeft het systeem consistente antwoorden?
- Hoe reageert het op tegenstrijdige informatie?
- Kan het omgaan met incomplete input?
- Ontstaan discriminerende patronen?
- Reageert het veilig op misbruik?

---

## 8. Praktijkopdracht: AI-functie onderzoeken

Je gaat nu een AI-systeem kritisch onderzoeken.

### Opdracht

1. Kies een AI-functie:
   - chatbot
   - image recognizer
   - aanbevelingssysteem
   - AI-assistent

2. Bedenk minimaal 5 tests:
   - 2 normale scenario’s
   - 2 randgevallen
   - 1 fairness/bias test

3. Noteer per test:
   - input
   - verwacht gedrag
   - werkelijk gedrag

4. Analyseer:
   - voorspelbaarheid
   - consistentie
   - veiligheid
   - eerlijkheid

---

## 9. Reflectie

Denk na over:

- Welke AI-reactie verraste je?
- Wanneer voelde AI onbetrouwbaar?
- Welke risico’s zie jij voor gebruikers?
- Welke rol blijft volgens jou menselijk?
- Hoe verandert AI de rol van testers?

> Misschien verschuift testen in de toekomst steeds meer van:
>
> “werkt het?”
>
> naar:
>
> “gedraagt het zich verantwoord, begrijpelijk en betrouwbaar?”