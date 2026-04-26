# Use Slim for better compatibility with FastAPI/Pydantic wheels
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install SQLite and any basic system utilities
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

RUN mkdir -p sqlitedb
RUN mkdir -p tables

# Expose the port FastAPI will run on
EXPOSE 8000

CMD ["bash", "entrypoint.sh"]