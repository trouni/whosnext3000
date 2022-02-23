from setuptools import setup, find_packages

setup(
    name="whosnext3000",
    version="0.1.0",
    author_email="trouni@kesseo.com",
    description="Spinning wheel utility to randomly pick a candidate.",
    packages=find_packages(),
    install_requires=["simple_term_menu"],
    scripts=["bin/whosnext3000"],
)
