import tkinter as tk
from vue import Vue
from controleur import Controller
import modele as modele
import LCD1602

def main():
    app = tk.Tk()
    app.title("Système d'alarme")

    vue = Vue(app)

    controller = Controller(vue, modele.Model())  

    vue.set_controller(controller)

    def on_closing():
        controller.cleanup()  
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()
    LCD1602.clear()
