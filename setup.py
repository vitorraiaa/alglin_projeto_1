from setuptools import setup, find_packages
import os

# Lendo o conteúdo do README.md para usar como descrição longa
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="angry_birds",  # Nome do seu pacote
    version="0.1.0",
    author="Artur Rizzi, Vitor Raia",
    author_email="arturrm1@al.insper.edu.br",
    description="Um pacote minimalista em Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vitorraiaa/alglin_projeto_1",  # Atualize com o URL correto
    packages=find_packages(),  # Encontra automaticamente todos os pacotes
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'angry_birds=angry_birds.game:main',  # Comando de console
        ],
    },
    install_requires=[  # Dependências especificadas no requirements.txt
        line.strip() for line in open("requirements.txt").readlines()
    ],
    include_package_data=True,  # Inclui arquivos descritos no MANIFEST.in
    package_data={
        "angry_birds": ["img/*.png", "img/*.jpg", "img/*.webp"],  # Ajuste os padrões conforme necessário
    },
)
