# -*- coding: utf-8 -*-
"""
Setup package for distribution. To build documentation (html) execute 
"python setup.py build_sphinx" in setup.py directory (package toplevel)
"""

import setuptools

with open("README.txt", "r") as f:
    long_description = f.read()

with open("LICENSE", "r") as f:
    license_file = f.read()
    
setuptools.setup(
        name="script_logger",
        version="1.2",
        author="Tobias Wulf",
        author_email="46107549+TobiasWulf@users.noreply.github.com",
        description="Tools for logging operations.",
        long_description=long_description,
        long_description_content_type="text/plain",
        url="https://github.com/TobiasWulf/script_logger.git",
        packages=setuptools.find_packages(),
        install_requires=["sys", "os", "re", "glob", "datetime", "logging"],
        keywords="script_logger logging Logger automated logs",
        license=license_file,
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: GNU GPLv3",
                "Operating System :: OS Independent",
                "Topic :: Logging :: App Tracking",
                "Topic :: Debugging :: Logfile Tracing"
                ]
        )
