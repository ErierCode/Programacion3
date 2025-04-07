# [S9] Implementación de Lista Doblemente Enlazada

import tkinter as tk
import ttkbootstrap as ttk


class DoublyNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_node = None

    def append(self, value):
        new_node = DoublyNode(value)

        if self.current_node and self.current_node != self.tail:
            temp = self.current_node.next
            while temp:
                next_node = temp.next
                temp.prev = None
                temp.next = None
                temp = next_node
            self.current_node.next = None
            self.tail = self.current_node

        if self.head is None:
            self.head = self.tail = self.current_node = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.current_node = new_node

    def move_backward(self):
        if self.current_node and self.current_node.prev:
            self.current_node = self.current_node.prev

    def move_forward(self):
        if self.current_node and self.current_node.next:
            self.current_node = self.current_node.next

    def current(self):
        if self.current_node:
            return self.current_node.value
        return ""



    
class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto con Historial")
        self.root.geometry("600x400")

        self.history = DoublyLinkedList()

        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill="both", expand=True)

        self.text_area = tk.Text(main_frame, wrap="word", font=("Arial", 12), height=20)
        self.text_area.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(btn_frame, text="Guardar Estado", command=self.guardar_estado).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Deshacer", command=self.deshacer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Rehacer", command=self.rehacer).pack(side="left", padx=5)

    def guardar_estado(self):
        contenido = self.text_area.get("1.0", tk.END).rstrip()
        self.history.append(contenido)

    def deshacer(self):
        self.history.move_backward()
        self._actualizar_texto()

    def rehacer(self):
        self.history.move_forward()
        self._actualizar_texto()

    def _actualizar_texto(self):
        self.text_area.delete("1.0", tk.END)
        actual = self.history.current()
        if actual is not None:
            self.text_area.insert(tk.END, actual)


root = ttk.Window(themename="litera")
app = TextEditorApp(root)
root.mainloop()