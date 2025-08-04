import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", base="Win32GUI") ]
cx_Freeze.setup(
    name = "LoginDiceApp",
    version="1.1.1",
    options={
        "build_exe":{
            "packages":["customtkinter", "sqlite3", "pytz", "PIL"],
            "include_files":["assets"]
        }
    }, executables = executaveis
)