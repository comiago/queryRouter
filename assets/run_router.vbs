Set oShell = CreateObject("WScript.Shell")
Dim fso, scriptDir
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

oShell.CurrentDirectory = scriptDir

' Usiamo il percorso completo che ti ha dato il terminale
Dim qrPath
qrPath = "C:\Users\tecno\AppData\Roaming\Python\Python314\Scripts\qr.exe"

' Avvia il server in modalità nascosta
oShell.Run """" & qrPath & """ start", 0, False