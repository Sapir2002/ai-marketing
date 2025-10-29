import os
from openai import OpenAI

# Initialize the client using your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def improve_gbp_listing(listing_data: dict):
    """
    Sends the listing data to OpenAI for improvement suggestions.
    """
    prompt = f"""
    You are a Google Business Profile optimization assistant.
    Improve the following business listing data to sound more professional, engaging, and SEO-optimized.
    Respond in valid JSON with the same structure.

    Listing:
    {listing_data}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You improve business listings for Google Business Profiles."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    improved_text = response.choices[0].message.content

    # Parse the model's JSON output
    import json
    try:
        improved_data = json.loads(improved_text)
    except json.JSONDecodeError:
        improved_data = {"error": "Model response not valid JSON", "raw": improved_text}

    return improved_data
