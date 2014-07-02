Registration System
============

Dependencies
--------
- virtualenv, npm 

Install bower (globally) (if you haven't already): 
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

- Install dependencies (in the venv/locally)
```sh
$ pip install -r requirements.txt
$ bower install
$ bower install viewport-units-buggyfill
```

Running
-------

- Make sure to have the venv enabled (see above)
```sh
(venv)$  python app.py
```
