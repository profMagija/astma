import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="astma",
    version="0.0.1",
    author="Nikola Bebić",
    author_email="prof@magija.rs",
    description="A Simple Text Mode App Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/profMagija/astma",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)