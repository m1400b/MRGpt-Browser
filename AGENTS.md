# MRGpt Browser - Agent Guide

## Project Overview

MRGpt Browser is a Python desktop browser application built with PySide6.

The main goals are:

- Privacy-focused browsing
- Incognito profile management
- Persian language and RTL support
- Modular and maintainable architecture
- Future AI/VPN integration

---

# Architecture Rules

The project follows a layered architecture.

## Core Layer

Location:

core/

Responsibilities:

- Browser engine logic
- Profiles
- Events
- Network handling
- Application infrastructure

Rules:

- Core must not depend on UI components.
- Business logic must stay outside UI files.

---

## Services Layer

Location:

services/

Responsibilities:

- Application services
- Coordination between modules
- Business workflows

Rules:

- Use services instead of directly accessing low-level modules.
- Keep services independent from UI.

---

## Models Layer

Location:

models/

Responsibilities:

- Data structures
- Entities
- Configuration models

Rules:

- Models should remain simple.
- Avoid putting business logic inside models.

---

## Database Layer

Location:

database/

Responsibilities:

- Persistence
- Repositories
- SQLite operations

Rules:

- Use repository pattern.
- Do not access database directly from UI.

---

## UI Layer

Location:

ui/

Responsibilities:

- Windows
- Widgets
- Dialogs
- User interaction

Rules:

- UI should call services.
- Avoid complex logic inside widgets.

---

# Coding Standards

Language:

- Python 3.12+

Framework:

- PySide6

Rules:

- Use type hints.
- Prefer clear class-based design.
- Keep functions focused.
- Avoid unnecessary dependencies.

---

# Browser Specific Rules

## Privacy

Browser profiles must respect privacy requirements:

- No persistent cookies for private mode.
- No unnecessary disk storage.
- Avoid storing user browsing data.

---

## Tab Management

Before modifying:

- browser_tab.py
- tab_manager.py
- browser.py

Understand the existing flow:

Tab
→ Tab Manager
→ Browser
→ Browser View

Do not rewrite architecture without strong reason.

---

# UI Rules

The application should support:

- Persian language
- RTL layout
- Persian fonts

Avoid breaking existing UI conventions.

---

# Change Policy

Before major changes:

1. Understand existing architecture.
2. Prefer small incremental modifications.
3. Do not remove existing modules without review.
4. Keep backward compatibility.

---

# Git Workflow

Branches:

main:
- Stable versions only.

development:
- Active development branch.

Feature branches:

feature/<name>

Example:

feature/vpn-service

---

# Commit Style

Commit messages should describe the change.

Examples:

Good:

"Fix new tab address reset"

"Add browser loading indicator"

Bad:

"update"

"changes"

---

# Agent Behavior

When modifying this project:

- Explain the reason for changes.
- Identify affected files.
- Avoid unnecessary refactoring.
- Respect existing architecture.
- Ask before making large structural changes.
