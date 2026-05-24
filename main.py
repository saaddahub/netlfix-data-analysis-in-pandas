import customtkinter as ctk
from gui.app import NetflixAnalyzerApp

# Start the application
if __name__ == "__main__":
    # Create the main window
    root = ctk.CTk()
    
    # Create our app object
    app = NetflixAnalyzerApp(root)
    
    # Run the window loop
    root.mainloop()
