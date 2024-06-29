import tkinter as tk
import subprocess
import os

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

def ejecutar_SUBNETEO_PASO1():
    python_path = os.path.join(current_dir, "Ventana1Mottoccanchi.py")
    subprocess.run(["python", python_path], check=True)

def ejecutar_LOG_PASO2():
    python_path = os.path.join(current_dir, "PASO 2 ARCHIVO LOG.py")
    subprocess.run(["python", python_path], check=True)

def ejecutar_leer_api_PAS3(): #API USADA: HUNTER.IO
    python_path = os.path.join(current_dir, "Leer una API.py")
    subprocess.run(["python", python_path], check=True)

def Analicis_de_PC_PASO4(): #LIBRERIA USADA: NMAP
    print("Ventana4")

window = tk.Tk()  # Ventana, contiene todo lo visual

icon_path = os.path.join(current_dir, "interfaz_principal.png")
icon = tk.PhotoImage(file=icon_path)
window.geometry("700x500")

# Poner nombre
window.title("VENTANA PRINCIPAL")
# Meter la imagen en el window
window.iconphoto(True, icon)
# Tamaño estático
window.resizable(width=False, height=False)

# Creación del menú principal
menu_bar = tk.Menu(master=window)
opciones = tk.Menu(
    master=menu_bar,
    font=("My boli", 20),
    tearoff=0
)
menu_bar.add_cascade(label="VENTANAS", menu=opciones)
menu_bar.add_command(label="Cerrar", command=lambda: print("Cerrar"))
menu_bar.add_command(label="Help", command=lambda: print("Help"))

# Agregar opciones al menú
opciones.add_command(label="Ventana1 (Mottoccanchi)", command=ejecutar_SUBNETEO_PASO1)
opciones.add_separator()
opciones.add_command(label="Ventana2 (Puma)", command=ejecutar_LOG_PASO2)
opciones.add_separator()
opciones.add_command(label="Ventana3 (Gutierrez)", command=ejecutar_leer_api_PAS3)
opciones.add_separator()
opciones.add_command(label="Ventana4 (Huarca)", command=Analicis_de_PC_PASO4)

window.config(menu=menu_bar)  # Para que el menú se agregue a la ventana

# Creación de label texto
photo_tecsup = tk.PhotoImage(file=icon_path).subsample(4)  # Acomodar
label = tk.Label(
    master=window,
    text="MENU PRINCIPAL",
    font=("Impact", 40, "bold"),
    foreground="green",
    background="black",
    relief="solid",
    border=5,
    padx=3,
    pady=3,
    image=photo_tecsup,
    compound="top"
)
label.pack(side="top")  # La posición arriba o abajo

# Creación de Grid en la pantalla principal, Frame
frame = tk.Frame(master=window, bg="pink")
frame.pack()  # Se pueda ver

tk.Button(master=frame, text="Ventana1", fg="white", bg="green", height=3, width=7, command=ejecutar_SUBNETEO_PASO1).pack(side="top")
tk.Button(master=frame, text="Ventana2", fg="white", bg="green", height=3, width=7, command=ejecutar_LOG_PASO2).pack(side="top")
tk.Button(master=frame, text="Ventana3", fg="white", bg="green", height=3, width=7, command=ejecutar_leer_api_PAS3).pack(side="top")
tk.Button(master=frame, text="Ventana4", fg="white", bg="green", height=3, width=7, command=Analicis_de_PC_PASO4).pack(side="top")

# Fondo ventana
window.config(background="#34ebdb")
window.mainloop()
