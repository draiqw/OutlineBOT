# Используем официальный образ Python (3.9-slim)
FROM python:3.9-slim

# Отключаем запись pyc-файлов и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект (включая папку bots и файл users.db)
COPY . /app/

# Запускаем скрипт бота (находится в папке bots)
CMD ["python", "bot/main.py"]
