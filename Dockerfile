FROM python:3.9-slim

WORKDIR /app

# System deps (optional but safe for many python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Production start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
