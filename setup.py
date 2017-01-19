from setuptools import setup

setup(  name='datadotworld',
        version='0.1',
        description='Python client library for data.world',
        url='http://github.com/datadotworld/data.world-py',
        author='Rebecca Clay',
        author_email='rebecca.clay@data.world',
        license='Apache 2.0',
        packages=['datadotworld'],
        install_requires=['pandas'],
        zip_safe=False)
