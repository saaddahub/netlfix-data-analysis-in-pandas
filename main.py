import customtkinter as ctk
from gui.app import NetflixAnalyzerApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = NetflixAnalyzerApp(root)
    root.mainloop()
