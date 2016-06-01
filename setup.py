from setuptools import setup

def readme():
        with open('README.rst') as f:
                    return f.read()

setup(name='wgpio',
      version='0.1',
      description='Rpi.GPIO simulation with winterface',
      long_description=readme(),
      url='http://github.com/msdavid/wgpio',
      author='Mauro D. Sauco',
      author_email='mauro@sauco.net',
      license='MIT',
      install_requires=['mako','cherrypy'],
      include_package_data=True,
      keywords='GPIO WGPIO simulation mauro sauco',
      zip_safe=False)
