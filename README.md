# Minimal Transcribe

Простой скрипт для транскрибации аудиофайлов с использованием API Cloud.ru (Whisper Large V3).

## Установка

1. Создайте и активируйте виртуальное окружение:

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **Linux/macOS:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Установите FFmpeg (необходим для работы с аудио):
   - Windows: скачайте с [ffmpeg.org](https://ffmpeg.org/download.html) или используйте `choco install ffmpeg`
   - Linux: `sudo apt install ffmpeg` или `sudo yum install ffmpeg`
   - macOS: `brew install ffmpeg`

## Настройка

1. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

2. Откройте `.env` и укажите свои значения:
```
API_KEY=your_api_key_here
API_URL=https://foundation-models.api.cloud.ru/v1/audio/transcriptions
MODEL=openai/whisper-large-v3
```

Переменные:
- `API_KEY` - ваш API ключ для доступа к Cloud.ru API
- `API_URL` - URL эндпоинта для транскрибации
- `MODEL` - модель для транскрибации (по умолчанию `openai/whisper-large-v3`)

## Предподготовка файла для транскрибации

Перед транскрибацией необходимо конвертировать аудио/видео файл в формат MP3. Используйте FFmpeg:

```bash
ffmpeg -i 'запись_встречи.mkv' -vn -acodec libmp3lame -ab 192k audio.mp3
```

Параметры команды:
- `-i 'запись_встречи.mkv'` - входной файл
- `-vn` - отключить видео (только аудио)
- `-acodec libmp3lame` - кодек для MP3
- `-ab 192k` - битрейт аудио (192 кбит/с)
- `audio.mp3` - выходной файл

Результирующий файл `audio.mp3` должен находиться в корне проекта.

## Использование

Запустите скрипт:
```bash
python convert.py
```

Скрипт автоматически:
1. Разобьет аудиофайл на части по 1 минуте
2. Отправит каждую часть на транскрибацию
3. Сохранит результат в файл `text.txt`

## Структура проекта

```
.
├── convert.py          # Основной скрипт транскрибации
├── requirements.txt    # Зависимости Python
├── .env               # Конфигурация (не коммитится)
├── .env.example       # Шаблон конфигурации
├── audio.mp3         # Входной аудиофайл
└── text.txt          # Результат транскрибации
```

