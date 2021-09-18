import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="text-conveyer-astromis",
    version="0.0.1",
    author="Igor Buyanov",
    author_email="buyanov.igor.o@yandex.ru",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Astromis/preprocess_conveyer",
    project_urls={
        "Bug Tracker": "https://github.com/Astromis/preprocess_conveyer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)