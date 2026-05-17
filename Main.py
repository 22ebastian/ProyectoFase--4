# =================================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# PROGRAMA: Ingeniería de Sistemas
# CURSO: Programación Orientada a Objetos - Código: 213023
# AUTOR: Juan Sebastian Vitola Polo
# PROYECTO: Sistema Integral de Gestión de Operaciones 'Software FJ'
# ARCHIVO: Main.py
# DESCRIPCIÓN: Punto de entrada oficial (Bootstrap) del sistema. Orquesta las
#              capas de negocio, validación, auditoría y el motor de simulaciones.
# =================================================================================

# Importación de módulos del sistema para interactuar con el entorno operativo y el intérprete
import sys
# Importación del módulo de auditoría persistente para registrar el ciclo de vida de la aplicación
from utils.Logger import GestorLogs
# Importación de la jerarquía de excepciones personalizadas para el control defensivo global
from utils.Excepciones import ErrorSoftwareFJ
# Importación del motor de simulación encargado de ejecutar el banco de 10 pruebas de estrés
from Simulaciones import ejecutar_banco_pruebas

# Importaciones explícitas de las entidades del núcleo (core) para garantizar su correcto empaquetado y compilación
from core.cliente import Cliente
from core.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from core.Reserva import Reserva


def inicializar_sistema_core() -> None:
    """
    Función principal de arranque (Bootstrap). Inicializa el entorno, gestiona el flujo
    operativo de las simulaciones y encapsula los fallos inesperados de última línea.
    """
    # --- ENCABEZADO PROFESIONAL POR CONSOLA ---
    # Imprime líneas decorativas para delimitar la presentación institucional en el terminal
    print("=====================================================================")
    # Muestra el nombre oficial de la compañía tecnológica asignada en el proyecto
    print("        SOFTWARE FJ - SISTEMA CORE DE GESTIÓN EMPRESARIAL            ")
    # Muestra la información académica obligatoria de la escuela de ciencias básicas e ingeniería
    print("   UNAD - INGENIERÍA DE SISTEMAS - PROGRAMACIÓN ORIENTADA A OBJETOS  ")
    # Muestra el código del curso reglamentario correspondiente a la rúbrica actual
    print("                        CURSO: 213023                                ")
    # Cierre de la sección visual del encabezado del software corporativo
    print("=====================================================================\n")

    # --- REGISTRO DE INICIO DE CICLO DE VIDA ---
    # Escribe de forma persistente en el archivo externo el momento exacto en el que el programa fue lanzado
    GestorLogs.registrar_evento("INFO", "SISTEMA INICIADO: El punto de entrada principal (Main.py) se está ejecutando.")

    # Bloque try/except/else/finally de nivel macro encargado de garantizar la estabilidad absoluta del software
    try:
        # Notificación visual en consola que indica la delegación de control al paquete de pruebas
        print("[ORQUESTADOR] Transfiriendo el flujo operativo al motor de simulaciones de Software FJ...\n")
        
        # Invocación obligatoria del lote de las 10 simulaciones mixtas desarrolladas en Simulaciones.py
        ejecutar_banco_pruebas()

    # Captura especializada para atrapar excepciones controladas del dominio que hayan escalado al nivel superior
    except ErrorSoftwareFJ as excepcion_negocio:
        # Registra el fallo de lógica empresarial en el logger externo sin interrumpir la ejecución del sistema operativo
        GestorLogs.registrar_evento("ERROR", "Se interceptó una excepción de negocio no controlada en la capa Main.", excepcion_negocio)
        # Informa amigablemente al usuario en terminal que el error fue mitigado de forma segura
        print(f"\n⚠️ [CONTROL DE ESTABILIDAD] Error de negocio mitigado en Main: {str(excepcion_negocio)}")

    # Captura universal (Fallback) encargada de atrapar cualquier error imprevisto (ej. falta de memoria, bugs del intérprete)
    except Exception as excepcion_inesperada:
        # Registra de forma crítica el error del sistema junto con su traza técnica completa para posterior depuración
        GestorLogs.registrar_evento("ERROR", "CRITICAL SYSTEM FAULT: Error imprevisto de bajo nivel mitigado.", excepcion_inesperada)
        # Despliega un mensaje controlado en consola impidiendo que el software muestre un volcado de memoria crudo
        print(f"\n🚨 [CRITICAL FALLBACK] El sistema ha controlado una anomalía técnica grave de forma exitosa.")

    # Bloque else que se ejecuta únicamente si las simulaciones y la orquestación transcurrieron sin registrar incidentes
    else:
        # Muestra un mensaje de éxito operativo total en la consola del terminal
        print("\n[ORQUESTADOR] Toda la secuencia de simulaciones fue procesada de manera íntegra y secuencial.")
        # Escribe en el archivo físico de texto externo la culminación exitosa de los hilos de ejecución de la suite
        GestorLogs.registrar_evento("INFO", "SISTEMA FINALIZADO: Flujo de ejecución completado satisfactoriamente.")

    # Bloque finally obligatorio ejecutado siempre para garantizar el cierre formal del ciclo de vida de la aplicación
    finally:
        # Imprime la confirmación del estado de resiliencia final antes de liberar el hilo del proceso actual
        print("\n=====================================================================")
        # Indica al usuario que la aplicación web/consola se cerró sin experimentar rupturas abruptas
        print("  ESTADO DE LA APLICACIÓN: ESTABLE | EJECUCIÓN CONTROLADA FINALIZADA ")
        print("=====================================================================\n")


# Bloque arquitectónico estándar de Python que valida si el archivo está siendo ejecutado de forma directa
if __name__ == "__main__":
    # Invoca la función core de arranque inicializando la orquestación global del ecosistema
    inicializar_sistema_core()
    # Finaliza el proceso del intérprete devolviendo un código de salida cero (operación exitosa sin fallos de salida)
    sys.exit(0)