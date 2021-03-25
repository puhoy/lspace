from setuptools import setup, find_packages

requirements = [
    "alembic==1.3.2",
    "aniso8601==8.0.0",
    "apispec==3.1.1",
    "attrs==19.3.0",
    "blinker==1.4",
    "certifi==2019.11.28",
    "chardet==3.0.4",
    "Click==7.0",
    "colorama==0.4.3",
    "EbookLib==0.17.1",
    "Flask==1.1.1",
    "Flask-Migrate==2.5.2",
    "flask-restplus==0.13.0",
    "Flask-SQLAlchemy==2.4.1",
    "flask-whooshee==0.7.0",
    "Flask-WTF==0.14.2",
    "gunicorn==20.0.4",
    "html2text==2019.9.26",
    "idna==2.8",
    "isbnlib==3.9.10",
    "itsdangerous==1.1.0",
    "Jinja2==2.10.3",
    "jsonschema==3.2.0",
    "lxml==4.4.2",
    "Mako==1.1.0",
    "MarkupSafe==1.1.1",
    "marshmallow==3.3.0",
    "PyPDF2==1.26.0",
    "pyrsistent==0.15.6",
    "python-dateutil==2.8.1",
    "python-editor==1.0.4",
    "python-slugify==4.0.0",
    "pytz==2019.3",
    "PyYAML==5.4",
    "requests==2.22.0",
    "six==1.13.0",
    "SQLAlchemy==1.3.12",
    "text-unidecode==1.3",
    "typing==3.7.4.1",
    "urllib3==1.25.7",
    "Werkzeug==0.16.0",
    "Whoosh==2.7.4",
    "WTForms==2.2.1",
]

test_requirements = [
    "pytest==5.3.2",
    "pytest-cov==2.8.1",
    "pytest-cover==3.0.0",
    "codecov==2.0.15"
]

dev_requirements = test_requirements + [
    "ipython==7.10.2",
    "doit==0.32.0",
]

setup(
    name='lspace',
    packages=find_packages(),
    include_package_data=True,
    version='0.4.2',
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
    ],
)
