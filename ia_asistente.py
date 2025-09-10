# Archivo: ia_asistente.py

# Se importan las librerías necesarias
import json
import sys
import os
import pyautogui
import psutil
import shutil

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

def abrir_programa(nombre_programa):
    # Detecta el sistema operativo y ejecuta el comando correcto
    if sys.platform == 'win32':
        # Comando para Windows
        os.system(f'start {nombre_programa}')
    elif sys.platform == 'darwin':
        # Comando para macOS
        os.system(f'open -a {nombre_programa}')
    elif sys.platform == 'linux':
        # Comando para Linux
        os.system(f'xdg-open {nombre_programa}')

def cerrar_programa_por_nombre(nombre_programa):
    for proc in psutil.process_iter():
        if nombre_programa.lower() in proc.name().lower():
            proc.kill()
            return True
    return False

def crear_carpeta(nombre_carpeta):
    try:
        os.makedirs(nombre_carpeta)
        return True
    except FileExistsError:
        return False

def buscar_archivo_o_carpeta(nombre, ruta_busqueda):
    for root, dirs, files in os.walk(ruta_busqueda):
        # Busca en los archivos
        if nombre in files:
            return os.path.join(root, nombre)
        # Busca en las carpetas
        if nombre in dirs:
            return os.path.join(root, nombre)
    return None

def mover_a_escritorio(nombre_a_mover):
    try:
        # Obtiene la ruta del escritorio del usuario
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Busca el archivo/carpeta desde la carpeta del usuario
        ruta_encontrada = buscar_archivo_o_carpeta(nombre_a_mover, os.path.expanduser('~'))

        if ruta_encontrada:
            shutil.move(ruta_encontrada, desktop_path)
            return True
        else:
            return False
    except OSError as e:
        print(f"Error al intentar mover: {e}")
        return False

def borrar_archivo_o_carpeta(ruta_completa_a_eliminar):
    try:
        if os.path.isdir(ruta_completa_a_eliminar):
            shutil.rmtree(ruta_completa_a_eliminar)
        elif os.path.isfile(ruta_completa_a_eliminar):
            os.remove(ruta_completa_a_eliminar)
        return True
    except FileNotFoundError:
        return False
    except OSError as e:
        print(f"Error al intentar eliminar: {e}")
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

    # La IA aprende a abrir programas.
    elif "abrir" in entrada_usuario.lower():
        print("¡Claro! ¿Qué programa o aplicación te gustaría abrir?")
        nombre_programa = input("Nombre del programa: ")
        
        abrir_programa(nombre_programa)
        print(f"Hecho, he abierto {nombre_programa}.")

    # La IA aprende a cerrar programas.
    elif "cerrar" in entrada_usuario.lower():
        print("¡Claro! ¿Qué programa te gustaría cerrar?")
        nombre_programa = input("Nombre del programa: ")

        if cerrar_programa_por_nombre(nombre_programa):
            print(f"Hecho, he cerrado {nombre_programa}.")
        else:
            print(f"No pude encontrar un programa con el nombre '{nombre_programa}' para cerrar.")
            
    # La IA aprende a crear carpetas.
    elif "crear carpeta" in entrada_usuario.lower() or "crea una carpeta" in entrada_usuario.lower():
        print("¡Claro! ¿Qué nombre le ponemos a la carpeta?")
        nombre_carpeta = input("Nombre de la carpeta: ")

        if crear_carpeta(nombre_carpeta):
            print(f"Hecho, he creado la carpeta '{nombre_carpeta}'.")
        else:
            print(f"La carpeta '{nombre_carpeta}' ya existe o hubo un error al crearla.")

    # La IA aprende a mover carpetas al escritorio.
    elif "mover" in entrada_usuario.lower() or "mueve" in entrada_usuario.lower():
        nombre_a_mover = entrada_usuario.split("mover")[-1].split("mueve")[-1].strip().replace("al escritorio", "").strip()
        print(f"Buscando '{nombre_a_mover}' en tu sistema...")
        
        ruta_encontrada = buscar_archivo_o_carpeta(nombre_a_mover, os.path.expanduser('~'))

        if ruta_encontrada:
            print(f"¡Lo encontré! La ruta es: '{ruta_encontrada}'.")
            confirmacion = input("¿Quieres moverlo al escritorio? (Sí/No): ")
            if confirmacion.lower() == 'si' or confirmacion.lower() == 'sí':
                if mover_a_escritorio(ruta_encontrada):
                    print(f"Hecho, he movido '{nombre_a_mover}' al escritorio.")
                else:
                    print(f"Hubo un error al mover '{nombre_a_mover}'.")
            else:
                print("Operación cancelada. El archivo o carpeta no fue movido.")
        else:
            print(f"No pude encontrar un archivo o carpeta con el nombre '{nombre_a_mover}'.")
    
    # La IA aprende a borrar archivos y carpetas.
    elif "borrar" in entrada_usuario.lower() or "eliminar" in entrada_usuario.lower() or "quitar" in entrada_usuario.lower():
        nombre_a_eliminar = entrada_usuario.split("borrar")[-1].split("eliminar")[-1].split("quitar")[-1].strip()
        print(f"Buscando '{nombre_a_eliminar}' en tu sistema...")

        ruta_encontrada = buscar_archivo_o_carpeta(nombre_a_eliminar, os.path.expanduser('~'))

        if ruta_encontrada:
            print(f"¡Lo encontré! La ruta es: '{ruta_encontrada}'.")
            confirmacion = input(f"Advertencia: ¿Estás seguro de que quieres eliminar '{nombre_a_eliminar}'? (Sí/No): ")
            if confirmacion.lower() == 'si' or confirmacion.lower() == 'sí':
                if borrar_archivo_o_carpeta(ruta_encontrada):
                    print(f"Hecho, he eliminado '{nombre_a_eliminar}'.")
                else:
                    print(f"Hubo un error al eliminar '{nombre_a_eliminar}'.")
            else:
                print("Operación cancelada. El archivo o carpeta no fue eliminado.")
        else:
            print(f"No pude encontrar un archivo o carpeta con el nombre '{nombre_a_eliminar}'.")

    else:
        print("Hmm, no estoy seguro de cómo ayudarte con eso. ¿Podrías ser más específico?")

# Se llama a la función principal para que el programa inicie.
if __name__ == "__main__":
    main()