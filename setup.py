import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-librus-api",
    version="0.2.0",
    author="Tomasz Nieżurawski",
    author_email="tomek.niezurawski@gmail.com",
    description="A librus api made in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheAmazingRak/py-librus-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)