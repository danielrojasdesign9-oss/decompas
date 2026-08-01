@echo off
rem Campana semanal automatica (Programador de tareas, lunes 07:00)
rem 1> NUL   oculta la ventana si se programa con "iniciar minimizado"
cd /d "%~dp0.."
echo [%date% %time%] Inicio de campana >> out\campaign_log.txt
python scripts\campaign.py --city Cali --max 15 >> out\campaign_log.txt 2>&1
echo [%date% %time%] Fin de campana >> out\campaign_log.txt
