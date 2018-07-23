import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='EnORM',
    version='0.1.0',
    author='Nima Bavari (Tural Mahmudov)',
    author_email='nima.bavari@gmail.com',
    description='EnDATA Object Relational Mapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NimaBavari/EnORM',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent'
    )
)
