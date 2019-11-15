from setuptools import setup, find_packages


setup(
    name='python_pkg_template',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "click",
        "ConfigParser",
    ]
    entry_points='''
        [console_scripts]
        do_smth=python_pkg_template.cli:do_smth
    ''',
)
