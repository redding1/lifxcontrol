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

# Program Setup Tips
# git clone ?
# sudo python setup.py install
# sudo wget http://xael.org/pages/python-nmap-0.1.4.tar.gz
# tar xvzf python-nmap-0.1.4.tar.gz
# cd python-nmap-0.1.4.tar.gz
# sudo python setup.py install
# tar xvzf https://pypi.python.org/packages/source/n/netaddr/netaddr-0.7.18.tar.gz
