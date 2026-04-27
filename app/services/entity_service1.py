from openai import OpenAI
from app.core.config import OPENAI_API_KEY
from app.utils.prompt_builder import build_entity_prompt
import json
import re

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_username(data):
    brand = data.get("brand") or data.get("primary_entity", "")
    return brand.replace(" ", "").lower()


def extract_json(text: str):
    """
    Cleans AI response and extracts valid JSON
    """
    # remove ```json and ```
    cleaned = re.sub(r"```json|```", "", text).strip()
    return json.loads(cleaned)

def generate_social_links(username: str):
    return {
        "youtube": f"https://www.youtube.com/@{username}",
        "twitter": f"https://twitter.com/{username}",
        "pinterest": f"https://www.pinterest.com/{username}/",
        "reddit": f"https://www.reddit.com/user/{username}/",
        "instapaper": f"https://www.instapaper.com/p/{username}"
    }


def generate_entities(data):
    prompt = build_entity_prompt(data)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content

    print("\n🔥 AI Raw Response:\n", content)

    try:
        result = extract_json(content)
        print("\n✅ Parsed Response:\n", result)

        # 🔥 NEW PART: generate social links
        username = extract_username(result)
        social_links = generate_social_links(username)

        result["social_profiles"] = social_links
        result["sameAs"] = list(social_links.values())

        return result

    except Exception as e:
        print("\n❌ JSON Parse Error:", str(e))
        return {
            "error": "Invalid JSON from AI",
            "raw": content,
            "details": str(e)
        }