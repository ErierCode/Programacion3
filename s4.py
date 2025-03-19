# [S4] Implementación de Colas

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.front_node = None
        self.rear_node = None
        self._size = 0

    def enqueue(self, element):
        new_node = Node(element)
        if self.rear_node is None:
            self.front_node = self.rear_node = new_node
        else:
            self.rear_node.next = new_node
            self.rear_node = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("La cola está vacía")
        value = self.front_node.value
        self.front_node = self.front_node.next
        if self.front_node is None: 
            self.rear_node = None
        self._size -= 1
        return value

    def front(self):
        if self.is_empty():
            raise IndexError("La cola está vacía")
        return self.front_node.value

    def is_empty(self):
        return self.front_node is None

    def size(self):
        return self._size


class TaskSystem:
    def __init__(self):
        self.high_priority = Queue()  
        self.normal_priority = Queue()  

    def add_task(self, task, urgent=False):
        if urgent:
            self.high_priority.enqueue(task)
        else:
            self.normal_priority.enqueue(task)

    def process_task(self):
        if not self.high_priority.is_empty():
            return f"Procesando tarea urgente: {self.high_priority.dequeue()}"
        elif not self.normal_priority.is_empty():
            return f"Procesando tarea normal: {self.normal_priority.dequeue()}"
        else:
            return "No hay tareas pendientes"

# Pruebas
task_system = TaskSystem()
task_system.add_task("Enviar reporte", urgent=True)
task_system.add_task("Responder emails")
task_system.add_task("Actualizar software", urgent=True)
task_system.add_task("Limpieza de archivos")

print(task_system.process_task())  # Procesa una tarea urgente
print(task_system.process_task())  # Procesa otra tarea urgente
print(task_system.process_task())  # Procesa una tarea normal
print(task_system.process_task())  # Procesa una tarea normal
print(task_system.process_task())  # No hay más tareas


class CustomerService:
    def __init__(self):
        self.vip_queue = Queue()
        self.regular_queue = Queue()

    def add_customer(self, name, vip=False):
        if vip:
            self.vip_queue.enqueue(name)
        else:
            self.regular_queue.enqueue(name)

    def serve_customer(self):
        if not self.vip_queue.is_empty():
            return f"Atendiendo a cliente VIP: {self.vip_queue.dequeue()}"
        elif not self.regular_queue.is_empty():
            return f"Atendiendo a cliente Regular: {self.regular_queue.dequeue()}"
        else:
            return "No hay clientes esperando"


# Pruebas
cs = CustomerService()
cs.add_customer("Juan")
cs.add_customer("Rosa", vip=True)
cs.add_customer("Jorge")
cs.add_customer("Clara", vip=True)

print(cs.serve_customer())  # Atiende a Rosa (VIP)
print(cs.serve_customer())  # Atiende a Clara (VIP)
print(cs.serve_customer())  # Atiende a Juan (Regular)
print(cs.serve_customer())  # Atiende a Jorge (Regular)
print(cs.serve_customer())  # No hay clientes
