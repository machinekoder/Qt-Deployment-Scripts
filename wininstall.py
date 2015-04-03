import sys
import os
import shutil

pythonExe = sys.executable
script = 'qt-deploy.py'
scriptOut = 'qt-deploy'
shellOut = 'qt-deploy.bat'
scriptsPath = os.path.join(os.path.split(pythonExe)[0], 'Scripts')
scriptOutPath = os.path.join(scriptsPath, scriptOut)
print('Installing script')
shutil.copyfile(script, scriptOutPath)
f=open(os.path.join(scriptsPath, shellOut), 'w')
f.write(pythonExe + ' ' + scriptOutPath + ' %* \n')
f.close()
print('Installed')
