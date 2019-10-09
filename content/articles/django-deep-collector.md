Title: Django object collector
Date: 2016-07-15 09:32
Category: Tech
Tags: Django, orm
Slug: django-deep-collector
Authors: Romain Garrigues
Summary: Collecting related objects in Django

I was working on a download feature for one of my project: I needed to get all objects that
were related to my user. How can I get all these objects easily?
You can directly have a look at the [github project](https://github.com/iwoca/django-deep-collector) or start by reading this article!

# Django built-in `NestedCollector`

There is a built-in feature in Django that is doing something really close to that: `NestedCollector`.
You have maybe never seen that class, but there is a high chance that you have used it without knowing: when you delete
an entry in the Django admin.
Do you remember that Django is displaying the whole list of objects that will be deleted with the current one if you do it ?

Django is following all reverse foreign key / one-to-one relations to determine which data are related to the one you are deleting
and also delete them, on a recursive way.
For information, you can change the default behaviour (delete `ON_CASCADE`) and you will have to define it explicitly from Django 1.9.

This is nice, but not enough for us, as we also want to get the direct foreign keys and many-to-many relations.

# Django Deep Collector

I have tried to spend some time to extend the `NestedCollector` without a lot of success, so I decided to write a "full" collector from scratch.

The algorithm is quite simple:

1. Start with a given object `A`,
2. Collect all objects that are linked to the object `A`, following all relations (one-to-one, foreign keys and many-to-many) in
   both directions (direct and reverse),
3. For each collected objects, come back to step 2, but `A` is now each of collected objects.

There are some rules/parameters that allows the algorithm to be effective:

- Never collect again an object already collected,
- Disable some models to be collected.
- Disable some relations to be followed.

# Usage

The only thing you have to do is call the `collect` method:

    from deep_collector.core import DeepCollector
    from django.contrib.auth.models import User

    collector = DeepCollector()
    user = User.objects.first()

    # We give "user" as a starting point of this collection
    collector.collect(user)

    # related_objects contains a list of all objects linked to "user"
    related_objects = collector.get_collected_objects()

# Import

If, like me, you wanted to download some data from a website and import it in another one, you can get the collected objects as a serialized json to be directly used by default Django load_data command:

    string_buffer = collector.get_json_serialized_objects()

This string can be saved in a file...

    with open("string_buffer.json") as string_buffer_file:
        string_buffer_file.write(string_buffer)

...and imported in another instance of Django for example (from production to local env):

    manage.py load_data string_buffer.json

You will find more details on the github page of the [project](https://github.com/iwoca/django-deep-collector), feel free to leave any comment/bug/feature request !!
