import setuptools

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(
    name="jsonViewer",
    license='MIT',
    version="0.0.1",
    author="Bepeho",
    author_email="contact@bepeho.Com",
    description="A simple json graphical viwer",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/patricerosay/jsonViewer",
    packages=['jsonViewer'],
    dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0'],

    install_requires=[
          'anytree',
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "json",
    ),
    scripts=['bin/jsonViewer'],
    include_package_data=True,
    zip_safe=False
)