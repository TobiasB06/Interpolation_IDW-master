import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import openpyxl as pxl

class Interpolacion_Interfaz():
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolacion")
        self.root.geometry("400x400")
        self.botones_hojas = []
        self.configurar_widgets()
        
    def configurar_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure((0, 2), weight=2)
        self.root.rowconfigure(1, weight=1)
        self.frame_excel = ttk.Labelframe(self.root, text="Excel")
        self.frame_archivo_interp = ttk.Labelframe(self.root, text="Archivo a interpolar")
        self.frame_resultados = ttk.Labelframe(self.root, text="Resultado")
        self.frame_excel.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)
        self.frame_archivo_interp.grid(row=1, column=0, sticky="nsew", padx=5, pady=2)
        self.frame_resultados.grid(row=2, column=0, sticky="nsew", padx=5, pady=2)

    def widgets(self):
        self.icono_carpeta = ImageTk.PhotoImage(Image.open("imagenes/icono_carpeta.png").resize((20, 20)))
        tk.Label(self.frame_excel, text="Archivo de excel").grid(row=0, column=1, pady=10)
        tk.Button(self.frame_excel, image=self.icono_carpeta, compound="left", command=self.open_excel).grid(row=0, column=0,padx=(0,10), pady=10)
        tk.Label(self.frame_excel, text="Hojas del archivo: ").grid(row=1, column=0,columnspan=2, padx=10, pady=10)
        self.frame_botones_hojas = tk.Frame(self.frame_excel)
        self.frame_botones_hojas.grid(row=2, column=0,columnspan=2, sticky="nsew", padx=10, pady=10)
        
    def open_excel(self):
        self.file_path = filedialog.askopenfilename()
        self.file_excel = pxl.load_workbook(self.file_path)
        self.sheet = self.file_excel.sheetnames
        for hoja in self.sheet:
            boton = tk.Button(self.frame_botones_hojas, text=hoja)
            boton.configure(command=lambda R=boton, hoja=hoja: self.seleccionar_hoja(hoja, R))
            boton.grid(row=2, column=self.sheet.index(hoja), sticky="nsew", padx=10, pady=10)

    def seleccionar_hoja(self,hoja,boton_seleccionado):
        self.hoja_seleccionada = hoja
        print(self.hoja_seleccionada)
        # Cambiar el color del botón seleccionado
        for widget in self.frame_excel.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="SystemButtonFace")
        boton_seleccionado.config(bg="blue")

if __name__ == '__main__':
    root1 = tk.Tk()
    interpolacion = Interpolacion_Interfaz(root1)
    interpolacion.widgets()
    root1.mainloop()