from openai import OpenAI
from app.core.config import OPENAI_API_KEY
from app.utils.prompt_builder import build_entity_prompt
import json
import re
import requests

client = OpenAI(api_key=OPENAI_API_KEY)


# ✅ Clean username generator
def extract_username(data):
    brand = data.get("brand") or data.get("primary_entity", "")
    username = re.sub(r'[^a-zA-Z0-9]', '', brand).lower()
    return username or "defaultname"


# ✅ Clean JSON extractor
def extract_json(text: str):
    """
    Cleans AI response and extracts valid JSON
    """
    cleaned = re.sub(r"```json|```", "", text).strip()
    return json.loads(cleaned)


# ✅ YouTube profile checker (REAL validation)
def check_youtube_profile(username: str):
    url = f"https://www.youtube.com/@{username}"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return {
                "url": url,
                "status": "exists"
            }
        else:
            return {
                "url": url,
                "status": "not_found"
            }
    
    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "details": str(e)
        }


# ✅ Social link generator (with validation)
def generate_social_links(username: str):
    return {
        "youtube": check_youtube_profile(username),  # ✅ validated
        "twitter": {
            "url": f"https://twitter.com/{username}",
            "status": "generated"
        },
        "pinterest": {
            "url": f"https://www.pinterest.com/{username}/",
            "status": "generated"
        },
        "reddit": {
            "url": f"https://www.reddit.com/user/{username}/",
            "status": "generated"
        },
        "instapaper": {
            "url": f"https://www.instapaper.com/p/{username}",
            "status": "generated"
        }
    }


# ✅ Main function
def generate_entities(data):
    prompt = build_entity_prompt(data)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content or ""

    print("\n🔥 AI Raw Response:\n", content)

    try:
        result = extract_json(content)
        print("\n✅ Parsed Response:\n", result)

        # 🔥 Generate username
        username = extract_username(result)

        # 🔥 Generate social links
        social_links = generate_social_links(username)

        # Attach to result
        result["social_profiles"] = social_links

        # # ✅ Fix sameAs (extract URLs properly)
        # result["sameAs"] = [
        #     v["url"] if isinstance(v, dict) else v
        #     for v in social_links.values()
        # ]

        return result

    except Exception as e:
        print("\n❌ JSON Parse Error:", str(e))
        return {
            "error": "Invalid JSON from AI",
            "raw": content,
            "details": str(e)
        }