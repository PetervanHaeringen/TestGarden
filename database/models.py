# =============================================================================
# models.py — Database modellen voor TestGarden
# =============================================================================
# In dit bestand beschrijven we de structuur van de database.
# Elke class is een "tabel" in de database.
# De velden in een class zijn de "kolommen" van die tabel.
#
# SQLAlchemy vertaalt deze Python-klassen automatisch naar SQL-tabellen.
# Flask-SQLAlchemy zorgt voor de koppeling met de Flask-applicatie.
#
# OVERZICHT VAN DE MODELLEN:
#
#   Gebruikers & toegang
#   ├── User             → accounts, rollen, dashboard-instellingen
#   ├── UserModule       → welke modules zijn toegewezen aan welke cursist
#   └── Progress         → voortgang per oefening (legacy)
#
#   Leerinhoud & antwoorden
#   └── Answer           → antwoorden op theorievragen per module
#
#   Praktijkbeoordeling (nieuw)
#   ├── PraktijkOpdracht    → docent vinkt praktijkopdracht af als voldaan
#   └── PraktijkBeoordeling → formeel eindoordeel per werkproces/competentie
#
#   Testbeheer (voor de testen-omgeving)
#   ├── TestCase         → een testcase met beschrijving
#   ├── TestStep         → stappen binnen een testcase
#   ├── Precondition     → voorwaarden voor een testcase
#   ├── TestRun          → een sessie waarin testcases worden uitgevoerd
#   ├── TestResult       → resultaat per testcase binnen een run
#   └── StepResult       → resultaat per stap binnen een testcase
# =============================================================================

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


# -----------------------------------------------------------------------------
# GEBRUIKERS
# Bevat alle accounts die kunnen inloggen op TestGarden.
# Rollen bepalen wat iemand mag zien en doen:
#   - student  : volgt modules, ziet eigen voortgang
#   - teacher  : kan modules toewijzen en praktijkopdrachten beoordelen
#   - admin    : volledige toegang
# module_visibility bepaalt wat een student ziet in "Mijn Tuin":
#   - alleen_toegewezen : ziet alleen eigen modules (bijv. korte bezoeker)
#   - vergrendeld       : ziet alle modules, niet-toegewezen zijn grijs
#   - alles             : ziet en opent alles (bijv. vast traject)
# -----------------------------------------------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="student")
    dashboard_theme = db.Column(db.String(20), nullable=False, default="plant")
    module_visibility = db.Column(db.String(20), nullable=False, default="alleen_toegewezen")

    # Relaties: koppeling naar andere tabellen
    progress = db.relationship("Progress", backref="user", lazy=True)
    assigned_modules = db.relationship("UserModule", backref="user", lazy=True,
                                       foreign_keys="UserModule.user_id")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# -----------------------------------------------------------------------------
# VOORTGANG (legacy)
# Slaat per gebruiker op welke oefeningen zijn gedaan en wat de score was.
# -----------------------------------------------------------------------------

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# -----------------------------------------------------------------------------
# MODULE TOEWIJZINGEN — het hart van "Mijn Tuin"
# Koppelt een specifieke module aan een specifieke student.
# assigned_by slaat op wie de toewijzing heeft gemaakt (teacher of admin).
# volgorde bepaalt in welke volgorde de modules op het dashboard verschijnen.
# -----------------------------------------------------------------------------

class UserModule(db.Model):
    __tablename__ = "user_module"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    module_slug = db.Column(db.String(120), nullable=False)

    assigned_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    volgorde = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "module_slug", name="uq_user_module"),
    )


# -----------------------------------------------------------------------------
# ANTWOORDEN OP THEORIEVRAGEN
# Slaat op hoe een student een vraag heeft beantwoord binnen een module.
#
# RELATIE MET PRAKTIJKBEOORDELING:
# Correcte antwoorden leveren evidence voor "vakkennis en vaardigheden"
# in het kwalificatiedossier. Gedragingen worden gedekt door
# PraktijkOpdracht — die vereisen observatie in de praktijk.
# -----------------------------------------------------------------------------

class Answer(db.Model):
    __tablename__ = "answer"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    module_slug = db.Column(db.String(120), nullable=False)
    question_id = db.Column(db.String(120), nullable=False)

    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    attempts = db.Column(db.Integer, nullable=False, default=1)
    last_answer = db.Column(db.Text, nullable=True)
    answer_text = db.Column(db.Text, nullable=True)  # voor open antwoorden

    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "module_slug", "question_id",
                         name="uq_user_module_question"),
    )


# -----------------------------------------------------------------------------
# PRAKTIJKOPDRACHTEN — beoordeeld door de docent
#
# Een PraktijkOpdracht is een concrete taak die een cursist uitvoert in de
# praktijk: een servicedesk-ticket, een testcase, een git-opdracht, etc.
#
# De DOCENT markeert de opdracht als voldaan — nooit de cursist zelf.
# Dit borgt de kwaliteitscontrole.
#
# De koppeling tussen opdracht_id en competenties staat in een YAML-bestand
# per leerpad (bijv. servicedesk_tickets.yaml). Zo is de koppeling
# aanpasbaar zonder database-migratie. Het competentie-overzicht wordt
# berekend op basis van voldane opdrachten + de YAML.
#
# leerpad  → "servicedesk" / "softwaretesten" / "git" / ...
#            Bepaalt welk YAML-bestand gebruikt wordt.
# kader    → "mbo_25999" / "uwv" / "heliomare" / "snuffel" / ...
#            Het beoordelingskader. Maakt het systeem geschikt voor
#            de diverse groepen die bij ICT vanaf Morgen instromen.
# -----------------------------------------------------------------------------

class PraktijkOpdracht(db.Model):
    __tablename__ = "praktijk_opdracht"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    opdracht_id = db.Column(db.String(120), nullable=False)  # bv. "servicedesk.basis.t01"
    leerpad = db.Column(db.String(60), nullable=False)       # bv. "servicedesk"
    kader = db.Column(db.String(60), nullable=False, default="mbo_25999")

    beoordeeld_door = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    beoordeeld_op = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    voldaan = db.Column(db.Boolean, nullable=False, default=False)
    notitie = db.Column(db.Text, nullable=True)  # observatie van de docent

    __table_args__ = (
        UniqueConstraint("user_id", "opdracht_id", name="uq_user_opdracht"),
    )


# -----------------------------------------------------------------------------
# PRAKTIJKBEOORDELING — het formele eindoordeel per werkproces
#
# Dit is het digitale equivalent van het praktijkbeoordelingsformulier
# (vervangt de Excel). Per cursist, per leerpad, per werkproces:
#   - tussenevaluatie en eindbeoordeling (door de docent)
#   - zelfevaluatie (door de cursist)
#   - notities van de docent
#
# werkproces_code is afhankelijk van het kader:
#   - MBO (mbo_25999) : "B1-K1-W1", "B1-K2-W1" etc.
#   - Andere kaders   : eigen structuur, bepaald door het leerpad-YAML
#
# De docent vult dit in op basis van:
#   1. Voldane PraktijkOpdrachten  (automatisch zichtbaar)
#   2. Correcte theorievragen      (automatisch zichtbaar)
#   3. Eigen observaties           (vrij tekstveld)
#
# Het systeem ondersteunt de docent — het oordeel blijft menselijk.
# -----------------------------------------------------------------------------

class PraktijkBeoordeling(db.Model):
    __tablename__ = "praktijk_beoordeling"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    leerpad = db.Column(db.String(60), nullable=False)
    kader = db.Column(db.String(60), nullable=False, default="mbo_25999")
    werkproces_code = db.Column(db.String(30), nullable=False)  # bv. "B1-K2-W1"

    beoordeeld_door = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Tussenevaluatie — halverwege het traject
    tussenevaluatie = db.Column(db.String(20), nullable=True)
    # Waarden: "voldaan" / "niet_voldaan" / None (nog niet ingevuld)
    datum_tussen = db.Column(db.DateTime, nullable=True)

    # Eindbeoordeling — aan het einde van het traject
    eindbeoordeling = db.Column(db.String(20), nullable=True)
    # Waarden: "voldaan" / "niet_voldaan" / None (nog niet ingevuld)
    datum_eind = db.Column(db.DateTime, nullable=True)

    # Zelfevaluatie door de cursist (open tekstvelden)
    zelfevaluatie_goed    = db.Column(db.Text, nullable=True)
    zelfevaluatie_beter   = db.Column(db.Text, nullable=True)
    zelfevaluatie_geleerd = db.Column(db.Text, nullable=True)

    # Observaties van de docent
    notitie_docent = db.Column(db.Text, nullable=True)

    __table_args__ = (
        # Één beoordelingsrecord per cursist, per leerpad, per werkproces
        UniqueConstraint("user_id", "leerpad", "werkproces_code",
                         name="uq_beoordeling_werkproces"),
    )


# -----------------------------------------------------------------------------
# TESTCASES
# Een testcase beschrijft wat getest moet worden, inclusief stappen en
# precondities. Wordt gebruikt in de testbeheer-omgeving van TestGarden.
# -----------------------------------------------------------------------------

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    module = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)

    tags = db.Column(db.String(250), nullable=True)
    priority = db.Column(db.String(20), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    steps = db.relationship("TestStep", backref="test_case",
                            cascade="all, delete-orphan", lazy=True)
    preconditions = db.relationship("Precondition", backref="test_case",
                                    cascade="all, delete-orphan", lazy=True)


# -----------------------------------------------------------------------------
# TESTSTAPPEN
# Elke testcase bestaat uit een of meerdere stappen.
# Een stap beschrijft een actie en het verwachte resultaat.
# -----------------------------------------------------------------------------

class TestStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"), nullable=False)

    step_no = db.Column(db.Integer, nullable=False)
    action = db.Column(db.Text, nullable=False)
    expected = db.Column(db.Text, nullable=True)


# -----------------------------------------------------------------------------
# PRECONDITIES
# Voorwaarden die gelden voordat een testcase uitgevoerd kan worden.
# -----------------------------------------------------------------------------

class Precondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"), nullable=False)

    text = db.Column(db.Text, nullable=False)


# -----------------------------------------------------------------------------
# TESTRUN EN RESULTATEN
# Een TestRun is een sessie waarin een gebruiker testcases uitvoert.
# Per testcase wordt een TestResult opgeslagen (pass/fail/skip/note).
# Per stap binnen een testcase wordt een StepResult opgeslagen.
#
# StepResult bevat een snapshot van de stap-tekst zodat oude runs
# kloppen, ook als de testcase later aangepast wordt.
# -----------------------------------------------------------------------------

class TestRun(db.Model):
    __tablename__ = "test_run"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)

    results = db.relationship("TestResult", backref="run",
                              cascade="all, delete-orphan")


class TestResult(db.Model):
    __tablename__ = "test_result"

    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey("test_run.id"), nullable=False)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"), nullable=False)

    status = db.Column(db.String(20))   # pass / fail / note / skip
    comment = db.Column(db.Text)

    step_results = db.relationship("StepResult", backref="result",
                                   cascade="all, delete-orphan", lazy=True)


class StepResult(db.Model):
    __tablename__ = "step_result"

    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey("test_result.id"), nullable=False)

    # Snapshot: kopie van de stap op het moment van uitvoeren
    step_no = db.Column(db.Integer, nullable=False)
    action_text = db.Column(db.Text, nullable=False)
    expected_text = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(20), nullable=False)  # pass / fail / note / skip
    comment = db.Column(db.Text, nullable=True)
