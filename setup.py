import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="flyingsnake",
    version="1.0",
    author="Stefano Pigozzi",
    author_email="ste.pigozzi@gmail.com",
    description="A Terraria world map renderer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steffo99/flyingsnake",
    packages=setuptools.find_packages(),
    install_requires=[
        "click>=7.0",
        "lihzahrd>=1.0b6",
        "Pillow>=6.1.0"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics",
        "Typing :: Typed"
    ],
    entry_points={
        "console_scripts": [
            "flyingsnake = flyingsnake.__main__:flyingsnake"
        ]
    }
)
