from setuptools import setup

setup(
    name = 'punchclock',
    version = '1.0',
    license = 'Apache',
    url = 'http://github.com/Haughar/punchclock',
    description = 'The punchclock/timekeeping app for the team tools app.',
    author = 'Ali Haugh',
    packages = ['punchclock',],
    install_requires = [
        'django',
        'mock==1.0.1',
        'requests',
        'setuptools',
        'django-compressor==1.1.2',
    ],
)
