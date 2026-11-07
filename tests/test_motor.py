"""Pruebas del motor de encadenamiento hacia adelante de Centinela."""

import unittest

from centinela_bc.base import REGLAS
from centinela_bc.casos import CASOS
from centinela_bc.motor import encadenar


def resumen(resultado):
    """Devuelve la traza como tuplas (ciclo, regla, conclusión)."""
    return [(paso.ciclo, paso.regla, paso.conclusion) for paso in resultado.traza]


class CasoDeEntrada(unittest.TestCase):
    """El caso del documento debe reproducir la Tabla 3 paso a paso."""

    def setUp(self):
        self.resultado = encadenar(CASOS["entrada"])

    def test_traza_igual_a_la_tabla_3(self):
        self.assertEqual(
            resumen(self.resultado),
            [(1, "R1", "D1"), (2, "R2", "D2"), (3, "R4", "A1")],
        )

    def test_punto_fijo_en_el_ciclo_4(self):
        self.assertEqual(self.resultado.ciclos, 4)

    def test_la_decision_es_reiniciar_la_aplicacion(self):
        self.assertEqual(self.resultado.acciones, ["A1"])

    def test_no_infiere_bloqueo_ni_disco(self):
        for hecho in ("D3", "A2", "A3", "A4"):
            self.assertNotIn(hecho, self.resultado.bc)


class OtrosEscenarios(unittest.TestCase):
    def test_si_el_502_sigue_tras_reiniciar_escala(self):
        resultado = encadenar(CASOS["reintento"])
        self.assertEqual(
            resumen(resultado),
            [(1, "R1", "D1"), (2, "R2", "D2"), (3, "R5", "A4")],
        )
        self.assertEqual(resultado.acciones, ["A4"])

    def test_si_el_reinicio_funciono_no_hay_accion(self):
        resultado = encadenar(CASOS["resuelto"])
        self.assertEqual(resultado.traza, [])
        self.assertEqual(resultado.acciones, [])
        self.assertEqual(resultado.ciclos, 1)

    def test_bloqueo_en_la_bd(self):
        resultado = encadenar(CASOS["bloqueo"])
        self.assertEqual(
            resumen(resultado),
            [(1, "R1", "D1"), (2, "R3", "D3"), (3, "R6", "A2")],
        )

    def test_disco_web_lleno(self):
        resultado = encadenar(CASOS["disco"])
        self.assertEqual(resumen(resultado), [(1, "R7", "A3")])


class ModusPonens(unittest.TestCase):
    def test_no_dispara_con_premisas_incompletas(self):
        resultado = encadenar({"P1"})
        self.assertEqual(resultado.traza, [])

    def test_un_hecho_desconocido_no_equivale_a_su_negacion(self):
        # Sin ¬P8 explícito, R4 no dispara: no hay supuesto de mundo cerrado.
        hechos = set(CASOS["entrada"]) - {"¬P8"}
        resultado = encadenar(hechos)
        self.assertNotIn("A1", resultado.bc)
        self.assertEqual(resultado.acciones, [])

    def test_cada_conclusion_tiene_todas_sus_premisas_en_la_bc(self):
        resultado = encadenar(CASOS["entrada"])
        for paso in resultado.traza:
            for premisa in paso.premisas:
                self.assertIn(premisa, resultado.bc)

    def test_rechaza_hechos_contradictorios(self):
        with self.assertRaises(ValueError):
            encadenar({"P8", "¬P8"})

    def test_rechaza_simbolos_que_no_son_observables(self):
        for hecho in ("P11", "D1", "A1", "¬D2"):
            with self.subTest(hecho=hecho), self.assertRaises(ValueError):
                encadenar({hecho})


class BaseDeConocimiento(unittest.TestCase):
    def test_hay_al_menos_5_proposiciones_y_3_reglas(self):
        from centinela_bc.base import PROPOSICIONES

        self.assertGreaterEqual(len(PROPOSICIONES), 5)
        self.assertGreaterEqual(len(REGLAS), 3)

    def test_todas_las_reglas_son_clausulas_de_horn(self):
        for regla in REGLAS:
            with self.subTest(regla=regla.id):
                self.assertFalse(regla.conclusion.startswith("¬"))
                self.assertGreaterEqual(len(regla.premisas), 1)


if __name__ == "__main__":
    unittest.main()
