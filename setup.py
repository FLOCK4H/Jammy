"""
    This file installs Jammy - making it available directly from the command line:
    'sudo Jammy'

    To uninstall Jammy run:
    'sudo pip uninstall Jammy'
"""

from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil

class PostInstallCommand(install):
    """Post-installation for installation."""
    def run(self):
        install.run(self)
        main_dir = '/usr/local/share/Jammy'
        if not os.path.exists(main_dir):
            os.makedirs(main_dir)
        template_dir = "/usr/share/eaphammer/templates"
        if not os.path.exists(f"{template_dir}/google"):
            os.makedirs(f"{template_dir}/google")
            dest = f"{template_dir}/google"
            shutil.copy("templates/google/meta.py", f"{dest}/meta.py")
            shutil.copy("templates/google/head.html", f"{dest}/head.html")
            shutil.copy("templates/google/body.html", f"{dest}/body.html")

setup(
    name='Jammy',
    version='4.2.0.26',
    author='FLOCK4H',
    url='github.com/FLOCK4H/Jammy',
    description='Jammy - Backpack full of hacking tools',
    license="MIT",
    packages=find_packages(),
    scripts=['Jammy'],
    cmdclass={
        'install': PostInstallCommand,
    }
)
