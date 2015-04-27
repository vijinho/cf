try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'CF',
    'author': 'Vijay Mahrra',
    'url': 'https://github.com/vijinho/cfchallenge',
    'download_url': 'https://github.com/vijinho/cfchallenge',
    'author_email': 'vijay.mahrra@gmail.com',
    'version': '1.0',
    'install_requires': ['nose','future', 'click', 'rethinkdb', 'cython', 'falcon', 'gunicorn', 'librabbitmq'],
    'packages': ['cf'],
    'scripts': [],
    'name': 'cf'
}

setup(**config)
