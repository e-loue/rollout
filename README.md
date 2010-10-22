# rollout

Rollout is a django application that allows one to easily
release new features to a subset of users.

Still very much a work in progress.

# Dependencies

rollout requires [django](http://www.djangoproject.com), [redis-py](http://github.com/andymccurdy/redis-py) and [proclaim](http://github.com/asenchi/proclaim) to work.

# Usage

Basically one would use this app to split their Django project up into
features that you can roll out to individuals, groups or a percentage of
users.  Many sites implement a similar strategy to catch bugs or see how
new features are received.

Option 1:

    {% proclaim "feature1" %}
        ... handy new feature of your site ...
    {% endproclaim %}

Option 2:

    {% proclaim "feature1" "path/to/template.html" %}

From the command line, add a percentage of users to 'feature1':

This will allow every fifth user to see "feature1":
    $ python manage.py proclaim "feature1" --percentage="20" --activate

Add a group to feature2:
    $ python manage.py proclaim "feature2" --group=Admins --activate

See which target is active for "feature3":
    $ python manage.py proclaim "feature3"
    >>> Group: Admins

You can always just use the
[proclaim](http://github.com/asenchi/proclaim) in your `views.py` or
`models.py` to target specific users with new features.
