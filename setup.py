from setuptools import setup, find_packages

requirements = [
    "alembic==1.11.1",
    "aniso8601==9.0.1",
    "apispec==6.3.0",
    "attrs==23.1.0",
    "blinker==1.6.2",
    "certifi==2023.5.7",
    "chardet==5.1.0",
    "Click==8.1.4",
    "colorama==version='version='0.4.6''",
    "EbookLib==0.18",
    "Flask==2.3.2",
    "Flask-Migrate==4.0.4",
    "flask-restx==1.1.0",
    "Flask-SQLAlchemy==3.0.5",
    "flask-whooshee==0.9.1",
    "Flask-WTF==1.1.1",
    "gunicorn==20.1.0",
    "html2text==2020.1.16",
    "idna==3.4",
    "isbnlib==3.10.14",
    "itsdangerous==2.1.2",
    "Jinja2==3.1.2",
    "jsonschema==4.18.1",
    "lxml==4.9.3",
    "Mako==1.2.4",
    "MarkupSafe==2.1.3",
    "marshmallow==3.19.0",
    "PyPDF2==3.0.1",
    "pyrsistent==0.19.3",
    "python-dateutil==2.8.2",
    "python-editor==1.0.4",
    "python-slugify==8.0.1",
    "pytz==2023.3",
    "PyYAML==6.0.1",
    "requests==2.31.0",
    "six==1.16.0",
    "SQLAlchemy==2.0.18",
    "text-unidecode==1.3",
    "typing==3.7.4.3",
    "urllib3==2.0.3",
    "Werkzeug==2.3.6",
    "Whoosh==2.7.4",
    "WTForms==3.0.1",
]

test_requirements = [
    "pytest==7.4.0",
    "pytest-cov==4.1.0",
    "pytest-cover==3.0.0",
    "codecov==2.1.13"
]

dev_requirements = test_requirements + [
    "ipython==8.14.0",
    "doit==0.36.0",
    "wheel==0.40.0",
    "twine==4.0.2",
    "build==0.10.0",
    "bump2version==1.0.1"
]

setup(
    name='lspace',
    packages=find_packages(),
    include_package_data=True,
    version='version='version='0.4.6''',
    entry_points={
        'console_scripts': [
            'lspace=lspace:cli'
        ],
    },
    description='ebook manager built around isbnlib',
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
