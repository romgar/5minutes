Title: How to deploy a python package on PyPi with GitHub and travis-ci
Date: 2015-05-05 08:12
Modified: 2015-05-05 08:12
Category: Tech
Tags: GitHub, travis-ci, python, PyPi
Slug: howto-deploy-python-package-on-pypi-with-github-and-travis
Authors: Romain Garrigues
Summary: How to deploy a python package on PyPi with GitHub and travis-ci

You want to make a python package available on PyPi without spending ages to learn how to do it ?

If you are using GitHub to host your project, this article is for you !

Create your setup.py file
=========================

Every python package needs a `setup.py` file to be deployed with `pip`.

You can use a `setup.py` example available on [Django website](https://docs.djangoproject.com/fr/1.8/intro/reusable-apps/) to create yours.

Then, your `GitHub` repository seems like:

    .
    +-- my_python_package <-- The package you want to deploy on PyPi
    +-- setup.py
    +-- README.rst

Configure Travis CI
===================

You need to configure `Tracis CI` to use continuous integration for your `GitHub` repository.

If it's your first time, go to [Tracis CI](http://travis-ci.org/), sign-in with `GitHub`, and activate your `GitHub` repository (`Travis CI` has access to your repositories, but their are disabled by default).

Then add a `.travis.yml` file, on your `GitHub` repository root, with this content:

    language: python

    python:
      - "2.7"

    script:
      - touch foo

For now, your `Travis CI` configuration is executing something totally useless (`touch foo`) on each commit, but usually people are using it to run tests.

Configure PyPi deployment with travis-ci
========================================

Now we also want our project to be deployed on `PyPi`. `Travis CI` can do that for us if we add a `deploy` section in `.travis.yml`, that is now:

    language: python

    python:
      - "2.7"

    script:
      - touch foo

    deploy:
      provider: pypi
      user: romgar
      password:
        secure: my_secure_password
      on:
        tags: true
        branch: master

With that configuration, this project will be deployed on `Pypi` with user `romgar` and password `my_secure_password`, but only when you create (and push) new tags on `master`.

Get PyPi deployment credentials
===============================

The username is the one you have used to register on [Pypi](http://pypi.python.org/). Yes, you have to create an account on `Pypi`.

You also need to generate an encrypted password with `Travis CI` command line client.

To install it (more details on [Travis blog](http://blog.travis-ci.com/2013-01-14-new-client/)):

    $ gem install travis

Maybe you will miss rdoc gem in some cases, depending on your OS. Just install it before:

    $ gem install rdoc

Then encrypt your PyPi password with `travis` cli:

    $ travis encrypt --add deploy.password

The generated password will be automatically added to your `.travis.yml` config file.

Finally
=======

At the end, you have a repository that is automatically deploying a new version of your python package each time you add a new tag on `master` !! Well done.
