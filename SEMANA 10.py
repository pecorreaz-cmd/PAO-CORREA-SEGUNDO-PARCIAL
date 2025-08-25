#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventario con archivos + manejo de excepciones (compatible Python 3.7+)
-------------------------------------------------------------------------
- Guarda/carga inventario desde "inventario.txt" (o ruta dada).
- Crea el archivo si no existe.
- Omite líneas corruptas informando en consola.
- Maneja PermissionError, FileNotFoundError y OSError.
- CLI simple sin emojis (amigable con consolas antiguas de Windows).
- Escritura atómica (archivo temporal + os.replace).

Formato del archivo:  id|nombre|cantidad|precio
Ejemplo:              P001|Lapiz HB|100|0.25
"""






class Producto:
    def __init__(self, id_prod, nombre, cantidad, precio):
        self.id = id_prod
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    @staticmethod
    def from_line(linea):
        """Crea un Producto desde 'id|nombre|cantidad|precio'."""
        partes = linea.strip().split(SEPARADOR)
        if len(partes) != 4:
            raise ValueError("Se esperaban 4 campos separados por '|'")
        id_, nombre, cantidad_str, precio_str = partes
        try:
            cantidad = int(cantidad_str)
        except ValueError:
            raise ValueError("Cantidad no es un entero")
        try:
            precio = float(precio_str)
        except ValueError:
            raise ValueError("Precio no es un número")
        return Producto(id_, nombre, cantidad, precio)

    def to_line(self):
        return f"{self.id}{SEPARADOR}{self.nombre}{SEPARADOR}{self.cantidad}{SEPARADOR}{self.precio}"


class Inventario:
    def __init__(self, ruta_archivo="inventario.txt"):
        self.ruta_archivo = ruta_archivo
        self.productos = {}  # type: Dict[str, Producto]
        self.cargar_desde_archivo()

    # ------------------ Persistencia ------------------
    def cargar_desde_archivo(self):
        """Carga productos desde archivo. Crea uno vacío si no existe."""
        try:
            if not os.path.exists(self.ruta_archivo):
                open(self.ruta_archivo, "a", encoding="utf-8").close()
                print("Archivo '{}' no existía. Se creó vacío.".format(self.ruta_archivo))
                return

            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                for n, linea in enumerate(f, start=1):
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        p = Producto.from_line(linea)
                        self.productos[p.id] = p
                    except Exception as e:
                        print("Advertencia: línea {} inválida en '{}': {}. Se omitió.".format(n, self.ruta_archivo, e))
            print("Inventario cargado desde '{}' ({} productos).".format(self.ruta_archivo, len(self.productos)))
        except PermissionError:
            print("Permiso denegado al leer '{}'.".format(self.ruta_archivo))
            raise
        except FileNotFoundError:
            # Condición de carrera poco probable
            try:
                open(self.ruta_archivo, "a", encoding="utf-8").close()
                print("Archivo '{}' no existía. Se creó vacío.".format(self.ruta_archivo))
            except Exception as e:
                print("No se pudo crear el archivo '{}': {}".format(self.ruta_archivo, e))
                raise
        except OSError as e:
            print("Error de E/S leyendo '{}': {}".format(self.ruta_archivo, e))
            raise

    def _guardar_en_archivo(self):
        """Guarda todos los productos en el archivo usando reemplazo atómico."""
        tmp = self.ruta_archivo + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                for p in self.productos.values():
                    f.write(p.to_line() + "\n")
            os.replace(tmp, self.ruta_archivo)
            print("Cambios guardados en '{}'.".format(self.ruta_archivo))
        except PermissionError:
            print("Permiso denegado al escribir en '{}'.".format(self.ruta_archivo))
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass
            raise
        except OSError as e:
            print("Error de E/S al guardar '{}': {}".format(self.ruta_archivo, e))
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass
            raise

    # ------------------ Operaciones -------------------
    def agregar_producto(self, producto):
        if producto.id in self.productos:
            raise ValueError("Ya existe un producto con id '{}'.".format(producto.id))
        self.productos[producto.id] = producto
        self._guardar_en_archivo()
        print("Producto '{}' agregado y guardado.".format(producto.id))

    def actualizar_producto(self, id_prod, nombre=None, cantidad=None, precio=None):
        if id_prod not in self.productos:
            raise KeyError("No existe producto con id '{}'.".format(id_prod))
        p = self.productos[id_prod]
        if nombre is not None and nombre != "":
            p.nombre = nombre
        if cantidad is not None:
            p.cantidad = int(cantidad)
        if precio is not None:
            p.precio = float(precio)
        self._guardar_en_archivo()
        print("Producto '{}' actualizado y guardado.".format(id_prod))

    def eliminar_producto(self, id_prod):
        if id_prod not in self.productos:
            raise KeyError("No existe producto con id '{}'.".format(id_prod))
        del self.productos[id_prod]
        self._guardar_en_archivo()
        print("Producto '{}' eliminado y guardado.".format(id_prod))

    def buscar(self, texto):
        t = texto.lower().strip()
        return [p for p in self.productos.values() if t in p.id.lower() or t in p.nombre.lower()]

    def listar(self):
        return list(self.productos.values())

    # Utilidad de prueba para generar archivo corrupto
    def generar_archivo_corrupto(self):
        contenido = [
            "P001|Lapiz HB|100|0.25",
            "MAL_FORMATO",
            "P002|Cuaderno|cincuenta|1.5",
            "P003|Borrador|25|x.y",
            "P004|Regla 30cm|15|0.8",
        ]
        with open(self.ruta_archivo, "w", encoding="utf-8") as f:
            f.write("\n".join(contenido))
        print("Archivo de prueba corrupto escrito en '{}'.".format(self.ruta_archivo))


# ------------------ CLI ------------------
def _leer_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Ingresa un número entero válido.")

def _leer_float(msg):
    while True:
        try:
            txt = input(msg).replace(",", ".")
            return float(txt)
        except ValueError:
            print("Ingresa un número válido (usa punto o coma).")

def _pedir_producto():
    id_ = input("ID: ").strip()
    nombre = input("Nombre: ").strip()
    cantidad = _leer_int("Cantidad: ")
    precio = _leer_float("Precio: ")
    return Producto(id_, nombre, cantidad, precio)

def run_cli(ruta_archivo=None):
    inv = Inventario(ruta_archivo or "inventario.txt")
    menu = """
================= MENÚ INVENTARIO =================
1) Agregar producto
2) Actualizar producto
3) Eliminar producto
4) Listar productos
5) Buscar producto
6) Generar archivo corrupto (PRUEBA)
0) Salir
===================================================
"""
    while True:
        try:
            print(menu)
            op = input("Elige una opción: ").strip()
            if op == "1":
                p = _pedir_producto()
                inv.agregar_producto(p)
            elif op == "2":
                id_ = input("ID a actualizar: ").strip()
                if id_ not in inv.productos:
                    print("No existe ese ID.")
                    continue
                print("(Deja vacío para mantener)")
                nombre = input("Nuevo nombre: ").strip()
                cant_txt = input("Nueva cantidad: ").strip()
                prec_txt = input("Nuevo precio: ").strip()
                cantidad = int(cant_txt) if cant_txt else None
                precio = float(prec_txt.replace(",", ".")) if prec_txt else None
                inv.actualizar_producto(id_, nombre or None, cantidad, precio)
            elif op == "3":
                id_ = input("ID a eliminar: ").strip()
                inv.eliminar_producto(id_)
            elif op == "4":
                items = inv.listar()
                if not items:
                    print("(Inventario vacío)")
                else:
                    print("{:<10}{:<25}{:>10}{:>12}".format("ID","Nombre","Cantidad","Precio"))
                    print("-"*57)
                    for p in items:
                        print("{:<10}{:<25}{:>10}{:>12.2f}".format(p.id, p.nombre, p.cantidad, p.precio))
            elif op == "5":
                q = input("Buscar por ID o nombre: ")
                for p in inv.buscar(q):
                    print("- {} | {} | {} uds | ${:.2f}".format(p.id, p.nombre, p.cantidad, p.precio))
            elif op == "6":
                inv.generar_archivo_corrupto()
                print("Reinicia el programa para ver cómo carga omitiendo líneas inválidas.")
            elif op == "0":
                print("Hasta luego.")
                break
            else:
                print("Opción inválida.")
        except (ValueError, KeyError) as e:
            print("Error:", e)
        except PermissionError:
            pass
        except OSError as e:
            print("Error del sistema de archivos:", e)


if __name__ == "__main__":
    run_cli()
