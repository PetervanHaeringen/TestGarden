# Module 3 — Talen en abstractie

Als je Python schrijft, praat je niet echt met de computer.
Je praat met Python. Python praat met C. C praat met assembly. Assembly praat met de processor.

Elke laag verbergt de complexiteit van de laag eronder. Dat heet **abstractie** — en het is een van de krachtigste ideeën in de informatica.

---

## 1. De computer spreekt alleen nullen en enen

Op het diepste niveau begrijpt een computer maar één ding: stroom of geen stroom. Aan of uit. 1 of 0.

Alle code die je ooit schrijft wordt uiteindelijk omgezet in een lange reeks van 1s en 0s — **machinetaal**.

Een simpele optelling in machinetaal ziet er zo uit:
```
10110000 01100001
00000101 00000001
10100010 01100001
```

Dit is letterlijk wat de processor uitvoert. Mensen kunnen dit niet schrijven of lezen zonder fouten te maken. Dat is waarom de volgende laag is uitgevonden.

---

## 2. Assembly — namen voor instructies

In de jaren '50 bedachten programmeurs: waarom geven we de meest gebruikte instructies geen namen?

In plaats van `10110000 01100001` schrijf je:
```asm
MOV AL, 1
ADD AL, 1
MOV geheugen, AL
```

`MOV` betekent "verplaats een waarde". `ADD` betekent "tel op".
Dit zijn dezelfde instructies als de nullen en enen — maar leesbaar voor mensen.

Een **assembler** zet assembly-code om naar machinetaal.

Assembly was een enorme stap vooruit. Maar het bleef dicht bij de hardware — je moest nog steeds precies weten hoeveel geheugen je had, welke registers beschikbaar waren, hoe de processor in elkaar zat.

---

## 3. Hoge-niveautalen — schrijven voor mensen

In de jaren '50 en '60 ontstond een nieuwe gedachte: wat als je code schrijft die meer lijkt op menselijke taal?

**FORTRAN** (1957) — voor wetenschappelijke berekeningen:
```fortran
X = A + B * C
```

**COBOL** (1959) — voor zakelijke toepassingen:
```cobol
ADD SALARY TO TOTAL-WAGES
```

**C** (1972) — compact, krachtig, dicht bij de hardware maar leesbaar:
```c
int som = a + b;
```

**Python** (1991) — zo leesbaar dat het bijna Engels is:
```python
som = a + b
```

Elke generatie taal werd leesbaarder. En elke stap verborg meer complexiteit.

![Lagen van abstractie in programmeertalen](/instructions/content-images/developer/module3/lagen_abstractie.svg)

---

## 4. Compilers en interpreters — de vertalers

Hoe komt leesbare code bij de processor terecht?

Via een **compiler** of een **interpreter**.

**Compiler** — vertaalt de hele code in één keer naar machinetaal voordat het programma draait.
Voordeel: het programma is snel.
Nadeel: je moet opnieuw compileren bij elke wijziging.
Voorbeelden: C, C++, Rust.

**Interpreter** — vertaalt de code regel voor regel terwijl het programma draait.
Voordeel: je ziet meteen het resultaat van een wijziging.
Nadeel: iets langzamer.
Voorbeelden: Python, JavaScript, Ruby.

De meeste talen die je als developer tegenkomt zijn geïnterpreteerd — Python en JavaScript allebei. Dat is handig voor leren: je schrijft een regel, je ziet wat er gebeurt.

---

## 5. Waarom is abstractie zo krachtig?

Stel je voor dat je elke keer dat je een website bouwt, de volledige machinetaalcode moet schrijven voor het weergeven van tekst op een scherm. Je zou nooit verder komen dan "Hallo wereld".

Abstractie maakt het mogelijk om **te bouwen op wat anderen al hebben gebouwd**.

Python is geschreven in C.
C is geschreven in assembly.
Assembly is geschreven in machinetaal.
Machinetaal wordt uitgevoerd door transistors.
Transistors zijn ontworpen door elektrotechnici.

Jij hoeft niets van dat alles te weten om een programma te schrijven dat iets nuttigs doet. Je gebruikt de lagen die anderen hebben gebouwd.

Dat is ook de filosofie achter open source: code delen zodat de volgende persoon verder kan bouwen.

---

## 6. De prijs van abstractie

Maar abstractie heeft ook een prijs.

Hoe hoger de abstractielaag, hoe minder controle je hebt over wat er precies gebeurt.
Een C-programmeur kan exact bepalen hoeveel geheugen een programma gebruikt.
Een Python-programmeur delegeert dat aan Python.

Voor de meeste toepassingen maakt dat niets uit. Maar voor systemen waar elke milliseconde telt — besturingssystemen, spelengines, embedded hardware — kies je een lagere laag.

Als developer leer je te kiezen welke laag past bij jouw probleem.
