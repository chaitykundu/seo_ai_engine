def build_entity_prompt(name, business_type, location):
    return f"""
You are an SEO entity generation expert.

Business Name: {name}
Business Type: {business_type}
Location: {location}

Generate structured SEO entities.

Return ONLY JSON:
{{
  "primary_entity": "",
  "brand": "",
  "location": "",
  "services": [],
  "industry": [],
  "audience": [],
  "related_entities": []
}}
"""