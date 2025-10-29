from openai import OpenAI
import os

# Initialize client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def improve_gbp_listing(data: dict):
    """
    Use GPT to enhance Google Business Profile content.
    """
    prompt = f"""
    You are an expert in writing Google Business Profile content.
    Improve the following business listing details to make them more appealing and professional.

    Business description:
    {data.get("description", "N/A")}

    Services:
    {data.get("services", "N/A")}

    Products:
    {data.get("products", "N/A")}

    Q&A:
    {data.get("qna", "N/A")}

    Reviews:
    {data.get("reviews", "N/A")}

    Return improved text in JSON format with the same structure.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful business profile optimizer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
