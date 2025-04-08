- name: Filter dead channels
  run: |
    # Устанавливаем необходимые пакеты
    sudo apt-get update
    sudo apt-get install -y ffmpeg
    
    # Используем ffprobe для проверки ссылок
    while IFS= read -r line; do
      if [[ "$line" == http* ]]; then
        if ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$line" > /dev/null 2>&1; then
          echo "$line"
        fi
      else
        echo "$line"
      fi
    done < ru.m3u > temp.m3u
    
    mv temp.m3u ru.m3u
