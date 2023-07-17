from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt', 'r') as req:
        content = req.read()
        requirements = content.split('\n')

    return requirements

setup(
    name='hollywood-agent',
    version='0.0.1',
    url='https://github.com/yourusername/hollywood_agent',
    author='Ryan Flynn',
    author_email='ryan@narwh.al',
    description='Client agent for Hollywood Hacker',
    packages=find_packages(),  # automatically find all packages and subpackages
    install_requires=read_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'hollywood-agent=hollywood_agent.main:main',
        ],
    },
)
