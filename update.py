name: Update IPTV Playlist

on:
  schedule:
    - cron: '0 0 * * *'  # Ежедневно в 00:00 UTC
  workflow_dispatch:      # Разрешает ручной запуск

permissions:
  contents: write        # Даем права на запись

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      # Шаг 1: Клонируем репозиторий
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      # Шаг 2: Создаем базовый файл если отсутствует
      - name: Create playlist file
        run: |
          if [ ! -f ru.m3u ]; then
            echo "#EXTM3U" > ru.m3u
          fi

      # Шаг 3: Устанавливаем Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # Шаг 4: Запускаем скрипт обновления
      - name: Run update script
        run: |
          pip install requests
          python update.py

      # Шаг 5: Фильтруем нерабочие каналы (ИСПРАВЛЕННЫЙ ШАГ)
      - name: Filter dead channels
        run: |
          sudo apt-get update
          sudo apt-get install -y npm
          npm install -g iptv-checker
          if [ ! -f ru.m3u ]; then
              echo "Error: ru.m3u not found!"
              exit 1
          fi
          iptv-checker --input ru.m3u --output temp.m3u --timeout 3000 || {
              echo "IPTV checker failed, keeping original file"
              cp ru.m3u temp.m3u
          }
          mv temp.m3u ru.m3u

      # Шаг 6: Пушим изменения
      - name: Commit and push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add ru.m3u
          git diff --quiet && git diff --staged --quiet || (git commit -m "Auto-update: $(date +'%Y-%m-%d %H:%M')" && git push origin main)
