from setuptools import setup

setup(
    name="whosnext3000",
    version="0.1.0",
    author_email="trouni@kesseo.com",
    description="Spinning wheel utility to randomly pick a candidate.",
    packages=["whosnext3000"],
    install_requires=["simple_term_menu"],
    scripts=["bin/whosnext3000"],
)
