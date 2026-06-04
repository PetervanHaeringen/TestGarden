# Aanvulling patronen — Claude & DeepSeek chats

---

## Patronen die werkten (aanvulling)

### P-06: CSS custom properties voor thema's (ontworpen door DeepSeek/Lao)

Het themasysteem gebruikt CSS custom properties op `:root` en per `html[data-theme="..."]`. Hierdoor kunnen thema's wisselen zonder JavaScript dat CSS klassen toevoegt — alleen het `data-theme` attribuut op `<html>` hoeft te veranderen.

**Thema's:** Garden Light (default), Sand, Modern, Garden Night.

Attribuut in de CSS: *"Stylesheet ontworpen door Lao | Themasysteem door ChatGPT"* — dit is het meest expliciete voorbeeld van multi-AI attributie in het project.

**Architectuurles:** theming via CSS custom properties is makkelijk uitbreidbaar. Een nieuw thema toevoegen = één nieuw blok in de stylesheet, geen code.

---

### P-07: Pending IDs als bewuste tijdelijke staat

Bij de import-tool (ADR-010) worden geen definitieve IDs gegenereerd. Alles wat centraal bepaald wordt, krijgt een expliciete placeholder:

```yaml
id: pending
slug: pending
order: pending
```

Dit voorkomt dat de tool beslissingen neemt die aan het centrale systeem toebehoren. Het patroon: **maak het tijdelijke zichtbaar en expliciet, niet impliciet leeg.**

---

### P-08: Externe review als kwaliteitscontrole

Claude bekeek de live site als externe reviewer (Claude_01) en vond zaken die van binnenuit niet meer zichtbaar waren:

- Debug-informatie publiek zichtbaar
- SECRET_KEY hardcoded in app.py terwijl config.py al bestond maar niet gebruikt werd
- Hardcoded statussen terwijl `compute_step_status()` al bestond maar niet aangeroepen werd
- Bestandsnamen met spaties (problematisch op Linux)
- Backup-bestanden als losse bestanden naast de echte

**Patroon:** periodieke externe review (door mens of AI met frisse context) vangt wat gewenning verbergt.

---

### P-09: Drie cursor-posities in de code

Geleerd uit Claude_01: er kunnen drie soorten "dode punten" zijn in een codebase:

1. **Code die bestaat maar niet aangeroepen wordt** — `compute_step_status()` bestond, werd nergens gebruikt
2. **Config die bestaat maar genegeerd wordt** — `config.py` had de juiste SECRET_KEY logica, maar `app.py` gebruikte een hardcoded string
3. **Functies die werken maar verkeerd geconfigureerd zijn** — databasepad wees naar verkeerde locatie

Al drie zijn subtiel en raken niet de compilatie. Ze komen boven bij tests of reviews.

---

## Anti-patronen (aanvulling)

### A-06: Meerdere GitHub-accounts op één computer

Bij de eerste push naar GitHub werden credentials van het verkeerde account gebruikt. Dit is een klassieker bij meerdere accounts op één machine.

**Oplossing gekozen:** username embedden in de remote URL:
```bash
git remote set-url origin https://PetervanHaeringen@github.com/PetervanHaeringen/TestGarden.git
```

**Structurele oplossing voor later:** SSH keys per account, configuratie via `~/.ssh/config`.

---

### A-07: .gitignore met underscore in plaats van punt

Het bestand heette `_gitignore` in plaats van `.gitignore`. Git herkent het dan niet — `__pycache__/` werd dus niet genegeerd hoewel het in het bestand stond.

**Symptoom:** `__pycache__` mapjes verschijnen in git status ondanks dat ze in het "gitignore" staan.

---

### A-08: Systemen naast elkaar bouwen bij migraties

Bij de overgang van hardcoded routes naar YAML/MD content werd bewust gekozen het oude systeem intact te laten totdat het nieuwe volledig werkt.

**Dit is goed** — maar het vraagt discipline om het ook echt op te ruimen als de migratie klaar is. Twee parallelle systemen worden anders permanent.

**Signaal dat het tijd is:** als de oude routes al maanden geen verkeer meer ontvangen en de nieuwe content_loader stabiel is.

---

## Teams/SharePoint notitie (voor ICT vanaf Morgen context)

Uit Claude_03: de behoefte aan cursist-overzicht bij ICT vanaf Morgen is reëel en urgent. Teams/SharePoint is structureel gebouwd rond groepen, niet individuele trajecten.

**Tijdelijke aanbeveling:** Microsoft Lists als centrale cursistenlijst (laagste drempel, werkt binnen bestaande M365-omgeving).

**Strategische richting:** TestGarden zelf als cursist-dashboard — de architectuur is er klaar voor (UserModule, module_visibility), de data leeft er al.

**De spanning die benoemd werd:** organisaties bouwen meerdere systemen naast elkaar. Elk systeem heeft zijn eigen overzicht. Overzicht zelf verdwijnt. Dit is een organisatorisch patroon, geen technisch probleem — en dus ook geen technische oplossing.
