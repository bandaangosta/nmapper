import setuptools

with open("README.md", "r") as f:
    readme = f.read()

setuptools.setup(
    name="nmapper",
    version="0.1.3",
    description="Scan and list local network hosts",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Jose L. Ortiz",
    author_email='jlortiz@uc.cl',
    url="https://github.com/bandaangosta/nmapper",
    packages=["nmapper"],
    package_data={"nmapper": ["resources/*"]},
    entry_points={
        "console_scripts": [
            "nmapper=nmapper.__main__:main"
        ],
    },
    license="MIT",
    install_requires=[
        "click==7.1.2",
        "typer==0.3.2",
        "configparser==4.0.2",
        "prettytable==0.7.2",
        "python-nmap==0.6.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)