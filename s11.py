# [11] Implementación de Grafos - Amigos y Sugerencias

import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import deque


class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
        self.amigos = set()

    def agregar_amigo(self, amigo):
        self.amigos.add(amigo)


class RedSocial:
    def __init__(self):
        self.personas = {}

    def agregar_persona(self, nombre):
        if nombre not in self.personas:
            self.personas[nombre] = Persona(nombre)

    def conectar_personas(self, nombre1, nombre2):
        if nombre1 in self.personas and nombre2 in self.personas:
            self.personas[nombre1].agregar_amigo(self.personas[nombre2])
            self.personas[nombre2].agregar_amigo(self.personas[nombre1])

    def listar_amigos(self, nombre):
        if nombre in self.personas:
            return [amigo.nombre for amigo in self.personas[nombre].amigos]
        return []

    def sugerir_amigos(self, nombre):
        if nombre not in self.personas:
            return []

        visitados = set()
        cola = deque()
        sugerencias = set()

        cola.append((self.personas[nombre], 0))
        visitados.add(nombre)

        while cola:
            actual, nivel = cola.popleft()

            if nivel >= 2:
                continue

            for amigo in actual.amigos:
                if amigo.nombre not in visitados:
                    if nivel == 1:
                        sugerencias.add(amigo.nombre)
                    visitados.add(amigo.nombre)
                    cola.append((amigo, nivel + 1))

        amigos_directos = set(self.listar_amigos(nombre))
        return list(sugerencias - amigos_directos)


class VentanaRedSocial:
    def __init__(self, master):
        self.master = master
        self.master.title("Mi Red Social")
        self.red = RedSocial()
        self.posiciones = {}
        self.colores = {}

        self.canvas = tk.Canvas(master, bg="white", width=800, height=500)
        self.canvas.pack(pady=10)

        self.frame_inferior = tk.Frame(master)
        self.frame_inferior.pack(pady=10)

        self.label_usuario = tk.Label(self.frame_inferior, text="Nuevo usuario:")
        self.label_usuario.grid(row=0, column=0)
        self.entry_usuario = tk.Entry(self.frame_inferior)
        self.entry_usuario.grid(row=0, column=1)
        self.boton_agregar = tk.Button(self.frame_inferior, text="Agregar", command=self.agregar_usuario)
        self.boton_agregar.grid(row=0, column=2, padx=5)

        self.label_conectar = tk.Label(self.frame_inferior, text="Conectar:")
        self.label_conectar.grid(row=1, column=0)
        self.entry_conectar1 = tk.Entry(self.frame_inferior)
        self.entry_conectar1.grid(row=1, column=1)
        self.entry_conectar2 = tk.Entry(self.frame_inferior)
        self.entry_conectar2.grid(row=1, column=2)
        self.boton_conectar = tk.Button(self.frame_inferior, text="Conectar", command=self.conectar)
        self.boton_conectar.grid(row=1, column=3, padx=5)

        self.label_operaciones = tk.Label(self.frame_inferior, text="Usuario:")
        self.label_operaciones.grid(row=2, column=0)
        self.combo_usuarios = ttk.Combobox(self.frame_inferior, state="readonly")
        self.combo_usuarios.grid(row=2, column=1)

        self.boton_mostrar = tk.Button(self.frame_inferior, text="Mostrar Amigos", command=self.mostrar_amigos)
        self.boton_mostrar.grid(row=2, column=2)
        self.boton_sugerir = tk.Button(self.frame_inferior, text="Sugerir Amigos", command=self.sugerir_amigos)
        self.boton_sugerir.grid(row=2, column=3)

        self.resultados = tk.Text(master, height=8, width=100)
        self.resultados.pack(pady=10)

    def actualizar_combo(self):
        self.combo_usuarios['values'] = list(self.red.personas.keys())

    def agregar_usuario(self):
        nombre = self.entry_usuario.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Ingrese un nombre.")
            return
        if nombre in self.red.personas:
            messagebox.showwarning("Atención", "El usuario ya existe.")
            return

        self.red.agregar_persona(nombre)
        self.posiciones[nombre] = (random.randint(50, 750), random.randint(50, 450))
        self.colores[nombre] = random.choice(["lightblue", "lightgreen", "lightpink", "lightyellow", "lavender"])
        self.actualizar_combo()
        self.dibujar()
        self.entry_usuario.delete(0, tk.END)

    def conectar(self):
        nombre1 = self.entry_conectar1.get().strip()
        nombre2 = self.entry_conectar2.get().strip()

        if nombre1 == nombre2:
            messagebox.showwarning("Atención", "No puede conectar un usuario consigo mismo.")
            return
        if nombre1 not in self.red.personas or nombre2 not in self.red.personas:
            messagebox.showerror("Error", "Ambos usuarios deben existir.")
            return

        self.red.conectar_personas(nombre1, nombre2)
        self.dibujar()
        self.entry_conectar1.delete(0, tk.END)
        self.entry_conectar2.delete(0, tk.END)

    def mostrar_amigos(self):
        usuario = self.combo_usuarios.get()
        if not usuario:
            messagebox.showerror("Error", "Seleccione un usuario.")
            return

        amigos = self.red.listar_amigos(usuario)
        self.resultados.delete(1.0, tk.END)
        self.resultados.insert(tk.END, f"Amigos de {usuario}:\n")
        if amigos:
            for amigo in amigos:
                self.resultados.insert(tk.END, f" - {amigo}\n")
        else:
            self.resultados.insert(tk.END, "No tiene amigos todavía.\n")

    def sugerir_amigos(self):
        usuario = self.combo_usuarios.get()
        if not usuario:
            messagebox.showerror("Error", "Seleccione un usuario.")
            return

        sugerencias = self.red.sugerir_amigos(usuario)
        self.resultados.delete(1.0, tk.END)
        self.resultados.insert(tk.END, f"Sugerencias para {usuario}:\n")
        if sugerencias:
            for sugerido in sugerencias:
                self.resultados.insert(tk.END, f" - {sugerido}\n")
        else:
            self.resultados.insert(tk.END, "No hay sugerencias por ahora.\n")

    def dibujar(self):
        self.canvas.delete("all")

        for nombre, persona in self.red.personas.items():
            x1, y1 = self.posiciones[nombre]
            for amigo in persona.amigos:
                x2, y2 = self.posiciones[amigo.nombre]
                self.canvas.create_line(x1, y1, x2, y2, fill="gray")

        for nombre, (x, y) in self.posiciones.items():
            color = self.colores.get(nombre, "lightblue")
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
            self.canvas.create_text(x, y, text=nombre, font=("Arial", 9))


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaRedSocial(root)
    root.mainloop()
