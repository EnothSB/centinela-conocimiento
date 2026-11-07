# Centinela · Fase 3: base de conocimiento y motor de reglas

Proyecto de la asignatura Inteligencia Artificial. Implementa la base de
conocimiento de **Centinela**, el agente de las fases 1 y 2, y un motor de
encadenamiento hacia adelante que diagnostica incidentes de la plataforma web
aplicando Modus Ponens. Solo usa la biblioteca estándar de Python.

| | |
|---|---|
| **Autor** | Enoth Salcedo Blandon (código 200632) |
| **Universidad** | Universidad Militar Nueva Granada, Facultad de Estudios a Distancia, Programa de Ingeniería |
| **Asignatura** | Inteligencia Artificial, Fase 3 del Proyecto Integrador |
| **Docente** | John Edwin Vera Vera |
| **Fecha** | Noviembre de 2026 |
| **Fase 2** | https://github.com/EnothSB/centinela-busqueda |

## Micro-dominio

Diagnóstico de fallas de una plataforma web de tres capas: nginx, aplicación
y base de datos (BD) sobre Oracle Linux 9, monitoreados con Prometheus, Loki
y Alertmanager. Ante una alerta de errores 502, Centinela identifica la
causa, elige el runbook que la corrige o escala a una persona.

## Base de conocimiento

**Proposiciones** (`centinela_bc/base.py`):

| Símbolo | Es verdadera cuando… |
|---|---|
| P1 | Más del 5 % de las respuestas de nginx son error 502 durante 5 minutos |
| P2 | La aplicación no responde a su verificación de salud |
| P3 | La memoria de la aplicación supera el 90 % y sigue creciendo |
| P4 | Los logs de la aplicación registran errores OutOfMemory |
| P5 | La aplicación registra timeouts al conectarse a la BD |
| P6 | Una consulta lleva más de 5 minutos bloqueando a otras en la BD |
| P7 | La BD está activa |
| P8 | La aplicación se reinició hace menos de 30 minutos |
| P9 | El disco del servidor web está al 95 % o más |
| P10 | nginx no responde |
| D1 a D3 | Diagnósticos: falla del backend, fuga de memoria, bloqueo en la BD |
| A1 a A4 | Acciones: reiniciar_app, terminar_bloqueo, liberar disco web, escalar a una persona |

**Reglas** (cláusulas de Horn):

| Regla | Implicación |
|---|---|
| R1 | P1 ∧ P2 → D1 |
| R2 | D1 ∧ P3 ∧ P4 → D2 |
| R3 | D1 ∧ P5 ∧ P6 → D3 |
| R4 | D2 ∧ P7 ∧ ¬P8 → A1 |
| R5 | D2 ∧ P8 → A4 |
| R6 | D3 ∧ P7 → A2 |
| R7 | P9 ∧ P10 → A3 |

## Uso

```bash
python -m centinela_bc               # caso de entrada del documento
python -m centinela_bc reintento     # el 502 sigue después de reiniciar
python -m centinela_bc --hechos P9 P10
```

Casos disponibles: `entrada`, `reintento`, `resuelto`, `bloqueo` y `disco`.

Salida del caso de entrada (igual a la Tabla 3 del documento):

```
Hechos: {P1, P2, P3, P4, ¬P5, ¬P6, P7, ¬P8, ¬P9, ¬P10}
Ciclo 1: R1 (P1 ∧ P2 → D1) ⊢ D1: Falla del backend: el 502 lo causa la aplicación y no nginx
Ciclo 2: R2 (D1 ∧ P3 ∧ P4 → D2) ⊢ D2: Fuga de memoria en la aplicación
Ciclo 3: R4 (D2 ∧ P7 ∧ ¬P8 → A1) ⊢ A1: Ejecutar reiniciar_app
Punto fijo en el ciclo 4.
Decisión: A1, Ejecutar reiniciar_app
```

## Pruebas

```bash
python -m unittest discover -s tests
```

Las 19 pruebas cubren la traza del documento, los otros cuatro escenarios, que
Modus Ponens no dispare con premisas incompletas, que un hecho desconocido no
equivalga a su negación (no hay supuesto de mundo cerrado) y la validación de
los hechos de entrada.

## Referencia

Russell, S. y Norvig, P. (2021). *Artificial intelligence: A modern approach*
(4.ª ed.). Pearson.
