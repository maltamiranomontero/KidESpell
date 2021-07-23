import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KidESpell",
    version="0.0.1",
    author="Matías Altamirano",
    author_email="author@example.com",
    description="python Spanish spell checking oriented to child, based on KidSpell",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maltamirano/KidESpell",
    project_urls={
        "Bug Tracker": "https://github.com/maltamirano/KidESpell/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "kidespell"},
    packages=setuptools.find_packages(where="kidespell"),
    python_requires=">=3.6",
)