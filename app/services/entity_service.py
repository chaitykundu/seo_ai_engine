from openai import OpenAI
from app.core.config import OPENAI_API_KEY
from app.utils.prompt_builder import build_entity_prompt
from app.services.social_service import build_social_profiles

import json
import re

client = OpenAI(api_key=OPENAI_API_KEY)


def extract_json(text: str):
    cleaned = re.sub(r"```json|```", "", text).strip()
    return json.loads(cleaned)


def generate_entities(data):
    prompt = build_entity_prompt(data)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content or ""

    try:
        result = extract_json(content)

        # 🔥 delegate everything else
        result = build_social_profiles(result, data)

        return result

    except Exception as e:
        return {
            "error": "Invalid JSON from AI",
            "raw": content,
            "details": str(e)
        }