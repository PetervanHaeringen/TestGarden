# Module 7 – API Testing

In deze module leer je de basis van API Testing.

Veel software bestaat uit onderdelen die via API’s met elkaar communiceren.

Als tester kun je deze API’s direct controleren met tools zoals Postman.
Dat maakt testen:
- sneller
- preciezer
- krachtiger

---

## 1. Wat is een API?

API betekent:

> **Application Programming Interface**

Een API is een manier waarop softwareonderdelen met elkaar communiceren.

Wanneer je een API test, controleer je bijvoorbeeld:

- wat gebeurt bij GET-verzoeken
- wat gebeurt bij POST/PUT-verzoeken
- welke foutmeldingen terugkomen
- of de JSON-structuur klopt
- hoe snel de server reageert

### Voorbeeld

Een webshop-app vraagt:

> “Geef alle producten uit categorie boeken.”

De server stuurt vervolgens JSON-data terug.

---

## 2. HTTP Statuscodes

Elke API-response bevat een statuscode.

Die vertelt of de aanvraag succesvol was.

### Veelgebruikte statuscodes

- **200** — OK
- **201** — Created
- **400** — Bad Request
- **401** — Unauthorized
- **404** — Not Found
- **500** — Server Error

> Een 500-statuscode wijst meestal op een fout in de backend.

---

## 3. JSON: de taal van API’s

Veel API’s communiceren met JSON.

JSON is gestructureerde tekstdata.

### Voorbeeld

```json
{
  "id": 42,
  "name": "Testproduct",
  "price": 9.99
}
```

### Tijdens API-testing controleer je:

- staan alle velden erin?
- kloppen de waardes?
- ontbreekt er data?
- zit er onverwachte data in?

---

## 4. API’s testen met Postman

Postman is een populaire tool voor API-testing.

Je kunt ermee testen:

- of endpoints bestaan
- hoe een API reageert op fouten
- response times
- JSON-structuren

### Basisaanvraag

1. Open Postman
2. Kies methode: GET
3. Vul URL in:
   `https://example.com/api/products`
4. Klik op Send
5. Bekijk:
   - statuscode
   - headers
   - body

---

## 5. Basis API-checklist

Gebruik deze checklist tijdens API-testing.

- [ ] Endpoint bestaat (geen 404)
- [ ] Correcte reactie op geldige input
- [ ] Correcte reactie op foutieve input
- [ ] JSON-structuur klopt
- [ ] Waardes zijn logisch
- [ ] Response time acceptabel

---

## 6. Praktijkopdracht: 6 API-checks

Je gaat nu zelf zes API-tests uitvoeren.

### Opdracht

1. Kies een openbare API of demo-API.
2. Voer drie positieve tests uit.
3. Voer drie negatieve tests uit.
4. Noteer:
   - statuscode
   - response time
   - response body
5. Beschrijf afwijkingen of bugs.

> Foutcodes zijn niet altijd fouten.  
> Vaak laten ze juist zien dat de API netjes reageert.

---

## 7. Reflectie

Denk terug aan jouw tests:

- Welke statuscodes zag je het meest?
- Was de API voorspelbaar?
- Welke negatieve test gaf interessante resultaten?
- Waar zou een beveiligingsrisico kunnen zitten?