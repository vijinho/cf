try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'CF',
    'author': 'Vijay Mahrra',
    'author_email': 'vijay.mahrra@gmail.com',
    'maintainer': 'Vijay Mahrra',
    'maintainer_email': 'vijay.mahrra@gmail.com',
    'contact': 'Vijay Mahrra',
    'contact_email': 'vijay.mahrra@gmail.com',
    'url': 'https://github.com/vijinho/cf',
    'download_url': 'https://github.com/vijinho/cf',
    'version': '1.0',
    'keywords': ['rethinkdb','falcon','celery','rabbitmq','gunicorn','currency','cf'],
    'install_requires': ['nose','future', 'click', 'rethinkdb', 'cython', 'falcon', 'gunicorn', 'librabbitmq', 'celery'],
    'packages': ['cf'],
    'scripts': [],
    'name': 'cf'
}

setup(**config)
