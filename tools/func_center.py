from pathlib import Path
import openpyxl
from datetime import datetime

from tools.logs.logs_func import configurar_logger

logger = configurar_logger()

#Errores especificos, manejo de errores personalizados

#El mas básico
class ProductoError(Exception):
    """Excepcion base para errores relacionados conproductos"""
    pass
#Errores especificos que usan ProductoError para dar error dentro de la claseProducto
class NombreVacioError(ProductoError):
    """Se lanza cuando el nombre esta vacio"""
    pass

class CantidadInvalidaError(ProductoError):
    """Se lanza cuando la cantidad no es compatible con los requisitos minimos"""
    pass

class PrecioInvalidoError(ProductoError):
    """Se lanza cuando el precio es = o <0"""
    pass

# --- 1. DEFINICIÓN DE LA CLASE (EL MOLDE) ---
class Producto:
    """Clase que representa un producto con sus cálculos de IVA."""
    
    def __init__(self, nombre, cantidad, pvp):


        if not nombre or not nombre.strip():
            raise NombreVacioError("El nombre no puede estar vacío.")
        if cantidad <= 0:
            raise CantidadInvalidaError("La cantidad debe ser mayor que 0.")
        if pvp <= 0:
            raise PrecioInvalidoError("El precio debe ser mayor que 0.")

        
        self.nombre = nombre
        self.cantidad = cantidad
        self.pvp = pvp
        self.base = round(pvp / 1.21, 2)  # Precio sin IVA
        self.iva = round(pvp - self.base, 2)  # Cuota de IVA
        self.total_base = round(self.base * cantidad, 2)  # Base total
        self.total_iva = round(self.iva * cantidad, 2)  # IVA total
        self.total_pvp = round(pvp * cantidad, 2)  # PVP total

# --- 2. LÓGICA DEL PROGRAMA (FUNCIONES) ---

def añadir_producto_interactivo(lista_productos):
    nombre = None
    cantidad = None
    pvp = None
    paso = 0

    while True:
        if paso == 0:
            entrada = input("\n📝 Nombre del producto (o '?' para atrás): ").strip()
            if entrada == '?':
                if nombre is not None:
                    print("↩️  Volviendo...")
                    paso = -1
                    break
                else:
                    print("ℹ️  No hay paso anterior.")
                    continue
            if not entrada:
                print("❌ El nombre no puede estar vacío.")
                continue
            nombre = entrada
            paso = 1

        elif paso == 1:
            entrada = input(f"\n📝 Cantidad de '{nombre}' (o '?' para atrás): ").strip()
            if entrada == '?':
                paso = 0
                print("↩️  Volviendo a nombre...")
                continue
            try:
                cantidad = float(entrada)
                if cantidad is None or cantidad <= 0:
                    print("❌ La cantidad debe ser mayor que 0.")
                    continue
                paso = 2
            except ValueError:
                print("❌ Introduce un número válido.")
                logger.warning(f"Entrada no númerica detectada en cantidad: {entrada}")

        elif paso == 2:
            entrada = input(f"\n📝 Precio PVP de '{nombre}' (o '?' para atrás): ").strip()
            if entrada == '?':
                paso = 1
                print("↩️  Volviendo a cantidad...")
                continue
            try:
                pvp = float(entrada)
                if pvp is None or pvp <= 0:
                    print("❌ El precio debe ser mayor que 0.")
                    continue
                paso = 3
            except ValueError:
                print("❌ Introduce un número válido.")
                logger.warning(f"Entrada no númerica en precio: {entrada}")

        elif paso == 3:
            print("\n" + "="*40)
            print("📋 RESUMEN DEL PRODUCTO")
            print("="*40)
            print(f"  Nombre:   {nombre}")
            print(f"  Cantidad: {cantidad}")
            print(f"  PVP:      {pvp} €")
            print("="*40)

            confirmar = input("\n¿Guardar este producto? (s/n): ").strip().lower()
            if confirmar == 's':
                try:
                    producto = Producto(nombre, cantidad, pvp)
                    lista_productos.append(producto)
                    print(f"✅ Producto '{nombre}' añadido correctamente.")
                    logger.info(f"Producto añadido: {nombre} x {cantidad} -> {pvp}€")
                    break

                except NombreVacioError as e:
                    print(f"Error de nombre: {e}")
                    logger.error(f"Error de nombre: {e}")
                    nombre = None
                    paso = 0

                except CantidadInvalidaError as e:
                    print(f"Ingresa la cantidad de productos: {e}")
                    logger.error(f"Error de cantidad: {e}")
                    cantidad = None
                    paso = 1

                except PrecioInvalidoError as e:
                    print(f"Introduce un precio válido: {e}")
                    logger.error(f"Error de precio: {e}")
                    pvp = None
                    paso = 2
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")
                    logger.critical(f"Error inesperado al añadir producto: {e}")
                    break
            elif confirmar == 'n':
                print("🗑️  Producto descartado.")
                break
            else:
                print("❌ Responde 's' para sí o 'n' para no.")

def ver_productos(lista_productos):
    if not lista_productos:
        print("No hay productos añadidos.")
        return
    
    print("\n PRODUCTOS AÑADIDOS:")
    print("-" * 60)
    for i, p in enumerate(lista_productos, 1):
        print(f"{i}. {p.nombre} x{p.cantidad} → {p.pvp}€ (Base: {p.base}€, IVA: {p.iva}€)")
    print("-" * 60)
    print(f"Total Base: {sum(p.total_base for p in lista_productos)}€")
    print(f"Total IVA: {sum(p.total_iva for p in lista_productos)}€")
    print(f"Total PVP: {sum(p.total_pvp for p in lista_productos)}€")

def guardar_excel(lista_productos):
    if not lista_productos:
        print("❌ No hay productos para guardar.")
        logger.warning("Intento de guardar Excel con lista vacía")
        return
    
    # Esta parte decide donde se guardan todos los archivos del programa creados con este.
    carpeta_raiz = Path(__file__).parent.parent  #Para subir dos niveles desde tools y dar con la carpeta raiz
    carpeta_destino = carpeta_raiz / "data"
    carpeta_destino.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe
    
    # --- Creamos el archivo Excel ---
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ventas"
    
    cabeceras = ["Producto", "Cantidad", "Base Imponible", "IVA (21%)", "PVP", "Total Base", "Total IVA", "Total PVP"]
    ws.append(cabeceras)
    
    total_base = 0
    total_iva = 0
    total_pvp = 0
    
    for item in lista_productos:
        ws.append([item.nombre, item.cantidad, item.base, item.iva, item.pvp, item.total_base, item.total_iva, item.total_pvp])
        total_base += item.total_base
        total_iva += item.total_iva
        total_pvp += item.total_pvp
    
    ws.append([])
    ws.append(["TOTALES", "", "", "", "", total_base, total_iva, total_pvp])
    
    # --- Guardado con nombre único ---
    nombre_archivo = f"ventas_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    ruta_completa = carpeta_destino / nombre_archivo
    
    try:
        wb.save(ruta_completa)
        print(f"✅ Archivo guardado correctamente.")
        print(f"📂 Ruta: {ruta_completa}")
        logger.info(f"excel guardado: {ruta_completa}")
    except Exception as e:
        print(f"❌ Error al guardar: {e}")
        logger.error(f"Error al guardar el Excel: {e}")


# --- 3. MENÚ PRINCIPAL ---

def menu():

    logger.info(f"Programa iniciado")


    lista_productos = []

    while True:
        print("\nGESTIÓN DE VENTAS")
        print("1. Añadir producto")
        print("2. Ver productos añadidos")
        print("3. Guardar y generar Excel")
        print("4. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            añadir_producto_interactivo(lista_productos)
        elif opcion == "2":
            ver_productos(lista_productos)
        elif opcion == "3":
            guardar_excel(lista_productos)
        elif opcion == "4":
            print("👋 ¡Hasta luego!")
            break
        else:
            print(" Opción no válida.")



if __name__ == "__main__":
    menu()