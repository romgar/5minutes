Title: TransactionTestCase and keepdb issues in Django
Date: 2015-04-22 23:51
Modified: 2015-04-22 23:51
Category: Tech
Tags: Django, database, tests
Slug: transactiontestcase-keepdb-django-issues
Authors: Romain Garrigues
Summary: Using keepdb with TransactionTestCase in Django test suite
Status: draft

Few days ago, I had several issues with some data (from migrations) that were no more in my database after running tests,
even with `--keepdb` option.
Let's see what happened.

Database tests cleaning
---

First, let's summarise how database test cleaning is working in Django.

TestCase
---
If you inherit from TestCase, each test you are writing is wrapped in a transaction (and since Django 1.9, there is also
a transaction wrapping all tests, which makes setUpClass and tearDownClass really useful, specially for test speed).
It means, for each test:

Before: database in state A,
During: you can change some data in your database, which will be in state B,
After: there is a rollback that brings you back to state A.

Neat.

TransactionTestCase
---
If you need to test some specific database behaviours (https://docs.djangoproject.com/en/1.9/topics/testing/tools/#django.test.TransactionTestCase),
you may need to use a TransactionTestCase, that is no more wrapping each test in a transaction.
What happens for each test is:

Before: database in state A,
During: you can change some data in your database, which will be in state B,
After: all tables are emptied (TRUNCATE), your database is in state Z (Zero data).

But then, what happens if you have 2 `TransactionTestCase` that need the same state A ?
The second one will be run with an empty database, which is maybe not what you wanted.

Solution: serialized_rollback option
---
To be sure that your `TransactionTestCase` are not dependent from each others, you can use `serialised_rollback = True` option.

If you use it, at the beginning (`SetUp` step) of each test, Django will load the data coming from initial migrations.
How ? Django is serializing these initial data, and loading them if you ask it.

What will happens then is:

Database initial state: A

First TransactionTestCase with `serialized_rollback = True`:

Pre-setup db state: A
SetUp step: loading initial data -> db in state A (unchanged)
Test: some data created -> db in state B
TearDown step: flushing everything, db in state Z

Second TransactionTestCase with `serialized_rollback = True`:

Pre-setup db state: Z (cleaned by previous TransactionTestCase)
SetUp step: loading initial data -> db in state A
Test: some data created -> db in state B
TearDown step: flushing everything, db in state Z

Nice !

But there are still some issues, even with this option.

Contraints errors
---
If you are working with Django 1.7.x/1.8.x, you have maybe encountered this error 'IntegrityError: duplicate key value violates unique constraint "django_content_type_app_label_<some_hex>_uniq"'
There is a StackOverflow thread about that http://stackoverflow.com/questions/29226869/django-transactiontestcase-with-rollback-emulation/35359897 that I recommand you to read carefully.

A patch has been created and shipped with django 1.9.x (https://github.com/django/django/commit/d3fdaf907db6a5be4d0391532d7e65688c19e851)
But if, like me, you can't really afford to work on latest stable version of Django, you can add a setting
`TEST_NON_SERIALIZED_APPS = ['django.contrib.contenttypes']`

Database empty at the end of the test run suite, even with --keepdb option
---
If you want to keep the database for future tests with —keepdb option, the last TransactionTestCase run will still delete all the data in the database.
There is an opened ticket related to that issue: https://code.djangoproject.com/ticket/25251

Finally, after all these tests, I can keep my TransactionTestCase tests and my data are still in the database \o/



