import tkinter as tk
import Read_excel


class Interpolacion_Interfaz():
    def __init__(self,root):
        self.root = root
        self.root.title("Interpolacion")
        self.root.geometry("400x400")
        
if __name__ == '__main__':
    root1 = tk.Tk()
    Interpolacion_Interfaz(root1)
    root1.mainloop()