Welcome to the 2014 HackMIT Repo
==========
Let's lay out some ground rules...
-----------
1. Pull Requests can come from either branches or forks, but branch is preferred.
2. The .gitignore ignores */config and *.pyc. Do not modify the .gitignore without notifying everyone, consequently, all code reviewers should verify this before accepting a pull. This could cause both headaches and a potential leak of private keys -- no bueno.
3. Push a false-valued version of the config files suffixed with .def
4. Before committing or pushing ask yourself...
    - Did I add all the files I meant to? (git status)
    - Do I have a clear-cut message on what I am committing?
    - Am I on the right branch


Files/Subprojects
------------
1. Each Subproject should have its own readme, with instructions on how to run it.
2. The current subprojects are:
    - reg - Regestration system, excluding puzzle code. Puzzle code should live in a private repo

