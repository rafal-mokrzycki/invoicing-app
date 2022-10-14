import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="invoicing_app",
    version="0.0.1",
    author="Rafał Mokrzycki",
    author_email="rafal.mokrzycki@interia.pl",
    description="Web Application for Issuing and Storing Invoices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafal-mokrzycki/invoicing_app/",
    packages=setuptools.find_packages(),
    license="Proprietary",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.10",
)
