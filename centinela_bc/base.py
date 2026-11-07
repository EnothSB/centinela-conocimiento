"""Base de conocimiento de Centinela: proposiciones atómicas y reglas."""

from dataclasses import dataclass

NEGACION = "¬"

# Hechos observables: Centinela los lee de sus sensores en cada alerta.
OBSERVABLES = {
    "P1": "Más del 5 % de las respuestas de nginx son error 502 durante 5 minutos",
    "P2": "La aplicación no responde a su verificación de salud (health check)",
    "P3": "La memoria de la aplicación supera el 90 % y sigue creciendo",
    "P4": "Los logs de la aplicación registran errores de falta de memoria (OutOfMemory)",
    "P5": "La aplicación registra tiempos de espera agotados al conectarse a la BD",
    "P6": "Una consulta lleva más de 5 minutos bloqueando a otras en la BD",
    "P7": "La BD está activa",
    "P8": "La aplicación se reinició hace menos de 30 minutos",
    "P9": "El disco del servidor web está al 95 % o más",
    "P10": "nginx no responde",
}

# Diagnósticos: solo se obtienen por inferencia.
DIAGNOSTICOS = {
    "D1": "Falla del backend: el 502 lo causa la aplicación y no nginx",
    "D2": "Fuga de memoria en la aplicación",
    "D3": "Bloqueo en la BD",
}

# Acciones: los runbooks de la Fase 2.
ACCIONES = {
    "A1": "Ejecutar reiniciar_app",
    "A2": "Ejecutar terminar_bloqueo",
    "A3": "Liberar el disco web (rotar logs y limpiar temporales)",
    "A4": "Escalar a una persona",
}

PROPOSICIONES = {**OBSERVABLES, **DIAGNOSTICOS, **ACCIONES}


@dataclass(frozen=True)
class Regla:
    """Cláusula de Horn: conjunción de literales → un átomo."""

    id: str
    premisas: tuple
    conclusion: str
    lectura: str

    def formula(self):
        return f"{' ∧ '.join(self.premisas)} → {self.conclusion}"


REGLAS = (
    Regla("R1", ("P1", "P2"), "D1",
          "Si hay 502 y la aplicación no responde, la falla está en el backend"),
    Regla("R2", ("D1", "P3", "P4"), "D2",
          "Si falla el backend con memoria alta y errores OutOfMemory, hay fuga de memoria"),
    Regla("R3", ("D1", "P5", "P6"), "D3",
          "Si falla el backend con timeouts hacia la BD y una consulta bloqueante, hay bloqueo"),
    Regla("R4", ("D2", "P7", "¬P8"), "A1",
          "Si hay fuga, la BD está activa y no hubo reinicio reciente, reiniciar la aplicación"),
    Regla("R5", ("D2", "P8"), "A4",
          "Si hay fuga y ya se reinició hace poco, escalar a una persona"),
    Regla("R6", ("D3", "P7"), "A2",
          "Si hay bloqueo y la BD está activa, terminar la consulta bloqueante"),
    Regla("R7", ("P9", "P10"), "A3",
          "Si el disco web está lleno y nginx no responde, liberar disco"),
)


def atomo(literal):
    """Quita la negación de un literal: '¬P8' → 'P8'."""
    return literal[1:] if literal.startswith(NEGACION) else literal
