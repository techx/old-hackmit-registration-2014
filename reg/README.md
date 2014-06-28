Registration System
============

Dependencies
--------
- Flask and others

Installation (One time)
-----------
- Git clone the repo (switch branches as appropriate)
- Create a new venv with 'virtualenv venv'
- Activate the venv with '. venv/bin/activate' or 'source venv/bin/activate'
- Install dependencies with 'pip install -r requirements.txt'
- Create a db by running a pythong shell in the reg folder and executing:
    - 'from app import db'
    - 'db.create_all()'

Running
-------
```python app.py```
