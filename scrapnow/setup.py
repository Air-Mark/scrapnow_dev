import sys

from pip._internal.req import parse_requirements
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

PACKAGE_TYPE = 'scrapnow_dev'
PACKAGE_NAME = 'scrapnow'
PACKAGE_DESC = 'scrapnow'
PACKAGE_LONG_DESC = ''
PACKAGE_VERSION = '0.1.0'


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = (
            '--flake8 {0} tests '
            '--junitxml=.reports/{0}_junit.xml '
            '--cov={0} --cov=tests '
            '-p no:logging'.format(
                PACKAGE_NAME.replace('-', '_')
            )
        )

    def run_tests(self):
        import shlex
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


install_requires = [
    str(ir.requirement) for ir in
    parse_requirements('requirements.txt', session=False)
]

tests_require = [
    str(ir.requirement) for ir in
    parse_requirements('test-requirements.txt', session=False)
]

console_scripts = [
    'scrapnow_runner=scrapnow.service_runner:main',
    'scrapnow_alembic=scrapnow.alembic_runner:main',
]

setup(
    name='{}'.format(PACKAGE_NAME),
    version=PACKAGE_VERSION,
    description=PACKAGE_DESC,
    long_description=PACKAGE_LONG_DESC,
    url='https://github.com/Air-Mark/{}/{}'.format(PACKAGE_TYPE, PACKAGE_NAME),
    author="Mark Trifonov",
    author_email="air.t.mark@gmail.com",
    license="Nodefined",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Framework :: Pytest',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Information Technology',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.8',
        'Topic :: Microservices',
    ],
    zip_safe=False,
    packages=find_packages(exclude=['tests', 'examples', '.reports']),
    entry_points={'console_scripts': console_scripts},
    python_requires='>=3.8',
    setup_requires=[],
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={},
    cmdclass={'test': PyTest}
)
