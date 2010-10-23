# rollout

Rollout is a django application that allows one to easily release new features to a subset of users.

## Dependencies

rollout requires [django](http://www.djangoproject.com), [redis-py](http://github.com/andymccurdy/redis-py) and [proclaim](http://github.com/asenchi/proclaim) to work.

## Usage

Basically one would use this app to split their Django project up into  features that you can roll out to individuals, groups or a percentage of users. Many sites implement a similar strategy to catch bugs or see how new features are received.

#### Option 1:

    {% rollout "newfeature" %}
     ... handy new feature of your site ...
    {% endrollout %}

#### Option 2:

    {% rollout "newfeature" "path/to/template.html" %}

From the command line, add a percentage of users to '_newfeature_':

    $ python manage.py rollout newfeature --percentage=20 --activate

Add a group to '_secretfeature_':

    $ python manage.py rollout "secretfeature" --group=Admins --activate

You can always just use the rollout in your `views.py` or `models.py` to target specific users with new features.

    from rollout import rollout
    rollout.activate_percentage("nextfeature", 20)
    rollout.deactivate_user("nextfeature", request.user)

