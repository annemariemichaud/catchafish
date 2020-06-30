from setuptools import find_packages
from setuptools import setup

#with open('requirements.txt') as f:
#    content = f.readlines()
#requirements = [x.strip() for x in content if 'git+' not in x]

REQUIRED_PACKAGES = [
    'pip>=9',
    'setuptools>=26',
    'wheel>=0.29',
    'pandas',
    'pytest',
    'coverage',
    'flake8',
    'black',
    'yapf',
    'python-gitlab',
    'twine',
    'numpy',
    'pandas',
    'tensorflow.keras',
    'termcolor',
    'scikit-learn',
    'h5py',
    'gcsfs==0.6.0',
    'google-cloud-storage==1.26.0',
    'streamlit',
    'scikit-image',
    'Pillow',
    'wikipedia'
    ]

setup(name='catchafish',
      version="1.0",
      description="Project Description",
      packages=find_packages(),
      install_requires=REQUIRED_PACKAGES,
      test_suite = 'tests',
      # include_package_data: to install data from MANIFEST.in
      include_package_data=False,
      scripts=['scripts/catchafish-run'],
      zip_safe=False)
