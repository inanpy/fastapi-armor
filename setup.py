from setuptools import setup, find_packages

setup(
    name="fastapi-armor",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.115.13",
        "starlette>=0.40.0,<0.47.0"
    ],
    python_requires=">=3.8",
)
