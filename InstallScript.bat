@echo off
echo Installing necessary Python libraries...

:: Update pip
python -m pip install --upgrade pip

:: Install libraries listed in requirements.txt
if exist requirements.txt (
    echo Installing libraries from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found, installing libraries manually...

    :: List your libraries here
    pip install csv
    pip install os
    pip install time
    pip install platform
    pip install rich
    pip install pandas
    pip install click

    :: Add any other libraries you need below
)

echo All libraries have been installed.


:: Execute main.py
python "main.py"

pause
