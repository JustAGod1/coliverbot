FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV INSIDE_A_DOCKER True

RUN pip install --upgrade pip
COPY ../requirements.txt /app/
RUN pip install -r requirements.txt

COPY ../.env /app/
COPY .. /app/
RUN chmod +x /app/bot.py

CMD ["python", "/app/bot.py"]