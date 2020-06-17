# Winged Messenger Blog

A blog application started at a DjangoGirls' event using Python and Django. Built and maintained until now, inflicting my thoughts on the internet.

## Where to find it ##

You can see the blog online at https://naeglinghaff.pythonanywhere.com/

It will also shortly be available at katewriting.co.uk.

## Running code locally

Clone this repo and then in the root directory:

```
python manage.py migrate
python manage.py runserver
```

To run the tests

```
python manage.py test blog.tests
```

To see an accurate representation of coverage, run the coverage report separately (coverage.py loads in the models too soon hence the differing results)
```
coverage run --source='.' ./manage.py test blog.tests
coverage report
```

## Additions and technologies used:

* bootstrap and custom CSS
* security protocols with Dotenv
* testing with unittest
* ckeditor for custom input to blog post form
* paginate for multiple page list views
* virtualenv for package management
* sentry for monitoring production errors
* continuous deployment with heroku
