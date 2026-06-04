# TestGarden — Projectbriefing

*Voor nieuwe medewerkers, AI-assistenten, en iedereen die na een pauze weer aansluit.*
*Leestijd: 5 minuten.*

---

## Wat is TestGarden?

Een leeromgeving voor jonge software-testers, gebouwd door Peter van Haeringen in samenwerking met AI-systemen. Gehost op PythonAnywhere, geschreven in Python/Flask.

De doelgroep: jongeren buiten het reguliere systeem, via ICT vanaf Morgen (sociale onderneming in Alkmaar/Amsterdam). Diversiteit is de regel — korte stages, lange trajecten, individuele paden.

De kern: niet alleen leren *wat* testen is, maar leren *kijken* zoals een tester kijkt.

**Live:** https://petervanhaeringen.pythonanywhere.com/
**Repository:** https://github.com/GitAI47/TestGarden.git

---

## Hoe het gebouwd is

Flask-app met Blueprint-architectuur. Elke functionaliteit heeft een eigen "tuinbed":

```
core/         — hoofdpagina's, menu
auth/         — login, logout, register
exercise/     — oefenbedden (sites met ingebouwde fouten)
instructions/ — leerpaden
feedback/     — feedbackformulier
tools/        — Python-tools als webinterface
```

Database: één centrale SQLite (niet per gebruiker — zie ADR-001).
Thema's: vier CSS-thema's via custom properties (ontworpen door DeepSeek).

---

## Lesinhoud: hoe het werkt

Inhoud staat *niet* in de Flask-code maar in open bestanden per module:

```
content/<track>/<module_slug>/
  meta.yaml       — configuratie (titel, volgorde, leerdoelen, ...)
  lesson.md       — lesinhoud
  questions.yaml  — vragen (mcq, truefalse, open)
```

Een `content_loader` laadt dit dynamisch. Nieuw lesmateriaal toevoegen = map aanmaken + drie bestanden, geen code aanpassen.

*Let op: de migratie van het oude systeem (hardcoded routes) naar dit nieuwe systeem loopt nog. Beide bestaan naast elkaar.*

---

## Leerlingen en voortgang

Leerlingen hebben een persoonlijk dashboard ("Mijn Tuin"). Welke modules ze zien hangt af van `module_visibility`:

| Instelling | Ziet |
|------------|------|
| `alleen_toegewezen` | Alleen hun modules (korte bezoeker) |
| `vergrendeld` | Hun modules + de rest grijs (maatwerk) |
| `alles` | Alles open (vast traject) |

Modules worden toegewezen door admin of teacher via een `UserModule` koppeltabel.
Voortgang wordt opgeslagen in de database (niet alleen in sessie).

---

## Wat er nu speelt

- **Jesse** (eerste actieve leerling) doorloopt module 1-2 van het Softwaretesten-pad en geeft feedback
- Voortgangsindicatie is in implementatie
- Individuele leerlijnen (UserModule) zijn in implementatie
- De YAML/MD content-migratie loopt

---

## Belangrijke beslissingen om te kennen

| Beslissing | Kern |
|------------|------|
| Één database | Niet per gebruiker — te complex, niet schaalbaar |
| Blueprints | Nieuwe functionaliteit = nieuw blueprint, bestaande code onaangeroerd |
| Content als bestanden | Inhoud los van code — docenten kunnen aanpassen zonder Flask |
| Voortgang in DB | Sessies zijn vluchtig, database is persistent |
| Multi-tenant | Goed idee voor later, nu bewust geparkeerd |

---

## Wat TestGarden niet is

- Geen beoordelingssysteem dat leerlingen afrekent
- Geen statische kennisbank
- Geen vervanging voor menselijke begeleiding

---

## Wie werkt hieraan

**Peter** — initiator, pedagoog, lerende developer, bewaker van intentie en cultuur.
**Cynthia** — medewerker ICT vanaf Morgen, mede-gebruiker en feedback.
**Jesse** — eerste actieve leerling/tester.
**AI-systemen** — ChatGPT (bouw), DeepSeek/Lao (CSS), Claude (architectuur, review), en anderen.

*De volledige ontwikkelgeschiedenis met alle keuzes en motivaties staat in de ADR-map.*
