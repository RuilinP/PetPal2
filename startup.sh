python3 -m venv venv
source venv/bin/activate
pip install -r packages.txt
python3 manage.py makemigrations
python3 manage.py migrate
