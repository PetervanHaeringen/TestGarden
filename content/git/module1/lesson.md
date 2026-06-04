# Module 1 — Oorsprong & filosofie

Git is vandaag de dag het meest gebruikte versiebeheersysteem ter wereld.
Maar het bestond niet altijd. En het is niet toevallig ontstaan — er zat een serieus probleem achter.

---

## 1. Het probleem: software maken met een team

Stel je voor: je werkt met tien mensen aan hetzelfde project.
Iedereen heeft dezelfde bestanden. Iedereen maakt wijzigingen.

Hoe weet je dan:
- wie wat heeft veranderd?
- wanneer een fout erin is geslopen?
- hoe je teruggaat naar gisteren?

Zonder versiebeheer is het antwoord: dat weet je niet.
Je stuurt bestanden via e-mail, overschrijft elkaars werk, verliest code.

Dat is precies wat er vroeger in softwareteams gebeurde.

---

## 2. Gecentraliseerd versiebeheer: de vorige generatie

Vóór Git bestonden er systemen zoals SVN en CVS.
Die werkten **gecentraliseerd**: één centrale server bewaarde alle geschiedenis.

Dat had nadelen:
- de server valt uit → iedereen staat stil
- je kunt niet werken zonder netwerkverbinding
- één fout op de server = alles weg

![Gecentraliseerd vs gedistribueerd versiebeheer](/instructions/content-images/git/module1/centralized_vs_distributed.svg)

---

## 3. Linus Torvalds en het conflict van 2005

Linus Torvalds is de maker van de Linux-kernel — het hart van veel besturingssystemen.
Duizenden ontwikkelaars werkten daaraan mee.

Ze gebruikten een commercieel systeem: **BitKeeper**.
Gratis voor open-source projecten — totdat de licentie in 2005 werd ingetrokken.

Linus had een keuze: overstappen op een bestaand systeem, of zelf iets bouwen.
Geen van de bestaande tools deed wat hij nodig had.

In **twee weken** schreef hij de basis van Git.

> "I'm an egotistical bastard, and I name all my projects after myself.
> First Linux, now Git."
> — Linus Torvalds

---

## 4. De filosofie van Git

Git is gebouwd op drie kernideeën:

**Gedistribueerd**
Iedereen heeft de volledige geschiedenis op de eigen computer.
Je kunt werken zonder internet. De server is niet heilig.

**Veilig**
Elke commit krijgt een unieke code (hash) die gebaseerd is op de inhoud.
Iets veranderen in de geschiedenis is direct merkbaar.

**Snel**
Git werkt lokaal. Bijna alles gebeurt op je eigen machine.
Geen wachttijd, geen afhankelijkheid van een server.

---

## 5. Git is niet GitHub

Dit is een veelgemaakte verwarring.

**Git** is het versiebeheersysteem — een programma dat je lokaal installeert.
**GitHub** is een website waar je Git-projecten kunt opslaan en delen.

Git is uitgevonden door Linus Torvalds.
GitHub is een bedrijf, opgericht in 2008, opgekocht door Microsoft in 2018.

Je kunt Git gebruiken zonder GitHub.
Maar GitHub zonder Git heeft geen zin.

---

## 6. Waarom is dit relevant voor jou als tester?

Als tester werk je met code, testscripts, bugrapporten en documentatie.
Al die bestanden veranderen in de tijd.

Git geeft je:
- een volledige geschiedenis van elk bestand
- inzicht in wie wat wanneer heeft gewijzigd
- de mogelijkheid om terug te gaan als iets fout gaat
- samenwerking zonder chaos

Je hoeft niet te programmeren om Git nuttig te vinden.
