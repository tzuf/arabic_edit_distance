from setuptools import setup

setup(name='edit_distance_arabic',
      version='1.0',
      description='Edit distance with different weights for frequent changes in Arabic',
      url='https://github.com/tzuf/arabic_edit_distance',
      author='tzuf',
      author_email='tzufar@gmail.com',
      packages=['edit_distance_arabic'],
      install_requires=['requests'],
      python_requires='>=3.6',
      keywords=['arabic'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.7.4',
          'Topic :: Software Development :: Libraries',
      ],
      include_package_data=True,
)