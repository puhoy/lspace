from setuptools import setup, find_packages

requirements = [
    "alembic==1.0.10",
    "aniso8601==7.0.0",
    "apispec==2.0.1",
    "attrs==19.1.0",
    "blinker==1.4",
    "certifi==2019.6.16",
    "chardet==3.0.4",
    "Click==7.0",
    "colorama==0.4.1",
    "EbookLib==0.17.1",
    "Flask==1.0.3",
    "Flask-Migrate==2.5.2",
    "flask-restplus==0.12.1",
    "Flask-SQLAlchemy==2.4.0",
    "flask-whooshee==0.7.0",
    "Flask-WTF==0.14.2",
    "gunicorn==19.9.0",
    "html2text==2018.1.9",
    "idna==2.8",
    "isbnlib==3.9.8",
    "itsdangerous==1.1.0",
    "Jinja2==2.10.1",
    "jsonschema==3.0.2",
    "lxml==4.3.4",
    "Mako==1.0.12",
    "MarkupSafe==1.1.1",
    "marshmallow==3.0.0rc9",
    "PyPDF2==1.26.0",
    "pyrsistent==0.15.4",
    "python-dateutil==2.8.0",
    "python-editor==1.0.4",
    "python-slugify==3.0.2",
    "pytz==2019.2",
    "PyYAML==5.1.1",
    "requests==2.22.0",
    "six==1.12.0",
    "SQLAlchemy==1.3.4",
    "text-unidecode==1.2",
    "typing==3.6.6",
    "urllib3==1.25.3",
    "Werkzeug==0.15.4",
    "Whoosh==2.7.4",
    "WTForms==2.2.1",
]

test_requirements = [
    "pytest==4.5.0",
    "pytest-cov==2.7.1",
    "pytest-cover==3.0.0",
    "codecov==2.0.1"
]

dev_requirements = test_requirements + [
    "ipython==7.5.0",
    "doit==0.31.1",
]

setup(
    name='lspace',
    packages=find_packages(),
    include_package_data=True,
    version='0.4.1',
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
