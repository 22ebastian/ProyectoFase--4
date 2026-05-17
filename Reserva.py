# ---------------------------------------------------------------------------------
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# PROGRAMA: Ingeniería de Sistemas
# CURSO: Programación Orientada a Objetos - Código: 213023
# PROYECTO: Sistema de Gestión Integral 'Software FJ'
# ARCHIVO: Reserva.py - Módulo de Integración y Lógica de Negocio
# ---------------------------------------------------------------------------------

# Importación de clases base para la integración de objetos
from core.cliente import Cliente # Importa la clase Cliente para asociar al titular de la reserva
from core.servicios import Servicio # Importa la clase abstracta Servicio para la polimorfismo
# Importación de excepciones personalizadas para el manejo robusto de errores
from utils.exceptions import (
    ValidationError, 
    ServiceUnavailableError, 
    CostCalculationError,
    ReservaError # Asumiendo una excepción base para este módulo
)
# Importación del sistema de logs para trazabilidad
from utils.logger import log_error 
import uuid # Librería para generar identificadores únicos universales (ID de Reserva)

class Reserva:
    """
    Clase que integra Cliente y Servicio para gestionar el ciclo de vida de una reserva.
    Aplica encapsulamiento estricto y manejo avanzado de excepciones.
    """

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: float):
        """
        Constructor de la clase Reserva. Recibe objetos instanciados para su integración.
        """
        # Bloque try-except para validar la integridad de los objetos recibidos en la inicialización
        try:
            # Encapsulación: Atributos privados con doble guion bajo para máxima protección
            self.__id_reserva = str(uuid.uuid4())[:8] # Genera un ID corto y único para la reserva
            
            # Validación de tipos: Asegura que los objetos integrados sean de las clases correctas
            if not isinstance(cliente, Cliente):
                raise ValidationError("El objeto proporcionado no es un Cliente válido.") # Lanza error si no es clase Cliente
            if not isinstance(servicio, Servicio):
                raise ValidationError("El objeto proporcionado no es un Servicio válido.") # Lanza error si no es clase Servicio
            
            self.__cliente = cliente # Asigna el objeto cliente de forma protegida
            self.__servicio = servicio # Asigna el objeto servicio de forma protegida
            self.__duracion = duracion # Asigna la duración (horas o días según el servicio)
            self.__estado = "PENDIENTE" # Estado inicial por defecto de toda reserva nueva
            self.__costo_total = 0.0 # Inicializa el costo en cero hasta que se procese
            
        except ValidationError as e:
            log_error(f"Error crítico en inicialización de Reserva: {str(e)}") # Registra el error en el log externo
            raise e # Propaga la excepción para evitar la creación de un objeto inconsistente
        finally:
            # Comentario técnico: El bloque finally asegura que el intento de creación sea registrado en consola
            print(f"[SISTEMA] Intento de creación de reserva finalizado para ID: {self.__id_reserva}")

    # --- MÉTODOS DE GESTIÓN (ENCAPSULAMIENTO DE LÓGICA) ---

    def confirmar_reserva(self) -> bool:
        """
        Cambia el estado de la reserva a CONFIRMADA tras validar disponibilidad del servicio.
        """
        try:
            # Verifica si el servicio integrado tiene disponibilidad operativa
            if not self.__servicio.is_available:
                # Lanza excepción personalizada si el servicio está ocupado o inactivo
                raise ServiceUnavailableError(f"El servicio {self.__servicio.name} no está disponible.")
            
            self.__estado = "CONFIRMADA" # Actualiza el atributo privado de estado
            print(f"[INFO] Reserva {self.__id_reserva} confirmada con éxito.") # Notificación en consola
            return True # Retorna éxito en la operación
            
        except ServiceUnavailableError as e:
            log_error(f"Fallo de confirmación: {str(e)}") # Registra el evento en Logger.py
            return False # Retorna falso para que el sistema continúe sin detenerse
        finally:
            # Registro técnico de auditoría interna
            print(f"[AUDIT] Ejecución del método confirmar_reserva para ID: {self.__id_reserva}")

    def cancelar_reserva(self) -> None:
        """
        Gestiona la anulación de la reserva de forma segura, actualizando el estado.
        """
        try:
            # Valida si la reserva ya está en un estado que no permite cancelación
            if self.__estado == "CANCELADA":
                print(f"[WARN] La reserva {self.__id_reserva} ya se encuentra anulada.") # Advertencia
                return # Sale del método sin errores
            
            self.__estado = "CANCELADA" # Realiza la mutación del estado privado
            print(f"[LOG] Reserva {self.__id_reserva} ha sido marcada como CANCELADA.") # Registro de éxito
            
        except Exception as e:
            # Captura cualquier error no previsto durante la cancelación
            log_error(f"Error inesperado al cancelar reserva {self.__id_reserva}: {str(e)}")
        finally:
            print(f"[INFO] Proceso de cancelación finalizado para ID: {self.__id_reserva}")

    def procesar_reserva(self, tasa_impuesto: float = 0.19) -> float:
        """
        Realiza el cálculo final del costo integrando los datos del servicio y el cliente.
        Implementa encadenamiento de excepciones (Exception Chaining).
        """
        try:
            # Bloque principal de procesamiento financiero
            print(f"[PROCESO] Iniciando cálculo de costos para {self.__cliente.name}...")
            
            # Polimorfismo: Se llama a calcular_costo independientemente del tipo de servicio
            # Se pasan las 'horas' o 'días' a través de los argumentos dinámicos del servicio
            params = {"hours": self.__duracion, "days": self.__duracion}
            
            # Intento de cálculo polimórfico
            resultado_base = self.__servicio.calcular_costo(tax_rate=tasa_impuesto, **params)
            
            self.__costo_total = resultado_base # Asigna el resultado final al atributo privado
            return self.__costo_total # Retorna el valor para reportes o facturación
            
        except (CostCalculationError, InvalidServiceParameterError) as error_original:
            # ENCADENAMIENTO DE EXCEPCIONES: Se lanza una nueva excepción detallando el origen
            msg = f"Error al procesar la reserva {self.__id_reserva} debido a un fallo en el cálculo del servicio."
            log_error(msg) # Registro en el log
            # Lanza la excepción personalizada 'ReservaError' encadenando el error previo con 'from'
            raise ReservaError(msg) from error_original 
            
        else:
            # Se ejecuta solo si el cálculo fue exitoso
            print(f"[EXITO] Facturación completada. Total: ${self.__costo_total:,.2f} COP.")
            
        finally:
            # El sistema garantiza que este mensaje aparezca sin importar si hubo error o no
            print(f"[CLEANUP] Recursos de procesamiento liberados para la reserva {self.__id_reserva}.")

    # --- GETTERS PARA ACCESO CONTROLADO (READ-ONLY) ---

    @property
    def id_reserva(self) -> str:
        return self.__id_reserva # Permite leer el ID pero no modificarlo directamente

    @property
    def cliente(self) -> Cliente:
        return self.__cliente # Retorna el objeto cliente asociado

    @property
    def estado(self) -> str:
        return self.__estado # Retorna el estado actual de la reserva

    @property
    def costo_total(self) -> float:
        return self.__costo_total # Retorna el valor final calculado
    