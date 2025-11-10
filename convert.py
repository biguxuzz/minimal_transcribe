import requests
from pydub import AudioSegment
import os
import tempfile
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

api_key = os.getenv("API_KEY")
url = os.getenv("API_URL")
model = os.getenv("MODEL")

payload = {
    "model": model,
    "response_format": "text",
    "temperature": "0.5",
    "language": "ru"
}

headers = {
    "Authorization": f"Bearer {api_key}"
}

# Загружаем аудиофайл
audio = AudioSegment.from_mp3("audio.mp3")
duration_ms = len(audio)
chunk_duration_ms = 60 * 1000  # 1 минута в миллисекундах

# Разбиваем на части по 1 минуте
chunks = []
for i in range(0, duration_ms, chunk_duration_ms):
    chunk = audio[i:i + chunk_duration_ms]
    chunks.append(chunk)

print(f"Аудио разбито на {len(chunks)} частей")

# Обрабатываем каждую часть
all_transcriptions = []

for idx, chunk in enumerate(chunks):
    print(f"Обработка части {idx + 1}/{len(chunks)}...")
    
    # Сохраняем чанк во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        chunk.export(temp_file.name, format="mp3")
        temp_filename = temp_file.name
    
    try:
        # Отправляем запрос
        with open(temp_filename, 'rb') as audio_file:
            files = {
                'file': (f'chunk_{idx}.mp3', audio_file, 'audio/mp3')
            }
            
            response = requests.post(
                url,
                headers=headers,
                data=payload,
                files=files
            )
            
            print(f"Статус код для части {idx + 1}: {response.status_code}")
            
            if response.status_code == 200:
                all_transcriptions.append(response.text)
            else:
                print(f"Ошибка при обработке части {idx + 1}: {response.text}")
                all_transcriptions.append(f"[Ошибка обработки части {idx + 1}]")
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

# Записываем все транскрипции в файл text.txt
with open('text.txt', 'w', encoding='utf-8') as f:
    for idx, transcription in enumerate(all_transcriptions):
        f.write(f"=== Часть {idx + 1} ===\n")
        f.write(transcription)
        f.write("\n\n")

print(f"Все транскрипции сохранены в text.txt")