import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest

from tools.func_center import (
    Producto,
    NombreVacioError,
    CantidadInvalidaError,
    PrecioInvalidoError
)


#Este archivo es enteramente de testeo, es una forma de asegurar que todo funciona antes de ejecutarlo y algo cause un error critico o leve.

#testeo de la clase Producto
class TestProducto(unittest.TestCase):

    def test_calculos_correctos(self):

        """Comprobacion del IVA para que sea correcto y todos los cálculos"""

        p = Producto("Camisa", 2, 24.20)


        self.assertEqual(p.base, 20.00)
        self.assertEqual(p.iva, 4.20)
        self.assertEqual(p.total_base, 40.00)
        self.assertEqual(p.total_iva, 8.40)
        self.assertEqual(p.total_pvp, 48.40)    

        pass

    def test_nombre_vacío(self):
        with self.assertRaises(NombreVacioError):
            Producto("",2,24.20)
            pass

    def test_nombre_solo_espacios(self):
        with self.assertRaises(NombreVacioError):
            Producto(" ",2,24.20)
            pass

    def test_cantidad_cero(self):
        with self.assertRaises(CantidadInvalidaError):
            Producto("Manta",0, 24.20)

    def test_cantidad_negativa(self):
        with self.assertRaises(CantidadInvalidaError):
            Producto("Manta",-3, 24.20)
            pass

    def test_precio_cero(self):
        with self.assertRaises(PrecioInvalidoError):
            Producto("Manta",1,00.00)
            pass

    def test_precio_negativo(self):
        with self.assertRaises(PrecioInvalidoError):
            Producto("Manta",1, -12.50)
            pass
if __name__ == "__main__":

    unittest.main()

