from setuptools import setup

setup(
    name='elib',
    version='0.1',
    py_modules=['elib'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        lib=elib.app:cli_group
    ''',
)