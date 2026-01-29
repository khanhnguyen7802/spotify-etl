# https://setuptools.pypa.io/en/latest/userguide/package_discovery.html

from setuptools import setup, find_packages

setup(
    name="spotify-wrapped",
    version="0.1.0",
    description="Spotify Wrapped data pipeline with Airflow",
    author="Khanh",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
        "pandas>=1.3.0",
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "flasgger>=0.9.7",
    ],
)
