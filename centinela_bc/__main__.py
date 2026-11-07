"""Uso: python -m centinela_bc [caso] | python -m centinela_bc --hechos P1 P2 ¬P8 ..."""

import argparse
import sys

from .base import ACCIONES, PROPOSICIONES, REGLAS
from .casos import CASOS
from .motor import encadenar


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m centinela_bc",
        description="Diagnóstico de incidentes de Centinela con encadenamiento hacia adelante.",
    )
    parser.add_argument("caso", nargs="?", default="entrada", choices=sorted(CASOS),
                        help="escenario a simular (por defecto: entrada)")
    parser.add_argument("--hechos", nargs="+", metavar="LITERAL",
                        help="hechos manuales, por ejemplo: P9 P10 ¬P8")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    hechos = set(args.hechos) if args.hechos else set(CASOS[args.caso])
    try:
        resultado = encadenar(hechos)
    except ValueError as error:
        parser.error(str(error))

    reglas = {r.id: r for r in REGLAS}
    print("Hechos: {" + ", ".join(sorted(hechos, key=lambda h: int(h.lstrip("¬P")))) + "}")
    for paso in resultado.traza:
        print(f"Ciclo {paso.ciclo}: {paso.regla} ({reglas[paso.regla].formula()}) "
              f"⊢ {paso.conclusion}: {PROPOSICIONES[paso.conclusion]}")
    print(f"Punto fijo en el ciclo {resultado.ciclos}.")
    if resultado.acciones:
        for accion in resultado.acciones:
            print(f"Decisión: {accion}, {ACCIONES[accion]}")
    else:
        print("Decisión: ninguna regla concluye una acción.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
