import re
from urllib.parse import unquote

def extract_urls(text):
    """Extract Discord promo URLs from text content"""
    url_pattern = re.compile(r'https?://[^\s"<>]+', re.IGNORECASE)
    urls = url_pattern.findall(text)

    filtered_urls = []
    for url in urls:
        decoded_url = unquote(url).lower()

        if (
            "discord.gg" in decoded_url or
            "promos.discord.gg" in decoded_url or
            "/nitro" in decoded_url or
            "discord.com/nitro" in decoded_url or
            "discordapp.com/nitro" in decoded_url
        ):
            filtered_urls.append(url)

    return filtered_urls
