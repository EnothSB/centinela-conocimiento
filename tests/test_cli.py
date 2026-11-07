"""Pruebas de la línea de comandos."""

import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def ejecutar(*args):
    return subprocess.run(
        [sys.executable, "-m", "centinela_bc", *args],
        cwd=RAIZ, capture_output=True, text=True, encoding="utf-8",
    )


class LineaDeComandos(unittest.TestCase):
    def test_caso_por_defecto_imprime_la_traza_y_la_decision(self):
        r = ejecutar()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("R1", r.stdout)
        self.assertIn("R4", r.stdout)
        self.assertIn("Punto fijo en el ciclo 4", r.stdout)
        self.assertIn("A1", r.stdout)

    def test_hechos_manuales(self):
        r = ejecutar("--hechos", "P9", "P10")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("A3", r.stdout)

    def test_caso_inexistente_falla(self):
        r = ejecutar("no-existe")
        self.assertNotEqual(r.returncode, 0)

    def test_hecho_invalido_falla_con_mensaje(self):
        r = ejecutar("--hechos", "P99")
        self.assertEqual(r.returncode, 2)
        self.assertIn("P99", r.stderr)


if __name__ == "__main__":
    unittest.main()
