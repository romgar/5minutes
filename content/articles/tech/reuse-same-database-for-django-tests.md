Title: Reuse the same database for django test suite
Date: 2015-04-22 23:51
Modified: 2015-04-22 23:51
Category: Tech
Tags: Django, database
Slug: reuse-same-db-django-tests
Authors: Romain Garrigues
Summary: Reuse the same database for django test suite
Status: draft

You are using django test command, and are annoyed because it takes time for django to create/delete the database on each test suite running (and also apply every `south` migration you have ?).

Since Django 1.8
================
A new `test` option, named `--keepdb`, appears in Django 1.8 to avoid this. The same database is then reused on each test running.

Before Django 1.8
=================
Before Django 1.8, there is no built-in solution for now.

I have then spend some time to see exactly how Django was managing the database creation/deletion, and created a `Django` app to reuse the same database for people that can't upgrade for now to 1.8

