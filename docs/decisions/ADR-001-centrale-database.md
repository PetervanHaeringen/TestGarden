# ADR-001 — Één centrale database, niet per gebruiker

**Status:** Geaccepteerd  
**Datum:** vroeg in de ontwikkeling (nov 2025)  
**Auteurs:** Peter + ChatGPT  
**Bron:** ChatGPT_3 - Database per gebruiker vermijden

---

## Context

TestGarden houdt voortgang bij per leerling. De eerste impuls was: geef elke gebruiker een eigen `.db` bestand, zodat gegevens persoonlijk en beheersbaar zijn. Gebruikers zouden hun eigen db kunnen meenemen als archief.

## Probleem

Hoe slaan we gebruikersdata op in een leerplatform met meerdere leerlingen?

## Beslissing

**Één centrale SQLite database** met een genormaliseerde tabelstructuur.

Tabelstructuur vastgesteld:
- `users` — id, username, password_hash, role
- `progress` — id, user_id, exercise_id, score, timestamp
- `exercises` — id, title, description, category
- `attempts` — id, user_id, question_id, correct, time

## Motivatie

Per-gebruiker databases werden expliciet besproken en verworpen om de volgende redenen:

- **Complexiteit explodeert**: tientallen losse bestanden, per gebruiker een verbinding, backups worden complex
- **Rapportages onmogelijk**: "wie heeft module X nog niet gedaan?" vereist alle databases tegelijk openen
- **Groter risico op dataverlies**: één beschadigde user-db = alles kwijt voor die gebruiker
- **Migraties worden een nachtmerrie**: schema-updates moeten op honderden bestanden worden toegepast

## Afgewezen alternatieven

- **Database per gebruiker**: technisch mogelijk, maar operationeel onhoudbaar bij groei
- **Platte bestanden (JSON/CSV) per leerling**: zelfde problemen als per-db, plus geen transacties

## Gevolgen

- Alle queries lopen via één verbinding — simpel en snel
- Rapportage op klas/groep niveau is triviaal met SQL GROUP BY
- Later migreren naar PostgreSQL of MySQL is mogelijk zonder modelwijziging
- Beveiliging en toegangscontrole gebeurt op applicatieniveau (niet bestandsniveau)

## Noot voor de toekomst

Er zijn niche-situaties waarin losse databases zinvol zijn (extreme privacy, portable archief). Die gelden niet voor TestGarden als leerplatform. Als de schaal ooit heel groot wordt, is migratie naar PostgreSQL de logische volgende stap — niet opsplitsing per gebruiker.
