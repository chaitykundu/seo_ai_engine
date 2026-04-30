import re
import requests
from app.services.scraper_service import extract_social_links_from_website


from urllib.parse import urlparse

def extract_username_from_url(url: str):
    if not url:
        return None

    # ✅ Case 1: YouTube (@username)
    match = re.search(r'@([a-zA-Z0-9_]+)', url)
    if match:
        return match.group(1)

    # ✅ Case 2: Domain-based portfolio
    parsed = urlparse(url)
    domain = parsed.netloc  # chaitykundu.netlify.app

    domain = domain.replace("www.", "")

    # remove hosting/domain suffix
    domain = domain.replace(".netlify.app", "")
    domain = domain.replace(".vercel.app", "")
    domain = domain.replace(".github.io", "")
    domain = domain.replace(".com", "")

    return domain


def extract_username(data):
    brand = data.get("brand") or data.get("primary_entity", "")
    username = re.sub(r'[^a-zA-Z0-9]', '', brand).lower()
    return username or "defaultname"


def generate_social_links(username: str):
    return {
        "youtube": f"https://www.youtube.com/@{username}",
        "twitter": f"https://twitter.com/{username}",
        "pinterest": f"https://www.pinterest.com/{username}/",
        "reddit": f"https://www.reddit.com/user/{username}/",
        "instapaper": f"https://www.instapaper.com/p/{username}"
    }


def build_social_profiles(result, data):
    # 1. extract username from URL first
    username = extract_username_from_url(getattr(data, "web_url", None))

    # 2. fallback to AI data
    if not username:
        username = extract_username(result)

    # 3. generate links
    generated = generate_social_links(username)

    # 4. scrape real links
    real_links = {}
    if getattr(data, "web_url", None):
        real_links = extract_social_links_from_website(data.web_url)

    # 5. merge (real overrides generated)
    final_links = {**generated, **real_links}

    result["social_profiles"] = final_links
    # result["sameAs"] = [
    #     v if isinstance(v, str) else v.get("url", v)
    #     for v in final_links.values()
    # ]

    return result