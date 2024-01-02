import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().split("\n")

setuptools.setup(
    name="textfab",
    version="0.2.0",
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
    install_requires=requirements,
    include_package_data=True,
)
