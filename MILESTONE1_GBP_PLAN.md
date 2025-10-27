# 🧩 Milestone 1 — Google Business Profile Optimizer

### 🎯 Core Goal  
Fetch all editable content from the Google Business Profile API, generate AI-based optimizations, and (after approval) push those updates back to GBP.  
Also, retrieve and AI-reply to reviews.

---

## 1️⃣ Fetch existing GBP data

| Feature | Endpoint | Purpose | Example Fields |
|----------|-----------|----------|----------------|
| **Business Info** | `GET /locations/{locationId}` | Get current name, description, categories, address, etc. | `name`, `primaryCategory`, `description` |
| **Services** | `GET /locations/{locationId}/services` | List services with titles, prices, and descriptions. | `serviceTypeId`, `price`, `description` |
| **Products** | `GET /locations/{locationId}/products` | Fetch product catalog. | `name`, `price`, `category`, `description` |
| **Q&A** | `GET /locations/{locationId}/questions` | Get customer questions + answers. | `question`, `answer`, `upvoteCount` |
| **Reviews** | `GET /locations/{locationId}/reviews` | Retrieve recent customer reviews. | `reviewId`, `starRating`, `comment` |

**Acceptance Criteria**
- FastAPI endpoints created for each: `/gbp/fetch/{type}` or combined `/gbp/fetch?scope=all`.
- Handles pagination + rate-limits.
- JSON normalized into unified structure:
  ```json
  {
    "description": "...",
    "services": [],
    "products": [],
    "qna": [],
    "reviews": []
  }
  ```
- Tests mock Google responses and verify schema.

---

## 2️⃣ Optimize content via AI

| Input | Output | Example Prompt |
|--------|---------|----------------|
| Description | Polished business description, keyword-focused | “Rewrite this GBP description to sound more professional and improve local SEO relevance.” |
| Services | Clearer service names/descriptions | “Enhance these service listings for clarity and conversion.” |
| Products | Better product copy | “Improve these product descriptions for readability and sales.” |
| Q&A | Suggested additional questions + improved answers | “Suggest 3 new relevant customer questions and concise answers.” |
| Reviews | Polite, branded responses | “Write friendly replies matching tone: {{tone}} for each review.” |

**Acceptance Criteria**
- `/gbp/analyze` takes the normalized JSON.
- Uses OpenAI (primary) with Anthropic fallback.
- Returns typed JSON object with optimized fields.
- Prompt templates stored under `/docs/ai_prompts.md`.

---

## 3️⃣ Approve and update content (POST back)

| Feature | Method | Purpose |
|----------|---------|----------|
| Description | `PATCH /locations/{id}?updateMask=description` | Push improved description |
| Services | `PATCH /locations/{id}/services` | Update or add new services |
| Products | `PATCH /locations/{id}/products` | Update or add products |
| Q&A | `POST /locations/{id}/questions` | Add new Q&A |
| Reviews | `POST /locations/{id}/reviews/{reviewId}/reply` | Publish AI-generated replies |

**Acceptance Criteria**
- `/gbp/apply` handles selected approved updates.
- Tokens from OAuth used for authorized writes.
- Logs each update, result, and timestamp.
- Write requests sandboxed to test GBP account.

---

## 4️⃣ Review-reply automation

| Task | Detail |
|------|--------|
| Fetch new reviews daily (via cron or WP-Cron) |
| Analyze sentiment & tone |
| Generate AI replies |
| Save replies for approval in WP |
| Optional: auto-publish after approval period |

**Acceptance Criteria**
- New endpoint `/gbp/reviews/auto-reply`.
- Configurable interval (daily/hourly).
- Retry logic + error logging.

---

## 5️⃣ Integration with WordPress

- Add “GBP Optimization” tab under each Location CPT.  
- Buttons: **Fetch Data**, **Run AI Optimization**, **Apply Changes**, **View Reviews**.  
- Displays before/after text diffs for each section.  
- Review replies appear under Reviews table with “Approve & Send.”  
- Uses HMAC-secured REST calls between WP and the microservice.

---

## 6️⃣ Deliverables Summary

- ✅ Fetch endpoints (description, services, products, Q&A, reviews)  
- ✅ AI optimization prompt layer  
- ✅ Apply endpoints for pushing updates  
- ✅ Review auto-reply mechanism  
- ✅ WP integration (fetch/preview/approve/publish)  
- ✅ Documentation:  
  - `docs/google_endpoints.md`  
  - `docs/ai_prompts.md`  
  - `docs/oauth.md`  
  - `docs/wp_field_map.md`  

---
