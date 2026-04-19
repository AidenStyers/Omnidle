Build backend: docker build -t backend .  
Run backend: docker run -d -p 8000:8000 -v <current directory>/sqlitedb:/app/sqlitedb --name backend backend