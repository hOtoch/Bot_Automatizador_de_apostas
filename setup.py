# setup.py
import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base="console" # para não abrir o console ao iniciar o EXE
    
build_exe_options = {
    "packages": ["tkinter", "ttkbootstrap", "pyautogui", "threading", "os", "time", "pyperclip"],
    "include_files": [
        ("icons/", "icons/"),  # Inclui a pasta icons
        ("resultados/", "resultados/"),  # Inclui a pasta resultados
        ("logs/", "logs/"),  # Inclui a pasta logs
        ("C:/Windows/System32/msvcp140.dll", "."),  # Adiciona a DLL C++ necessária
        ("C:/Windows/System32/vcruntime140.dll", "."),
    ],
    "excludes": ["unittest", "email", "html", "http", "xml"]  # Exclui módulos desnecessários
}

executables = [
    Executable(
        script="app.py",      
        base=base,
        icon="robo.ico"         
    )
]

setup(
    name="BotCsGoEmpire",
    version="1.0.0",
    description="Bot utilizado para automatizar as apostas no site csgoempire.com",
    options={"build_exe": build_exe_options},
    executables=executables
)
