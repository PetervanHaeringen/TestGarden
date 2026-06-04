# =============================================================================
# core/menu.py — Menustructuur voor TestGarden
# =============================================================================
# Elke functie geeft een lijst van menu-items terug.
# Elk item heeft een "name" (zichtbare tekst) en een "endpoint" (Flask route).
# De base.html template gebruikt deze lijsten om de navigatie op te bouwen.
#
# Welk menu zichtbaar is hangt af van de rol van de gebruiker —
# dat wordt geregeld in base.html, niet hier.
# =============================================================================


def get_exercises_menu():
    return [
        {"name": "Oefening 1", "endpoint": "exercises.een_overview"},
    ]


# def get_instructions_menu():
#     return [
#         {"name": "Softwaretesten", "endpoint": "instructions.testen_overview"},
#         {"name": "Git & GitHub",   "endpoint": "instructions.git_overview"},
#     ]


def get_content_menu():
    return [
        {"name": "Softwaretesten (nieuw)", "endpoint": "instructions.testen_content_overview"},
        {"name": "Git & GitHub (nieuw)",   "endpoint": "instructions.git_content_overview"},
        {"name": "Programmeren (nieuw)",   "endpoint": "instructions.developer_content_overview"},
    ]


def get_scripts_menu():
    return [
        {"name": "🔄 Testronden",       "endpoint": "testronden.overzicht"},
        {"name": "📋 Testscripts",      "endpoint": "scripts.overzicht"},
        {"name": "🏨 Van der Valk",     "endpoint": "scripts.omgeving"},
        {"name": "🐛 Bevindingen",      "endpoint": "bevindingen.overzicht"},
        {"name": "📄 Rapport",          "endpoint": "bevindingen.rapport"},
    ]


def get_tools_menu():
    return [
        {"name": "QRCode", "endpoint": "tools.qrcode_page"},
        {"name": "Statuscode Checker", "endpoint": "tools.statuscode"},
    ]


def get_main_menu(logged_in=False):
    if logged_in:
        return [
            {"name": "Home",      "endpoint": "core.index"},
            {"name": "Mijn Tuin", "endpoint": "users.dashboard"},
            {"name": "Logout",    "endpoint": "users.logout"},
        ]
    return [
        {"name": "Home",     "endpoint": "core.index"},
        {"name": "Login",    "endpoint": "users.login"},
        {"name": "Register", "endpoint": "users.register"},
    ]


def get_teacher_menu():
    return [
        # Uitgefaseerd: dit dashboard hoort bij de oude HTML-sjabloonmodules
        # (testen_m1..m9). De inhoud is overgegaan naar de content-modules
        # (softwaretesten.m01..m09). De route en question bank blijven bestaan
        # zodat bestaande voortgang zichtbaar blijft en de sjabloonstructuur
        # herbruikbaar is voor nieuwe vaste modules (onboarding, EHBO, BHV).
        # Haal het commentaar weg om het dashboard weer in het menu te tonen.
        # {"name": "Softwaretesten Dashboard",         "endpoint": "teacher.teacher_testen_dashboard"},
        {"name": "Softwaretesten Content Dashboard", "endpoint": "teacher.teacher_content_testen_dashboard"},
        {"name": "Git & GitHub Content Dashboard",           "endpoint": "teacher.teacher_content_git_dashboard"},
        {"name": "Developer Content Dashboard",           "endpoint": "teacher.teacher_content_developer_dashboard"},
        # Cursisten volgen: zie per cursist aan welke modules is gewerkt
        {"name": "👀 Cursisten volgen",              "endpoint": "teacher.cursisten_overzicht"},
        # Toewijzen: bepaal per cursist welke modules zichtbaar zijn in Mijn Tuin
        {"name": "📚 Modules toewijzen",             "endpoint": "teacher.toewijzen_overzicht"},
        # Praktijkbeoordeling: opdrachten afvinken en formeel eindoordeel invullen
        {"name": "📋 Praktijkbeoordeling",           "endpoint": "teacher.praktijk_overzicht"},
        {"name": "Vertaaloverzicht", "endpoint": "teacher.translation_overview"},
    ]


def get_all_menus(logged_in=False, username=None):
    return {
        "main":         get_main_menu(logged_in),
        "exercises":    get_exercises_menu(),
        #"instructions": get_instructions_menu(),
        "content":      get_content_menu(),
        "tools":        get_tools_menu(),
        "teacher":      get_teacher_menu(),
        "scripts":      get_scripts_menu(),
    }
