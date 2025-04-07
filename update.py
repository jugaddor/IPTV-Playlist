import requests
sources = [
    "https://iptv-org.github.io/iptv/countries/ru.m3u",
    "https://raw.githubusercontent.com/freearhey/iptv/master/channels/ru.m3u"
]
with open("ru.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for url in sources:
        try: f.write(requests.get(url).text + "\n")
        except: pass
