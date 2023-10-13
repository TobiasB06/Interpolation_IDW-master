import tkinter as tk
from tkinter import ttk,filedialog
import Read_excel


class Interpolacion_Interfaz():
    def __init__(self,root):
        self.root = root
        self.root.title("Interpolacion")
        self.root.geometry("400x400")
        self.widgets()
    def widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure((0,2), weight=2)
        self.root.rowconfigure(1, weight=1)
        self.frame_excel = ttk.Labelframe(self.root,text="Excel")
        self.frame_archivo_interp=ttk.Labelframe(self.root,text="Archivo a interpolar")
        self.frame_resultados=ttk.Labelframe(self.root,text="Resultado")
        self.frame_excel.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)
        self.frame_archivo_interp.grid(row=1, column=0, sticky="nsew", padx=5, pady=2)
        self.frame_resultados.grid(row=2, column=0, sticky="nsew", padx=5, pady=2)
if __name__ == '__main__':
    root1 = tk.Tk()
    Interpolacion_Interfaz(root1)
    root1.mainloop()