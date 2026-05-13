# Use Slim for better compatibility with FastAPI/Pydantic wheels
FROM python:3.11-slim as base

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

# Copy all needed files in base directory
# Add onto this list as mroe fiels are required
# Folders will be mounted via the compose file
COPY entrypoint.sh .
COPY main.py .
COPY db_management.py .


# Expose the port FastAPI will run on
EXPOSE 8000

CMD ["bash", "entrypoint.sh"]

# --- Stage 2: Test (Only used for testing) ---
FROM base as test-env
# Install testing only packages
COPY test_requirements.txt .
RUN pip install --no-cache-dir -r test_requirements.txt


