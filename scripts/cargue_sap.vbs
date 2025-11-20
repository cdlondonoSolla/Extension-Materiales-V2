If Not IsObject(application) Then
   Set SapGuiAuto  = GetObject("SAPGUI")
   Set application = SapGuiAuto.GetScriptingEngine
End If
If Not IsObject(connection) Then
   Set connection = application.Children(0)
End If
If Not IsObject(session) Then
   Set session    = connection.Children(0)
End If
If IsObject(WScript) Then
   WScript.ConnectObject session,     "on"
   WScript.ConnectObject application, "on"
End If

ruta = Replace(WScript.ScriptFullName, "scripts\" & WScript.ScriptName, "logs\")

' Obtener la primera letra y convertirla a mayúscula
Dim primeraLetraMayuscula
primeraLetraMayuscula = UCase(Mid(ruta, 1, 1))

' Obtener el resto de la cadena (desde el segundo carácter)
Dim restoDeLaCadena
restoDeLaCadena = Mid(ruta, 2)

' Concatenar y guardar en la variable
ruta = primeraLetraMayuscula & restoDeLaCadena


session.findById("wnd[0]/tbar[0]/okcd").text = "/nZMM004_V2"
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/usr/ctxtP_ARCH").text = ruta & "archivo_cargue.txt"
session.findById("wnd[0]/usr/txtP_ARCSAL").text = ruta
session.findById("wnd[0]/tbar[1]/btn[8]").press