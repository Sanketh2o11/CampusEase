FROM python:3.11-slim

# Install system deps required by mysqlclient (works on all platforms via Docker)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source is bind-mounted at runtime; this COPY is for image completeness
COPY . .

RUN chmod +x entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
