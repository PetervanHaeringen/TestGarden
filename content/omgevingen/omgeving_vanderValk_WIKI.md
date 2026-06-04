Aangemaakt door jvanoostenbrugge op 18-03-2024 09:25  
Bijgewerkt door lblauw op 11-07-2025 10:09
Bijgewerkt door Cynthia 
Omgezet door Peter van Haeringen

---

Info

**Contactpersoon**:	Danny Adamse, 

* **Jira**:	https://endeavour-nl.atlassian.net/jira/software/projects/VDV/boards/299
* **Google Chat (intern)**:	https://chat.google.com/room/AAAA5SOruBo
* **Google Chat (extern)**:	https://chat.google.com/room/AAAAkBdpjeI

## Omgevingen:



### Acceptatie

* **Manager omgeving**:	https://valk-manager-app.acceptance.kubernetes.pwstaging.tech/
* **Employee app**:	https://valk-employee-app.acceptance.kubernetes.pwstaging.tech/
* **Timer app**:	https://valk-timer.acceptance.kubernetes.pwstaging.tech/

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

## Logins:

### Sprint

| Rol | Email | WW | NR | PIN |
| --- | --- | --- | --- | --- |
| Vestigingsmanager | vesma@valkplanner.nl | test |  |  |
| Junior Manager | junma@valkplanner.nl | test |  |  |
| Employee 1 | employee1@valkplanner.nl | test |  |  |
|  | hoofdmanager@valkplanner.nl |  |  |  |

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

### Acceptatie

| Rol | Email | WW | NR | PIN |
| --- | --- | --- | --- | --- |
| Vestigingsmanager | vesma@valkplanner.nl | Akertest1! |  |  |
| Hoofd Manager | hoofdma@valkplanner.nl | 3CrsLGgCw!9Lw6kGXL6d | 12345 | 1234 |
| Manager 1 | manager1@valkplanner.nl | Timcreate1! | 1234 | 1234 |
| Junior Manager | junma@valkplanner.nl | Timcreate1! |  |  |
| PZ Valktest | pz@valkplanner.nl | Akertest1! |  |  |
| Employee 1 | employee1@valkplanner.nl | Akertest1! | 10001 | 1234 |
| Employee 2 | employee2@valkplanner.nl | Akertest1! | 20002 | 1234 |
| Employee 3 (loket gekoppeld) | employee3@valkplanner.nl | Akertest1! | 30003 | 1234 |
| Employee 4 (loket gekoppeld) | employee4@valkplanner.nl | Akertest1! | 40004 | 1234 |
| Employee 5 | employee5@valkplanner.nl | Akertest1! | 50005 | 1234 |


Danny U.: Op dit moment is dit lijstje medewerkers gekoppeld, maar we gaan er nog wat meer koppelen:

* Teun Walstra
* Paula Boots
* Jan de Bakker
* Piet van Braakman
* Test Testmaamt

## Reacties

### lblauw op 30-08-2024 11:56

mastercode: 1236987455

### lblauw op 13-01-2025 11:21

### **TvT-berekening:**

#### **Voorwaarden:**

1. **Medewerkers met een vast aantal contracturen**:
   * Komen standaard in aanmerking voor TvT.
2. **Medewerkers met een 0-urencontract**:
   * Komen alleen in aanmerking als dit expliciet is toegestaan (via een vinkje op de medewerkerskaart).

---

### **Basisformule voor de berekening:**

![](../assets/{CF5D6140-0DD5-4BBF-9DC9-6945AFB55027}.png){width=70%}



```latex
TvT-mutatie=(gewerkte uren+ziekte-uren+verlofuren+TvT-uren+wachturen)−contracturen\text{TvT-mutatie} = (\text{gewerkte uren} + \text{ziekte-uren} + \text{verlofuren} + \text{TvT-uren} + \text{wachturen}) - \text{contracturen}TvT-mutatie=(gewerkte uren+ziekte-uren+verlofuren+TvT-uren+wachturen)−contracturen
```

```
Toelichting op de componenten:
```

1. **Positieve bijdragen (bijtellingen)**:
   * Gewerkte uren (inclusief eventuele overuren).
   * Ziekte-uren (verzuim).
   * Verlofuren voor kinderen.
   * Bijzonder verlofuren.
   * Tijd voor tijd-uren.
   * Reguliere verlofuren.
   * Onbetaalde verlofuren.
   * Wachturen bij ziekte.
2. **Negatieve bijdrage (aftrekking)**:
   * Contracturen (uren die volgens het contract verplicht gewerkt moeten worden in de betreffende periode).

---

### **Voorbeeldberekening:**

#### Situatie:

* **Medewerker A** heeft een **32-urige werkweek** (128 contracturen per 4 weken).
* In een periode heeft medewerker A:
  * **99 gewerkte uren** (inclusief 3 extra uren).
  * **32 ziekte-uren**.

#### **Berekening:**

![](../../assets/{158A7221-C13A-431B-96FB-28C667A7EF6F}.png)

```latex-plain
TvT-mutatie=(99+32)−128=+3 uur\text{TvT-mutatie} = (99 + 32) - 128 = +3 \, \text{uur}TvT-mutatie=(99+32)−128=+3uur
```

---

### **Speciale gevallen:**

1. **Vrije dagen of ziekten**:
   * Deze worden opgeteld bij gewerkte uren, afhankelijk van het type afwezigheid (ziekte, verlof, etc.).
2. **Overruled 0-urencontract**:
   * Indien toegestaan, worden mutaties op dezelfde manier berekend als bij medewerkers met vaste contracturen.

**Bijlagen:**
- [{CF5D6140-0DD5-4BBF-9DC9-6945AFB55027}.png](../../assets/{CF5D6140-0DD5-4BBF-9DC9-6945AFB55027}.png)
- [{158A7221-C13A-431B-96FB-28C667A7EF6F}.png](../../assets/{158A7221-C13A-431B-96FB-28C667A7EF6F}.png)

# Verouderderde omgevingen

### Sprint

* **Manager omgeving**:	https://valk-manager-app-sprint-2024-19.cdemo.dev/				(Nummer in Sprint URLs wijzigt elke sprint)
* **Employee app**:	https://valk-employee-app-sprint-2024-19.cdemo.dev/
* **Timer app**:	https://valktimer-sprint-2024-19.cdemo.dev/~

## login

### Sprint

| Rol | Email | WW | NR | PIN |
| --- | --- | --- | --- | --- |
| Vestigingsmanager | vesma@valkplanner.nl | test |  |  |
| Junior Manager | junma@valkplanner.nl | test |  |  |
| Employee 1 | employee1@valkplanner.nl | test |  |  |
|  | hoofdmanager@valkplanner.nl |  |  |  |

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;