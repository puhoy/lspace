from setuptools import setup, find_packages

requirements = [
    "alembic==1.8.1",
    "aniso8601==8.0.0",
    "apispec==3.1.1",
    "attrs==19.3.0",
    "blinker==1.4",
    "certifi==2019.11.28",
    "chardet==3.0.4",
    "Click==8.0.3",
    "colorama==0.4.3",
    "EbookLib==0.17.1",
    "Flask==2.0.3",
    "Flask-Migrate==2.5.2",
    "flask-restx==0.5.1",
    "Flask-SQLAlchemy==2.5.1",
    "flask-whooshee==0.8.2",
    "Flask-WTF==1.0.0",
    "gunicorn==20.1.0",
    "html2text==2020.1.16",
    "idna==3.3",
    "isbnlib==3.10.9",
    "itsdangerous==2.0.1",
    "Jinja2==3.0.3",
    "jsonschema==3.2.0",
    "lxml==4.9.1",
    "Mako==1.1.0",
    "MarkupSafe==2.0.1",
    "marshmallow==3.14.1",
    "PyPDF2==1.27.5",
    "pyrsistent==0.15.6",
    "python-dateutil==2.8.1",
    "python-editor==1.0.4",
    "python-slugify==4.0.0",
    "pytz==2021.3",
    "PyYAML==5.4",
    "requests==2.27.0",
    "six==1.13.0",
    "SQLAlchemy==1.4.31",
    "text-unidecode==1.3",
    "typing==3.7.4.1",
    "urllib3==1.26.8",
    "Werkzeug==2.0.3",
    "Whoosh==2.7.4",
    "WTForms==3.0.1",
]

test_requirements = [
    "pytest==7.0.1",
    "pytest-cov==3.0.0",
    "pytest-cover==3.0.0",
    "codecov==2.1.12"
]

dev_requirements = test_requirements + [
    "ipython==8.0.1",
    "doit==0.34.1",
    "wheel==0.37.1",
    "twine==3.8.0"
]

setup(
    name='lspace',
    packages=find_packages(),
    include_package_data=True,
    version='0.4.5',
    entry_points='''
        [console_scripts]
        lspace=lspace.app:cli_group
    ''',
    description='a ebook manager built around isbnlib',
    url='https://github.com/puhoy/lspace',
    author='jan',
    author_email='stuff@kwoh.de',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    extras_require={
        'dev': dev_requirements,
        'test': test_requirements
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
