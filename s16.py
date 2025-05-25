import osmnx as ox
import networkx as nx
import folium
import webbrowser
import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ruta_app_osmnx")

def obtener_coordenadas(lugar):
    try:
        location = geolocator.geocode(lugar + ", Retalhuleu, Guatemala")
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener las coordenadas para '{lugar}': {e}")
        return None

def calcular_y_mostrar_ruta():
    origen_str = entry_origen.get()
    destino_str = entry_destino.get()

    if not origen_str or not destino_str:
        messagebox.showwarning("Entrada incompleta", "Por favor, ingresa tanto el origen como el destino.")
        return

    origen_coords = obtener_coordenadas(origen_str)
    destino_coords = obtener_coordenadas(destino_str)

    if not origen_coords or not destino_coords:
        messagebox.showerror("Error de ubicacion", "No se pudo encontrar las coordenadas para el origen o el destino.")
        return

    place = "Retalhuleu, Guatemala"
    try:
        grafo = ox.graph_from_place(place, network_type='drive')
    except Exception as e:
        messagebox.showerror("Error de red", f"No se pudo descargar el grafo de calles para {place}: {e}")
        return

    try:
        origen_nodo = ox.distance.nearest_nodes(grafo, origen_coords[1], origen_coords[0])
        destino_nodo = ox.distance.nearest_nodes(grafo, destino_coords[1], destino_coords[0])
    except Exception as e:
        messagebox.showerror("Error de nodos", f"No se pudieron encontrar nodos cercanos para el origen o destino: {e}")
        return

    try:
        ruta = nx.shortest_path(grafo, origen_nodo, destino_nodo, weight='length')
    except nx.NetworkXNoPath:
        messagebox.showinfo("Ruta no encontrada", "No se encontro una ruta entre los puntos especificados.")
        return
    except Exception as e:
        messagebox.showerror("Error de ruta", f"Error al calcular la ruta: {e}")
        return

    mapa = folium.Map(location=origen_coords, zoom_start=15)
    ruta_coords = [(grafo.nodes[n]['y'], grafo.nodes[n]['x']) for n in ruta]
    folium.PolyLine(ruta_coords, color="blue", weight=4).add_to(mapa)
    folium.Marker(location=origen_coords, tooltip=f"Inicio: {origen_str}").add_to(mapa)
    folium.Marker(location=destino_coords, tooltip=f"Destino: {destino_str}", icon=folium.Icon(color="black")).add_to(mapa)

    mapa_filename = "ruta.html"
    mapa.save(mapa_filename)
    webbrowser.open(mapa_filename)

ventana = tk.Tk()
ventana.title("Buscador de rutas en Retalhuleu")
ventana.geometry("400x200") 

label_origen = tk.Label(ventana, text="Origen:")
label_origen.pack(pady=5)
entry_origen = tk.Entry(ventana, width=50)
entry_origen.pack(pady=5)

label_destino = tk.Label(ventana, text="Destino:")
label_destino.pack(pady=5)
entry_destino = tk.Entry(ventana, width=50)
entry_destino.pack(pady=5)

boton_calcular = tk.Button(ventana, text="Planificar ruta", command=calcular_y_mostrar_ruta)
boton_calcular.pack(pady=20)

ventana.mainloop()
