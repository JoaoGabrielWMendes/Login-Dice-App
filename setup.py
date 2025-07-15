import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py") ]
cx_Freeze.setup(
    name = "LoginDiceApp",
    options={
        "build_exe":{
            "packages":["customtkinter", "sqlite3"],
            "include_files":["assets"]
        }
    }, executables = executaveis
)