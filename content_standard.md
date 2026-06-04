# 🌱 TestGarden Content Standard v0.1

This document defines the standard structure for learning content inside TestGarden.

The goal is:

- scalable growth
- reusable learning modules
- clear migration path
- multilingual readiness
- adaptive learning paths in the future
- human-readable content files

---

# 📁 Folder Structure

Each module lives inside:

content/<track>/<module_slug>/

Example:

content/softwaretesten/module1/

Required files:

- meta.yaml
- lesson.md
- questions.yaml

---

# 📘 meta.yaml

Defines metadata for the learning module.

## Required Fields

```yaml
id: softwaretesten.m01
track_id: softwaretesten
slug: module1
title: Wat is Softwaretesten?
order: 1
level: beginner
status: active
version: 0.1.0
```

## Recommended Fields

```yaml
description: Introductie tot softwaretesten en leren kijken naar gedrag.
estimated_minutes: 30

learning_objectives:
  - Begrijpen wat softwaretesten is
  - Weten waarom testen belangrijk is

prerequisites: []

tags:
  - softwaretesten
  - kwaliteit
  - observatie
```

## Notes

- `id` must be globally unique.
- `slug` should match folder name.
- `order` controls overview sorting.
- `status` can be:
  - active
  - draft
  - archived

---

# 📖 lesson.md

Contains the lesson text in Markdown.

Use:

- headings
- bullet lists
- numbered lists
- emphasis
- links
- images (future)

Example:

```markdown
# Wat is Softwaretesten?

Softwaretesten betekent leren kijken hoe software zich werkelijk gedraagt.
```

---

# ❓ questions.yaml

Contains self-check questions.

Root structure:

```yaml
questions:
```

---

## Supported Types

### Multiple Choice (mcq)

```yaml
- id: softwaretesten.m01.q01
  type: mcq
  prompt: Wat is het doel van softwaretesten?

  options:
    - id: a
      text: Bewijzen dat software foutloos is
    - id: b
      text: Onderzoeken of software werkt zoals verwacht

  answer: b

  hint: Denk aan gedrag en kwaliteit.

  feedback:
    correct: Goed gezien.
    incorrect: Nog niet helemaal.

  explanation: Testen helpt kwaliteit zichtbaar maken.
```

---

### True / False

```yaml
- id: softwaretesten.m01.q02
  type: truefalse
  prompt: Testen kan bewijzen dat software foutloos is.

  answer: false

  explanation: Testen kan fouten aantonen, niet foutloosheid bewijzen.
```

---

### Open Question

```yaml
- id: softwaretesten.m01.q03
  type: open
  prompt: Noem iets dat je als tester zou controleren.

  sample_answer: Bijvoorbeeld of een knop werkt.

  keywords:
    - knop
    - formulier
    - foutmelding

  explanation: Kijk naar gedrag dat belangrijk is voor gebruikers.
```

---

# 🆔 ID Rules

## Module IDs

Format:

track.mXX

Example:

softwaretesten.m01

## Question IDs

Format:

track.mXX.qXX

Example:

softwaretesten.m01.q01

## Rules

- IDs never reused for different content
- IDs remain stable over time
- Titles may change, IDs should not

---

# 🔁 Versioning

Use semantic style:

```yaml
version: 0.1.0
```

Meaning:

- major = breaking changes
- minor = new content/features
- patch = typo/fixes

Examples:

- 0.1.1
- 0.2.0
- 1.0.0

---

# 🧭 Migration Rules

Legacy HTML modules may coexist during migration.

Preferred loading order:

1. new content module
2. legacy template fallback

This allows gradual transition.

---

# 🌍 Multilingual Direction (future)

Possible future structure:

content/softwaretesten/module1/translations/

- nl.yaml
- en.yaml
- zh.yaml

Or phrase-key based translation layer.

---

# 🌱 Future Extensions Allowed

Possible later fields:

- difficulty_score
- ai_coach_prompt
- badge_reward
- practical_assignment
- media_gallery
- xapi_mapping

---

# 🤍 Guiding Principle

Do not trap knowledge in proprietary files.

Build living learning content that can grow, adapt and serve people.

