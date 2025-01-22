from setuptools import find_packages, setup


def parse_requirements():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f if line and not line.startswith("#")]


setup(
    name="thesis-genius",
    version="1.0.0",
    description="CLI for managing the Thesis Genius application",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements(),
    entry_points={
        "console_scripts": [
            "thesis-genius=cli.main:cli",
        ],
    },
)
