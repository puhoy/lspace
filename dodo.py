from doit.tools import PythonInteractiveAction


def task_build():
    return {
        'targets': ['build', 'dist', 'lspace.egg-info', '.pytest_cache', 'htmlcov'],
        'actions': ['rm -fr %(targets)s', 'python3 -m build'],
        'clean': ['rm -fr %(targets)s'],
        'verbosity': 2
    }


def task_bump_dryrun():
    return {'actions': ['bump2version --verbose --dry-run --allow-dirty %(part)s'],
            'params': [{'name': 'part',
                        'long': 'part',
                        'type': str,
                        'choices': (('patch', ''), ('minor', ''), ('major', '')),
                        'default': False,
                        'help': 'Choose between patch, minor, major'}],
            'verbosity': 2, }


def task_bump():
    return {'actions': ['bump2version --verbose %(part)s'],
            'params': [{'name': 'part',
                        'long': 'part',
                        'type': str,
                        'choices': (('patch', ''), ('minor', ''), ('major', '')),
                        'default': False,
                        'help': 'Choose between patch, minor, major'}],
            'verbosity': 2, }


def task_release_pypi():
    def confirm():
        res = input('running release on NON-test pypy!\n'
                    'remember to install from a build to test if everytihng is included!\n'
                    'is the version bumped and everything commited and pushed?\n'
                    'everything tested?\n'
                    '[yesanditsnotatest/OHMYGODNO] ')
        if res != 'yesanditsnotatest':
            raise Exception

    return {
        'task_dep': ['build'],
        'actions': [
            (PythonInteractiveAction(confirm)),
            'twine upload --verbose --disable-progress-bar --repository pypi dist/*'],
        'verbosity': 2
    }


def task_release_test_pypi():
    def confirm():
        res = input('running release on test pypy!\n'
                    '[yes/NO] ')
        if res != 'yes':
            raise Exception

    return {
        'task_dep': ['build'],
        'actions': [
            (PythonInteractiveAction(confirm)),
            'twine upload --verbose --disable-progress-bar --repository testpypi dist/*'],
        'verbosity': 2,
    }
