"""Hechos de entrada de los escenarios."""

CASOS = {
    # Caso del documento: martes 7:42 p. m., alerta de 502 por fuga de memoria.
    "entrada": frozenset({"P1", "P2", "P3", "P4", "¬P5", "¬P6", "P7", "¬P8", "¬P9", "¬P10"}),
    # El 502 sigue 10 minutos después de reiniciar la aplicación.
    "reintento": frozenset({"P1", "P2", "P3", "P4", "¬P5", "¬P6", "P7", "P8", "¬P9", "¬P10"}),
    # El reinicio funcionó: ya no hay síntomas.
    "resuelto": frozenset({"¬P1", "¬P2", "¬P3", "¬P4", "¬P5", "¬P6", "P7", "P8", "¬P9", "¬P10"}),
    # 502 causado por una consulta bloqueante en la BD.
    "bloqueo": frozenset({"P1", "P2", "¬P3", "¬P4", "P5", "P6", "P7", "¬P8", "¬P9", "¬P10"}),
    # nginx caído porque el disco del servidor web está lleno.
    "disco": frozenset({"¬P1", "¬P2", "¬P3", "¬P4", "¬P5", "¬P6", "P7", "¬P8", "P9", "P10"}),
}
