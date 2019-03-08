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
    'celery',
    'cython',
    'fastText',
    'cld2-cffi',
    'pdftotext'
]

setup(
    name='tracker',
    version='0.0',
    description='Data miner crawling bot',
    author='simon sicard',
    author_email='simon.sicard@gmail.com',
    keywords='crawling scrapping data mining ai content extracting',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'serve_app = tracker:main',
            'initdb = tracker.scripts.initialize_db:main',
            'reset_db = tracker.scripts.reset_db:main'
        ],
    },
)