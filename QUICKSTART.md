# ⚡️ Quickstart — EP Marketing Google Business Profile Optimizer

## Overview  
This project is part of the **EP Marketing AI System** and powers Google Business Profile (GBP) optimization.  
It connects to the Google Business Profile API, analyzes profile data with AI, and returns structured suggestions for review and approval inside our WordPress plugin.

---

## What You’ll Build  
- A **Python FastAPI microservice** that handles Google OAuth, data fetching, and AI analysis.  
- A **direct integration** with our existing WordPress plugin (no Docker, no n8n).  
- An **internal preview system** for optimized GBP content — description, Q&A, products, services, posts, and review replies.  

---

## Architecture Summary  

| Component | Purpose |
|------------|----------|
| **WordPress Plugin** | Central hub for businesses, locations, approvals, and post scheduling. |
| **Microservice (FastAPI)** | Handles Google API, AI content generation, and secure communication with WordPress. |
| **AI Providers** | OpenAI (default) and Anthropic (optional fallback). |
| **Auth Layer** | HMAC-secured REST calls between WordPress ↔ Microservice + Google OAuth for each account. |
| **Scheduling** | Internal WP-Cron events for testing automatic post publishing. |

---

## Prerequisites  

- EP Marketing Google Cloud project (GBP API enabled)  
- Access to **EP Marketing GitHub organization**  
- Access to **1Password → Dev Vault** for API keys  
- Added as **OAuth Test User** in Google Cloud (see `docs/google_access.md`)  
- Python 3.11+ and Cursor IDE installed locally  

---

## High-Level Steps  

1. **Clone the Repo**  
   - Use your EP Marketing GitHub account (not personal).  

2. **Create Environment File**  
   - Copy `.env.example` → `.env`  
   - Fill in credentials from 1Password.  

3. **Connect Google Account**  
   - Visit `/oauth/init?state=dev-test` to authorize your Google test account.  
   - Tokens are stored locally (encrypted).  

4. **Test Fetch + Analyze Flow**  
   - Hit `/gbp/fetch` to pull down a test business profile.  
   - Hit `/gbp/analyze` to generate optimization suggestions.  

5. **Review in WordPress**  
   - Open any test Location in WP Admin → GBP tab.  
   - View AI suggestions, approve/reject changes.  

6. **Phase 1B (Optional)**  
   - Configure WP-Cron to auto-post approved drafts for internal testing.  

---

## Folder Layout  

```
src/
  routes/          # FastAPI endpoints
  services/        # Google + AI logic
  models/          # Pydantic schemas
  tests/           # Pytest suite
docs/
  google_access.md
  ai_prompts.md
  oauth.md
  wp_field_map.md
.env.example
README.md
STARTUP.md
```

---

## Deliverables for Milestone 1  

- ✅ Working FastAPI service (`/health`, `/fetch`, `/analyze`, `/apply`)  
- ✅ Secure integration with WP plugin via HMAC  
- ✅ OAuth connection working with test user  
- ✅ Preview and approval UI live in WP  
- ✅ Documentation under `/docs`  
- ✅ Basic WP-Cron post scheduling for internal testing  

---

## Quick Reminders  
- All API keys are managed via **1Password → Dev Vault**.  
- Do not commit `.env` or credentials to GitHub.  
- Use **ClickUp** for all tasks, updates, and blockers.  
- Push branches following this pattern:  
  `feat/<task-name>` or `fix/<bug-description>`  
- All code merges require a Pull Request.  

---

**Next Milestone:** Content Engine – AI-powered post creation and cross-platform automation.  

**Maintainer:** EP Marketing Engineering Team  
**Last Updated:** October 2025  
