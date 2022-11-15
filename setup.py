from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mix_inventory/__init__.py
from mix_inventory import __version__ as version

setup(
	name="mix_inventory",
	version=version,
	description="Mixing Systems Iventory Management",
	author="Steven J Lightfoot",
	author_email="steve.lightfoot@crownpaints.co.uk",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
