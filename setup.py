from setuptools import setup, find_packages

setup(
    name='hollywood-agent',
    version='0.0.1',
    url='https://yourprojecturl.com',
    author='Your Name',
    author_email='your-email@example.com',
    description='Description of your project',
    packages=find_packages(),    
    install_requires=[],
    entry_points={
        'console_scripts': [
            'hollywood-agent=hollywood_agent:main',
        ],
    },
)
