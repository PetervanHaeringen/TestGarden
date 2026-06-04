# TestGarden — Architectuuroverzicht (stand: mei 2026)

Gedestilleerd uit ChatGPT_8 en ChatGPT_17.

---

## Hosting

- **Platform:** PythonAnywhere
- **URL:** https://petervanhaeringen.pythonanywhere.com/
- **Repository:** https://github.com/GitAI47/TestGarden.git

---

## Stack

| Laag | Technologie |
|------|-------------|
| Web framework | Flask (Blueprint-architectuur) |
| Database | SQLite via Flask-SQLAlchemy |
| Templates | Jinja2 via base.html |
| Styling | Eigen style.css + thema-selector |
| Authenticatie | Werkzeug (password hashing) + Flask session |
| Deployment | PythonAnywhere (WSGI) |

**Dependencies (minimaal):**
```
Flask
Flask-SQLAlchemy
Werkzeug
python-dotenv
qrcode[pil]
```

---

## Blueprint-structuur

```
testgarden/
├── __init__.py          (create_app factory)
├── app.py               (entry point)
├── instance/
│   └── testgarden.db    (SQLite database — LET OP: niet in werkmap)
├── blueprints/
│   ├── core/            (index, dashboard)
│   ├── auth/            (login, logout, register)
│   ├── exercise/        (exercise1 t/m exercise4)
│   ├── instructions/    (leerpaden: Softwaretesten, Git, Selenium)
│   ├── feedback/        (feedbackformulier)
│   └── tools/           (Python-tools als webinterface)
├── static/
│   └── style.css
└── templates/
    └── base.html        (gedeeld door alle blueprints)
```

---

## Database-schema

```sql
users      (id, username, password_hash, role)
progress   (id, user_id, exercise_id, score, timestamp)
exercises  (id, title, description, category)
attempts   (id, user_id, question_id, correct, time)
```

---

## Navigatie

- Menu dynamisch gegenereerd via centrale registry + context processor
- `logged_in` bepaalt welke menu-items zichtbaar zijn
- Breadcrumbs aanwezig in leerpaden
- Thema-selector: Zen, Botanical, Modern, Forest
- Dark mode toggle

---

## Voortgang (in ontwikkeling)

- Voortgang wordt opgeslagen in de `progress`-tabel
- Definitie: voltooide leerstappen, niet paginanummers
- Jesse (leerling) testte als eerste en gaf feedback op dit onderdeel

---

## Leerpaden (status)

| Leerpad | Status |
|---------|--------|
| Softwaretesten | Actief — Jesse doorloopt module 1-2 |
| Git & GitHub (GitQuest) | Ontworpen, nog niet geïmplementeerd |
| Selenium / automatisering | Concept aanwezig |
| API-testen | Concept aanwezig |

---

## Oefenbedden

Vier exercise-blueprints aanwezig (exercise1 t/m exercise4).

Ontwerp: drie-laags model (zie ADR-004):
1. Foute website in iframe
2. Interactieve opdracht
3. Automatische check via solutions.json

Status: exercise1 actief, overige in voorbereiding.
