'''This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

import os
import sys
import subprocess
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       )
# from qgis.core import *
from qgis.utils import iface
from PyQt5.QtWidgets import QMessageBox,QComboBox

class configureTOOLS(QgsProcessingAlgorithm):

    def __init__(self):
        super().__init__()

    def name(self):
        return "configure"

    def tr(self, text):
        return QCoreApplication.translate("Configure IDP Sites Mapping Tools", text)

    def displayName(self):
        return self.tr("Configure IDP Sites Mapping Tools")

    def group(self):
        return self.tr("Configure")

    def shortHelpString(self):
        return self.tr('''This script will attempt to install the dependencies required for the IDP Sites Mapping Tools for Windows users.
        If the tool fails, manual installation will be required using 'pip install module'. ''')

    def helpUrl(self):
        return "https://github.com/passies95/IDP-Sites-Mapping-Toolbox/wiki"

    def groupId(self):
        return "Configure"

    def createInstance(self):
        return configureTOOLS()

    def initAlgorithm(self, config=None):
        pass

    def processAlgorithm(self, parameters, context, feedback):

        if os.name == 'nt': ##GUI for python installer via subprocess module
            reply = QMessageBox.question(iface.mainWindow(), 'Install Dependencies',
                 'Attempting to install several packages. Do you wish to continue?', QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                try:
                    is_admin = os.getuid() == 0
                except AttributeError:
                    import ctypes
                    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

                # modules = ['segment-geospatial==0.5.0']
                modules = ['segment-geospatial==0.5.0','numpy==1.24.1', 'rasterio', 'opencv-python==4.5.5.64', 'networkx==3.2.1', 'scikit-image==0.22.0',
                            'scikit-learn==1.4.2', ]

                for module in modules:
                    try:
                        if is_admin:
                            status = subprocess.check_call(['python3','-m', 'pip', 'install', module])
                        else:
                            status = subprocess.check_call(['python3','-m', 'pip', 'install', module,'--user'])

                        if status != 0:
                            feedback.reportError(QCoreApplication.translate('Warning','Failed to install %s - consider installing manually'%(module)))
                    except subprocess.CalledProcessError:
                        feedback.reportError(self.tr('Warning','Failed to install %s - consider installing manually'%(module)))
                        return {}
                    # except Exception:
                    #     feedback.reportError(QCoreApplication.translate('Warning','Failed to install %s - consider installing manually'%(module)))
                    #     return {}
        else:
            feedback.reportError(QCoreApplication.translate('Warning','macOS and Linux users - manually install the segment-geospatial python package.'))
            return {}

        return {}

if __name__ == '__main__':
    pass
