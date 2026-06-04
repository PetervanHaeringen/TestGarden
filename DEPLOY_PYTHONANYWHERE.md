# TestGarden – PythonAnywhere Deploy Stappenplan

---

## 1. Zip uploaden

Maak lokaal een zip van de nieuwe versie en upload deze naar de home directory van PythonAnywhere via de **Files** tab.

Voorbeeld bestandsnaam: `Testgarden_v11.zip`

---

## 2. Oude map verwijderen (optioneel)

> ⚠️ Alleen verwijderen als je zeker weet dat de nieuwe zip goed is.

```bash
rm -rf ~/Testgarden_v11
```

---

## 3. Zip uitpakken

```bash
cd ~
unzip Testgarden_v11.zip -d Testgarden_v11
```

---

## 4. Naar projectmap gaan

```bash
cd ~/Testgarden_v11
```

---

## 5. Virtualenv activeren

```bash
workon testgarden-venv
```

Controleer of je de juiste Python gebruikt:

```bash
which python
```

---

## 6. Dependencies installeren

```bash
pip install -r requirements.txt
```

---

## 7. Database initialiseren

```bash
python init_db.py
```

Of via Flask CLI:

```bash
flask --app app init-db
```

---

## 8. Web tab controleren

Ga naar **PythonAnywhere → Web** en controleer:

| Instelling | Waarde |
|---|---|
| Source code | `/home/PetervanHaeringen/Testgarden_v11` |
| Working directory | `/home/PetervanHaeringen/Testgarden_v11` |
| Virtualenv | pad naar `testgarden-venv` |

---

## 9. WSGI bestand controleren

Het WSGI bestand moet verwijzen naar de juiste map en app:

```python
path = '/home/PetervanHaeringen/Testgarden_v11'
```

```python
from app import app as application
```

---

## 10. Reload webapp

Klik op **Reload** in de Web tab.

---

## 11. Fouten controleren

Bij problemen: **PythonAnywhere → Web → Error log**

Veel voorkomende oorzaken:

| Fout | Oplossing |
|---|---|
| `markdown` ontbreekt | `pip install markdown` |
| `yaml` ontbreekt | `pip install pyyaml` |
| `flask` ontbreekt | `pip install flask` |

---

## 12. Eerste gebruiker registreren

Ga naar de website en gebruik **Register** om een account aan te maken.

---

## 13. Admin rol geven

```bash
cd ~/Testgarden_v11
workon testgarden-venv
python
```

```python
from app import create_app
from database.models import db, User

app = create_app()

with app.app_context():
    u = User.query.filter_by(username="JOUWNAAM").first()
    u.role = "admin"
    db.session.commit()
    print(u.username, u.role)
```

---

## 14. Testen

Controleer na de deploy:

- [ ] Login
- [ ] Dashboard
- [ ] Content modules
- [ ] Teacher menu
- [ ] Module toewijzing
- [ ] Database opslag
- [ ] Markdown rendering
- [ ] YAML vragen

---

## 15. Backup maken

Na een succesvolle deploy:

- [ ] Zip bewaren als versie-archief
- [ ] Database backup maken:

```bash
cp instance/testgarden.db instance/testgarden_backup.db
```

---

*Dit soort bestanden worden goud waard na verloop van tijd.  
Je bouwt daarmee niet alleen software, maar ook het geheugen van het project.*



## 16. Deploy van nieuwe inhoud

Nieuwe deploy checklist
- [ ] core/track_loader.py
- [ ] tracks/*.yaml
- [ ] teacher/routes.py
- [ ] teacher/templates/*
- [ ] users/routes.py
- [ ] users/templates/*
- [ ] core/menu.py
- [ ] reload webapp

Dat gaat later goud waard zijn.