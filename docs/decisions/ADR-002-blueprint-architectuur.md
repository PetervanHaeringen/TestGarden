# ADR-002 — Migratie naar Blueprint-architectuur ("de tuin")

**Status:** Geaccepteerd  
**Datum:** nov 2025  
**Auteurs:** Peter + ChatGPT  
**Bron:** ChatGPT_6 - Tuinaanleg met blueprint, ChatGPT_8 - Samenvatting

---

## Context

TestGarden begon als een monolithische Flask-app met één `app.py` bestand. Naarmate functionaliteit groeide — login, oefeningen, instructies, feedback — werd het bestand onbeheerbaar groot. De code werd moeilijk te navigeren en nieuwe functies introduceerden risico op regressie in bestaande delen.

## Probleem

Hoe structureer je een groeiende Flask-app zodat nieuwe "tuinbedden" (functionaliteitsgebieden) onafhankelijk kunnen worden toegevoegd zonder de rest te verstoren?

## Beslissing

**Flask Blueprints** als organiserend principe, met de metafoor van een tuin met aparte bedden.

Vastgestelde indeling (gebaseerd op scan van alle 9 routes in de originele app.py):

```
blueprints/
├── core/       — hoofdpagina's, layout, menu's
├── auth/       — login, logout, register (eerder: users/)
├── exercise/   — oefenbedden (exercise1, exercise2, ...)
├── instructions/ — leerpaden (Softwaretesten, Git, Selenium)
├── feedback/   — feedbackformulier en opslag
└── tools/      — Python-tools als webinterface
```

Templates per blueprint: eerst overwogen om templates centraal te houden, maar uiteindelijk gekozen voor **templates per blueprint** voor betere isolatie.

## Motivatie

- Nieuwe functionaliteit toevoegen = nieuw blueprint aanmaken, bestaande code onaangeroerd
- Teams (of leerlingen) kunnen aan verschillende blueprints werken zonder conflicten
- Testbaarheid per blueprint
- De tuinmetafoor werkt pedagogisch: elk bed heeft een eigen verantwoordelijkheid

## Proces van de migratie

De migratie werd stap voor stap gedaan (niet in één keer):
1. Alle routes gescand en geclusterd
2. `create_app()` factory patroon geïntroduceerd
3. Blueprints één voor één aangemaakt en gevuld
4. Routes pas verwijderd uit app.py nadat de blueprint werkte

## Afgewezen alternatieven

- **Monoliet laten groeien**: expliciet afgewezen omdat nieuwe features onvoorspelbare neveneffecten hadden
- **Microservices**: te zwaar voor de huidige schaal en het leerdoel

## Bekende valkuilen (geleerd tijdens de migratie)

- **Endpoint-naamgeving verandert**: `url_for('login')` wordt `url_for('auth.login')` — templates en andere routes moeten allemaal worden bijgewerkt
- **Template-locatie is een beslissing**: consistent kiezen voor templates-per-blueprint OF centrale templates-map, niet beide
- **`current_user` in Jinja2**: vereist expliciete context injection of Flask-Login

## Gevolgen

- Schaalbaar: nieuwe leerpaden en oefenbedden toevoegen is een gestandaardiseerde operatie
- Menu's worden dynamisch gegenereerd via een centrale registry
- Thema-selector en dark-mode werken via base.html die door alle blueprints wordt gebruikt
