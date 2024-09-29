import tkinter as tk
from tkinter import messagebox, Listbox, Text

class Vue:
    def __init__(self, app):
        self.app = app
        self.app.title("Système d'alarme")

        self.app.geometry("600x600")

        frame_buttons = tk.Frame(app)
        frame_buttons.pack(pady=10)

        self.btn_activer = tk.Button(frame_buttons, text="Activer Système", command=self.start)
        self.btn_activer.pack(side=tk.LEFT)

        self.btn_desactiver = tk.Button(frame_buttons, text="Désactiver Système", command=self.stop, state=tk.DISABLED)
        self.btn_desactiver.pack(side=tk.LEFT)

        self.status_label = tk.Label(frame_buttons, text="Non Actif", fg="red", font=("Helvetica", 12))
        self.status_label.pack(side=tk.LEFT, padx=20)

        self.action_listbox = Listbox(app)
        self.action_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.action_listbox.bind("<ButtonRelease-1>", self.listebox_selection)

        self.info_text = Text(app, height=5, state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, padx=10, pady=5)

        self.save_button = tk.Button(app, text="Sauvegarder", command=self.sauvegarder)
        self.save_button.pack(pady=5)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def ajouter_action(self, action):
        self.action_listbox.insert(tk.END, action.afficher())

    def desactiver_btn_activer(self):
        self.btn_activer.config(state="disabled")

    def activer_btn_activer(self):
        self.btn_activer.config(state="normal")

    def activer_btn_desactiver(self):
        self.btn_desactiver.config(state="normal")

    def start(self):
        if self.controller:
            self.controller.start()
            self.btn_desactiver.config(state="disabled")

    def stop(self):
        if self.controller:
            self.controller.stop()
            self.btn_desactiver.config(state="disabled")

    def listebox_selection(self, action):
        selected_index = self.action_listbox.curselection()
        if selected_index:
            selected_text = self.action_listbox.get(selected_index)
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, selected_text)
            self.info_text.config(state=tk.DISABLED)

    def sauvegarder(self):
        if self.controller:
            self.controller.save_actions_to_db()
            messagebox.showinfo("Information", "Événements sauvegardés avec succès")

    def quit_application(self):
        self.app.quit()
        self.app.destroy()

    def update_status_label(self, active):
        if active:
            self.status_label.config(text="Actif", fg="green")
        else:
            self.status_label.config(text="Non Actif", fg="red")

    def on_close(self):
        if self.controller:
            self.controller.cleanup()
        self.quit_application()
