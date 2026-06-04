# TestGarden — Ontwikkelgeheugen

Gedestilleerd uit de chatgeschiedenis van de ontstaansperiode (nov 2025 – mei 2026).
Bronnen: 17 ChatGPT-chats + 2 DeepSeek-chats + 6 Claude-chats = 25 gesprekken.

Dit is geen documentatie van *wat* het systeem is.
Dit is het geheugen van *waarom het zo werd*.

---

## Structuur

```
decisions/      — Architectuurbeslissingen (ADR-formaat)
architecture/   — Hoe het systeem nu in elkaar zit
pedagogy/       — Pedagogische keuzes en leerfilosofie
patterns/       — Herkenbare patronen en anti-patronen
```

## Tijdlijn in één oogopslag

| Fase | Wat er gebeurde | AI |
|------|----------------|----|
| Start | Cursusopzet, eerste Flask-app, SQLite | ChatGPT |
| ADR-001 | Één centrale database (niet per gebruiker) | ChatGPT |
| ADR-002 | Migratie naar Blueprint-architectuur | ChatGPT |
| ADR-003 | Multi-AI curriculum: 5 systemen vergeleken | ChatGPT + 4 anderen |
| ADR-004 | Oefensites: drie-laags model | ChatGPT |
| ADR-005 | Tools als service-laag | ChatGPT |
| CSS themasysteem | Custom properties, vier thema's | DeepSeek ("Lao") |
| Externe review | Live site bekeken, 5 verbeterpunten gevonden | Claude |
| ADR-006 | Voortgang in database (Jesse's feedback) | ChatGPT |
| ADR-007 | YAML/MD content-architectuur | Claude |
| ADR-008 | Individuele leerlijnen (UserModule + visibility) | Claude |
| ADR-009 | Multi-tenant idee (geparkeerd) | Claude |
| ADR-010 | Streamlit import-tool | Claude |
| Nu | GitHub actief, Jesse test module 1-2 | — |

---

## Beslissingsindex

| ADR | Onderwerp | Status |
|-----|-----------|--------|
| 001 | Één centrale database | ✅ Geaccepteerd |
| 002 | Blueprint-architectuur | ✅ Geaccepteerd |
| 003 | Multi-AI curriculum | ✅ Geaccepteerd |
| 004 | Oefensites drie-laags model | ✅ Geaccepteerd |
| 005 | Tools als service-laag | ✅ Geaccepteerd |
| 006 | Voortgang in database | ✅ In implementatie |
| 007 | YAML/MD content-architectuur | ✅ In migratie |
| 008 | Individuele leerlijnen | ✅ In implementatie |
| 009 | Multi-tenant | ⏸ Geparkeerd (bewust) |
| 010 | Streamlit import-tool | ✅ Los prototype |

---

## Betrokken AI-systemen

| Systeem | Bijdrage |
|---------|---------|
| ChatGPT | Primaire bouwpartner vroege fase |
| DeepSeek ("Lao") | CSS themasysteem, GitHub credentials |
| Gemini / Grok / Mistral | Curriculum-input (samengevoegd in ADR-003) |
| Claude | Content-architectuur, leerlijnen, externe review |

---

*Peter cureert. AI-systemen organiseren en structureren. De pedagogische intentie is van Peter.*
