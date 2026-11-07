"""Motor de encadenamiento hacia adelante con Modus Ponens."""

from dataclasses import dataclass, field

from .base import ACCIONES, NEGACION, OBSERVABLES, REGLAS, atomo


@dataclass(frozen=True)
class Paso:
    """Una aplicación de Modus Ponens dentro de la traza."""

    ciclo: int
    regla: str
    premisas: tuple
    conclusion: str


@dataclass
class Resultado:
    bc: set
    traza: list = field(default_factory=list)
    ciclos: int = 0

    @property
    def acciones(self):
        return sorted(h for h in self.bc if h in ACCIONES)


def validar(hechos):
    """Los hechos de entrada solo pueden ser literales observables y consistentes."""
    for literal in hechos:
        if atomo(literal) not in OBSERVABLES:
            raise ValueError(f"'{literal}' no es un hecho observable (P1 a P10)")
        if literal.startswith(NEGACION) and atomo(literal) in hechos:
            raise ValueError(f"Hechos contradictorios: {atomo(literal)} y {literal}")


def encadenar(hechos, reglas=REGLAS):
    """Aplica encadenamiento hacia adelante hasta llegar a un punto fijo.

    En cada ciclo se revisan las reglas con los hechos que había al empezar el
    ciclo. Si todas las premisas de una regla están en la BC, se unen en una
    conjunción y se aplica Modus Ponens: de α → β y α se concluye β. Un hecho
    desconocido no equivale a su negación (no hay supuesto de mundo cerrado).
    """
    hechos = set(hechos)
    validar(hechos)
    resultado = Resultado(bc=set(hechos))
    ciclo = 0
    while True:
        ciclo += 1
        inicio = frozenset(resultado.bc)
        nuevos = [
            r for r in reglas
            if r.conclusion not in inicio and all(p in inicio for p in r.premisas)
        ]
        if not nuevos:
            resultado.ciclos = ciclo
            return resultado
        for regla in nuevos:
            resultado.bc.add(regla.conclusion)
            resultado.traza.append(Paso(ciclo, regla.id, regla.premisas, regla.conclusion))
