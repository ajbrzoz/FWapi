try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'Simple Python API for filmweb.pl',
    'author': 'Anna Brzozowska',
    'url': 'https://github.com/ajbrzoz/FWapi',
    'download_url': '',
    'author_email': 'brzozowskaanna5@gmail.com',
    'version': '0.2',
    'install_requires': ['requests', 'beautifulsoup4'],
    'packages': find_packages,
    'scripts': [],
    'name': 'FWapi'
}

setup(**config)