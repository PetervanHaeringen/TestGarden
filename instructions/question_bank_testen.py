# instructions/question_bank_testen.py

TESTEN_QUESTION_BANK = {
    "testen_m1": {
        "title": "Module 1 — Wat is testen?",
        "questions": [
            {
                "id": "st_m1_q1_doel_testen",
                "type": "mcq",
                "prompt": "Wat is het primaire doel van softwaretesten?",
                "options": [
                    "Bewijzen dat software foutloos is",
                    "Fouten vinden en risico’s verkleinen",
                    "De klant tevreden houden",
                    "Ontwikkelaars werk geven",
                ],
                "answer": 1,
                "explanation": "Testen helpt defects vinden en risico’s verkleinen; het bewijst nooit foutloosheid."
            },
            {
                "id": "st_m1_q2_testcase",
                "type": "truefalse",
                "prompt": "Een testgeval beschrijft invoer, stappen en een verwachte uitkomst.",
                "answer": True,
                "explanation": "Klopt: een testcase bevat stappen + expected result."
            },
            {
                "id": "st_m1_q3_functioneel_voorbeeld",
                "type": "short",
                "prompt": "Noem 1 voorbeeld van een functionele test (1 zin is genoeg).",
                "rubric_keywords": ["inloggen", "betaling", "zoek", "registr", "wachtwoord", "winkelmand"],
                "min_keywords": 1,
                "explanation": "Voorbeeld: 'Inloggen met geldig wachtwoord werkt en toont dashboard'."
            },
        ]
    },


    "testen_m2": {
        "title": "Module 2 — Testsoorten",
        "questions": [
            {
                "id": "st_m2_q1_unit",
                "type": "mcq",
                "prompt": "Wat test je bij een unit test?",
                "options": [
                    "Het hele systeem",
                    "Een klein stuk code (bijv. een functie)",
                    "De database connectie",
                    "De gebruikersinterface",
                ],
                "answer": 1,
                "explanation": "Een unit test test één klein onderdeel van de code, meestal een functie of methode."
            },
            {
                "id": "st_m2_q2_integratie",
                "type": "truefalse",
                "prompt": "Een integratietest controleert of verschillende onderdelen goed samenwerken.",
                "answer": True,
                "explanation": "Integratietesten richten zich op de samenwerking tussen componenten."
            },
            {
                "id": "st_m2_q3_systeemtest",
                "type": "short",
                "prompt": "Noem één voorbeeld van een systeemtest.",
                "rubric_keywords": ["e2e", "end-to-end", "volledige", "complete", "gehele applicatie"],
                "min_keywords": 1,
                "explanation": "Een systeemtest controleert het volledige systeem als geheel."
            },
        ]
    },


    "testen_m3": {
    "title": "Module 3 — Testplan en risico",
    "questions": [
        {
            "id": "st_m3_q1_testplan_doel",
            "type": "mcq",
            "prompt": "Wat is een belangrijk doel van een testplan?",
            "options": [
                "Alle bugs vooraf oplossen",
                "Vastleggen wat, hoe en wanneer er getest wordt",
                "De software automatisch verbeteren",
                "Ontwikkelaars vervangen"
            ],
            "answer": 1,
            "explanation": "Een testplan beschrijft de aanpak: wat je test, hoe je dat doet, wanneer en met welke prioriteiten."
        },
        {
            "id": "st_m3_q2_risico_truefalse",
            "type": "truefalse",
            "prompt": "Risicogericht testen betekent dat je meer aandacht geeft aan onderdelen waar fouten de meeste impact hebben.",
            "answer": True,
            "explanation": "Ja. Bij risicogericht testen geef je prioriteit aan onderdelen met hoge kans op fouten of grote impact."
        },
        {
            "id": "st_m3_q3_risico_voorbeeld",
            "type": "short",
            "prompt": "Noem één voorbeeld van een onderdeel met hoog risico in een applicatie.",
            "rubric_keywords": ["betaling", "inloggen", "beveilig", "privacy", "database", "registratie", "account"],
            "min_keywords": 1,
            "explanation": "Voorbeelden zijn inloggen, betalingen, privacygevoelige gegevens of databasebewerkingen."
        },
    ]
},

"testen_m4": {
    "title": "Module 4 — Testtechnieken",
    "questions": [
        {
            "id": "st_m4_q1_techniek_doel",
            "type": "mcq",
            "prompt": "Waarom gebruik je testtechnieken?",
            "options": [
                "Om willekeurig testgevallen te bedenken",
                "Om gestructureerd en efficiënter testgevallen te ontwerpen",
                "Om bugs automatisch op te lossen",
                "Om minder documentatie te hoeven schrijven"
            ],
            "answer": 1,
            "explanation": "Testtechnieken helpen je systematisch testgevallen ontwerpen, zodat je slimmer en vollediger test."
        },
        {
            "id": "st_m4_q2_equivalence_truefalse",
            "type": "truefalse",
            "prompt": "Equivalentieklassen helpen om invoerwaarden in logische groepen te verdelen.",
            "answer": True,
            "explanation": "Ja. Met equivalentieklassen deel je invoer op in groepen die je op vergelijkbare manier verwacht te behandelen."
        },
        {
            "id": "st_m4_q3_boundary_example",
            "type": "short",
            "prompt": "Noem één voorbeeld van een grenswaarde die je zou testen.",
            "rubric_keywords": ["0", "1", "minimum", "maximum", "grens", "leeftijd", "limiet", "100"],
            "min_keywords": 1,
            "explanation": "Bij grenswaardetesten kijk je bijvoorbeeld naar minimum, maximum en waarden net daar omheen."
        },
    ]
},

"testen_m5": {
    "title": "Module 5 — Exploratory Testing",
    "questions": [
        {
            "id": "st_m5_q1_exploratory_doel",
            "type": "mcq",
            "prompt": "Wat past het best bij exploratory testing?",
            "options": [
                "Alleen vooraf vastgelegde teststappen uitvoeren",
                "Tegelijk leren, onderzoeken en testen",
                "Alleen geautomatiseerde tests draaien",
                "Alleen bugs registreren zonder te testen"
            ],
            "answer": 1,
            "explanation": "Bij exploratory testing combineer je leren, testontwerp en uitvoering tijdens het onderzoeken van de software."
        },
        {
            "id": "st_m5_q2_charter_truefalse",
            "type": "truefalse",
            "prompt": "Een charter kan helpen om exploratory testing richting te geven.",
            "answer": True,
            "explanation": "Ja. Een charter geeft focus aan wat je wilt onderzoeken tijdens een exploratory testsessie."
        },
        {
            "id": "st_m5_q3_observatie_voorbeeld",
            "type": "short",
            "prompt": "Noem één ding waar je tijdens exploratory testing extra op zou letten.",
            "rubric_keywords": ["foutmelding", "navigatie", "gebruiksvriend", "consistent", "performance", "vertraging", "workflow", "interface"],
            "min_keywords": 1,
            "explanation": "Je kunt bijvoorbeeld letten op foutmeldingen, onverwacht gedrag, gebruiksvriendelijkheid, performance of inconsistenties."
        },
    ]
},

"testen_m6": {
    "title": "Module 6 — Bug Reporting",
    "questions": [
        {
            "id": "st_m6_q1_bug_doel",
            "type": "mcq",
            "prompt": "Wat is het doel van een bug report?",
            "options": [
                "De ontwikkelaar bekritiseren",
                "Een probleem duidelijk beschrijven zodat het opgelost kan worden",
                "Alleen fouten opschrijven zonder context",
                "De software opnieuw ontwerpen"
            ],
            "answer": 1,
            "explanation": "Een bug report helpt ontwikkelaars om een probleem te begrijpen en te reproduceren."
        },
        {
            "id": "st_m6_q2_reproduce_truefalse",
            "type": "truefalse",
            "prompt": "Een bug moet reproduceerbaar zijn om goed opgelost te kunnen worden.",
            "answer": True,
            "explanation": "Ja, zonder reproduceerbare stappen is een bug lastig te verhelpen."
        },
        {
            "id": "st_m6_q3_inhoud_bug",
            "type": "short",
            "prompt": "Noem één belangrijk onderdeel van een bug report.",
            "rubric_keywords": ["stappen", "verwacht", "resultaat", "foutmelding", "omgeving", "browser", "versie"],
            "min_keywords": 1,
            "explanation": "Bijvoorbeeld: stappen om te reproduceren, verwacht resultaat, werkelijk resultaat."
        },
    ]
},

"testen_m7": {
    "title": "Module 7 — API testen",
    "questions": [
        {
            "id": "st_m7_q1_api_betekenis",
            "type": "mcq",
            "prompt": "Wat is een API?",
            "options": [
                "Een gebruikersinterface",
                "Een manier waarop systemen met elkaar communiceren",
                "Een database",
                "Een testscript"
            ],
            "answer": 1,
            "explanation": "Een API is een interface waarmee systemen gegevens uitwisselen."
        },
        {
            "id": "st_m7_q2_statuscode",
            "type": "truefalse",
            "prompt": "Een HTTP statuscode 200 betekent meestal dat een request succesvol was.",
            "answer": True,
            "explanation": "Ja, 200 betekent doorgaans dat het verzoek succesvol is verwerkt."
        },
        {
            "id": "st_m7_q3_api_test",
            "type": "short",
            "prompt": "Noem één aspect dat je test bij een API.",
            "rubric_keywords": ["response", "status", "data", "json", "tijd", "performance", "authenticatie"],
            "min_keywords": 1,
            "explanation": "Bijvoorbeeld response data, statuscodes, snelheid of authenticatie."
        },
    ]
},

"testen_m8": {
    "title": "Module 8 — Testautomatisering",
    "questions": [
        {
            "id": "st_m8_q1_doel",
            "type": "mcq",
            "prompt": "Waarom gebruik je testautomatisering?",
            "options": [
                "Om nooit meer handmatig te testen",
                "Om herhaalbare tests sneller en consistenter uit te voeren",
                "Om minder software te schrijven",
                "Om bugs te verbergen"
            ],
            "answer": 1,
            "explanation": "Automatisering helpt bij herhaalbare tests en verhoogt efficiëntie."
        },
        {
            "id": "st_m8_q2_altijd_truefalse",
            "type": "truefalse",
            "prompt": "Alle tests moeten geautomatiseerd worden.",
            "answer": False,
            "explanation": "Nee, sommige tests (zoals exploratory testing) blijven handmatig waardevol."
        },
        {
            "id": "st_m8_q3_voordeel",
            "type": "short",
            "prompt": "Noem één voordeel van testautomatisering.",
            "rubric_keywords": ["snel", "herhaalbaar", "efficiënt", "consistent", "tijd", "besparing"],
            "min_keywords": 1,
            "explanation": "Bijvoorbeeld snelheid, consistentie en tijdsbesparing."
        },
    ]
},

"testen_m9": {
    "title": "Module 9 — Eindproject",
    "questions": [
        {
            "id": "st_m9_q1_doel",
            "type": "mcq",
            "prompt": "Wat is het doel van een eindproject?",
            "options": [
                "Alle theorie herhalen zonder toepassing",
                "Alles wat je geleerd hebt toepassen in een realistische situatie",
                "Alleen fouten opschrijven",
                "Nieuwe theorie leren"
            ],
            "answer": 1,
            "explanation": "Een eindproject draait om toepassen van kennis in de praktijk."
        },
        {
            "id": "st_m9_q2_toepassing",
            "type": "truefalse",
            "prompt": "In een eindproject gebruik je meerdere testtechnieken samen.",
            "answer": True,
            "explanation": "Ja, je combineert kennis en vaardigheden."
        },
        {
            "id": "st_m9_q3_vaardigheid",
            "type": "short",
            "prompt": "Noem één vaardigheid die je hebt ontwikkeld in deze cursus.",
            "rubric_keywords": ["testen", "analyseren", "rapporteren", "denken", "debuggen", "onderzoek"],
            "min_keywords": 1,
            "explanation": "Bijvoorbeeld analyseren, testen, rapporteren of kritisch denken."
        },
    ]
},

}


TESTEN_STEPS = [
    {"nr": 1, "order": 1, "title": "Wat is testen?", "module_slug": "testen_m1", "endpoint": "instructions.testen_module1"},
    {"nr": 2, "order": 2, "title": "Testsoorten", "module_slug": "testen_m2", "endpoint": "instructions.testen_module2"},
    {"nr": 3, "order": 3, "title": "Testplan maken", "module_slug": "testen_m3", "endpoint": "instructions.testen_module3"},
    {"nr": 4, "order": 4, "title": "Testtechnieken", "module_slug": "testen_m4", "endpoint": "instructions.testen_module4"},
    {"nr": 5, "order": 5, "title": "Exploratory Testing", "module_slug": "testen_m5", "endpoint": "instructions.testen_module5"},
    {"nr": 6, "order": 6, "title": "Bug Reporting", "module_slug": "testen_m6", "endpoint": "instructions.testen_module6"},
    {"nr": 7, "order": 7, "title": "API's testen", "module_slug": "testen_m7", "endpoint": "instructions.testen_module7"},
    {"nr": 8, "order": 8, "title": "Testautomatisering", "module_slug": "testen_m8", "endpoint": "instructions.testen_module8"},
    {"nr": 9, "order": 9, "title": "Eindproject", "module_slug": "testen_m9", "endpoint": "instructions.testen_module9"},
]

