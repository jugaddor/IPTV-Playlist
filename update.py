import requests
from collections import defaultdict

# Источники плейлистов
SOURCES = [
    "https://iptv-org.github.io/iptv/countries/ru.m3u",
    "https://raw.githubusercontent.com/freearhey/iptv/master/channels/ru.m3u"
]

# Категории каналов
CATEGORIES = {
    "Новости": ["news", "новости", "rt", "bbc", "cnn"],
    "Спорт": ["спорт", "sport", "матч", "футбол"],
    "Кино": ["кино", "film", "premiere", "hbo"],
    "Детские": ["cartoon", "мульт", "карусель"]
}

def get_category(channel_name):
    channel_lower = channel_name.lower()
    for cat, keywords in CATEGORIES.items():
        if any(kw in channel_lower for kw in keywords):
            return cat
    return "Другие"

def main():
    all_channels = []
    
    # Загрузка каналов из всех источников
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                all_channels.extend(response.text.splitlines())
        except:
            continue

    # Обработка и группировка
    with open("ru.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U x-tvg-url=\"http://epg.it999.ru/epg2.xml.gz\"\n")
        
        current_group = None
        for i in range(len(all_channels)):
            line = all_channels[i]
            if line.startswith("#EXTINF"):
                channel_name = line.split(",")[-1]
                group = get_category(channel_name)
                
                if group != current_group:
                    f.write(f"\n#EXTGRP:{group}\n")
                    current_group = group
                
                f.write(f"{line}\n{all_channels[i+1]}\n")

if __name__ == "__main__":
    main()
