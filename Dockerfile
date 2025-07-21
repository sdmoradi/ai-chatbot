FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app
COPY docs /app/data

# Run ingest and then start app
CMD ["sh", "-c", "python ingest.py && uvicorn app:app --host 0.0.0.0 --port 8000 --log-level debug"]