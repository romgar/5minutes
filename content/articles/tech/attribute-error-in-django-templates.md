Title: AttributeError management in Django templates
Date: 2016-02-25 23:51
Modified: 2016-02-27 10:08
Category: Tech
Tags: Django, template
Slug: attribute-error-django-templates
Authors: Romain Garrigues
Summary: How Django is managing AttributeError in template engine
Status: Draft

I came across a singular problem in my production environment which was provoking some template rendering to break.
Some AttributeError were raised and `500` errors resulted.
I precise that this behaviour didn't happen with the previous version of Django we were using (1.4 before, 1.8 now).
This also happens only if you are not in debug mode (setting `DEBUG = False`, `TEMPLATE_DEBUG = False`).

How was it before Django 1.?
===
AttributeError were swallowed when raised in a template rendering.

How is it as of Django 1.?
===
AttributeError are raised like any other exception (check it).

So, if you want to not impact your production environment with these changes if you upgrade your Django version, you
can catch AttributeError and re-raise it with a custom Exception that sets the parameter `silent_template_error` to `True`.

