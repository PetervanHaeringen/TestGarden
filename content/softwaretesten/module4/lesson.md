# Module 4 – Testtechnieken

In deze module leer je hoe je goede testgevallen ontwerpt.

Niet “zomaar wat klikken”, maar gestructureerd, slim en creatief testen.

Deze technieken helpen je fouten te vinden die je anders nooit zou zien.

---

## 1. Waarom testtechnieken?

Testtechnieken helpen je **bewuster, vollediger en slimmer** te testen.

Ze zorgen ervoor dat je niet alleen de “gelukkige paden” test, maar ook:
- foutscenario’s
- rare invoer
- grenswaarden

Een goede tester gebruikt technieken om:
- meer fouten te vinden
- efficiënter te testen
- te laten zien dat er over de testcases is nagedacht
- herhaalbare en duidelijke testcases te maken

---

## 2. Equivalence Partitioning (EP)

Bij Equivalence Partitioning (EP) verdeel je alle mogelijke invoer in groepen (“partities”) waarvan je verwacht dat ze hetzelfde gedrag opleveren.

### Voorbeeld

Een leeftijdsveld accepteert leeftijden tussen **18 en 65**.

Dan zijn de partities:

- Te jong (0–17)
- Geldig (18–65)
- Te oud (66+)

> In plaats van 48 mogelijke geldige leeftijden test je er gewoon 1.  
> Minder werk, dezelfde dekking.

---

## 3. Boundary Value Analysis (BVA)

Fouten zitten vaak aan de randen van invoerwaarden.

Boundary testing focust daarom op:
- minima
- maxima
- net-over-de-grens waarden

### Voorbeeld

Leeftijd 18–65 is geldig.

Dan test je:

- 17 (net te laag)
- 18 (laagste geldige)
- 65 (hoogste geldige)
- 66 (net te hoog)

Deze techniek vindt veel fouten die gebruikers direct raken.

---

## 4. Decision Tables

Gebruik dit wanneer meerdere regels of voorwaarden tegelijk gelden.

Je zet alles in een tabel en maakt testcases per combinatie.

### Voorbeeld: inloggen

| Gebruikersnaam | Wachtwoord | Verwachting |
|---|---|---|
| Goed | Goed | Login ok |
| Goed | Fout | Foutmelding |
| Fout | Goed | Foutmelding |
| Fout | Fout | Foutmelding |

---

## 5. State Transition Testing

Sommige systemen veranderen van status.

Bijvoorbeeld:
- gebruiker logt in of uit
- bestelling verandert van status
- workflow gaat naar volgende stap

Hier test je:
- geldige overstappen
- ongeldige overstappen
- wat gebeurt als stappen worden overgeslagen

### Voorbeeld: bestelstatus

#### Geldige transities
- Geplaatst → Betaald
- Betaald → Verzonden

#### Ongeldige transities
- Verzonden → Geplaatst
- Verzonden → Betaald

---

## 6. Praktijkopdracht: schrijf 8 testcases

Je gaat nu zelf testgevallen maken voor een inlogscherm of invoerveld naar keuze.

Gebruik minimaal twee technieken.

### Opdracht

1. Kies een onderdeel:
   - login
   - wachtwoord reset
   - leeftijdsveld
   - of iets anders

2. Schrijf 8 testcases met:
   - stappen
   - verwacht resultaat
   - gebruikte techniek

3. Laat een klasgenoot jouw testcases uitvoeren.

4. Verbeter je testcases op basis van feedback.

> Een goede testcase is:
> - kort
> - duidelijk
> - reproduceerbaar

---

## 7. Reflectie

Denk na over jouw testcases:

- Welke techniek voelde het meest logisch?
- Wat kostte de meeste tijd?
- Welke techniek vond je verrassend effectief?