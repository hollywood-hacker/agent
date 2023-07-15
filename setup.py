from setuptools import setup

setup(
    name='worker',
    version='1.0',
    py_modules=['worker'],
    install_requires=[
        'configparser',
        'keyboard',
        'flask',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'worker = worker:main',
        ],
    },
)
