# Crée (ou supprime) la tâche planifiée Windows qui vérifie chaque jour les nouveaux dépôts.
#
#   Créer     :  powershell -ExecutionPolicy Bypass -File .\planifier_tache.ps1
#   Changer l'heure : ajouter  -Heure 07:30
#   Supprimer :  powershell -ExecutionPolicy Bypass -File .\planifier_tache.ps1 -Supprimer
#
# La tâche tourne sous ton compte, seulement quand ta session Windows est ouverte.
# Si le PC était éteint à l'heure prévue, elle se lance dès que possible (StartWhenAvailable).

param(
    [string]$Heure = "19:00",
    [switch]$Supprimer
)

$Nom = "SuiviEtatsFinanciers"

if ($Supprimer) {
    Unregister-ScheduledTask -TaskName $Nom -Confirm:$false
    Write-Host "Tâche '$Nom' supprimée."
    return
}

$Script = Join-Path $PSScriptRoot "lancer_suivi.bat"
$Action = New-ScheduledTaskAction -Execute $Script -WorkingDirectory $PSScriptRoot
$Declencheur = New-ScheduledTaskTrigger -Daily -At $Heure
$Reglages = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

Register-ScheduledTask -TaskName $Nom -Action $Action -Trigger $Declencheur -Settings $Reglages `
    -Description "Vérifie les nouveaux 10-K/10-Q à la SEC et met à jour etats_financiers.xlsx" -Force | Out-Null

Write-Host "Tâche '$Nom' créée : tous les jours à $Heure."
Write-Host "Journal d'exécution : $(Join-Path $PSScriptRoot 'journal\execution.log')"
