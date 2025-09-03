# Archivo: ia_asistente.py

# Se importa la biblioteca json para guardar los datos de forma estructurada.
import json

def guardar_lista(data):
    # Se abre el archivo de datos en modo de escritura ('w').
    # Si el archivo no existe, lo crea automáticamente.
    with open('listas.json', 'w') as file:
        # json.dump() escribe la lista de diccionarios en el archivo en formato JSON.
        json.dump(data, file, indent=4)

def leer_listas():
    # La IA intenta leer el archivo "listas.json".
    try:
        with open('listas.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # Devuelve una lista vacía si el archivo no existe, para poder empezar a guardar.
        return []

def borrar_tareas(nombre, tareas_a_borrar):
    listas = leer_listas()
    if listas:
        # Busca la lista por su nombre.
        for lista in listas:
            if lista.get('nombre_lista') == nombre:
                tareas_existentes = lista.get('tareas')
                
                # Filtramos la lista para quedarnos con las tareas que NO queremos borrar
                tareas_actualizadas = [tarea for tarea in tareas_existentes if tarea not in tareas_a_borrar]
                
                # Reemplazamos las tareas de la lista por las actualizadas.
                lista['tareas'] = tareas_actualizadas
                
                guardar_lista(listas)
                return True
    return False

def main():
    entrada_usuario = input("Hola, soy tu IA. ¿Qué necesitas que haga por ti? ")
    
    # Reconocemos la intención principal: "crear una lista"
    if "lista" in entrada_usuario.lower() and ("crear" in entrada_usuario.lower() or "crea" in entrada_usuario.lower() or "haz" in entrada_usuario.lower()):
        print("¡Entendido! Vamos a crear una lista.")
        
        nombre_lista = input("¿Qué nombre le ponemos a la lista? ")
        tareas_lista = input("¿Qué tareas quieres añadir? (separa con comas) ")
        
        # Nueva estructura de datos para guardar
        nueva_lista = {
            'nombre_lista': nombre_lista,
            'tareas': [tarea.strip() for tarea in tareas_lista.split(',')]
        }
        
        listas_existentes = leer_listas()
        listas_existentes.append(nueva_lista)
        
        guardar_lista(listas_existentes)
        print(f"Perfecto, he creado la lista '{nombre_lista}' con tus tareas. ¡Ya no la olvidaré!")
    
    # La IA aprende a leer.
    elif any(keyword in entrada_usuario.lower() for keyword in ["muéstrame", "ver", "revisar", "leer"]) and "listas" in entrada_usuario.lower():
        listas = leer_listas()
        if listas:
            print("Aquí están todas las listas que recuerdo:")
            for lista in listas:
                nombre = lista.get('nombre_lista')
                tareas = lista.get('tareas')
                print(f"\nNombre: {nombre}")
                print("Tareas:")
                for tarea in tareas:
                    print(f"- {tarea}")
        else:
            print("No recuerdo ninguna lista en este momento.")

    # La IA aprende a añadir.
    elif any(keyword in entrada_usuario.lower() for keyword in ["añadir", "agregar", "sumar"]) and "lista" in entrada_usuario.lower():
        listas = leer_listas()
        if listas:
            nombre_lista_a_modificar = input("¿A qué lista quieres añadir tareas? ")
            for lista in listas:
                if lista.get('nombre_lista') == nombre_lista_a_modificar:
                    tareas_existentes = lista.get('tareas')
                    nuevas_tareas = input("¿Qué nuevas tareas quieres añadir? (separa con comas) ")
                    
                    tareas_completas = tareas_existentes + [tarea.strip() for tarea in nuevas_tareas.split(',')]
                    
                    lista['tareas'] = tareas_completas
                    
                    guardar_lista(listas)
                    print(f"He añadido las nuevas tareas a la lista '{nombre_lista_a_modificar}'.")
                    return # Salimos de la función después de encontrar la lista.
            
            print(f"No encontré una lista con el nombre '{nombre_lista_a_modificar}'.")
        else:
            print("No tienes ninguna lista creada. Primero debes crear una.")

    # La IA aprende a borrar.
    elif any(keyword in entrada_usuario.lower() for keyword in ["borrar", "quitar", "eliminar"]) and "lista" in entrada_usuario.lower():
        listas = leer_listas()
        if listas:
            nombre_lista_a_borrar = input("¿De qué lista quieres borrar tareas? ")
            
            tareas_a_borrar = input("¿Qué tareas quieres borrar? (separa con comas) ").split(',')
            
            if borrar_tareas(nombre_lista_a_borrar, tareas_a_borrar):
                print(f"He borrado las tareas de la lista '{nombre_lista_a_borrar}'.")
            else:
                print("No pude borrar las tareas. ¿Estás seguro de que la lista existe?")
        else:
            print("No tienes ninguna lista creada para borrar.")

    else:
        print("Hmm, no estoy seguro de cómo ayudarte con eso. ¿Podrías ser más específico?")

# Se llama a la función principal para que el programa inicie.
if __name__ == "__main__":
    main()