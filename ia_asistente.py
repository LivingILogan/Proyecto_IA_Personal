# Archivo: ia_asistente.py

# Se importa la biblioteca json para guardar los datos de forma estructurada.
import json

def guardar_lista(nombre, tareas):
    # La información se guarda en un diccionario para que sea fácil de leer.
    data = {
        'nombre_lista': nombre,
        'tareas': tareas.split(',') # .split(',') separa las tareas por comas y las guarda en una lista.
    }
    
    # Se abre el archivo de datos en modo de escritura ('w').
    # Si el archivo no existe, lo crea automáticamente.
    with open('listas.json', 'w') as file:
        # json.dump() escribe el diccionario en el archivo en formato JSON.
        json.dump(data, file, indent=4)

def leer_listas():
    # La IA intenta leer el archivo "listas.json".
    try:
        with open('listas.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None # Devuelve 'None' si no encuentra el archivo.

def main():
    entrada_usuario = input("Hola, soy tu IA. ¿Qué necesitas que haga por ti? ")
    
    # Reconocemos la intención principal: "crear una lista"
    if "lista" in entrada_usuario.lower() and ("crear" in entrada_usuario.lower() or "crea" in entrada_usuario.lower() or "haz" in entrada_usuario.lower()):
        print("¡Entendido! Vamos a crear una lista.")
        
        nombre_lista = input("¿Qué nombre le ponemos a la lista? ")
        tareas_lista = input("¿Qué tareas quieres añadir? (separa con comas) ")
        
        guardar_lista(nombre_lista, tareas_lista)
        print(f"Perfecto, he creado la lista '{nombre_lista}' con tus tareas. ¡Ya no la olvidaré!")
    
    # --- NUEVO CÓDIGO ---
    # La IA aprende a leer y recordar lo que ya tiene guardado.
    elif "muéstrame las listas" in entrada_usuario.lower() or "muéstrame mis listas" in entrada_usuario.lower():
        listas = leer_listas()
        if listas:
            nombre = listas.get('nombre_lista')
            tareas = listas.get('tareas')
            print("Aquí está la lista que recuerdo:")
            print(f"Nombre: {nombre}")
            print("Tareas:")
            for tarea in tareas:
                print(f"- {tarea}")
        else:
            print("No recuerdo ninguna lista en este momento.")
    # --- FIN NUEVO CÓDIGO ---

    elif "añadir a la lista" in entrada_usuario.lower():
        print("¡Claro! Añadiremos algo a una lista existente.")
        
    else:
        print("Hmm, no estoy seguro de cómo ayudarte con eso. ¿Podrías ser más específico?")

# Se llama a la función principal para que el programa inicie.
if __name__ == "__main__":
    main()