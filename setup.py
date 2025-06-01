from setuptools import setup, find_packages

setup(
    name="card-game-api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "websockets>=12.0",
        "python-multipart>=0.0.6",
        "anyio>=3.7.1,<4.0.0",
        "pydantic>=2.0.0",
        "starlette>=0.27.0",
        "typing-extensions>=4.5.0",
    ],
) 