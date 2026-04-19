#!/bin/sh
# Run the database initialization
python db_management.py

# Start the actual application
exec uvicorn main:app --host 0.0.0.0 --port 8000