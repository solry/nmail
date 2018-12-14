import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nmail",
    version="0.0.3",
    author="Roman Solyanik",
    author_email="solyanikry@gmail.com",
    description="One-line SMPT email sender",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/solry/nmail",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)