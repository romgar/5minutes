Title: factory_boy in depth
Date: 2016-02-25 23:51
Modified: 2016-02-27 10:08
Category: Tech
Tags: Django, tests
Slug: factory-boy-in-depth
Authors: Romain Garrigues
Summary: Using factory_boy on its best way
Status: Draft


What
===
`factory_boy` is a really good library if you need to generate some data quickly, specially focused on testing.

Why
===
Amongst the advantages:
- Well integrated with Django,
- Simplify objects creation,
- Encourage DRY,
- Clean your tests, making them more readable (no need to initialise non-meaningful data),
- Makes every model update easy to also be impacted in your tests,
- So elegant with multiple nested objects.

Why not
===
It's quite hard to find any reason not to use it, as alternatives are suffering the comparison:
- Using Django ORM -> can be fastidious to initialise if a model has a lot of dependencies with other models.
- Fixtures -> have to be constantly updated in case of model changes.

Examples
===
<fkey>
<o2o>
<m2m>

Tips
===

Don't define all fields, only mandatory ones
---
- Better to set fields in tests, than unset the ones that annoy you.
- Make the factories simpler.

Don't create too specific factories, like `UserWithPhoneAndAddressFactory`.
---
At that stage, we can create a function that will deal with calling basic factories.
We don't want as many factories as use cases, or your test complexity will increase.

How to deal with data that has already been created through migrations
---
You should create a factory for them, but they will probably raise an unique constraint error.
Use `django_get_or_create` attribute on those models to manage it.

<example>

