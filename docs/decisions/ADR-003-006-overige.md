# ADR-003 — Multi-AI curriculum: vijf systemen vergeleken

**Status:** Geaccepteerd  
**Datum:** vroeg in de ontwikkeling  
**Auteurs:** Peter + ChatGPT, DeepSeek, Gemini, Grok, Mistral  
**Bron:** ChatGPT_5 - Samengevoegde testgarden introductie

---

## Context

Voor de inhoud van de TestGarden-cursus (wat leerlingen moeten leren over softwaretesten) vroeg Peter aan vijf verschillende AI-systemen om een cursusopzet te maken. De resultaten werden vergeleken en samengevoegd.

## Beslissing

De sterkste elementen uit alle vijf systemen werden gecombineerd tot één structuur. Geen enkel systeem werd blindelings gevolgd.

**Bron per module:**
- Module 1 (Wat is testen): ChatGPT + Gemini
- Module 2 (Smoke testing): ChatGPT + DeepSeek
- Module 3 (Testplan): ChatGPT + DeepSeek + Mistral
- Module 4 (Testtechnieken): ChatGPT + Grok + Mistral
- Module 5 (Exploratory): ChatGPT

## Motivatie

- Geen enkel AI-systeem heeft het complete beeld
- Vergelijking maakt zwakke plekken zichtbaar
- Peter als mens bewaakt pedagogische intentie, cultuur en menselijke nuance
- Proces als kwaliteitscontrole

## Patroon

Dit is het eerste expliciete voorbeeld van **multi-AI witnessing** toegepast op inhoudsontwikkeling. Het patroon: AI organiseert, mens cureert.

---

---

# ADR-004 — Oefensites: drie-laags model

**Status:** Geaccepteerd  
**Datum:** nov/dec 2025  
**Auteurs:** Peter + ChatGPT  
**Bron:** ChatGPT_13 - Oefensites voor testers

---

## Context

Leerlingen moeten niet alleen theorie leren maar ook echt leren kijken. Daarvoor zijn oefensites nodig — webapplicaties met ingebouwde fouten in oplopende moeilijkheid.

## Beslissing

Elke oefensite heeft **drie lagen**:

1. **Een foute website** — mini-webapplicatie met voorgeprogrammeerde fouten (layout, functionaliteit, validatie, state, API)
2. **Een interactieve opdrachtpagina** — leerling vult in: fouttitel, omschrijving, reproduceerbare stappen, verwacht vs. werkelijk resultaat, bug-type
3. **Automatische nakijk- en feedbackmodule** — vergelijkt met `solutions.json`, kent partiële punten toe

**Puntenverdeling per bevinding:**
- 40% voor bug-identificatie
- 20% voor juiste classificatie
- 40% voor goede uitleg/reproduceerbaarheid

**Bestandsstructuur per oefening:**
```
exerciseX/
├── templates/exerciseX.html
├── static/faulty_site/
├── data/solutions.json
└── routes.py
```

## Motivatie

Leerlingen leren niet alleen bugs *vinden*, maar ook:
- kritisch kijken
- reproduceerbare stappen formuleren
- uitleggen *waarom* iets een bug is
- onderscheid maken tussen een designkeuze en een echte fout

## Afgewezen alternatieven

- Alleen handmatige nakijk door docent: niet schaalbaar
- Volledig automatisch zonder solutions.json: te rigide, mist partiële erkenning

---

---

# ADR-005 — Tools als service-laag

**Status:** Geaccepteerd  
**Datum:** dec 2025  
**Auteurs:** Peter + ChatGPT  
**Bron:** ChatGPT_11 - Tools in Flask App

---

## Context

Peter wilde Python-tools (scripts, validators, monitors) toegankelijk maken via de TestGarden-website.

## Probleem

Hoe integreer je bestaande Python-tools in een Flask-app zonder de weblaag te vervuilen met business logic?

## Beslissing

**Drie-laags patroon:**
1. **Service-module** — pure Python, geen Flask, bevat de logica als functies
2. **Blueprint** — routes + templates, dun, roept service-functies aan
3. **Drie ingangen** op dezelfde kernfunctie: web UI, API endpoint, CLI

```
tools/
├── csv_validator.py      # pure Python, testbaar, CLI-klaar
└── blueprints/tools/
    ├── routes.py         # Flask-laag
    └── templates/
```

## Motivatie

- Core logic is herbruikbaar buiten web (pytest, CLI)
- Weblaag blijft dun en vervangbaar
- Langlopende tools kunnen later naar een job queue (Celery/RQ) zonder de architectuur te breken

## Vuistregel vastgesteld

- Kleine, snelle tools (< 2-5 seconden): in dezelfde Flask-app
- Zware/langlopende tools: job queue of aparte worker
- Tools die gebruikerscode uitvoeren: sandboxing — **niet in hetzelfde proces**

---

---

# ADR-006 — Voortgang: sessie vs. database

**Status:** In ontwikkeling — probleem geïdentificeerd, oplossing geïmplementeerd  
**Datum:** mei 2026  
**Auteurs:** Peter + ChatGPT, input van leerling Jesse  
**Bron:** ChatGPT_17 - Keuzes in leerpadontwikkeling

---

## Context

Voortgangsindicatie werkte niet correct. Leerling Jesse (eerste actieve gebruiker) meldde dit als zijn eerste prioriteit — niet de inhoud maar de voortgangsindicatie.

## Probleem

Voortgang werd berekend maar niet correct opgeslagen. Drie mogelijke oorzaken geïdentificeerd:

1. Voortgang alleen in sessie, niet in database → verdwijnt bij refresh
2. Sessie wordt niet bijgewerkt bij AJAX/fetch routes
3. Frontend balk update, backend niet → DOM-staat ≠ server-staat

## Beslissing

Voortgang opslaan in de **database** (progress-tabel, zie ADR-001), niet alleen in de sessie.

**Definitie verschoven:** voortgang ≠ paginanummer, voortgang = voltooide leerstappen.

```
# Niet:  pagina 3 van 10
# Maar:  7 van 18 concepten beheerst
```

## Motivatie

- Sessies zijn vluchtig; database is persistent
- De nieuwe definitie maakt later adaptief leren mogelijk (herhalen, overslaan, testen)
- Jesse's feedback was een UX-prioriteit, geen bugmelding — hij gaf aan dat zonder voortgang het platform voelt als "rondklikken in informatie" in plaats van "ergens naartoe gaan"

## Gevolgen voor toekomstige features

Deze beslissing opent de deur voor:
- Adaptief leerpad (stappen overslaan op basis van bewezen kennis)
- Docent-dashboard met voortgang per leerling
- Herhaalmodules die zich aanpassen aan fouten

## Noot

Database-pad bug gevonden tegelijkertijd: `sqlite:///testgarden.db` wees naar de werkmap, niet naar `/instance/`. Dit verklaarde waarom voortgang soms leek te verdwijnen — de app draaide soms met een andere database dan verwacht.
