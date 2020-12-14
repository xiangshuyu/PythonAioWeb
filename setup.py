from setuptools import setup, find_packages

setup(
    name='AsyncWeb',
    version='1.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'resource': ['db/*', 'font/*', 'templates/*'],
    },
    python_requires='>=3.6'
)

# python3 setup.py bdist_egg : build a python package
# python3 setup.py install : install the package to the python3 dist-packages
