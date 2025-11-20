'************************************************************
' Script VBS: Leer datos desde Excel y copiar al portapapeles
' Autor: Christian Londoño
' Objetivo: Capturar datos de un archivo Excel (.xlsx),
'           almacenarlos en un array y copiarlos como texto plano.
'************************************************************


'--- Variables principales ---
Dim objExcel, objWorkbook, objSheet
Dim lastRow, lastCol, i, j, x
Dim dataArray(), textOutput
Dim objClipboard

'--- Ruta del archivo Excel ---
Dim excelFilePath

rutaBase = "scripts\" & WScript.ScriptName
excelFilePath = Replace(WScript.ScriptFullName, rutaBase, "data\templates\") & "Plantilla Extension Materiales.xlsx"

' 1. Crear instancia de Excel y abrir el archivo
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False
Set objWorkbook = objExcel.Workbooks.Open(excelFilePath)
Set objSheet = objWorkbook.Sheets(1)


' 2. Determinar el rango de datos (última fila y columna)
lastRow = objSheet.Cells(objSheet.Rows.Count, 1).End(-4162).Row  ' xlUp = -4162
lastCol = objSheet.Cells(1, objSheet.Columns.Count).End(-4159).Column  ' xlToLeft = -4159

' Redimensionar el array para almacenar datos
ReDim dataArray(lastRow - 1, lastCol - 1)



' 3. Leer datos
For i = 2 To lastRow
    dataArray(i - 1, 0) = Trim(CStr(objSheet.Cells(i, 1).Value))
Next

' ' 4. Convertir a texto plano
' textOutput = ""
' For i = 0 To UBound(dataArray, 1)
'     For j = 0 To UBound(dataArray, 2)
'         textOutput = textOutput & dataArray(i, j)
'         If j < UBound(dataArray, 2) Then
'             textOutput = textOutput & vbTab
'         End If
'     Next
'     textOutput = textOutput & vbCrLf
' Next


' 4. Convertir el array en texto plano (tabuladores) evitando filas vacías
'************************************************************
textOutput = ""
Dim rowHasData

For i = 0 To UBound(dataArray, 1)
    rowHasData = False
    
    ' Verificar si la fila tiene al menos un dato
    For j = 0 To UBound(dataArray, 2)
        If Trim(dataArray(i, j)) <> "" Then
            rowHasData = True
            Exit For
        End If
    Next
    
    ' Si la fila tiene datos, agregarla al texto
    If rowHasData Then
        For j = 0 To 1 'UBound(dataArray, 2)
            If Trim(dataArray(i, j)) <> "" Then
                textOutput = textOutput & Trim(dataArray(i, j))
            End If
            If j < UBound(dataArray, 2) Then
                textOutput = textOutput
            End If
        Next
        textOutput = textOutput & vbCrLf
    End If
Next




' 5. Guardar en archivo temporal y copiar al portapapeles con clip.exe
Set objFSO = CreateObject("Scripting.FileSystemObject")
tempFilePath = objFSO.GetSpecialFolder(2) & "\temp_clip.txt"  ' Carpeta temporal
Dim objTempFile
Set objTempFile = objFSO.CreateTextFile(tempFilePath, True)
objTempFile.Write textOutput
objTempFile.Close

' Ejecutar clip.exe para copiar al portapapeles
Dim objShell
Set objShell = CreateObject("WScript.Shell")
objShell.Run "cmd /c type """ & tempFilePath & """ | clip", 0, True



' 6. Cerrar Excel y liberar memoria
objWorkbook.Close True
objExcel.Quit
Set objSheet = Nothing
Set objWorkbook = Nothing
Set objExcel = Nothing
Set objFSO = Nothing
Set objShell = Nothing

