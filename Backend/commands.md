Build backend: docker build -t backend .  
Run backend: docker run -d -p 8000:8000 -v <current directory>/sqlitedb:/app/sqlitedb --name backend backend
Test receive_game_results: curl.exe -X POST "http://localhost:8000/game-results?guesses=3"
Fast API Docs at: http://localhost:8000/docs#/