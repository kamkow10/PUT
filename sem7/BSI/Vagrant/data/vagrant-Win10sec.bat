@echo off
rem M. Szychowiak 2020-09-03
powercfg /hibernate off
net stop wuauserv
sc config wuauserv start=disabled
net stop bits
sc config bits start=disabled
net stop dosvc
sc config dosvc start=disabled

:User Policy:
net accounts /maxpwage:unlimited
wmic UserAccount set PasswordExpires=False
net user Administrator /active:yes
net user Administrator P@ssw0rd
net user JamesBond walther9mm /add /fullname:"James Bond" /expires:never
net localgroup Administrators JamesBond /add
net user SherlockHolmes ""  /add /fullname:"Sherlock Holmes" /passwordreq:no /expires:never
net user HerculePoirot ""  /add /fullname:"Hercule Poirot" /passwordreq:no /expires:never
net user Guest /active:no
rem net user vagrant /active:no

:Filesystem:
fsutil behavior set disablelastaccess 1
REG ADD HKLM\System\CurrentControlSet\Control\FileSystem /f /v NtfsDisable8dot3NameCreation /t REG_DWORD /d 2
REG ADD "HKLM\System\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters" /f /v EnablePrefetcher /t REG_DWORD /d 0
REG ADD "HKLM\System\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters" /f /v EnableSuperfetch /t REG_DWORD /d 0
REG ADD "HKLM\System\CurrentControlSet\Control\Session Manager\Power" /f /v HiberbootEnabled /t REG_DWORD /d 0

:Explorer:
set config_dir="c:\vagrant"
REG ADD HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /f /v EncryptionContextMenu /t REG_DWORD /d 1
reg import "%config_dir%\Win10sec.reg"
reg import "%config_dir%\Open_Command_Window_Here.reg"
reg import "%config_dir%\Open_Command_Window_Here_as_Administrator.reg"

:Anti-spy:
SCHTASKS /DELETE /TN "\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\Application Experience\ProgramDataUpdater" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\Autochk\Proxy" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\Customer Experience Improvement Program\Consolidator" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\Customer Experience Improvement Program\HypervisorFlightingTask" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\Customer Experience Improvement Program\KernelCeipTask" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\Customer Experience Improvement Program\Uploader" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\IME\SQM data sender" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\PI\Sqm-Tasks" /F
SCHTASKS /DELETE /TN "\Microsoft\Windows\Windows Error Reporting\QueueReporting" /F

:Tools:
set target=%WinDir%\tools
if not exist %target%/nul (mkdir %target%)
echo Installing lab tools to %target% ...
copy /b %config_dir%\*.exe %target%\
%target%\unzip.exe -uo %config_dir%\SysinternalsSuite.zip -d %target%
%target%\unzip.exe -uo %config_dir%\sid.zip *.exe -d %target%
setx PATH "%PATH%;%target%"

%target%\wget.exe --tries=1 -O FirefoxSetup.exe "https://download.mozilla.org/?product=firefox-latest&os=win64" && %config_dir%\FirefoxSetup.exe -ms -ma
