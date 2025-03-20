FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


COPY . .

# # Install Docker CLI and dependencies 
# RUN apt-get update && apt-get install -y \
#     docker.io \
#     && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["uvicorn", "main:main", "--host", "0.0.0.0", "--port", "8000"]