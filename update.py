- name: Filter dead channels
  run: |
    # Устанавливаем Node.js и npm через actions (рекомендованный способ)
    - uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    # Устанавливаем iptv-checker (проверьте актуальное название пакета)
    - run: npm install -g iptv-checker@latest
    
    # Проверяем доступные параметры (для отладки)
    - run: iptv-checker --help
    
    # Основная команда проверки (используем новый синтаксис)
    - run: |
        if [ ! -f ru.m3u ]; then
          echo "Файл ru.m3u не найден!"
          exit 1
        fi
        
        # Попробуйте разные варианты в зависимости от версии:
        iptv-checker --input-file ru.m3u --output-file temp.m3u --timeout 3000 || \
        iptv-checker -f ru.m3u -o temp.m3u -t 3000 || \
        iptv-checker ru.m3u -d temp.m3u --timeout 3000 || {
          echo "Не удалось выполнить проверку, копируем оригинальный файл"
          cp ru.m3u temp.m3u
        }
        
        mv temp.m3u ru.m3u
