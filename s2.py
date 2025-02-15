import random
import string
import timeit

class User:
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age

    def __repr__(self):
        return f"User(ID={self.user_id}, Name={self.name}, Age={self.age})"

def linear_search(users, target_id):
    for i, user in enumerate(users):
        if user.user_id == target_id:
            return user
    return None  

def binary_search(users, target_id):
    izquierda, derecha = 0, len(users) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if users[medio].user_id == target_id:
            return users[medio]
        elif users[medio].user_id < target_id:
            izquierda = medio + 1
        else:
            derecha = medio - 1 
    return None

users = []
user_ids = random.sample(range(100000, 1000000), 100000)
for user_id in user_ids:
    name = ''.join(random.choices(string.ascii_letters, k=8))
    age = random.randint(1, 90)
    users.append(User(user_id, name, age))

examples = []
for _ in range(10):
    examples.append(random.choice(users).user_id)

print("Examples: ")
for example in examples:
    print("id: ", example)
    
try:
    target_id = int(input("Ingrese el ID que desea buscar (1000 - 999999): "))
except ValueError:
    print("El ID debe ser un número entero.")
    exit()
    
users_sorted = sorted(users, key=lambda user: user.user_id)

linear_time = timeit.timeit(lambda: linear_search(users, target_id), number=10)
binary_time = timeit.timeit(lambda: binary_search(users_sorted, target_id), number=10)

user_linear = linear_search(users, target_id)
user_binary = binary_search(users_sorted, target_id)

if user_linear:
    print(f"Usuario encontrado por búsqueda lineal: {user_linear}")
else:
    print("Usuario no encontrado por búsqueda lineal.")

if user_binary:
    print(f"Usuario encontrado por búsqueda binaria: {user_binary}")
else:
    print("Usuario no encontrado por búsqueda binaria.")

print(f"Tiempo de búsqueda lineal: {linear_time:.6f} segundos")
print(f"Tiempo de búsqueda binaria: {binary_time:.6f} segundos")
