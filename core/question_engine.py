# core/question_engine.py

from database.models import Answer, db


def get_question(module: dict, question_id: str):
    for q in module.get("questions", []):
        if q.get("id") == question_id:
            return q
    return None


def check_answer(question: dict, user_answer: str) -> bool:
    qtype = question.get("type")

    if qtype == "mcq":
        return str(user_answer) == str(question.get("answer"))

    if qtype == "truefalse":
        val = (user_answer or "").strip().lower()
        user_bool = val in ("true", "1", "yes", "ja", "waar")

        correct_answer = question.get("answer")

        if isinstance(correct_answer, str):
            correct_bool = correct_answer.strip().lower() in ("true", "1", "yes", "ja", "waar")
        else:
            correct_bool = bool(correct_answer)

        return user_bool == correct_bool

    if qtype == "short":
        text = (user_answer or "").strip().lower()
        keywords = question.get("rubric_keywords", [])
        min_k = int(question.get("min_keywords", 1))
        hits = sum(1 for kw in keywords if kw in text)
        return hits >= min_k

    return False


def upsert_answer(user_id: int, module_slug: str, question_id: str, user_answer: str, is_correct: bool):
    row = Answer.query.filter_by(
        user_id=user_id,
        module_slug=module_slug,
        question_id=question_id,
    ).first()

    if row:
        row.attempts += 1
        row.is_correct = row.is_correct or is_correct
        row.last_answer = str(user_answer)
        row.answer_text = str(user_answer)
    else:
        row = Answer(
            user_id=user_id,
            module_slug=module_slug,
            question_id=question_id,
            is_correct=is_correct,
            attempts=1,
            last_answer=str(user_answer),
            answer_text=str(user_answer),
        )
        db.session.add(row)

    db.session.commit()
    return row


def compute_progress(user_id: int, module_slug: str, module: dict) -> dict:
    total = len(module.get("questions", []))
    if total == 0:
        return {"correct": 0, "total": 0, "percent": 0}

    rows = Answer.query.filter_by(user_id=user_id, module_slug=module_slug).all()
    correct = sum(1 for r in rows if r.is_correct)
    percent = int((correct / total) * 100)
    return {"correct": correct, "total": total, "percent": percent}


def get_answer_map(user_id: int, module_slug: str) -> dict:
    rows = Answer.query.filter_by(user_id=user_id, module_slug=module_slug).all()
    return {r.question_id: r for r in rows}


def compute_step_status(user_id: int, module_slug: str, module: dict) -> str:
    total = len(module.get("questions", []))
    if total == 0:
        return "not"

    rows = Answer.query.filter_by(user_id=user_id, module_slug=module_slug).all()
    if not rows:
        return "not"

    correct = sum(1 for r in rows if r.is_correct)
    if correct >= total:
        return "done"

    return "progress"