from setuptools import setup

setup(
    name="cartography",
    version="0.1",
    author="Hakan TASPINAR, Alexis RANDON",
    author_email="me@example.com",
    description="A fantastic module for cartography of planes",
    long_description=open(
        "readme.txt"
    ).read(),
    license="MIT",
    packages=[
        "cartography",
    ],  # folder name
    install_requires=["numpy>=1.23.3", "nb-black>=1.0.7", "cartes>=0.7.2", "geopandas>=0.11.1", "Fiona>=1.8.21", "matplotlib>=3.6.1"],
)
