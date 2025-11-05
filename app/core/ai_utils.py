# app/core/ai_utils.py
import os
from typing import Any, Dict, List

def _mock_analyze(data: Dict[str, Any]) -> Dict[str, Any]:
    desc = data.get("description")
    improved_desc = None
    if desc:
        improved_desc = {
            "original": desc,
            "improved": f"{desc} — Now with faster booking and friendly service.",
            "notes": "mock",
        }

    replies: List[Dict[str, Any]] = []
    for r in data.get("reviews", []):
        replies.append(
            {
                "reviewId": r.get("reviewId"),
                "reply": "Thank you for your review! We appreciate you.",
                "tone": "friendly",
            }
        )

    return {
        "description": improved_desc,
        "services": data.get("services", []),
        "products": data.get("products", []),
        "qna": data.get("qna", []),
        "reviewReplies": replies,
    }

def improve_gbp_listing(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns optimized GBP content.
    - Uses MOCK_AI=1 (default) to avoid external calls during tests/dev.
    - If MOCK_AI=0 and a valid OPENAI_API_KEY is present, calls OpenAI.
    """
    use_mock = os.getenv("MOCK_AI", "1") == "1"
    api_key = os.getenv("OPENAI_API_KEY", "")

    # Mock by default or when no real key is present
    if use_mock or not api_key or api_key.startswith("sk-your_"):
        return _mock_analyze(data)

    # --- Real provider path (only used if you unset MOCK_AI and provide a real key) ---
    try:
        from openai import OpenAI  # type: ignore
        client = OpenAI(api_key=api_key)

        prompt = (
            "You are optimizing Google Business Profile content. "
            "Return concise improved text and friendly replies."
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Data JSON:\n{data}\n\nImprove briefly."},
        ]
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            messages=messages,
        )
        improved_text = resp.choices[0].message.content or ""

        # Keep the shape the tests expect; this is a simplistic example.
        return {
            "description": {
                "original": data.get("description"),
                "improved": improved_text[:300],  # trim
                "notes": "openai",
            },
            "services": data.get("services", []),
            "products": data.get("products", []),
            "qna": data.get("qna", []),
            "reviewReplies": [],
        }
    except Exception:
        # Fallback to mock if anything fails
        return _mock_analyze(data)
