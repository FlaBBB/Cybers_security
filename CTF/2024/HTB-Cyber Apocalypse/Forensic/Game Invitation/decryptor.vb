Function xorring(given_string() As Byte, length As Long) As Boolean
    Dim xor_key As Byte
    xor_key = 45
    For i = 0 To length - 1
        given_string(i) = given_string(i) Xor xor_key
        xor_key = ((xor_key Xor 99) Xor (i Mod 254))
    Next i
    xorring = True
End Function

Sub Decryptor()
    ' Define the variables'
    Dim IOFile_input
    Dim IOFile_output
    Dim filename_input_length As Long
    Dim length As Long
    Dim file_input_content() As Byte
    Dim file_input_content_1 As String
    Dim mathced_AD, matched_file_input_content
    Dim regex_Obj
    Dim mathced_AD_FirstIndex
    Dim result() As Byte
    Dim result_size As Long
    Dim filename_input As String
    Dim filename_output As String

    filename_input = "D:\Programming\CySec\Cyber Security\CTF\2024\HTB-Cyber Apocalypse\Forensic\Game Invitation\invitation.docm"
    filename_output = "D:\Programming\CySec\Cyber Security\CTF\2024\HTB-Cyber Apocalypse\Forensic\Game Invitation\mailform.js"

    result_size = 13082
    ReDim result(result_size) 'set size'

    filename_input_length = FileLen(filename_input)
    IOFile_input = FreeFile
    Open (filename_input) For Binary As #IOFile_input
    ReDim file_input_content(filename_input_length) 'set size', likely get all the content of the file'
    Get #IOFile_input, 1, file_input_content
    file_input_content_1 = StrConv(file_input_content, vbUnicode)

    ' searching last index of matched string pattern in the file content and get the first index of the matched string pattern in the file content'
    Set regex_Obj = CreateObject("vbscript.regexp")
    regex_Obj.Pattern = "sWcDWp36x5oIe2hJGnRy1iC92AcdQgO8RLioVZWlhCKJXHRSqO450AiqLZyLFeXYilCtorg0p3RdaoPa"
    Set matched_file_input_content = regex_Obj.Execute(file_input_content_1)
    If matched_file_input_content.Count = 0 Then
        GoTo exit_label
    End If
    ' this the searcher last index of matched string pattern in the file content and get the first index of the matched string pattern in the file content'
    For Each mathced_AD In matched_file_input_content
        mathced_AD_FirstIndex = mathced_AD.FirstIndex
    Exit For
    Next

    ' get the content of the file from the first index of the matched string pattern in the file content to the end of the file content'
    Get #IOFile_input, mathced_AD_FirstIndex + 81, result
    If Not xorring(result(), result_size + 1) Then
        GoTo exit_label
    End If

    ' write the content of the file to the mailform.js file'
    Dim ExcelApp As Object
    Set ExcelApp = CreateObject("Excel.Application")
    ExcelApp.Visible = True
    ExcelApp.Workbooks.Add
    ExcelApp.Cells(1, 1).Value = StrConv(result, vbUnicode)
    

    Exit Sub 'exit the sub, this is like a return statement'

exit_label:
    Close #IOFile_output
    ActiveDocument.Save
End Sub
