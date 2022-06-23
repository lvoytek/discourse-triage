"""Setup.py file."""
from setuptools import setup

setup(name='dsctriage',
      version='0.1',
      description='Output Ubuntu Discourse comments for triage',
      author='Lena Voytek',
      author_email='lena.voytek@canonical.com',
      url='https://github.com/lvoytek/discourse-triage',
      download_url=('https://github.com/lvoytek/discourse-triage' +
                    'tarball/main'),
      keywords=['ubuntu', 'discourse', 'triage'],
      license='GNU General Public License v3 or later',
      classifiers=[
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v3 or later"
          " (GPLv3+)",
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 3 :: Only",
      ],
      packages=['dsctriage'],
      entry_points={
          'console_scripts': ['dsctriage=dsctriage.dsctriage:launch']
      },
      install_requires=[],
      zip_safe=False)
