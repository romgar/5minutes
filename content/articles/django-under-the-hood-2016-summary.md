Title: Django Under the Hood 2016 summary
Date: 2016-11-07 19:32
Category: Tech
Tags: Django Conference
Slug: django-under-the-hood-2016-summary
Authors: Romain Garrigues
Summary: Django Under the Hood 2016 summary

I attended this year [DjangoUnderTheHood](https://www.djangounderthehood.com/), an event hosted in Amsterdam. This is a highly technical conference focussed on the Django web framework. Talks are usually given by Django core developers, or experienced people, which means there are always interesting talks to hear. DjangoUnderTheHood is probably the best event to meet Django core developers, this year there were 20+ gathered for this event.

The event in itself is held in a nice place, [Pakhuis de Zwijger](https://www.google.co.uk/maps/place/Pakhuis+De+Zwijger/@52.3768451,4.9221174,15z/data=!4m2!3m1!1s0x0:0x2d9e404fc8f71f8d?sa=X&ved=0ahUKEwjgufLsyq_PAhVBK8AKHSloCKAQ_BIIgQEwDQ), which is starting to become too small as the number of attendees increases over the years (this was the third annual conference).

The format is quite unusual, with only 9 talks of 1 hour each, which leave the speakers enough space to dive deeply under the hood of Django.

Here we go for the talks!

# Channels

The first talk started by explaining the goal of this project, which is one of the most exciting in the Django ecosystem.

The original idea - to open Django to the non-http-request-response cycle - is an impressive ambition, defining the equivalent of WSGI in an asynchronous world: ASGI.

This ambition would cover more than what everyone had hoped for - web sockets in Django - by generalising this approach to other protocols, and not sticking closely to the Django project.

So now, we have a ASGI norm that some web servers can stick to - like [Daphne](https://github.com/django/daphne) - and that can handle different protocols, like HTTP and web sockets. Channels is the adapter that allows Django to communicate with an ASGI-compatible server and make HTTP requests AND web sockets possible without any extra effort.

In production, you can even keep your traditional gunicorn - or anything else you already have - stack for http requests, and let your load-balancer redirect the web sockets’ requests to Daphne. This lets you begin slowly without any risk.

Plans are to extend the already implemented protocols with email / Slack (XMPP?), and have more than Daphne as ASGI servers.

# Testing

Another topic I'm always curious about, as my way of testing has improved (hopefully!) during the past years...

The speaker told us some history about test classes used in Django over years.

It was nice to have a quick reminder of when using SimpleTestCase (no database access), TransactionTestCase (database + transactions), TestCase (database), LiveServerTestCase (live server for integration tests with Selenium for example) and [StaticLiveServerTestCase](https://docs.djangoproject.com/en/1.10/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase)</a> (no need anymore for collectstatic? interesting...).

Some other tips, always useful, were given:

- don't forget MIRROR parameter in your test settings if you want to create test databases for your replica,
- use @tag to group your tests, so that you can run tests with only a specific tag, or exclude it,
- think about setUpTestData if you have several tests that need the same set of data, not altered during these tests.

coverage was also a part of the talk, with an accurate reminder about "low coverage is bad, but high coverage is not ensuring anything".

But this time, the speaker talked about an interesting alternative: "mutation testing".

The idea is to mutate your code at test runtime, for example an AND-condition changed to OR-condition. The mutation library (mutpy) will then consider the tests that were passing and failing when mutated as good, and the ones that don't change their status as bad.

That gives then a percentage of mutation that you can correlate with your percentage of coverage to increase code trust, which sounds interesting if you want to detect which parts of your system are less reliable.

# Debugging

This talk was about slow request debugging.

A complex stack is involved every time an end-user accesses our website, from the redirects (?), AppCache, DNS resolution, TCP transfer, Request handling, Response result, browser processing, ...

A non-intuitive statistic showed that only 10-20% of the request is spent on the backend stack. It gives food for thought to invest some time on DNS - CDN configuration, and on HTML/CSS/JavaScript loading.

Going through the different states of document.readyState, and understanding the dependencies between DOM building, CSSOM building and JavaScript execution seems essential for efficient optimisations on the front-end side.

That reminds me to spend a bit of time in the future to go a bit more deeply into it.

He also gave us some insights about the server-side:

- use pgbench,
- list_select_related in Django admin to prefetch some fields and avoid query spamming,
- think that ForeignKey nullable or not can change the type of JOIN (nullable - LEFT OUTER, non-null - INNER),
- iterator() on query can save Django model instantiation,

# Mental health

Definitely a habit from Django conference, people are talking about their mental illness. This time, a psychologist was telling her own story being bipolar, and gave crazy statistics. Following them, almost half of the room in Amsterdam was anxious and taking medication for that, almost 10% bipolar. Hopefully that’s just about statistics, and it’s well-known that the Django community is much more mentally sane than other ones ;-).

I definitely think well-being is a serious matter and can help people to work in a better way. We also improved our well-being at iwoca over time, from a much better onboarding process to the activities organised to ease communication.

If you are in a situation where you feel bad, find somebody to talk to. Sounds naive. But it works. Really. Do it.

[Devpressed](https://devpressed.com)

# Validation

Did you already ask yourself where you should validate data in the whole Django stack?

Between the front-end (html/js validation), the view, the form (clean\* methods), the model (save/full_clean) and the database (have a look at CHECK keyword), there are a lot of different ways to validate the data coming from an user/external system.

There is no perfect way to do it. You should play with a mix of all these layers, depending on how critical your data are used for, and what are your business perspectives. And databases constraints/checks are still the best way to be sure that you won’t finish with crappy data in your database.

I heard that some Djangonauts were trying to think about an uniform data serialisation to improve the current situation, but it's still more an idea than anything concrete.

# Javascript

This Javascript-only talk was a summary of the current JavaScript ecosystem. I will spare you the traditional tools (node, npm, grunt/gulp, ...), but it's still nice to have heard about:

- Babel: indispensable library to enjoy ECMA6 enhancements (sugar syntax, arrow functions, ...) and be still compatible with ECMA5,
- A new - faster - alternative to npm named [YARN](https://github.com/yarnpkg/yarn) from Facebook,
- The JavaScript PEP8 equivalent named [StandardJS](http://standardjs.com/rules.html),
- While [mypy](http://mypy-lang.org/) seems to gain some popularity amongst python lovers, [Flow](https://flowtype.org/) and [TypeScript](https://www.typescriptlang.org/) are the most popular type checking libraries in JavaScript,
- Webpack and its [hot module replacement](https://webpack.github.io/docs/hot-module-replacement.html)</a>.

# Database backend

If you have ever thought about creating your own database backend to make the ORM work with other databases than SQLite, MySQL, PostgreSQL and Oracle (the 4 officially supported databases), the creator of django-mssql - backend for Microsoft SQL Server - explained how to create a new backend.

And the conclusion of this talk was: "do it only if you really have to do it". Achieving this kind of project is really complex, complicated and lead to a lot of hacks to take into account the database you want to make compatible with the Django ORM.

# Django @ Instagram

This talk was just brilliant. Funny, technical, high-level and deep explanations, probably the best talk of the conference for me.

The speaker talked about the system evolution from the first months to nowadays:

- Started with a classic Django stack,
- Written a custom ORM to manage sharded queries across PostgreSQL databases,
- Added memcached with each PostgreSQL database,
- Used pg_queue for multi-region cache invalidation (each PostgreSQL - memcached couple should sync with all other couples),
- Integrated Tao (Facebook MySQL + memcached custom stack),
- Migrated from Django 1.3 to 1.8 (making their project 1.3 AND 1.8 compatible to make the switch seamless),
- Full stack being: Proxygen, Django/WSGI, TAO, Cassandra, Everstore, Celery/RabbitMQ,

A part of the talk was related to performance measures, aiming to maximise the servers utilisation (user per server as the main metric).

They were also using Django middlewares to grab samples of production data to measure the system performances, through cProfile, Cython, …

# Sprints

After this day and a half of intense talks, 2 days of sprints were organised to contribute to Django or other open-source projects.

The venue (ImpactHub) was quite nice and calm.

That was the perfect occasion for me to discuss about my pending tickets related to TransactionTestCase and [--keepdb](https://code.djangoproject.com/ticket/25251) option (patch [on its way](https://github.com/django/django/pull/7528)), and [--parallel](https://code.djangoproject.com/ticket/26822) issues. And as expected, the issues are progressing so much when you can discuss directly with the person, instead of back and forth on GitHub merge requests. Refreshing and motivating!

I had the chance to bring up a not-yet-realistic idea of building a tool to help for Django upgrades. This project - codename [django-seven](https://github.com/iwoca/django-seven) - aims to ease the process of upgrading your Django project from a version to another one, by making your code compatible with both version. It still needs a proof of concept, but several people from the Django core team have shown an interest in it. Let's try something!

I can't wait for next Django conference!!
