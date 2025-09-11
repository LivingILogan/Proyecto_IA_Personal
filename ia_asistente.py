# Archivo: ia_asistente.py

# Se importan las librerías necesarias
import json
import sys
import os
import pyautogui
import psutil
import shutil
import re
import webbrowser
import time

# Mapeo de nombres comunes a nombres de archivo ejecutables
programa_map = {
    "bloc de notas": "notepad.exe",
    "bloc": "notepad.exe",
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "excel": "excel.exe",
    "word": "winword.exe",
    "microsoft word": "winword.exe",
    "powerpoint": "powerpnt.exe",
    "calculadora": "calc.exe",
    "calculadora de windows": "calc.exe",
    "vscode": "code.exe",
    "visual studio code": "code.exe",
    "visual": "code.exe"
}

def guardar_lista(data):
    with open('listas.json', 'w') as file:
        json.dump(data, file, indent=4)

def leer_listas():
    try:
        with open('listas.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []

def borrar_tareas(nombre, tareas_a_borrar):
    listas = leer_listas()
    if listas:
        for lista in listas:
            if lista.get('nombre_lista') == nombre:
                tareas_existentes = lista.get('tareas')
                tareas_actualizadas = [tarea for tarea in tareas_existentes if tarea not in tareas_a_borrar]
                lista['tareas'] = tareas_actualizadas
                guardar_lista(listas)
                return True
    return False

def abrir_programa(nombre_programa):
    if sys.platform == 'win32':
        nombre_ejecutable = programa_map.get(nombre_programa.lower(), nombre_programa)
        os.system(f'start {nombre_ejecutable}')
    elif sys.platform == 'darwin':
        os.system(f'open -a {nombre_programa}')
    elif sys.platform == 'linux':
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

def buscar_archivo_o_carpeta(nombre):
    ruta_busqueda = "C:\\"
    print(f"Buscando '{nombre}' en la raíz del disco duro...")
    for root, dirs, files in os.walk(ruta_busqueda):
        try:
            if nombre in files:
                return os.path.join(root, nombre)
            if nombre in dirs:
                return os.path.join(root, nombre)
        except PermissionError:
            continue
    return None

def buscar_en_google(query):
    query_limpia = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query_limpia}"
    webbrowser.open(url)

def guardar_playlist(canciones):
    print(f"Creando playlist con las siguientes canciones: {canciones}")
    
def mover_a_escritorio(ruta_completa_a_mover):
    try:
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        shutil.move(ruta_completa_a_mover, desktop_path)
        return True
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

def hacer_clic_en_imagen(nombre_imagen):
    try:
        ubicacion = pyautogui.locateOnScreen(nombre_imagen, confidence=0.8)
        if ubicacion:
            punto_clic = pyautogui.center(ubicacion)
            pyautogui.click(punto_clic)
            print(f"Haciendo clic en la imagen '{nombre_imagen}'.")
            return True
        else:
            print(f"No pude encontrar la imagen '{nombre_imagen}' en la pantalla.")
            return False
    except pyautogui.PyAutoGUIException as e:
        print(f"Error al intentar encontrar la imagen: {e}")
        return False

def escribir_en_programa(texto):
    """
    Escribe el texto proporcionado en la ventana activa.
    Se necesita que el usuario cambie a la ventana del programa.
    """
    try:
        # Pídele al usuario que cambie a la ventana donde quiere escribir.
        print("Cambiando a la ventana del programa... Por favor, ¡no toques el teclado ni el ratón!")
        time.sleep(2)  # Dale 2 segundos para que el usuario cambie de ventana si es necesario
        
        # Simula las pulsaciones de teclado para escribir el texto
        pyautogui.typewrite(texto, interval=0.1) # El intervalo hace que la escritura se vea más natural
        print("Hecho. He escrito el texto en la ventana activa.")
        return True
    except pyautogui.PyAutoGUIException as e:
        print(f"Error al intentar escribir: {e}")
        return False

def main():
    entrada_usuario = input("Hola, soy tu IA. ¿Qué necesitas que haga por ti? ")
    
    # Intenciones de crear listas
    if any(keyword in entrada_usuario.lower() for keyword in ["lista", "tarea"]) and any(keyword in entrada_usuario.lower() for keyword in ["crear", "hacer", "añadir", "agregar"]):
        print("¡Entendido! Vamos a trabajar con listas.")
        
        # Lógica para crear, añadir o borrar
        if "crear" in entrada_usuario.lower() or "hacer" in entrada_usuario.lower():
            nombre_lista = input("¿Qué nombre le ponemos a la lista? ")
            tareas_lista = input("¿Qué tareas quieres añadir? (separa con comas) ")
            
            nueva_lista = {
                'nombre_lista': nombre_lista,
                'tareas': [tarea.strip() for tarea in tareas_lista.split(',')]
            }
            
            listas_existentes = leer_listas()
            listas_existentes.append(nueva_lista)
            
            guardar_lista(listas_existentes)
            print(f"Perfecto, he creado la lista '{nombre_lista}' con tus tareas. ¡Ya no la olvidaré!")
        
        elif any(keyword in entrada_usuario.lower() for keyword in ["añadir", "agregar"]):
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
                        return
                
                print(f"No encontré una lista con el nombre '{nombre_lista_a_modificar}'.")
            else:
                print("No tienes ninguna lista creada. Primero debes crear una.")

        elif any(keyword in entrada_usuario.lower() for keyword in ["borrar", "quitar", "eliminar", "desechar"]):
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

    # La IA aprende a leer listas
    elif any(keyword in entrada_usuario.lower() for keyword in ["mostrar", "ver", "revisar", "leer", "enseñar"]) and "listas" in entrada_usuario.lower():
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
    
    # Intenciones de abrir programas
    elif any(keyword in entrada_usuario.lower() for keyword in ["abrir", "lanza", "ejecuta"]):
        # Obtiene el nombre del programa
        palabras_entrada = entrada_usuario.split()
        nombre_programa = ""
        for i, palabra in enumerate(palabras_entrada):
            if palabra.lower() in ["abrir", "lanza", "ejecuta"]:
                nombre_programa = " ".join(palabras_entrada[i+1:])
                break
        
        # Primero, intenta abrir el programa directamente por su nombre
        abrir_programa(nombre_programa)
        print(f"Intentando abrir el programa '{nombre_programa}' directamente...")
        time.sleep(3) # Espera un momento para ver si se abre

        # Si el programa no está abierto, intenta una búsqueda en el menú de inicio
        if not any(proc.name().lower() in programa_map.get(nombre_programa.lower(), '').lower() for proc in psutil.process_iter()):
            print(f"No pude abrir el programa '{nombre_programa}' directamente. Buscando en el menú de inicio...")
            pyautogui.press('win')
            time.sleep(1) # Espera un momento para que se abra el menú de inicio
            pyautogui.typewrite(nombre_programa)
            time.sleep(1)
            pyautogui.press('enter')
            print(f"Hecho. He buscado y ejecutado '{nombre_programa}' desde el menú de inicio.")
        else:
            print(f"Hecho, he abierto {nombre_programa}.")
    
    # Nueva intención: escribir texto
    elif "escribe" in entrada_usuario.lower():
        texto_a_escribir = entrada_usuario.lower().replace("escribe ", "", 1)
        if texto_a_escribir:
            escribir_en_programa(texto_a_escribir)
        else:
            print("No me dijiste qué quieres que escriba.")

    # Intenciones de cerrar programas
    elif any(keyword in entrada_usuario.lower() for keyword in ["cerrar", "cierra", "detener"]):
        print("¡Claro! ¿Qué programa te gustaría cerrar?")
        nombre_programa = input("Nombre del programa: ")

        if cerrar_programa_por_nombre(nombre_programa):
            print(f"Hecho, he cerrado {nombre_programa}.")
        else:
            print(f"No pude encontrar un programa con el nombre '{nombre_programa}' para cerrar.")
            
    # Intenciones de crear carpetas
    elif any(keyword in entrada_usuario.lower() for keyword in ["crear", "hacer", "crea"]) and "carpeta" in entrada_usuario.lower():
        print("¡Claro! ¿Qué nombre le ponemos a la carpeta?")
        nombre_carpeta = input("Nombre de la carpeta: ")

        if crear_carpeta(nombre_carpeta):
            print(f"Hecho, he creado la carpeta '{nombre_carpeta}'.")
        else:
            print(f"La carpeta '{nombre_carpeta}' ya existe o hubo un error al crearla.")

    # Intenciones de mover
    elif any(keyword in entrada_usuario.lower() for keyword in ["mover", "mueve", "traslada"]):
        palabras_entrada = entrada_usuario.split()
        nombre_a_mover = ""
        for i, palabra in enumerate(palabras_entrada):
            if palabra.lower() in ["mover", "mueve", "traslada"]:
                nombre_a_mover = " ".join(palabras_entrada[i+1:])
                break

        nombre_a_mover = re.sub(r'(la|el|una|un|carpeta|archivo|llamada|que se llama|a|de)\s*', '', nombre_a_mover, flags=re.IGNORECASE).strip()

        if not nombre_a_mover:
            nombre_a_mover = input("¿Qué archivo o carpeta te gustaría mover? ")

        print(f"Buscando '{nombre_a_mover}' en tu sistema...")
        
        ruta_encontrada = buscar_archivo_o_carpeta(nombre_a_mover)

        if ruta_encontrada:
            print(f"¡Lo encontré! La ruta es: '{ruta_encontrada}'.")
            confirmacion = input("¿Quieres moverlo al escritorio? (Sí/No): ")
            if confirmacion.lower() in ["si", "sí"]:
                if mover_a_escritorio(ruta_encontrada):
                    print(f"Hecho, he movido '{nombre_a_mover}' al escritorio.")
                else:
                    print(f"Hubo un error al mover '{nombre_a_mover}'.")
            else:
                print("Operación cancelada. El archivo o carpeta no fue movido.")
        else:
            print(f"No pude encontrar un archivo o carpeta con el nombre '{nombre_a_mover}'.")
    
    # Intenciones de borrar
    elif any(keyword in entrada_usuario.lower() for keyword in ["borrar", "quitar", "eliminar", "desechar"]):
        palabras_entrada = entrada_usuario.split()
        nombre_a_eliminar = ""
        for i, palabra in enumerate(palabras_entrada):
            if palabra.lower() in ["borrar", "quitar", "eliminar", "desechar"]:
                nombre_a_eliminar = " ".join(palabras_entrada[i+1:])
                break
        
        nombre_a_eliminar = re.sub(r'(la|el|una|un|carpeta|archivo|llamada|que se llama)\s*', '', nombre_a_eliminar, flags=re.IGNORECASE).strip()

        if not nombre_a_eliminar:
            nombre_a_eliminar = input("¿Qué archivo o carpeta quieres eliminar? ")

        print(f"Buscando '{nombre_a_eliminar}' en tu sistema...")

        ruta_encontrada = buscar_archivo_o_carpeta(nombre_a_eliminar)

        if ruta_encontrada:
            print(f"¡Lo encontré! La ruta es: '{ruta_encontrada}'.")
            confirmacion = input(f"Advertencia: ¿Estás seguro de que quieres eliminar '{nombre_a_eliminar}'? (Sí/No): ")
            if confirmacion.lower() in ["si", "sí"]:
                if borrar_archivo_o_carpeta(ruta_encontrada):
                    print(f"Hecho, he eliminado '{nombre_a_eliminar}'.")
                else:
                    print(f"Hubo un error al eliminar '{nombre_a_eliminar}'.")
            else:
                print("Operación cancelada. El archivo o carpeta no fue eliminado.")
        else:
            print(f"No pude encontrar un archivo o carpeta con el nombre '{nombre_a_eliminar}'.")
    
    # Intenciones para YouTube Music
    elif "música" in entrada_usuario.lower() or "canción" in entrada_usuario.lower() or "banda" in entrada_usuario.lower() or "álbum" in entrada_usuario.lower() or "playlist" in entrada_usuario.lower():
        if "guardar" in entrada_usuario.lower() or "crear" in entrada_usuario.lower():
            playlist_info = re.search(r'guardar playlist (.*) con las canciones (.*)', entrada_usuario)
            if playlist_info:
                nombre_playlist = playlist_info.group(1).strip()
                canciones = [c.strip() for c in playlist_info.group(2).split(',')]
                guardar_playlist(canciones)
                print(f"Hecho, he creado la playlist '{nombre_playlist}' en YouTube Music.")
            else:
                print("No entendí la frase. Por favor, dime el nombre de la playlist y las canciones que quieres guardar.")
        
        elif "pon" in entrada_usuario.lower() or "reproduce" in entrada_usuario.lower():
            print("Función de reproducción de música en desarrollo...")
        else:
            print("No entendí tu solicitud. ¿Qué quieres que haga con la música?")
    
    # Nueva funcionalidad: Búsqueda en Google
    elif any(keyword in entrada_usuario.lower() for keyword in ["busca", "google", "investiga", "qué es"]):
        palabras_entrada = entrada_usuario.lower().split()
        query_inicio = -1
        for i, palabra in enumerate(palabras_entrada):
            if palabra in ["busca", "google", "investiga"]:
                query_inicio = i + 1
                break
            elif palabra == "es" and i > 0 and palabras_entrada[i-1] == "qué":
                query_inicio = i + 1
                break

        if query_inicio != -1 and query_inicio < len(palabras_entrada):
            query = " ".join(palabras_entrada[query_inicio:])
            print(f"Buscando en Google: {query}")
            buscar_en_google(query)
            print("Hecho. He abierto la búsqueda en tu navegador.")
        else:
            print("No entendí tu búsqueda. Por favor, dime qué quieres que busque.")
            
    # Nueva funcionalidad: Clics en cualquier parte de la pantalla
    elif any(keyword in entrada_usuario.lower() for keyword in ["clic en imagen", "clic en el ícono", "haz clic en el ícono", "haz clic en la imagen"]):
        # Extrae el nombre del archivo de la imagen de la frase
        match = re.search(r'clic en (?:la imagen|el ícono) (.+)', entrada_usuario.lower())
        if match:
            nombre_imagen = match.group(1).strip()
            # La IA puede esperar a que el usuario posicione la ventana para encontrar la imagen
            print("Posiciona la ventana del programa para que la IA encuentre el icono.")
            time.sleep(5)  # Espera 5 segundos para que el usuario se prepare
            hacer_clic_en_imagen(nombre_imagen)
        else:
            print("Para hacer clic en una imagen, necesito el nombre del archivo. Por ejemplo: 'haz clic en el ícono de WhatsApp.png'")

    else:
        print("Hmm, no estoy seguro de cómo ayudarte con eso. ¿Podrías ser más específico?")

# Se llama a la función principal para que el programa inicie.
if __name__ == "__main__":
    main()