import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsonViewer",
    version="0.0.1",
    author="Bepeho",
    author_email="contact@bepeho.Com",
    description="A simple json graphical viwer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patricerosay/jsonViewer",
    packages=setuptools.find_packages(),
    install_requires=[
          'anytree',
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "json"
    ),
)