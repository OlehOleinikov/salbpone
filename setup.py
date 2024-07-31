from setuptools import setup


def get_version():
    with open("salbpone/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"\'')
    raise RuntimeError("Unable to find version string.")


setup(
    version=get_version(),
    packages=['salbpone']
)
