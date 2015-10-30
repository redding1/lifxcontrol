from setuptools import setup

setup(name='lifxlan',
      version='0.2.3',
      description='API for local communication with LIFX devices over a LAN.',
      url='https://github.com/redding1/lifxcontrol/',
      author='Meghan Clark/Matthew Redding',
      author_email='matthewreddin@gmail.com',
      license='TBD',
      packages=['lifxlan'],
      install_requires=[
        "bitstring",
	  ],
      zip_safe=False)
