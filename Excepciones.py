# =================================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# PROGRAMA: Ingeniería de Sistemas
# CURSO: Programación Orientada a Objetos - Código: 213023
# PROYECTO: Sistema Integral de Gestión de Operaciones 'Software FJ'
# ARCHIVO: Excepciones.py
# DESCRIPCIÓN: Jerarquía de excepciones personalizadas para manejo robusto de errores.
# =================================================================================

# Importación de la clase genérica 'Any' y 'Optional' del módulo typing para definir tipos de datos dinámicos opcionales.
from typing import Any, Optional

# Definición de la clase base de excepciones del sistema, la cual hereda de la clase estándar Exception de Python.
class ErrorSoftwareFJ(Exception):
    # Docstring que describe el propósito de la clase base dentro del dominio de la aplicación.
    """Clase base general para todas las excepciones personalizadas del sistema Software FJ."""

    # Constructor de la clase que recibe un mensaje de error y, opcionalmente, el valor que originó la falla.
    def __init__(self, mensaje: str, valor_causante: Optional[Any] = None) -> None:
        # Se invoca el constructor de la superclase (Exception) pasándole el mensaje para el registro base del error.
        super().__init__(mensaje)
        # Se asigna el mensaje personalizado a un atributo público de la instancia para fácil acceso.
        self.mensaje = mensaje
        # Se almacena el valor específico que causó la excepción, útil para trazabilidad en archivos de log (debugging).
        self.valor_causante = valor_causante

    # Sobrescritura del método mágico __str__ para definir cómo se representa la excepción en formato de cadena (string).
    def __str__(self) -> str:
        # Condicional que verifica si el desarrollador proporcionó un valor causante al momento de lanzar la excepción.
        if self.valor_causante is not None:
            # Si existe un valor causante, retorna el mensaje concatenado con el valor problemático formateado.
            return f"{self.mensaje} (Valor causante: {self.valor_causante})"
        # Si no hay valor causante, retorna únicamente el mensaje de error estandarizado.
        return self.mensaje


# Clase derivada para manejar errores de validación de datos (nombres, IDs alfanuméricos, etc.).
class ErrorDatoInvalido(ErrorSoftwareFJ):
    # Docstring explicativo para la clase de datos inválidos.
    """Excepción lanzada cuando un dato de entrada no cumple con las reglas de negocio o formato."""
    
    # Constructor que predefine un mensaje por defecto, pero permite sobrescritura y recibe el valor erróneo.
    def __init__(self, mensaje: str = "El dato ingresado no es válido.", valor_causante: Optional[Any] = None) -> None:
        # Llama al constructor de la clase padre ErrorSoftwareFJ enviando los parámetros procesados.
        super().__init__(mensaje, valor_causante)


# Clase derivada para controlar la ausencia de argumentos obligatorios en la inicialización de objetos o métodos.
class ErrorParametroFaltante(ErrorSoftwareFJ):
    # Docstring explicativo para la clase de parámetros faltantes.
    """Excepción lanzada cuando falta un parámetro obligatorio en la creación de clientes o servicios."""
    
    # Constructor que requiere el mensaje específico del parámetro que falta, e incluye el contexto opcional.
    def __init__(self, mensaje: str = "Falta un parámetro obligatorio para la operación.", valor_causante: Optional[Any] = None) -> None:
        # Invoca al constructor de la jerarquía superior para acoplar el mensaje y el contexto.
        super().__init__(mensaje, valor_causante)


# Clase derivada para gestionar problemas de inventario, concurrencia o estado inactivo de los servicios.
class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    # Docstring explicativo para indisponibilidad de catálogo o servicios.
    """Excepción lanzada cuando un servicio solicitado se encuentra inactivo, ocupado o fuera de stock."""
    
    # Constructor adaptado para recibir el ID o nombre del servicio problemático.
    def __init__(self, mensaje: str = "El servicio solicitado no está disponible actualmente.", valor_causante: Optional[Any] = None) -> None:
        # Transmite la información al eslabón superior de la cadena de herencia.
        super().__init__(mensaje, valor_causante)


# Clase derivada para atrapar flujos anómalos en el ciclo de vida de la clase Reserva.
class ErrorReservaInvalida(ErrorSoftwareFJ):
    # Docstring explicativo para el control transaccional de las reservas.
    """Excepción lanzada ante intentos de confirmar reservas canceladas o con conflictos lógicos."""
    
    # Constructor de la excepción transaccional.
    def __init__(self, mensaje: str = "Operación de reserva inválida o lógicamente inconsistente.", valor_causante: Optional[Any] = None) -> None:
        # Instancia la clase base inyectando la trazabilidad del error de reserva.
        super().__init__(mensaje, valor_causante)


# Clase derivada específica para el módulo de polimorfismo financiero y tasación de tarifas.
class ErrorCalculoInconsistente(ErrorSoftwareFJ):
    # Docstring explicativo para errores matemáticos o financieros del dominio.
    """Excepción lanzada cuando el cálculo de costos arroja valores ilógicos (ej. tarifas negativas)."""
    
    # Constructor que procesa el error aritmético o financiero de los servicios corporativos.
    def __init__(self, mensaje: str = "El cálculo del costo final arrojó un valor inconsistente.", valor_causante: Optional[Any] = None) -> None:
        # Cierra la implementación llamando al constructor base y preparando el objeto para ser atrapado (catched).
        super().__init__(mensaje, valor_causante)

# =================================================================================
# BLOQUE DE PRUEBA DE ESTABILIDAD Y ENCADENAMIENTO (TESTING UNITARIO LOCAL)
# =================================================================================

# Condición estándar de Python para asegurar que las pruebas solo corran si el archivo se ejecuta directamente.
if __name__ == "__main__":
    # Importación del módulo traceback para demostrar el encadenamiento de excepciones exigido por el nivel alto.
    import traceback
    
    # Se notifica el inicio del test transaccional por consola.
    print("--- INICIANDO TEST DE EXCEPCIONES Y ENCADENAMIENTO ---")
    
    # Bloque try/except para simular una caída del sistema basada en reglas de validación estricta.
    try:
        # Simulación de un dato de entrada corrupto proporcionado por un sistema externo o usuario.
        edad_ingresada = -5
        
        # Validación defensiva de negocio: si la edad es negativa, disparamos una excepción nativa de tipo ValueError.
        if edad_ingresada < 0:
            # Bloque try interno para forzar y atrapar el error primario originado en Python base.
            try:
                # Lanzamos intencionalmente el ValueError básico simulando un fallo lógico en un cálculo subyacente.
                raise ValueError("La edad matemática no puede ser un número entero negativo.")
            
            # Capturamos el ValueError base en la variable 'e' para utilizarlo como causa original.
            except ValueError as e:
                # ENCADENAMIENTO EXPLICITO: Lanzamos nuestra excepción de dominio personalizada 'from e'.
                # Esto vincula el error original de Python con el error de negocio de 'Software FJ'.
                raise ErrorDatoInvalido("Fallo en la creación del Cliente por datos corruptos.", valor_causante=edad_ingresada) from e

    # Bloque except generalizado que atrapa nuestra excepción personalizada de alto nivel.
    except ErrorSoftwareFJ as error_capturado:
        # Se imprime la estructura del error capturado demostrando la herencia y el método __str__ sobrescrito.
        print(f"Excepción de Dominio Capturada: {error_capturado}")
        # Se imprime visualmente la traza completa de la pila (StackTrace) demostrando que no se perdió el origen del error (ValueError).
        print("\nTraza completa demostrando encadenamiento (Raise from):")
        # Invocamos la impresión del traceback para validar frente a auditoría técnica.
        traceback.print_exc()