python -m venv env
copy ..\pip.ini .\env\pip.ini
echo "Installing"
dir
call ".\env\Scripts\activate.bat"
pip install -r .\requirements.txt twine keyring artifacts-keyring 