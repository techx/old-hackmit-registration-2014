Welcome to the HackMIT website repo!
==========
Dependencies
--------
- virtualenv, npm 

- bower (automatically installed by the install script)

Installation (One time)
-----------
- Git clone the repo (switch branches as appropriate)

- Move into the website folder 
```sh
$ cd website
```

- Run the install script (run with -h to see what it does)
```sh
$ ./install.sh
```

- Activate the venv
```sh
$ source venv/bin/activate
```

Running
-------

- Make sure to have the venv enabled (see above)
```sh
(venv)$  python runserver.py
```

Modules
------------
1. The code is broken up and modularized with flask blueprints, each in their own folder with README info.
2. The current modules are:
    - core - Serves static pages, index pages, etc.
    - auth - Handles accounts and basic user authentication.
    - hackers - Provides the 'hacker' account role and related endpoints.
    - puzzle - This lives in a separate, private repo.
3. Generally speaking, different features should be orthogonalized into separate blueprints. When possible, design for future flexibility and extensibility.

Testing
-----------
1. For testing, use the different config files, the $HACKMIT_FLASK_CONFIG_MODULE environment variable, and ngrok.
