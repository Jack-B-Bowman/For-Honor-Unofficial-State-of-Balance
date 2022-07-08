$date = Get-Date -Format "MM-dd-yyyy-HH-mm"
Set-Location 'C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper'
# C:\ProgramData\Anaconda3\python.exe 'C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\userParserMultiThreaded.py' 2
C:\ProgramData\Anaconda3\python.exe 'C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\userParserSelenium.py' 2
C:\ProgramData\Anaconda3\python.exe '.\AddJsonToDB.py'
Set-Location 'C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\datafiles'
C:\'Program Files'\7-Zip\7z.exe a -sdel "D:\Archive\UserScraper\datafiles$date" .



