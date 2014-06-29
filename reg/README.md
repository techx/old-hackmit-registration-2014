Registration System
============

Dependencies
--------
- virtualenv, flask, npm, bower 

Install bower (if you haven't already): 
```sh
$ npm install -g bower
```

Installation (One time)
-----------
- Git clone the repo (switch branches as appropriate)

- Create a new venv
```sh
$ virtualenv venv
```

- Activate the venv
```sh
$ source venv/bin/activate
```

- Install flask in your venv
```sh
$ pip install flask
```

- Install dependencies
```sh
$ pip install -r requirements.txt
$ bower install
```

- Create a db by running a python shell in the reg folder and executing:
```python
from app import db
db.create_all()
```

Running
-------

```sh
$ source path/to/venv/bin/activate
(venv)$  python app.py
```
