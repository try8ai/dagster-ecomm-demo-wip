from setuptools import setup

setup(
    name="dagster_ecommerce",
    install_requires=[
        "dagster",
        "dagster-cloud",
        "pandas",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
