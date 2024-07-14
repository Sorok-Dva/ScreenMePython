import subprocess
import shutil
import os
import platform

# Définir le chemin du fichier principal
main_script = 'main.py'

# Nom du fichier exe généré
exe_name = 'ScreenMe.exe'

# Chemins des fichiers et des répertoires à inclure
icon_path = 'resources/icon.png'
config_path = 'resources/config.json'

# Déterminer le séparateur correct pour --add-data
sep = ';' if platform.system() == 'Windows' else ':'

# Commande PyInstaller pour générer le fichier exe
pyinstaller_command = [
    'pyinstaller',
    '--onefile',
    '--windowed',  # Utilisez --windowed pour les applications GUI (enlève la console)
    '--name', 'ScreenMe',
    f'--add-data={icon_path}{sep}resources',
    f'--add-data={config_path}{sep}resources',
    '--hidden-import=PyQt5.sip',
    '--hidden-import=PyQt5.QtCore',
    '--hidden-import=PyQt5.QtGui',
    '--hidden-import=PyQt5.QtWidgets',
    main_script
]

# Exécuter la commande PyInstaller
subprocess.run(pyinstaller_command)

# Chemin de destination de l'exécutable généré
dist_path = os.path.join('dist', exe_name)
destination_path = os.path.join('.', exe_name)

# Vérifier et supprimer le fichier existant s'il existe
if os.path.exists(destination_path):
    os.remove(destination_path)

# Déplacer le fichier exe généré dans le répertoire principal
if os.path.exists(dist_path):
    shutil.move(dist_path, destination_path)

# Supprimer les dossiers temporaires générés par PyInstaller s'ils existent
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('__pycache__'):
    shutil.rmtree('__pycache__')
spec_file = f'{exe_name}.spec'
if os.path.exists(spec_file):
    os.remove(spec_file)
