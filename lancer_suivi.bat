@echo off
rem Lance la mise à jour et ajoute la sortie au journal d'exécution.
rem Utilisé par la tâche planifiée Windows ; tu peux aussi double-cliquer dessus.
chcp 65001 >nul
cd /d "%~dp0"
if not exist journal mkdir journal
set PYTHONIOENCODING=utf-8
"C:\Program Files\Python312\python.exe" -m suivi %* >> journal\execution.log 2>&1
