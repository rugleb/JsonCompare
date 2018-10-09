import setuptools

with open('README.md', 'r') as fd:
    long_description = fd.read()

setuptools.setup(
    name='comparejson',
    version='0.0.2',
    author='Gleb Karpushkin',
    author_email='rugleb@gmail.com',
    description='JSON comparator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rugleb/jsoncompare',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)