"""
/***************************************************************************
 Plugin Dependencies Installer
 credits to: https://github.com/Pa-Ez/qgis-dependencies-installer/blob/master/installer.py
 for the initial version
                              -------------------
        begin                : 2024-07-24
        copyright            : (C) 2024 by pascal ogola
        email                : pascaladongo@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import pathlib
import sys
import os
import subprocess
import platform


def install_dependencies():
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    operating_system = platform.system()
    try:
        import pip
    except ImportError:
        exec(open(str(pathlib.Path(plugin_dir, "scripts", "get_pip.py"))).read())
        import pip

        if operating_system == "Darwin":
            pip.main(["install", "--upgrade", "pip"])
        elif operating_system == "Linux":
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "upgrade", "pip"]
            )
        elif operating_system == "Windows":
            subprocess.check_call(
                ["python3", "-m", "pip", "install", "--upgrade", "pip"]
            )
    sys.path.append(plugin_dir)

    with open(os.path.join(plugin_dir, "requirements.txt"), "r") as requirements:
        for dep in requirements.readlines():
            dep = dep.replace("\n", "")
            dep_noversion = dep.strip().split("==")[0]
            try:
                __import__(dep_noversion)
            except ImportError:
                print("{} not available, installing".format(dep))
                if operating_system == "Darwin":
                    pip.main(["install", dep])
                elif operating_system == "Linux":
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                elif operating_system == "Windows":
                    subprocess.check_call(["python3", "-m", "pip", "install", dep])