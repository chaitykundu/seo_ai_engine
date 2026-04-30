import requests
from bs4 import BeautifulSoup


def extract_social_links_from_website(url: str):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a", href=True)

        social_links = {}

        for link in links:
            href = link["href"]

            if "linkedin.com" in href: 
                social_links["linkedin"] = href
            elif "github.com" in href:
                social_links["github"] = href
            elif "twitter.com" in href:
                social_links["twitter"] = href
            elif "youtube.com" in href:
                social_links["youtube"] = href

        return social_links

    except Exception:
        return {}