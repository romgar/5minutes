Title: TransactionTestCase and keepdb issues in Django
Date: 2016-02-25 23:51
Modified: 2016-02-27 10:08
Category: Tech
Tags: Django, database, tests
Slug: transactiontestcase-keepdb-django-issues
Authors: Romain Garrigues
Summary: Using keepdb with TransactionTestCase in Django test suite

Few days ago, I had several issues with some data (from migrations) that were no more in my database after running tests,
even with `--keepdb` option.
Let's see what happened, but before that, here is a quick reminder of how database test cleaning is working in Django.

TestCase
========
If you inherit from TestCase, each test you are writing is wrapped in a transaction (and since Django 1.9, there is also
a transaction wrapping all tests, which makes setUpClass and tearDownClass really useful, specially for test speed).
It means, for each test:

    - Before: database in state A,
    - During: you can change some data in your database, which will be in state B,
    - After: there is a rollback that brings you back to state A.

Neat.

TransactionTestCase
===================
If you need to test some [specific database behaviours](https://docs.djangoproject.com/en/1.9/topics/testing/tools/#django.test.TransactionTestCase),
you may need to use a `TransactionTestCase`, that is no more wrapping each test in a transaction.
What happens for each test is:

    - Before: database in state A,
    - During: you can change some data in your database, which will be in state B,
    - After: all tables are emptied (TRUNCATE), your database is in state E (Empty).

But then, what happens if you have 2 `TransactionTestCase` that need the same initial state A ?
The second one will be run with an empty database, which is maybe not what you wanted.

serialized_rollback option
==========================
To be sure that your `TransactionTestCase` are not dependent from each others, you can use `serialised_rollback = True` option.

If you use it, at the beginning (`SetUp` step) of each test, Django will load the data coming from initial data migrations.

What will happens then is:

    - Database initial state: A

    - First TransactionTestCase with `serialized_rollback = True`:

        - Pre-setup db state: A
        - >>> SetUp step: loading initial data -> db in state A (unchanged) <<<
        - Test: some data created -> db in state B
        - TearDown step: flushing everything, db in state E

    - Second TransactionTestCase with `serialized_rollback = True`:

        - Pre-setup db state: E (cleaned by previous TransactionTestCase)
        - >>> SetUp step: loading initial data -> db in state A <<<
        - Test: some data created -> db in state C
        - TearDown step: flushing everything, db in state E

Nice !

*But there are still some issues, even with this option.*

Issue 1: Constraints errors
===========================
If you are working with Django 1.7.x/1.8.x, you have maybe encountered this error:

    IntegrityError: duplicate key value violates unique constraint "django_content_type_app_label_<some_hex>_uniq"

There is a [StackOverflow thread](http://stackoverflow.com/questions/29226869/django-transactiontestcase-with-rollback-emulation/35359897) about this topic.

A [patch](https://github.com/django/django/commit/d3fdaf907db6a5be4d0391532d7e65688c19e851) has been created and shipped with django 1.9.x.
But if, like me, you can't always work with latest stable version of Django, you can add a setting:

    TEST_NON_SERIALIZED_APPS = ['django.contrib.contenttypes']

Issue 2: Empty database at the end of the tests, even with --keepdb option
==========================================================================
If you want to keep the database for future tests with `-—keepdb` option, the last `TransactionTestCase` run will still delete all the data in the database.
There is an [open ticket](https://code.djangoproject.com/ticket/25251) related to that issue.

I have proposed a [solution](https://github.com/django/django/pull/6137) that resolves this problem by updating where we load the initial data.

    - Database initial state: A

    - First TransactionTestCase with `serialized_rollback = True`:

        - Pre-setup db state: A
        - Test: some data created -> db in state B
        - TearDown step: flushing everything, db in state E
        - >>> Post-TearDown step: loading initial data -> db in state A <<<

    - Second TransactionTestCase with `serialized_rollback = True`:

        - Pre-setup db state: A (loaded after the last flush from previous `TransactionTestCase`)
        - Test: some data created -> db in state C
        - TearDown step: flushing everything, db in state E
        - >>> Post-TearDown step: loading initial data -> db in state A <<<

Finally, after all these tests, I can keep my `TransactionTestCase` tests and my data are still in the database. Victory.
