FROM python:3.11.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8080

CMD ["python3", "-m", "src.main"]