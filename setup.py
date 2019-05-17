from setuptools import setup, find_packages

requirements = [
    "alembic==1.0.10",
    "blinker==1.4",
    "Click==7.0",
    "colorama==0.4.1",
    "EbookLib==0.17.1",
    "Flask==1.0.2",
    "flask-marshmallow==0.10.1",
    "Flask-Migrate==2.4.0",
    "Flask-SQLAlchemy==2.4.0",
    "flask-whooshee==0.7.0",
    "html2text==2018.1.9",
    "isbnlib==3.9.8",
    "itsdangerous==1.1.0",
    "Jinja2==2.10.1",
    "lxml==4.3.3",
    "Mako==1.0.10",
    "MarkupSafe==1.1.1",
    "marshmallow==2.19.2",
    "marshmallow-sqlalchemy==0.16.3",
    "PyPDF2==1.26.0",
    "python-dateutil==2.8.0",
    "python-editor==1.0.4",
    "python-slugify==3.0.2",
    "PyYAML==5.1",
    "six==1.12.0",
    "SQLAlchemy==1.3.3",
    "text-unidecode==1.2",
    "Werkzeug==0.15.4",
    "Whoosh==2.7.4",
]

dev_requirements = [
    "ipython==7.5.0",
    "doit==0.31.1"
]

setup(
    name='lspace',
    packages=find_packages(),
    include_package_data=True,
    version='0.1.4',
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
        'dev': dev_requirements
    },
    install_requires=requirements
)
