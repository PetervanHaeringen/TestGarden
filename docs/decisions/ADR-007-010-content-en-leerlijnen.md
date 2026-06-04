# ADR-007 — YAML/Markdown content-architectuur (ontkoppeld van routes)

**Status:** Geaccepteerd — in migratie  
**Datum:** begin 2026  
**Auteurs:** Peter + ChatGPT, daarna verder uitgewerkt met Claude  
**Bron:** Claude_02 - TestGarden content structuur migratie

---

## Context

De lesinhoud van TestGarden zat aanvankelijk opgesloten in hardcoded Flask-routes en HTML-templates. Elke nieuwe module vereiste:
1. Een nieuwe route aanmaken in routes.py
2. Een nieuwe HTML-template bouwen
3. Eventuele vragen in een Python-bestand toevoegen (question_bank_testen.py)

Dit werkte voor de eerste fase maar schaalde niet. Negen afzonderlijke routes voor negen modules van één leerpad.

## Probleem

Hoe maak je lesinhoud beheerbaar, overdraagbaar, en onafhankelijk van de Flask-code — zodat een docent of vakinhoudelijk expert inhoud kan aanpassen zonder Flask te hoeven kennen?

## Beslissing

Drie-bestandenstructuur per module, opgeslagen als open formaten:

```
content/<track>/<module_slug>/
  meta.yaml       — configuratie (id, titel, volgorde, tags, leerdoelen, ...)
  lesson.md       — lesinhoud in Markdown
  questions.yaml  — vragen (mcq, truefalse, open)
  images/         — afbeeldingen
```

Centrale `content_loader` in Flask met twee functies:
- `load_lesson(track, module)` — leest de drie bestanden
- `load_track_modules(track)` — ontdekt automatisch welke modules bestaan door de map door te lopen

Twee dynamische routes vervangen de negen hardcoded:
- `/testen/content/<module_name>`
- `/testen/content/overview`

## Motivatie

- Drie verschillende verantwoordelijkheden, drie verschillende redenen om iets aan te passen — logisch gescheiden
- Docent/vakinhoudelijk expert kan MD en YAML bewerken zonder Flask te kennen
- Nieuwe module toevoegen = map aanmaken + drie bestanden erin + klaar
- Content is versiebeheerbaar in Git los van de applicatiecode

## Technische aandachtspunten (geleerd tijdens uitwerking)

**MCQ antwoorden als index is fragiel:**
```yaml
answer: 1  # index 0-based of 1-based? onduidelijk
```
Beter:
```yaml
answer: "Onderzoeken of software werkt zoals verwacht"  # expliciet, veilig bij herordening
```

**Open vragen hebben nog geen beoordelingscriterium.** Reserveer een veld voor later:
```yaml
# toekomstig: keywords of sample_answer voor automatische of geassisteerde nakijk
```

**module_slug en id zijn twee identifiers voor hetzelfde object** — bewaken dat ze niet uiteen lopen naarmate er meer modules komen.

## Huidige status

De migratie loopt parallel: het oude systeem (hardcoded routes) staat nog naast het nieuwe. Bewuste keuze: pas omschakelen als alles werkt. De oude structuur wordt niet eerder verwijderd.

## Gevolgen

- TestGarden kan straks meerdere tracks en inhoudsgebieden ondersteunen zonder codeveranderingen
- Content kan worden gegenereerd via de Streamlit import-tool (zie ADR-010)
- Docenten zonder programmeerkennis kunnen modules onderhouden

---

---

# ADR-008 — Individuele leerlijnen: UserModule + module_visibility

**Status:** Geaccepteerd — in implementatie  
**Datum:** mei 2026  
**Auteurs:** Peter + Claude  
**Bron:** Claude_06 - Individuele leerlijnen in testgarden

---

## Context

ICT vanaf Morgen heeft drie soorten cursisten:
- Cursisten met een vast traject (langdurig, heel pad relevant)
- Cursisten die een paar dagen komen (korte stage, alleen toegewezen modules)
- Cursisten met een individueel maatwerk-traject

De bestaande dashboard-route was hardcoded: iedereen zag dezelfde modules.

## Beslissing

**UserModule koppeltabel** en **module_visibility veld** op User.

```
UserModule
├── user_id
├── module_slug        (bv. "softwaretesten.m01")
├── assigned_by        (user_id van admin/teacher)
├── assigned_at
└── volgorde           (eigen volgorde per cursist)

User (uitbreiden)
└── module_visibility  ("alleen_toegewezen" | "vergrendeld" | "alles")
```

**Drie zichtbaarheidsmodi:**

| Profiel | module_visibility | Ziet |
|---------|-------------------|------|
| Korte bezoeker | `alleen_toegewezen` | Alleen toegewezen modules |
| Maatwerk-individu | `vergrendeld` | Toegewezen + overige als grijs/vergrendeld |
| Vast traject | `alles` | Alles open |

## Motivatie

- Diversiteit is de regel bij ICT vanaf Morgen, niet de uitzondering
- Een cursist die een paar dagen komt heeft er niets aan het hele landschap te zien
- Voor langdurige cursisten kan het juist uitdagend zijn het hele traject te overzien
- De instelling wordt bepaald door admin/docent, niet door de cursist zelf

## Afgewezen alternatieven

- **Aparte "leerlijn"-entiteit**: te veel abstractie voor nu
- **Volgorde-afdwinging**: bewust niet — cursisten mogen vrij bewegen binnen het toegewezen pad

## Noot

Dit model is ook compatibel met de multi-tenant gedachte (ADR-009): per organisatie kunnen andere defaults worden ingesteld voor module_visibility.

---

---

# ADR-009 — Multi-tenant architectuur (geparkeerd, niet vergeten)

**Status:** Bewust uitgesteld  
**Datum:** mei 2026  
**Auteurs:** Peter + Claude  
**Bron:** Claude_08 - Opzet van de testgarden

---

## Context

Peter stelde de vraag: stel dat TestGarden niet alleen voor ICT vanaf Morgen wordt gebruikt, maar ook voor zijn vroegere school (natuur/scheikunde op het vmbo) of andere organisaties — hoe zou dat architectureel werken?

## Idee

Database per organisatie (tenant), gekozen na login:

```
login → organisatie bepaald → juiste SQLite geladen → sessie gebonden aan die db

databases/
  ivm.db
  vmbo_natuur.db

content/
  ivm/           (modules voor ICT vanaf Morgen)
  vmbo_natuur/   (modules voor de andere school)
```

Gedeeld: Flask-app, templates, logica.
Gescheiden per tenant: SQLite (voortgang, gebruikers) + content/

## Beslissing

**Nu niet implementeren.** Het idee rijpt. De code hoeft nu nog niet te bewegen.

**Wél nu doen:** centraliseer de database-verbinding op één plek. Geen hardcoded paden verspreid door de code. Eén configuratie-punt. Dan is de stap naar multi-tenant later klein.

## Voorwaarde voor implementatie later

- Databaseverbinding al gecentraliseerd (via config of factory)
- Geen hardcoded `sqlite:///testgarden.db` verspreid door de code

## Waarde

Het pedagogische model van TestGarden — modules, voortgang, vragen — werkt voor elke vakinhoud. De architectuur kan dit ondersteunen zonder fundamentele herstructurering.

---

---

# ADR-010 — Streamlit import-tool (apart prototype)

**Status:** Geaccepteerd als los prototype  
**Datum:** begin 2026  
**Auteurs:** Peter + Claude  
**Bron:** Claude_04 - TestGarden content importtool prototype

---

## Context

Nieuwe modules aanmaken via handmatig schrijven van YAML en MD is tijdrovend. Er is behoefte aan een tool die bestaand materiaal (Word, PDF, TXT) kan omzetten naar een draft-module in de TestGarden content-structuur.

## Beslissing

**Apart Streamlit-prototype**, niet geïntegreerd in de Flask-app.

Werkwijze:
1. Gebruiker uploadt Word/PDF/TXT
2. Tool extraheer tekst en herkent koppen
3. Tool genereert concept meta.yaml, lesson.md en questions.yaml
4. Gebruiker bewerkt in de editor-interface
5. Na goedkeuring: export naar mapstructuur

**Cruciale beperking:** de tool bepaalt geen definitieve module-IDs of volgorde-nummers. Die worden centraal door TestGarden toegekend.

Tijdelijke placeholders in export:
```yaml
id: pending
slug: pending
order: pending
```

## Motivatie

- Bestaand materiaal (lesplannen, Word-documenten) hergebruiken
- Mens blijft in de loop: AI genereert draft, mens cureert
- Streamlit voor snelle lokale UI zonder Flask-complexiteit
- De import-tool en de TestGarden-app zijn bewust gescheiden — verschillende lifecycle, andere gebruikers

## Aandachtspunten

- PDF: alleen tekstextractie (v1), geen afbeeldingen, geen tabellen
- Word: koppen worden herkend via opmaakstijlen (Heading 1/2/3)
- Open vragen worden automatisch herkend maar vereisen menselijke controle
- MCQ-vragen genereren is experimenteel — altijd nakijken

## Toekomstige uitbreiding

De tool kan later AI-assistentie krijgen voor vraaggeneratie. Nu: extraheer, niet genereer. Dat onderscheid is bewust.
