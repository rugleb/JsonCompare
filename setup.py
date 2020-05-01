import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="jsoncomparison",
    version="1.0.1",
    author="Gleb Karpushkin",
    author_email="rugleb@gmail.com",
    description="JSON comparator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rugleb/jsoncomparison",
    download_url="https://pypi.org/project/jsoncomparison",
    packages=setuptools.find_packages(),
    keywords=[
        "json",
        "compare",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
