Title: TransactionTestCase and keepdb issues in Django
Date: 2015-04-22 23:51
Modified: 2015-04-22 23:51
Category: Tech
Tags: Django, database, tests
Slug: transactiontestcase-keepdb-django-issues
Authors: Romain Garrigues
Summary: Using keepdb with TransactionTestCase in Django test suite
Status: draft

Before that, summarise how database test cleaning is working in Django:
TestCase: each test is in a transaction, everything is rollback at the end.
Database status: untouched from before the test.

TransactionTestCase: There is a TRUNCATE on all tables at the end of the test
Database status: before, X data in your db (coming from initial data migrations, if any), after, nothing.

Problem: if another test after this transaction test case needs the initial data, they are been flushed.

1/ Solution: serialized_rollback option
You can then use serialised_rollback option to change this behaviour.
The idea is,
TransactionTestCase: the serialised content of initial database will be loaded at the beginning your test
So even if a previous TransactionTestCase has flushed the database, then this one has all the informations he need.

Problem1: (django 1.7-1.8) http://stackoverflow.com/questions/29226869/django-transactiontestcase-with-rollback-emulation/35359897
There are some constraint errors, fixed in a patch deployed in django 1.9.x (https://github.com/django/django/commit/d3fdaf907db6a5be4d0391532d7e65688c19e851)
Can be avoided in previous versions by using TEST_NON_SERIALIZED_APPS = ['django.contrib.contenttypes', 'django.contrib.auth']

Problem2: If you want to keep the database for future tests with —keepdb option, the last TransactionTestCase run will still delete all the data in the database…
I have proposed a patch for that: https://code.djangoproject.com/ticket/25251#comment:5

Finally, after all these tests, I can keep my TransactionTestCase tests and my data are still in the database \o/



