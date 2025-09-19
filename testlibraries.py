# fix_pyqt.py - run this in your Boggle directory
import os
import re

files_to_fix = [
    'main.py',
    'modules/homepageWindow.py',
    'modules/configWindow.py',
    'modules/boggleGame.py',
    'modules/analyticsWindow.py'
]

replacements = [
    ('from PyQt6', 'from PyQt5'),
    ('Qt.AlignmentFlag.AlignCenter', 'Qt.AlignCenter'),
    ('QDialog.DialogCode.Accepted', 'QDialog.Accepted'),
    ('QMessageBox.StandardButton.Yes', 'QMessageBox.Yes'),
    ('QMessageBox.StandardButton.No', 'QMessageBox.No'),
    ('app.exec()', 'app.exec_()')
]

for filepath in files_to_fix:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()

        for old, new in replacements:
            content = content.replace(old, new)

        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")