# A Bulma Theme for Django Projects

<a href="https://github.com/timonweb/django-bulma"><img src="https://raw.githubusercontent.com/timonweb/django-bulma/master/demo/static/images/django-bulma-logo.png" alt="Django Bulma"></a>

A Django base theme based on Bulma (<a href="https://bulma.io/">bulma.io</a>). Bulma is a modern CSS framework based on Flexbox.

*** work in progress ***

## Installation

1. Install the python package django-bulma from pip

  ``pip install django-bulma``

  Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to INSTALLED_APPS in your **settings.py**:

  `'bulma',`

3. If you want to use the provided base template, extend from **bulma/base.html**:

  ```
  {% extends 'bulma/base.html' %}

  {% block title %}Bulma Site{% endblock %}

  {% block content %}
    Content goes here...
  {% endblock content %}

  ```
  
4. If you want to customize bulma sass and your own components:

    4.1 Copy bulma static files into your project's **STATIC_ROOT**:

    ```
    python manage.py copy_bulma_static_into_project
    ```  
    You should see **bulma** dir appeared in your **STATIC_ROOT**. It contains
    three dirs:
    * **lib** - where we put original and untouched bulma package, in most cases
    you shouldn't mess with it
    * **sass** - this is the place where you can put your own sass code and customize
    bulma variables
    * **css** - this is where compiled sass output goes, you should link this file
    in your base.html 

    4.2 Install npm packages for sass compilation to work:    
    
    ```
    python manage.py bulma install
    ```
    
    4.3 Start sass watch mode:
    ```
    python manage.py bulma start
    ```

5. For forms, in your templates, load the `bulma_tags` library and use the `|bulma` filters:

    ##### Example template
    
    ```django

    {% load bulma_tags %}

    {# Display a form #}

    <form action="/url/to/submit/" method="post">
       {% csrf_token %}
       {% form|bulma %}
       <div class="field">
         <button type="submit" class="button is-primary">Login</button>
       </div>
       <input type="hidden" name="next" value="{{ next }}"/>
    </form>
    ```

## Included templates

**django-bulma** comes with:
* a base template
* registration templates
* account templates

## Bugs and suggestions

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

[https://github.com/timonweb/django-bulma/issues](https://github.com/timonweb/django-bulma/issues)
