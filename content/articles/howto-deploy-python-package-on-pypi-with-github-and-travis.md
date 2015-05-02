Title: How to deploy a python package on PyPi with GitHub and travis-ci
Date: 2015-05-02 15:11
Modified: 2015-05-02 15:11
Category: Tech
Tags: GitHub, travis-ci, python, PyPi
Slug: howto-deploy-python-package-on-pypi-with-github-and-travis
Authors: Romain Garrigues
Summary: How to deploy a python package on PyPi with GitHub and travis-ci

You want to make a python package available on PyPi without spending ages to learn how to do it ? If you are using GitHub, it will be really fast !

Create your setup.py file
=========================

Every python package needs a `setup.py` file to describe it to python world.

You can use the `setup.py` example file available on [Django website](http://djangoproject.org/) to initialize yours.

Then, you just need to have this folder tree:

    .
    +-- my_python_package <-- The package you want to deploy on PyPi
    +-- setup.py
    +-- README.rst

Configure travis-ci
===================

You need to configure `travis` to automatically launch continuous integration on each commit on your repository.

Add a `.travis.yml` file at folder root with this content:

    language: python

    python:
      - "2.7"

    script:
      - touch foo

For now, your travis config is just executing something totally useless (`touch foo`) on each commit, but usually people are running project tests.

Configure PyPi deployment with travis-ci
========================================

Now we also want our project to be deployed on PyPi. `travis-ci` can do that for us if we add a `deploy` section:

    deploy:
      provider: pypi
      user: romgar
      password:
        secure: my_secure_password
      on:
        tags: true
        branch: master

With that configuration, I want my project to be deployed on `Pypi` with user `romgar` and password `my_secure_password`, but only when I create tags on `master`.

Get PyPi deployment credentials
===============================

The username is the one you have used to register on [Pypi](http://pypi.python.org/). Yes, you have to create an account on Pypi.

For the password, you need to generate an encrypted one with a tool named `travis-cli`.

To install it:

    $ gem install travis-cli

Maybe you will miss rdoc gem in some cases, depending on your OS. Just install it before:
    $ gem install rdoc

Then encrypt your PyPi password with travis cli:
    $ travis encrypt deploy.password

The generated password will be automatically added to your `.travis.yml` config file.

Finally
=======

At the end, you have a repository that is automatically deploying a new version of your python package each time you add a new tag on `master` !! Well done.
