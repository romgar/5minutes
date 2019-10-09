Title: Migrations on monkey-patched Django core model
Date: 2016-02-25 23:51
Modified: 2016-02-27 10:08
Category: Tech
Tags: Django, migrations
Slug: migrations-monkey-patched-model
Authors: Romain Garrigues
Summary: How to manage migrations of monkey-patched Django core models
Status: Draft

I was in charge of a Django upgrade from 1.4 to 1.8 on a quite big project, and one big step was to switch from south
to Django built-in migrations.
There were several challenges, but one of them was to create the proper migrations for 2 models we have currently
monkey-patched: `User` and `Site`.

The problem
===
With the new-style migrations framework, what happens if you run `makemigrations` with these 2 models monkey-patched ?
It will generate a migration with our change for both `User` and `Site` in ... django lib repository !


First idea: create a custom migration
===
The idea was to create a migration with a `RunPython` function to use `schema_editor` to manually write the changes
provoked by our monkey-patching.

    def manual_update(apps, schema_editor):
        schema_editor.add_field(User, last_password_changed, ...)

    class CustomMigration(migrations.Migration):

        dependencies = []
        operations = [
            migrations.RunPython(manual_update)
        ]

That works, the migrations are correctly applied and `makemigrations` is no more generating migrations in django lib
folder !
But...

    def manual_update(apps, schema_editor):
        schema_editor.add_field(User, last_password_changed, ...)

        User = apps.get_model('auth', 'User')
        user = User.objects.all().first()
        user.last_password_changed = True

        # BOOM: last_password_changed is not a field of User
        user.save()

    class CustomMigration(migrations.Migration):

        dependencies = []
        operations = [
            migrations.RunPython(manual_update)
        ]

Yep, `schema_editor` has done its job on the database side, but definitely not everything we needed.


Second try: use migrated app folder
===
From Django 1.?, we can specify in which folder an app will look for its migrations.
Sounds nice to give a try: let's Django generate the proper migrations for the monkey-patched models in its own folder,
then copy/paste all migrations related to `auth` and `site` apps in our own folder.

    MIGRATED_APPS = {
        'auth': 'our_custom_folder.auth_migrations',
        'site': 'our_custom_folder.site_migrations',
    }

With this file system:

    .
    +-- my_custom_app
    +-- settings.py
    +-- our_custom_folder
    |   +-- auth_migrations
    |   |   +-- 0001_initial.py } Copied from Django core django.contrib.auth.migrations folder
    |   |   +-- [...]
    |   +-- site_migrations
    |   |   +-- 0001_initial.py } Copied from Django core django.contrib.sites.migrations folder
    |   |   +-- [...]

Now `makemigrations` is working as expected, and we can also update our `last_password_changed` field in migrations.

This is still not a perfect solution, as I will have to keep these migrations up-to-date with django core ones, but
that's the best compromise I found so far.

I will probably remove the monkey-patching on these models at some point, but that requires some extra work, and a Django
upgrade from an LTS to another one is enough work :-)
