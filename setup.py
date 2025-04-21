# /workspaces/ai-manifestation-coach_/setup.py
from setuptools import setup, find_packages

setup(
    name="manifestation_coach",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "llama-index",
        "chromadb",
        "pypdf",
        "pytesseract",
        "unstructured",
        "polars"
    ],
    python_requires=">=3.8",
)