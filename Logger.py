# =================================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# PROGRAMA: Ingeniería de Sistemas
# CURSO: Programación Orientada a Objetos - Código: 213023
# AUTOR: Juan Sebastian Vitola Polo
# PROYECTO: Sistema Integral de Gestión de Operaciones 'Software FJ'
# ARCHIVO: Logger.py
# DESCRIPCIÓN: Motor de auditoría y persistencia de eventos en archivos de texto.
# =================================================================================

# Importación del módulo datetime para la gestión y formateo de marcas de tiempo.
import datetime
# Importación del módulo os para operaciones del sistema operativo y rutas de archivos.
import os
# Importación del módulo traceback para extraer y formatear la traza de pila de las excepciones.
import traceback
# Importación de utilidades de tipado estático (Type Hinting) para robustez del código.
from typing import Optional

# Definición de la clase GestorLogs que encapsulará la lógica de auditoría del sistema.
class GestorLogs:
    # Definición de una constante de clase con el nombre del archivo de texto externo.
    ARCHIVO_LOGS: str = "registro_eventos.txt"

    # Decorador que convierte el método en estático, permitiendo llamarlo sin instanciar la clase.
    @staticmethod
    # Definición de la función universal requerida con parámetros fuertemente tipados.
    def registrar_evento(nivel: str, mensaje: str, excepcion: Optional[Exception] = None) -> None:
        # Bloque try/except general para garantizar que el logger nunca detenga la aplicación principal.
        try:
            # Obtención de la fecha y hora actual del sistema.
            momento_actual = datetime.datetime.now()
            # Formateo de la fecha y hora en un estándar ISO legible (Año-Mes-Día Hora:Minuto:Segundo).
            timestamp: str = momento_actual.strftime("%Y-%m-%d %H:%M:%S")
            
            # Normalización del nivel de severidad ingresado (pasándolo a mayúsculas y eliminando espacios).
            nivel_formateado: str = str(nivel).strip().upper()
            
            # Creación de la estructura base de la línea de log con los requerimientos exigidos.
            entrada_log: str = f"[{timestamp}] [{nivel_formateado}] {mensaje}"

            # Verificación condicional para determinar si se adjuntó un objeto de excepción al evento.
            if excepcion is not None:
                # Extracción de los detalles técnicos del error (nombre de la excepción y mensaje interno).
                detalle_error: str = f" | EXCEPCIÓN: {type(excepcion).__name__} - {str(excepcion)}"
                # Concatenación del detalle del error a la línea de log base.
                entrada_log += detalle_error
                
                # Verificación para incluir la traza completa (StackTrace) solo en casos de severidad ERROR.
                if nivel_formateado == "ERROR":
                    # Formateo de la traza de pila completa como una cadena de texto.
                    traza_pila: str = "".join(traceback.format_exception(type(excepcion), excepcion, excepcion.__traceback__))
                    # Adición de la traza de pila con saltos de línea y tabulaciones para facilitar la lectura.
                    entrada_log += f"\n\t--- DETALLE TÉCNICO ---\n\t{traza_pila.replace('\n', '\n\t')}"

            # Apertura del archivo de texto en modo "a" (append/añadir) especificando codificación UTF-8.
            # El uso del bloque 'with' (context manager) garantiza el cierre seguro del archivo incluso si hay errores de I/O.
            with open(GestorLogs.ARCHIVO_LOGS, mode="a", encoding="utf-8") as archivo:
                # Escritura de la cadena de texto final en el archivo, añadiendo un salto de línea al final.
                archivo.write(entrada_log + "\n")

        # Captura de cualquier excepción nativa durante la escritura (ej. permisos denegados, disco lleno).
        except Exception as error_sistema:
            # Requisito cumplido: La aplicación NUNCA se detiene. Imprime un mensaje fallback en la consola del servidor.
            print(f"[FALLO CRÍTICO DEL LOGGER] No se pudo escribir en {GestorLogs.ARCHIVO_LOGS}. Motivo: {str(error_sistema)}")
            # Impresión de la entrada que se perdió para que no desaparezca por completo del flujo de consola temporal.
            print(f"Log irrecuperable: {mensaje}")