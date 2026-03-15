# Repo Structure Governance Skill

## Purpose

Protect the repository from uncontrolled sprawl while preserving extension paths.

## Responsibilities

- keep new files inside clearly named domains
- preserve phase boundaries
- prevent feature work from leaking into the wrong layer

## Rules

- route HTTP concerns through `app/api`
- put configuration in `app/core`
- keep persistence helpers in `app/db`
- place future integrations behind `app/services`
- document placeholders instead of overbuilding them

## Repo Touchpoints

- repository root
- `app/`
- `docs/`
- `agents/`
