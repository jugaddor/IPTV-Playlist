import requests
from collections import defaultdict

SOURCES = [
    "https://iptv-org.github.io/iptv/countries/ru.m3u",
    "https://raw.githubusercontent.com/freearhey/iptv/master/channels/ru.m3u"
]

# Словарь для категорий (можно редактировать)
CATEGORIES = {
    "новости": ["news", "rt", "bbc", "cnn"],
    "спорт": ["sport", "матч", "футбол"],
    "кино": ["кино", "film", "premiere"],
    "детские": ["cartoon", "мульт", "карусель"]
}

def categorize_channel(name):
    name = name.lower()
    for cat, keywords in CATEGORIES.items():
        if any(kw in name for kw in keywords):
            return cat
    return "другое"

def process_playlist():
    channels = defaultdict(list)
    
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=10)
            for line in response.text.splitlines():
                if line.startswith('#EXTINF'):
                    name = line.split(',')[-1]
                    category = categorize_channel(name)
                    channels[category].append(f"{line}\n{next(response.iter_lines()).decode()}")
        except Exception as e:
            print(f"Error: {e}")

    with open("ru.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U x-tvg-url=\"http://epg.it999.ru/epg2.xml.gz\"\n")
        for category, items in channels.items():
            f.write(f"\n#EXTGRP:{category}\n")
            f.write("\n".join(items))
            
process_playlist()
