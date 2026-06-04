# TestGarden — Patronen en anti-patronen

Herkenbare patronen uit de chatgeschiedenis — dingen die keer op keer terugkwamen, goed of slecht.

---

## Patronen die werkten

### P-01: Stap voor stap migreren

Bij de overgang van monoliet naar blueprints werd niet alles in één keer omgezet. Eerst scannen, dan clusteren, dan één blueprint tegelijk activeren, dan pas de oude code verwijderen.

**Toepasbaar wanneer:** grote structuurwijzigingen aan een werkend systeem.

---

### P-02: Templates consistent plaatsen

Keuze: templates per blueprint óf centrale templates-map. Niet beide.

In de chatgeschiedenis ontstond verwarring toen dit wisselde midden in de samenwerking (AI gebruikte een andere bron en volgde een andere conventie). Peter wees dit terecht aan.

**Leer:** AI-assistenten kunnen van bron wisselen en daarmee van conventie. De mens moet de consistentie bewaken.

---

### P-03: Menu als registry, niet als hard-coded HTML

Menu's worden gegenereerd vanuit een centrale lijst met endpoints. Dit maakt toevoegen van nieuwe blueprints eenvoudig zonder base.html aan te raken.

```python
TOOLS = [
    {"name": "CSV Validator", "endpoint": "tools.csv_validator"},
]
```

---

### P-04: Context processor voor globale variabelen

`logged_in`, menu's, thema — via `@app.context_processor` beschikbaar in alle templates zonder dat elke route ze explicief mee hoeft te geven.

---

### P-05: Multi-AI voor inhoudsontwikkeling

Vijf AI-systemen gevraagd hetzelfde probleem op te lossen, resultaten vergeleken, beste elementen gecombineerd. Peter als curator.

**Opbrengst:** rijker dan één systeem alleen, maar vereist menselijk oordeel over welke elementen pedagogisch kloppen.

---

## Anti-patronen (dingen die mis gingen)

### A-01: Database-pad verwarring

`sqlite:///testgarden.db` wijst naar de *werkmap* van het proces, niet naar `/instance/`. Dit veroorzaakte een subtiele bug: de app draaide soms met een lege database terwijl de gevulde in `/instance/` stond.

**Symptoom:** voortgang verdween, logout verscheen niet, registraties leken te verdwijnen.

**Fix:** altijd het volledige pad of `app.instance_path` gebruiken.

---

### A-02: Endpoint-naamgeving na blueprint-migratie

Na de migratie zijn alle endpoints van naam veranderd (`login` → `auth.login`). Templates en `url_for()`-aanroepen in de hele app moesten worden bijgewerkt.

**Symptoom:** `BuildError: Could not build url for endpoint 'login'. Did you mean 'auth.login' instead?`

**Les:** bij een blueprint-migratie systematisch zoeken naar alle `url_for()` aanroepen.

---

### A-03: Voortgang alleen in sessie opslaan

Sessies zijn vluchtig. Voortgang die alleen in `session["progress"]` wordt opgeslagen verdwijnt bij een nieuwe sessie, andere browser, of serverherstart.

**Fix:** voortgang altijd in de database opslaan (progress-tabel).

---

### A-04: Library-afhankelijkheid onderschatten

Peter constateerde zelf: "dit vind ik het kwetsbare van dit paketten/library systeem — de onderliggende bibliotheek is niet in je beheer."

**Patroon:** bij elke nieuwe library afvragen: hoe actief is het onderhoud? Wat is de fallback als dit pakket stopt?

**Actueel voorbeeld:** Selenium vs Playwright — Playwright is moderner, beter onderhouden. Selenium is bekender en didactisch goed inzetbaar als startpunt, maar voor productie heeft Playwright de voorkeur.

---

### A-05: AI wisselt van architectuurconventie zonder waarschuwing

Tijdens de samenwerking volgde de AI soms een andere bron dan de eerder gekozen aanpak. Dit veroorzaakte inconsistentie in de directory-structuur.

**Les voor toekomstige nieuwe developers:** vraag altijd de huidige projectstructuur op (via TREE.md of GitHub) *voordat* je AI om code vraagt. Anders genereert de AI code die past bij de conventies uit zijn trainingsdata, niet bij jullie project.

---

## Patroon dat nog onderzocht wordt

### O-01: GitQuest — team-based Git training

Concept: leden van een team krijgen elk een "puzzelstukje" van een codebase. Samen moeten ze via branches, commits en pull requests het geheel samenvoegen.

Status: ontworpen, nog niet geïmplementeerd. Wacht op stabiele voortgangsinfrastructuur.

Potentieel: direct inzetbaar als les bij ICT vanaf Morgen, teams van 3-6 deelnemers.
