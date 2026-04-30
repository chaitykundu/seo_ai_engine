def build_entity_prompt(data):
    return f"""
You are an advanced SEO Entity Intelligence System.

Your job is to analyze input (keyword or website URL) and generate structured SEO entities.

INPUT:
- Keyword: {data.keyword}
- Web URL: {data.web_url}

TASK:
1. Detect user intent:
   - commercial (buying/searching services)
   - informational (learning)
   - navigational (brand search)

2. Infer business type if not explicitly given.

3. Generate SEO entities based on meaning, not just words.

4. Expand into search engine entities:
   - services
   - industry
   - audience
   - related search terms
   - local SEO variations (if location exists)

RULES:
- Do NOT copy input blindly.
- Think like Google search engine.
- Be specific, not generic.
- Avoid repeating same entities.

OUTPUT FORMAT:
Return ONLY valid JSON. No markdown. No explanations.

{{
  "primary_entity": "",
  "brand": "",
  "intent": "",
  #"location": "",
  "services": [],
  "industry": [],
  "audience": [],
  "related_entities": []
}}
"""