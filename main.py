import customtkinter as ctk
from gui import ToDoApp

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Pode mudar para "light" por padrão
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    ToDoApp(app)
    app.mainloop()
