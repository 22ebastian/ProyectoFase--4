# core/servicios.py

# Importación de la infraestructura de clases abstractas del lenguaje
from abc import ABC, abstractmethod
# Importación de utilidades de tipado estático estructurado para robustez en producción
from typing import Optional, Dict, Any
# Importación de las excepciones personalizadas del dominio corporativo
from utils.exceptions import ServiceUnavailableError, InvalidServiceParameterError, CostCalculationError
# Importación del módulo de auditoría de logs
from utils.logger import log_error

class Servicio(ABC):
    """
    Clase abstracta pura que define el contrato arquitectónico y el estado base
    para todas las ofertas de servicios dentro de la organización Software FJ.
    """

    # Constructor base con encapsulamiento estricto mediante Name Mangling (doble guion bajo)
    def __init__(self, service_id: str, name: str, base_cost: float):
        # Validación defensiva en constructor base para evitar objetos corruptos en memoria
        if not service_id or not name or base_cost < 0:
            raise InvalidServiceParameterError("Datos de inicialización de servicio inválidos o costo negativo.")
            
        self.__service_id: str = str(service_id).strip()
        self.__name: str = str(name).strip()
        self.__base_cost: float = float(base_cost)
        self.__is_available: bool = True  # Flag de control operativo interno

    # --- MÉTODOS ABSTRACTOS DE CONTRATO OBLIGATORIO ---

    @abstractmethod
    def calcular_costo(self, tax_rate: Optional[float] = None, discount: Optional[float] = None, **kwargs: Any) -> float:
        """Calcula el costo total neto aplicando polimorfismo y sobrecarga opcional."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna la ficha técnica descriptiva del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, params: Dict[str, Any]) -> bool:
        """Verifica la integridad de los parámetros requeridos para la operación."""
        pass

    # --- INTERFAZ DE ENCAPSULAMIENTO (PROPERTIES / GETTERS Y SETTERS) ---

    @property
    def service_id(self) -> str:
        """Expone de forma segura el ID de solo lectura del servicio."""
        return self.__service_id

    @property
    def name(self) -> str:
        """Expone el nombre del servicio."""
        return self.__name

    @property
    def base_cost(self) -> float:
        """Expone el costo financiero base del servicio."""
        return self.__base_cost

    @property
    def is_available(self) -> bool:
        """Expone el estado de disponibilidad del servicio en el catálogo."""
        return self.__is_available

    @is_available.setter
    def is_available(self, status: bool) -> None:
        """Permite mutar la disponibilidad operativa bajo control de tipo."""
        if not isinstance(status, bool):
            raise InvalidServiceParameterError("El estado de disponibilidad debe ser un valor booleano.")
        self.__is_available = status


class ReservaSala(Servicio):
    """
    Servicio especializado en la gestión y reserva temporal de salas físicas o virtuales.
    """

    def __init__(self, service_id: str, name: str, base_cost: float, room_capacity: int):
        # Transfiere los atributos core a la superclase abstracta
        super().__init__(service_id, name, base_cost)
        if room_capacity <= 0:
            raise InvalidServiceParameterError("La capacidad de la sala debe ser un entero positivo.")
        # Atributo privado específico de la clase hija
        self.__room_capacity: int = int(room_capacity)

    def validar_parametros(self, params: Dict[str, Any]) -> bool:
        # Bloque try/except/else/finally de control estructural de calidad académica y de producción
        try:
            if not self.is_available:
                raise ServiceUnavailableError(f"La sala '{self.name}' se encuentra fuera de servicio temporalmente.")
            
            hours = params.get("hours")
            if hours is None or not isinstance(hours, (int, float)) or hours <= 0:
                raise InvalidServiceParameterError("El parámetro 'hours' es mandatorio y debe ser mayor a cero.")
                
        except (ServiceUnavailableError, InvalidServiceParameterError) as error:
            log_error(f"[ReservaSala ID: {self.service_id}] Error de Validación: {str(error)}")
            raise error
        else:
            return True
        finally:
            print(f"[AUDIT] Proceso de validación completado para la Sala ID: {self.service_id}")

    def calcular_costo(self, tax_rate: Optional[float] = None, discount: Optional[float] = None, **kwargs: Any) -> float:
        try:
            # Extrae las horas pasadas por kwargs dinámicos, por defecto evalúa 1
            hours = kwargs.get("hours", 1)
            # Invoca la validación interna del estado y parámetros
            self.validar_parametros({"hours": hours})
            
            # Lógica financiera base: Costo proporcional al tiempo de uso de la infraestructura
            total_cost = self.base_cost * hours
            
            # Sobrecarga opcional: Aplicación de impuestos (IVA)
            if tax_rate is not None:
                if tax_rate < 0:
                    raise CostCalculationError("La tasa impositiva (tax_rate) no puede adoptar valores negativos.")
                total_cost += total_cost * tax_rate
                
            # Sobrecarga opcional: Aplicación de descuentos promocionales corporativos
            if discount is not None:
                if discount < 0 or discount > total_cost:
                    raise CostCalculationError("El descuento aplicado corrompe el balance neto o supera el costo total.")
                total_cost -= discount

        except (CostCalculationError, ServiceUnavailableError, InvalidServiceParameterError) as error:
            log_error(f"[ReservaSala ID: {self.service_id}] Fallo en cálculo financiero: {str(error)}")
            raise error
        else:
            return float(total_cost)

    def describir_servicio(self) -> str:
        return f"Servicio Sala: {self.name} | ID: {self.service_id} | Capacidad: {self.__room_capacity} pax | Tarifa/Hora: ${self.base_cost:.2f}"


class AlquilerEquipo(Servicio):
    """
    Servicio encargado del procesamiento logístico de renta de hardware corporativo.
    """

    def __init__(self, service_id: str, name: str, base_cost: float, equipment_type: str):
        super().__init__(service_id, name, base_cost)
        if not equipment_type or not str(equipment_type).strip():
            raise InvalidServiceParameterError("El tipo de equipo es un campo obligatorio.")
        self.__equipment_type: str = str(equipment_type).strip()

    def validar_parametros(self, params: Dict[str, Any]) -> bool:
        try:
            if not self.is_available:
                raise ServiceUnavailableError(f"El equipo '{self.name}' no está disponible en inventario.")
            
            days = params.get("days")
            if days is None or not isinstance(days, int) or days <= 0:
                raise InvalidServiceParameterError("El parámetro 'days' es mandatorio y debe ser un entero positivo.")
                
        except (ServiceUnavailableError, InvalidServiceParameterError) as error:
            log_error(f"[AlquilerEquipo ID: {self.service_id}] Error de Validación: {str(error)}")
            raise error
        else:
            return True
        finally:
            print(f"[AUDIT] Proceso de validación completado para el Equipo ID: {self.service_id}")

    def calcular_costo(self, tax_rate: Optional[float] = None, discount: Optional[float] = None, **kwargs: Any) -> float:
        try:
            days = kwargs.get("days", 1)
            self.validar_parametros({"days": days})
            
            # Cálculo base basado en días calendario de alquiler
            total_cost = self.base_cost * days
            
            if tax_rate is not None:
                if tax_rate < 0:
                    raise CostCalculationError("La tasa de impuesto no puede ser negativa.")
                total_cost += total_cost * tax_rate
                
            if discount is not None:
                if discount < 0 or discount > total_cost:
                    raise CostCalculationError("El descuento supera el umbral financiero permitido.")
                total_cost -= discount

        except (CostCalculationError, ServiceUnavailableError, InvalidServiceParameterError) as error:
            log_error(f"[AlquilerEquipo ID: {self.service_id}] Fallo en cálculo financiero: {str(error)}")
            raise error
        else:
            return float(total_cost)

    def describir_servicio(self) -> str:
        return f"Servicio Hardware: {self.name} | ID: {self.service_id} | Categoría: {self.__equipment_type} | Tarifa/Día: ${self.base_cost:.2f}"


class AsesoriaEspecializada(Servicio):
    """
    Servicio de consultoría y arquitectura senior de soluciones empresariales software.
    """

    def __init__(self, service_id: str, name: str, base_cost: float, consultant_level: str):
        super().__init__(service_id, name, base_cost)
        if not consultant_level or str(consultant_level).strip().upper() not in ["JUNIOR", "SENIOR", "PRINCIPAL"]:
            raise InvalidServiceParameterError("Nivel de consultor inválido. Debe ser JUNIOR, SENIOR o PRINCIPAL.")
        self.__consultant_level: str = str(consultant_level).strip().upper()

    def validar_parametros(self, params: Dict[str, Any]) -> bool:
        try:
            if not self.is_available:
                raise ServiceUnavailableError(f"La consultoría '{self.name}' no posee agenda libre.")
            
            hours = params.get("hours")
            if hours is None or not isinstance(hours, (int, float)) or hours <= 0:
                raise InvalidServiceParameterError("El parámetro 'hours' de consultoría es mandatorio y debe ser numérico positivo.")
                
        except (ServiceUnavailableError, InvalidServiceParameterError) as error:
            log_error(f"[Asesoria ID: {self.service_id}] Error de Validación: {str(error)}")
            raise error
        else:
            return True
        finally:
            print(f"[AUDIT] Proceso de validación completado para la Asesoría ID: {self.service_id}")

    def calcular_costo(self, tax_rate: Optional[float] = None, discount: Optional[float] = None, **kwargs: Any) -> float:
        try:
            hours = kwargs.get("hours", 1)
            self.validar_parametros({"hours": hours})
            
            # Tarificación base por hora consultada
            total_cost = self.base_cost * hours
            
            # Variación polimórfica: Un consultor de nivel 'PRINCIPAL' aplica un multiplicador técnico por expertise del 30%
            if self.__consultant_level == "PRINCIPAL":
                total_cost *= 1.30
            # Un consultor de nivel 'SENIOR' aplica un recargo del 15%
            elif self.__consultant_level == "SENIOR":
                total_cost *= 1.15
                
            if tax_rate is not None:
                if tax_rate < 0:
                    raise CostCalculationError("Impuesto parametrizado inválido.")
                total_cost += total_cost * tax_rate
                
            if discount is not None:
                if discount < 0 or discount > total_cost:
                    raise CostCalculationError("El descuento excede el costo de la consultoría.")
                total_cost -= discount

        except (CostCalculationError, ServiceUnavailableError, InvalidServiceParameterError) as error:
            log_error(f"[Asesoria ID: {self.service_id}] Fallo en cálculo financiero: {str(error)}")
            raise error
        else:
            return float(total_cost)

    def describir_servicio(self) -> str:
        return f"Servicio Consultoría: {self.name} | ID: {self.service_id} | Rango: {self.__consultant_level} | Tarifa/Hora: ${self.base_cost:.2f}"