# A Bulma Theme for Django Projects

A Django base theme based on Bulma (bulma.io). Bulma is a modern CSS framework based on Flexbox.

*** work in progress ***

## Installation

1. Install the python package django-bulma from pip

  ``pip install django-bulma``

  Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to INSTALLED_APPS in your ``settings.py``:

  ``'bulma',``

3. You can now extend the bulma theme:

  ```
  {% extends 'bulma/base.html' %}

  {% block title %}Bulma Site{% endblock %}

  {% block content %}
  bla...
  {% endblock content %}

  ```

3. In your templates, load the ``bulma_tags`` library and use the ``|bulma`` filters:

## Example template

  ```django

   {% load bulma_tags %}

   {# Display a form #}

   <form action="/url/to/submit/" method="post">
       {% csrf_token %}
       {% form|bulma %}
       <div class="field">
         <button type="submit" class="button is-primary">Login/button>
       </div>
       <input type="hidden" name="next" value="{{ next }}"/>
   </form>
   ```

## Included templates

**django-bulma** comes with:
* a base template
* registration templates
* account templates

## Documentation

To be done

## Bugs and suggestions

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/timonweb/django-bulma/issues
