# =================================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# PROGRAMA: Ingeniería de Sistemas
# CURSO: Programación Orientada a Objetos - Código: 213023
# PROYECTO: Sistema Integral de Gestión de Operaciones 'Software FJ'
# ARCHIVO: Simulaciones.py
# DESCRIPCIÓN: Motor de pruebas automatizado que ejecuta 10 escenarios complejos
#              para evaluar consistencia, polimorfismo y estabilidad absoluta.
# =================================================================================

# Importación de utilidades del sistema para la verificación de persistencia de logs
import os
# Importación de la entidad cliente desde el paquete core
from core.cliente import Cliente
# Importación de las variantes de servicio polimórficas desde el paquete core
from core.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
# Importación de la clase de integración Reserva desde el paquete core
from core.Reserva import Reserva
# Importación del catálogo de excepciones personalizadas del negocio
from utils.Excepciones import (
    ErrorSoftwareFJ,
    ErrorDatoInvalido,
    ErrorParametroFaltante,
    ErrorServicioNoDisponible,
    ErrorCalculoInconsistente,
    ErrorReservaInvalida
)
# Importación del componente de registro de auditoría externo
from utils.Logger import GestorLogs


def ejecutar_banco_pruebas() -> None:
    """
    Función principal encargada de coordinar, secuenciar y procesar los 10 escenarios
    de simulación bajo aislamiento de memoria para garantizar la continuidad del software.
    """
    # Variables contadoras locales para estructurar el informe final en consola de cara al usuario
    pruebas_exitosas: int = 0
    pruebas_fallidas: int = 0

    # Notificación técnica en consola que marca el arranque de los servicios de simulación
    print("=====================================================================")
    print("     SOFTWARE FJ - SUBSISTEMA DE SIMULACIÓN Y ESTRÉS DE OPERACIONES  ")
    print("=====================================================================\n")
    
    # Registro del evento de inicio en el archivo físico de logs externos
    GestorLogs.registrar_evento("INFO", "Iniciando el banco automatizado de 10 simulaciones del sistema.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 1: Creación de cliente válido, servicio válido y cálculo financiero exitoso con IVA.
    # ----------------------------------------------------------------------------------------------------
    print(">>> Ejecutando Simulación 1: Flujo estándar exitoso de Reserva de Sala...")
    try:
        # Instanciación correcta de un objeto Cliente con datos alfabéticos y numéricos idóneos
        cliente_1 = Cliente(identification="10123456", name="Juan Sebastian", contact="juan.vitola@unad.edu.co")
        # Instanciación correcta de un servicio tipo ReservaSala con parámetros válidos de negocio
        sala_1 = ReservaSala(service_id="SAL-A", name="Sala de Desarrollo Codding", base_cost=60000.0, room_capacity=15)
        # Orquestación de la reserva uniendo los objetos válidos y fijando una duración de 5 horas
        reserva_1 = Reserva(cliente=cliente_1, servicio=sala_1, duracion=5)
        # Cambio de estado de la reserva aplicando las políticas operativas internas
        reserva_1.confirmar_reserva()
        # Procesamiento financiero polimórfico inyectando la tasa impositiva estándar del 19%
        total_1 = reserva_1.procesar_reserva(tasa_impuesto=0.19)
        # Incremento del contador si el hilo operativo no arrojó interrupciones
        pruebas_exitosas += 1
        # Envío de evidencia de éxito rotundo al archivo log externo
        GestorLogs.registrar_evento("INFO", f"Simulación 1 Exitosa. Reserva: {reserva_1.reserva_id}. Facturado: ${total_1:.2f} COP")
    except ErrorSoftwareFJ as error:
        # Captura de fallos de dominio para evitar el colapso del software
        pruebas_fallidas += 1
        # Envío del error capturado con su traza y causa al archivo externo de texto
        GestorLogs.registrar_evento("ERROR", "Fallo crítico en Simulación 1", error)
    finally:
        # Mensaje mandatorio de liberación de recursos en consola para auditoría visual rápida
        print("[FINALLY] Recursos depurados en Simulación 1.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 2: Intento de registro de cliente inválido (Identificación con caracteres alfabéticos).
    # ----------------------------------------------------------------------------------------------------
    print("\n>>> Ejecutando Simulación 2: Validación defensiva de Cliente (ID no numérico)...")
    try:
        # Se fuerza el error inyectando letras en la identificación, lo cual viola el método .isdigit() del Cliente
        cliente_2 = Cliente(identification="ID-INVALIDO123", name="Pedro Perez", contact="pedro@fj.com")
        # Esta línea no se ejecutará debido a que el constructor de Cliente disparará la excepción primero
        sala_2 = ReservaSala(service_id="SAL-B", name="Sala de Juntas", base_cost=40000.0, room_capacity=5)
        reserva_2 = Reserva(cliente=cliente_2, servicio=sala_2, duracion=2)
        pruebas_exitosas += 1
    except (ErrorDatoInvalido, Exception) as error:
        # El sistema captura de manera efectiva el error mitigando la caída de la aplicación
        pruebas_fallidas += 1
        # Registra el error en el log externo demostrando la robustez del manejo de excepciones
        GestorLogs.registrar_evento("ERROR", "Simulación 2 detectó correctamente anomalía en datos del Cliente.", error)
    finally:
        print("[FINALLY] Recursos depurados en Simulación 2.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 3: Intento de registro de cliente inválido (Nombre vacío o con números).
    # ----------------------------------------------------------------------------------------------------
    print("\n>>> Ejecutando Simulación 3: Validación defensiva de Cliente (Nombre con caracteres numéricos)...")
    try:
        # Se introduce un dígito numérico dentro del argumento del nombre para corromper la validación alfabética
        cliente_3 = Cliente(identification="98765432", name="Carlos 3ra Edad", contact="carlos@fj.com")
        # El flujo se corta inmediatamente protegiendo la base de datos en memoria
        pruebas_exitosas += 1
    except (ErrorDatoInvalido, Exception) as error:
        pruebas_fallidas += 1
        # Guarda la evidencia de la detención preventiva del registro anómalo
        GestorLogs.registrar_evento("ERROR", "Simulación 3 bloqueó de forma exitosa un nombre corrupto.", error)
    finally:
        print("[FINALLY] Recursos depurados en Simulación 3.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 4: Creación incorrecta de servicio especializado (Capacidad de personas negativa).
    # ----------------------------------------------------------------------------------------------------
    print("\n>>> Ejecutando Simulación 4: Validación de límites de Servicio (Capacidad de sala inválida)...")
    try:
        # Se define un cliente adecuado para aislar la prueba en el constructor del Servicio
        cliente_4 = Cliente(identification="11223344", name="Laura Gomez", contact="laura@fj.com")
        # Se envía una capacidad de -10 personas, lo que viola las reglas lógicas de un espacio físico
        sala_incorrecta = ReservaSala(service_id="SAL-C", name="Sala Mini", base_cost=30000.0, room_capacity=-10)
        reserva_4 = Reserva(cliente=cliente_4, servicio=sala_incorrecta, duracion=1)
        pruebas_exitosas += 1
    except (ErrorParametroFaltante, ErrorDatoInvalido, Exception) as error:
        pruebas_fallidas += 1
        # Registro de evidencia de la inconsistencia de datos del servicio en el archivo externo
        GestorLogs.registrar_evento("ERROR", "Simulación 4 atajó una capacidad de sala negativa.", error)
    finally:
        print("[FINALLY] Recursos depurados en Simulación 4.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 5: Polimorfismo Exitoso con AlquilerEquipo (Cálculo basado en días con descuento).
    # ----------------------------------------------------------------------------------------------------
    print("\n>>> Ejecutando Simulación 5: Evaluación Polimórfica de Alquiler de Hardware Corporativo...")
    try:
        cliente_5 = Cliente(identification="55667788", name="Andres Torres", contact="andres@fj.com")
        # Instanciación correcta de AlquilerEquipo, activando la firma polimórfica por días calendarios
        servidor_5 = AlquilerEquipo(service_id="EQP-DEV", name="Servidor GPU Nvidia RTX", base_cost=120000.0, equipment_type="Computo Avanzado")
        # Se genera la reserva por una duración de 10 días continuos
        reserva_5 = Reserva(cliente=cliente_5, servicio=servidor_5, duracion=10)
        reserva_5.confirmar_reserva()
        # Se procesa la reserva llamando de forma dinámica al método de costo específico de la subclase
        total_5 = reserva_5.procesar_reserva(tasa_impuesto=0.0)  # Simulación de tarifa cero impuestos
        pruebas_exitosas += 1
        GestorLogs.registrar_evento("INFO", f"Simulación 5 (Hardware Polimórfico) Completada. Total: ${total_5:.2f} COP")
    except ErrorSoftwareFJ as error:
        pruebas_fallidas += 1
        GestorLogs.registrar_evento("ERROR", "Fallo inesperado en Simulación 5", error)
    finally:
        print("[FINALLY] Recursos depurados en Simulación 5.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 6: Intento de Reserva sobre un servicio marcado como No Disponible (Fuera de línea).
    # ----------------------------------------------------------------------------------------------------
    print("\n>>> Ejecutando Simulación 6: Gestión de estados críticos (Servicio No Disponible)...")
    try:
        cliente_6 = Cliente(identification="33445566", name="Marta Polo", contact="marta@fj.com")
        sala_6 = ReservaSala(service_id="SAL-VIP", name="Sala Presidencial", base_cost=150000.0, room_capacity=8)
        # Cambio explícito del flag operativo de disponibilidad para simular que la sala fue ocupada previamente
        sala_6.is_available = False
        reserva_6 = Reserva(cliente=cliente_6, servicio=sala_6, duracion=3)
        # El método confirmar_reserva debe evaluar la disponibilidad y rechazar la asignación
        reserva_6.confirmar_reserva()
        pruebas_exitosas += 1
    except (ErrorServicioNoDisponible, ErrorReservaInvalida, Exception) as error:
        pruebas_fallidas += 1
        # Envío del reporte detallado al log externo explicando la indisponibilidad del recurso tecnológico
        GestorLogs.registrar_evento("ERROR", "Simulación 6 controló correctamente el intento de rentar un servicio sin stock.", error)
    finally:
        print("[FINALLY] Recursos depurados en Simulación 6.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 7: Polimorfismo Exitoso con AsesoriaEspecializada Nivel Principal (Recargo Premium).
    # ----------------------------------------------------------------------------------------------------
    print("\n>>> Ejecutando Simulación 7: Evaluación Polimórfica de Asesoría Senior (Tarifa con Multiplicador)...")
    try:
        cliente_7 = Cliente(identification="88990011", name="Diana Vitola", contact="diana@fj.com")
        # Creación de servicio de consultoría bajo el rango 'PRINCIPAL', lo cual inyecta un recargo del 30% en cascada
        consultoria_7 = AsesoriaEspecializada(service_id="CON-CYBER", name="Auditoría Pentesting", base_cost=200000.0, consultant_level="Principal")
        reserva_7 = Reserva(cliente=cliente_7, servicio=consultoria_7, duracion=4)  # 4 horas de consultoría de élite
        reserva_7.confirmar_reserva()
        # Procesamiento que ejecuta la fórmula de la subclase y adiciona el IVA reglamentario del 19%
        total_7 = reserva_7.procesar_reserva(tasa_impuesto=0.19)
        pruebas_exitosas += 1
        GestorLogs.registrar_evento("INFO", f"Simulación 7 (Consultor Principal) Exitosa. Total Facturado con Recargo: ${total_7:.2f} COP")
    except ErrorSoftwareFJ as error:
        pruebas_fallidas += 1
        GestorLogs.registrar_evento("ERROR", "Fallo inesperado en Simulación 7", error)
    finally:
        print("[FINALLY] Recursos depurados en Simulación 7.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 8: Intento de cálculo financiero con parámetros inconsistentes (Duración negativa).
    # ----------------------------------------------------------------------------------------------------
    print("\n>>> Ejecutando Simulación 8: Detección de anomalías aritméticas (Duración de actividad negativa)...")
    try:
        cliente_8 = Cliente(identification="44556677", name="Roberto Polo", contact="roberto@fj.com")
        sala_8 = ReservaSala(service_id="SAL-D", name="Sala de Pruebas", base_cost=50000.0, room_capacity=10)
        # Se inicializa el objeto reserva inyectando una duración de -8 horas, rompiendo la lógica temporal
        reserva_8 = Reserva(cliente=cliente_8, servicio=sala_8, duracion=-8)
        reserva_8.confirmar_reserva()
        # Al procesarse, el motor financiero de la capa Servicio debe lanzar un CostCalculationError
        reserva_8.procesar_reserva()
        pruebas_exitosas += 1
    except (ErrorCalculoInconsistente, ErrorReservaInvalida, Exception) as error:
        pruebas_fallidas += 1
        # El encadenamiento de excepciones permite resguardar que la causa original fue la inconsistencia aritmética
        GestorLogs.registrar_evento("ERROR", "Simulación 8 interceptó de manera correcta una duración negativa en el procesamiento contable.", error)
    finally:
        print("[FINALLY] Recursos depurados en Simulación 8.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 9: Intento de inyección de parámetros de inicialización del servicio corruptos.
    # ----------------------------------------------------------------------------------------------------
    print("\n>>> Ejecutando Simulación 9: Control de Calidad de Datos del Servicio (Costo Base Negativo)...")
    try:
        # Inicialización de un servicio con un costo base negativo (-50000 COP), violando los principios contables
        servicio_corrupto = ReservaSala(service_id="SAL-FAIL", name="Sala Inexistente", base_cost=-50000.0, room_capacity=10)
        print(servicio_corrupto)
        pruebas_exitosas += 1
    except (ErrorParametroFaltante, ErrorDatoInvalido, Exception) as error:
        pruebas_fallidas += 1
        # Se envía la evidencia del rechazo de costos negativos al almacenamiento físico persistente
        GestorLogs.registrar_evento("ERROR", "Simulación 9 bloqueó exitosamente la instanciación de un servicio con costo financiero negativo.", error)
    finally:
        print("[FINALLY] Recursos depurados en Simulación 9.")

    # ----------------------------------------------------------------------------------------------------
    # SIMULACIÓN 10: Flujo alternativo exitoso con AsesoriaEspecializada Nivel Junior sin IVA.
    # ----------------------------------------------------------------------------------------------------
    print("\n>>> Ejecutando Simulación 10: Flujo exitoso final con Consultoría Nivel Junior...")
    try:
        cliente_10 = Cliente(identification="99001122", name="Esteban Vitola", contact="esteban@fj.com")
        # Creación de consultoría nivel 'JUNIOR' el cual no altera con recargos el costo financiero base establecido
        consultoria_10 = AsesoriaEspecializada(service_id="CON-BASIC", name="Soporte Técnico de Redes", base_cost=80000.0, consultant_level="Junior")
        reserva_10 = Reserva(cliente=cliente_10, servicio=consultoria_10, duracion=2)
        reserva_10.confirmar_reserva()
        # Cálculo contable limpio sin adición de tasa de impuestos
        total_10 = reserva_10.procesar_reserva(tasa_impuesto=0.0)
        pruebas_exitosas += 1
        # Registro del éxito final cerrando de manera perfecta el lote de transacciones simuladas
        GestorLogs.registrar_evento("INFO", f"Simulación 10 Completada Exitosamente. Código Reserva: {reserva_10.reserva_id}. Total: ${total_10:.2f} COP")
    except ErrorSoftwareFJ as error:
        pruebas_fallidas += 1
        GestorLogs.registrar_evento("ERROR", "Fallo inesperado en Simulación 10", error)
    finally:
        print("[FINALLY] Recursos depurados en Simulación 10.")

    # ----------------------------------------------------------------------------------------------------
    # INTERFAZ DE SALIDA E INFORME DE CONSOLIDACIÓN
    # ----------------------------------------------------------------------------------------------------
    print("\n=====================================================================")
    print("        INFORME DE CIERRE DE SIMULACIONES - SOFTWARE FJ               ")
    print("=====================================================================")
    print(" >> ESTADO: Proceso de evaluación automatizado finalizado de forma estable.")
    print(f" >> SIMULACIONES COMPLETADAS EXITOSAMENTE : {pruebas_exitosas} / 10")
    print(f" >> SIMULACIONES CONTROLADAS CON FALLO    : {pruebas_fallidas} / 10")
    print(" >> NOTA IMPORTANTE: El detalle pormenorizado técnico, los mensajes de error")
    print("    y las trazas de pila se encuentran en 'registro_eventos.txt'.")
    print("=====================================================================\n")
    
    # Registro final en log para auditoría de sistemas externa
    GestorLogs.registrar_evento("INFO", f"Banco de pruebas cerrado. Exitosas: {pruebas_exitosas}. Fallidas: {pruebas_fallidas}.")


# Punto de entrada estándar para asegurar la ejecución limpia del módulo desde la terminal
if __name__ == "__main__":
    ejecutar_banco_pruebas()