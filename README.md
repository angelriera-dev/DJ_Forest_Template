# 🛡️ Django Fortress SaaS

[![Django](https://img.shields.io/badge/Django-6.0-092e20?logo=django)](https://www.djangoproject.com/)
[![Security](https://img.shields.io/badge/Security-OWASP%202026-red)](docs/adr/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Type Checking](https://img.shields.io/badge/Type%20Checking-Pyright-brightgreen)](pyproject.toml)

**Django Fortress** is a security-first, military-grade SaaS boilerplate designed for the AI era. It implements **OWASP Top 10 2026** mitigations natively while maintaining a modern, high-performance frontend stack.

---

## 🎯 Primary Objectives

1.  **Security by Design**: Native mitigations for authentication, data integrity, and session management.
2.  **AI-Ready Architecture**: A robust backend infrastructure designed to handle secure AI integrations without compromising sensitive data.
3.  **Zero Technical Debt**: Strict adherence to quality gates (Ruff, Pyright) and a clean `src/` modular layout.
4.  **Production Parity**: Seamless transition between development and production via modular configuration and Docker.

---

## 🎓 The Educational Differentiator: Why > How

Unlike generic boilerplates, Django Fortress is built to be a learning tool for architects and security-conscious developers.

-   **The "Why" Guides**: Every architectural decision is backed by an **ADR (Architecture Decision Record)** in `docs/adr/`, explaining the rationale, trade-offs, and security implications.
-   **OWASP Mapping**: The documentation includes direct mappings between code implementations and OWASP Top 10 threats.
-   **Transparent Architecture**: No "magic" packages. We prefer modular, standard Django patterns that are easy to audit and hard to break.

---

## 🚀 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Django 6.0 (Python 3.12+) |
| **Frontend** | HTMX + Alpine.js + Tailwind CSS + DaisyUI |
| **Identity** | django-allauth (Email-first, MFA Ready) |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Quality** | Ruff (Linter), Pyright (Static Typing) |
| **Security** | Bandit (SAST), Semgrep (OWASP Scans) |
| **Testing** | Pytest + Pytest-Django (Strict TDD Mode) |

---

## 🛠️ Getting Started

The project uses a `Makefile` to standardize the workflow across all environments.

### 1. Create your SaaS Project from this Template

To start a new SaaS project while maintaining the ability to pull future security updates, follow the **Upstream Remote Strategy**. Choose the workflow that fits your needs:

**Option A: Extensible Mode (Authoritative)**
Use the template as a base, modify any file freely, and manually merge upstream updates taking only what you need.
1. Click **[Use this template](https://github.com/new?template_name=Saas_Forest_Bolier&template_owner=angelriera-dev)** to create your new repository.
2. Clone your repository and configure the upstream tracking:
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-NEW-REPO.git
   cd YOUR-NEW-REPO
   make saas-init
   # Or using raw bash: git remote add template https://github.com/angelriera-dev/Saas_Forest_Bolier.git
   ```

**Option B: Collaborative Mode (Strict & Protected)**
Sync from the template and avoid modifying core files locally. This mode installs a local Git hook that blocks accidental modifications to template-owned files (like `config/` and `components/`) to prevent merge conflicts.
1. Click **[Use this template](https://github.com/new?template_name=Saas_Forest_Bolier&template_owner=angelriera-dev)**.
2. Clone and install the protection hooks:
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-NEW-REPO.git
   cd YOUR-NEW-REPO
   make saas-collab

   # Or using raw bash:
   # git remote add template https://github.com/angelriera-dev/Saas_Forest_Bolier.git
   # echo -e '#!/bin/sh\nif git diff --cached --name-only | grep -E "^(src/config/|src/templates/components/|SKILLS/)"; then echo "\\n[BLOCK] ERROR: Protected files modified!\\n"; exit 1; fi\nif git diff --cached --name-only | grep -E "^src/apps/users/"; then echo "\\n[WARN] Modifying apps/users.\\n"; fi' > .git/hooks/pre-commit
   # chmod +x .git/hooks/pre-commit
   ```

*(To pull future template updates to your SaaS, run `make saas-sync` or `git fetch template && git merge template/main --allow-unrelated-histories`)*.

### 2. Local Installation
```bash
make install
```

### 3. Database & Data
```bash
make migrate
# Seed admin (admin@example.com / admin123) and plans
.venv/bin/python src/manage.py seed_data
```

### 4. Run Development Server
```bash
make run
```

### 5. Quality Suite (Run before every commit)
```bash
make check_code
```

---

## 📂 Project Structure

We follow the **`src/` layout** to separate core source code from configuration and infrastructure.

```text
.
├── src/                # Project Source Code
│   ├── apps/           # Modular Django Applications
│   │   ├── users/      # Identity & Authentication
│   │   └── dashboard/  # Business Logic & UI
│   ├── config/         # Central Configuration
│   │   └── settings/   # Modular, Adaptive Settings
│   ├── templates/      # Shared Components & Layouts
│   └── requirements/   # Segmented Dependencies
├── docs/               # PDR, ADRs, and Governance
├── Makefile            # Unified Command Entry Point
└── pyproject.toml      # Tooling Configuration
```

---

## 🗺️ Roadmap Overview

1.  **Phase 1 (Foundations)**: Infrastructure, Quality Standards, and Base Hardening. [DONE]
2.  **Phase 2 (Identity)**: Brute-force protection, MFA, and Mandatory Verification. [IN PROGRESS]
3.  **Phase 3 (Infrastructure)**: IaC with Terraform and AWS Hardening.
4.  **Phase 4 (Scalability)**: Redis, Celery, and Load Testing.
5.  **Phase 5 (AI Secure Prompt)**: Sanitized LLM integrations.
6.  **Phase 6 (API Economy)**: Hardened DRF and OpenAPI 3.1.

---

## 🛡️ Security Enforcement

The project enforces high standards via the `make check_code` gate:
- **Zero Errors Policy**: Zero errors allowed in Ruff (Linting) and Pyright (Typing).
- **Security Scans**: Automated Bandit and Semgrep scans on every build.
- **Strict TDD**: Minimum 90% coverage target for identity and core flows.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
