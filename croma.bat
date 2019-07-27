CALL "C:\Users\Agarwal\Desktop\venv\Scripts\activate.bat"

chdir "C:\Users\Agarwal\Desktop\venv\src"

START chrome http://127.0.0.1:8000

python server.py

PAUSE 1000