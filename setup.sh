#/bin/sh

brew install python@3.12
python3.12 -m venv env

source env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
