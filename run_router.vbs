Set WshShell = CreateObject("WScript.Shell")
' Replace the path below with the real one if it differs
WshShell.Run "python -m queryRouter.cli start", 0, False