@echo off
echo ======================================
echo        AUTO-MAGIC FOR WINDOWS
echo ======================================

python -m venv venv

call venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

echo   
echo  Setup complete!
echo   
pause
