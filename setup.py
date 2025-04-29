import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="textfab",
    version="1.1.0",
    author="Igor Buyanov",
    author_email="buyanov.igor.o@yandex.ru",
    description="A tiny library for text preprocessing in NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Astromis/textfab",
    project_urls={
        "Bug Tracker": "https://github.com/Astromis/textfab/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["pymystem3>=0.2.0",
                      "nltk>=3.6.7",
                      "omegaconf>=2.3.0",
                      "pandas>=1.3.4"],
    include_package_data=True,
)
