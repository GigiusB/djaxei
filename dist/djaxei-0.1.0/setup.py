# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djaxei']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'djaxei',
    'version': '0.1.0',
    'description': 'A django admin extension for importing exporting records from/to xls/ods',
    'long_description': None,
    'author': 'Giovanni Bronzini',
    'author_email': 'g.bronzini@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7,<4',
}


setup(**setup_kwargs)
