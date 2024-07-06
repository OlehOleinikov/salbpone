from setuptools import setup, find_packages


def get_version():
    with open("salbpone/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"\'')
    raise RuntimeError("Unable to find version string.")


setup(
    name='salbpone',
    version=get_version(),
    py_modules=['salbpone'],
    packages=find_packages(),
    include_package_data=True,
    author='Oleh Oleinikov',
    author_email='oleh.oleynikov@gmail.com',
    description='Simple Assembly Line Balancing Problem - 1 solver',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'loguru ~= 0.7',
        'numpy ~= 2',
        'pulp ~=2.8'
    ],
    extras_require={
        'dev': [
            'jupyter',
            'sphinx',
            'sphinx_rtd_theme',
            'sphinx-copybutton',
            'sphinx-toggleprompt',
            'sphinx-automodapi',
            'readthedocs-sphinx-search',
            'recommonmark'
        ]
    },

    python_requires='>=3.10',
    license='GNU GPL v3',
    classifiers=[
        'Intended Audience :: Developers, Students, Researchers',
        'Operating System :: OS Independent',
    ],
)