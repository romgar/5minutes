Title: Django collector for objects related to a given one
Date: 2016-02-25 23:51
Modified: 2016-02-27 10:08
Category: Tech
Tags: Django, orm
Slug: django-deep-collector
Authors: Romain Garrigues
Summary: Collecting related objects in Django
Status: Draft

I was working on an anonymisation feature for one of my project when I realised that I needed to update all objects that
were related to my user.
How to get all these objects then ?

Django built-in `NestedCollector`
===
There is a built-in feature in Django that is doing something really close to that: `NestedCollector`.
You have maybe never seen that class, but there is a high chance that you have used it without knowing: when you delete
an entry in the Django admin.
Do you remember that Django is displaying the whole list of objects that will be deleted with the current one if you do it ?

<screenshot>

Django is following all reverse foreign key / one-to-one relations to determine which data are related to the one you are deleting
and also delete them, on a recursive way.
For information, you can change the default behaviour (delete `ON_CASCADE`) and you will have to define it explicitly from Django 1.?

This is nice, but not enough for us, as we also want to get the direct foreign keys and many-to-many relations.

Django Deep Collector
===
I have tried to spend some time to extend the `NestedCollector` without a lot of success, so I decided to write a "full" collector
from scratch.

The algorithm is quite simple:
1. Start with a given object `A`,
2. Collect all objects that are linked to the object `A`, following all relations (one-to-one, foreign keys and many-to-many) in
both directions (direct and reverse),
3. For each collected objects, come back to step 2, but `A` is now each of collected objects.

There are some rules/parameters that allows the algorithm to be effective:
- Never collect again an object already collected,
- Disable some models to be collected.
- Disable some relations to be followed.

Usage
===
The only thing you have to do is call the `collect` method:

    from deep_collector.core import RelatedObjectsCollector
    from django.contrib.auth.models import User

    user = User.objects.all()[0]
    collector = RelatedObjectsCollector()

    # We give "user" as a starting point of this collection
    collector.collect(user)

    # related_objects contains a list of all objects linked to "user"
    related_objects = collector.get_collected_objects()





