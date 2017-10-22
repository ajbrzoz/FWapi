try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'Simple Python API for filmweb.pl',
    'author': 'Anna Brzozowska',
    'url': '',
    'download_url': '',
    'author_email': 'brzozowskaanna5@gmail.com',
    'version': '0.1',
    'install_requires': ['requests', 'beautifulsoup4'],
    'packages': ['fwapi',],
    'scripts': [],
    'name': 'FWapi'
}

setup(**config)