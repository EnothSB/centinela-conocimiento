"""Centinela, Fase 3: base de conocimiento y motor de reglas.

Centinela es el agente de las fases 1 y 2 que atiende los incidentes de una
plataforma web institucional (nginx, aplicación y base de datos sobre Oracle
Linux 9, monitoreados con Prometheus, Loki y Alertmanager). En esta fase
diagnostica la causa de un incidente con una base de conocimiento en lógica
proposicional y un motor de encadenamiento hacia adelante que aplica Modus
Ponens (Russell y Norvig, 2021).

Módulos:

- ``base``: diccionario de proposiciones y reglas de inferencia (R1 a R7).
- ``motor``: encadenamiento hacia adelante con traza paso a paso.
- ``casos``: hechos de entrada de los escenarios de prueba.
"""

__author__ = "Enoth Salcedo Blandon"
