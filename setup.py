from setuptools import setup, find_packages

setup(
    name="azure",
    version="21.0.0",
    description="Azure SDK for Python - Springfield Workshop Edition",
    author="Springfield Team",
    author_email="team@springfield.com",
    packages=find_packages(include=["azure*"]),
    python_requires=">=3.8",
)