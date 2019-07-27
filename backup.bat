CALL C:\Users\Agarwal\Desktop\venv\Scripts\activate.bat
chdir "C:\Users\Agarwal\Desktop\venv\src"

set name=back_%date:~-7,2%-%date:~-10,2%-%date:~-4,4%.json

echo.
echo It wil take 5 minutes. Sit back and relax

echo.

echo Executing ...
python manage.py dumpdata > E:\backup\%name%

echo.
echo Your backup "%name%" will be avalilabe at "E:\backup\%name%"


exit
