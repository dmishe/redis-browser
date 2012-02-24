from setuptools import setup

setup(
    name='redis_browser',
    version='0.1',
    description='simple browser for your redis db',
    packages=['redis_browser'],
    include_package_data=True,
    zip_safe=False,
    scripts = ['redis_browser/bin/redis-browser.py'],
    install_requires=[
        'flask',
        'redis'
        ]
)