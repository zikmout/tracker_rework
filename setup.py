from setuptools import setup, find_packages

requires = [
    'tornado',
    'psycopg2-binary',
    'sqlalchemy',
    'werkzeug',
    'redis',
    'ujson',
    'uuid',
    'pandas',
    'lxml',
    'bs4',
    'requests',
    'pdfminer.six',
    'xlrd',
    'celery'
]

setup(
    name='pintell',
    version='0.0',
    description='Data miner crawling bot',
    author='simon sicard',
    author_email='simon.sicard@gmail.com',
    keywords='crawling scrapping data mining ai content extracting',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'serve_app = pintell:main',
            'initdb = pintell.scripts.initialize_db:main',
            'reset_db = pintell.scripts.reset_db:main'
        ],
    },
)