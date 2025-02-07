# Используем официальный образ CUDA runtime от NVIDIA (подберите версию, подходящую для вашего проекта)
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Переменная для неинтерактивной установки пакетов
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем системные зависимости, включая Python 3, pip, ffmpeg и другие библиотеки
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    ffmpeg \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip
RUN python3 -m pip install --upgrade pip

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем остальной код проекта
COPY . .

# Задаём переменную окружения для использования GPU с индексом 0
ENV CUDA_VISIBLE_DEVICES=0
ENV fastapi_port=${fastapi_port}

EXPOSE ${fastapi_port}

# По умолчанию запускаем FastAPI (можно переопределить через docker-compose)
CMD ["uvicorn", "main_fastapi:app", "--host", "0.0.0.0", "--port", "${fastapi_port}", "--reload"]
