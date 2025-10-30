## Milestone 1 TODOs

### Bad Review Alert System
- [ ] Add endpoint to fetch new reviews and queue AI replies (`app/routes/gbp_reviews.py`)
- [ ] Implement sentiment/tone analysis and reply generation (`app/services/ai_optimizer.py`, `app/services/ai.py`)
- [ ] Add persistence/logging for replies awaiting approval (`app/services/google_api.py`, `app/core/config.py`)
- [ ] Schedule periodic fetch (cron-like) and retries (`app/main.py`, `app/core/config.py`)
- [ ] Expose approve-and-send review reply endpoint (`app/routes/gbp_reviews.py`)
- [ ] Tests for auto-reply flow and error handling (`tests/test_gbp_endpoints.py`)

Done when…
- New reviews are detected on schedule, AI replies are generated and stored for approval, approval endpoint publishes via Google API, and tests cover positive/negative cases.

### Auto-Post to GBP Feed
- [ ] Create GBP Post creation endpoint (draft + publish) (`app/routes/gbp_routes.py` or new `app/routes/gbp_posts.py`)
- [ ] Add Google API client methods for GBP Posts (create/update) (`app/services/google_api.py`)
- [ ] Add AI content generation for post title/body and CTAs (`app/services/ai_optimizer.py`)
- [ ] Support scheduled auto-posting with config flags (`app/core/config.py`, `app/main.py`)
- [ ] Validate media handling (images/links) and error logging (`app/services/google_api.py`)
- [ ] Unit tests for post generation and publishing (`tests/test_gbp_endpoints.py`)

Done when…
- A post can be AI-generated, previewed, and published to GBP via API with optional scheduling, with tests verifying payloads and failures.

### WordPress Integration
- [ ] Add HMAC verification middleware for WP → service requests (`app/core/oauth.py` or new middleware module)
- [ ] Endpoints to trigger: Fetch, Analyze, Apply, View Reviews (`app/routes/gbp_fetch.py`, `app/routes/gbp_analyze.py`, `app/routes/gbp_apply.py`, `app/routes/gbp_reviews.py`)
- [ ] Return before/after diffs for preview (`app/services/ai_optimizer.py`)
- [ ] Configurable mapping and field names for WP (`docs/wp_field_map.md`, `app/core/config.py`)
- [ ] Documentation for WP usage and endpoint contracts (`docs/oauth.md`, `docs/google_endpoints.md`)

Done when…
- WP can securely call the microservice to fetch data, run AI optimization, preview diffs, approve and apply updates, and view/approve review replies.

### Deliverables
- [ ] Fetch endpoints (description, services, products, Q&A, reviews) (`app/routes/gbp_fetch.py`, `app/services/google_api.py`)
- [ ] AI optimization prompt layer with fallbacks (`app/services/ai_optimizer.py`, `app/services/ai.py`, `docs/ai_prompts.md`)
- [ ] Apply endpoints for pushing updates (`app/routes/gbp_apply.py`, `app/services/google_api.py`)
- [ ] Review auto-reply mechanism (`app/routes/gbp_reviews.py`, `app/main.py`)
- [ ] WP integration endpoints and docs (`app/routes/`, `docs/wp_field_map.md`, `docs/oauth.md`, `docs/google_endpoints.md`)

Done when…
- All endpoints function against a test GBP account, prompts and docs are present, and tests pass for core flows.


