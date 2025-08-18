# ============================================
# Sistema de Gestión de Inventarios - Consola
# ============================================

# ------- Clase Producto -------
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self._id = str(id_producto).strip()
        self._nombre = str(nombre).strip()
        self._cantidad = int(cantidad)
        self._precio = float(precio)

    # Getters
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # Setters
    def set_cantidad(self, cantidad):
        self._cantidad = int(cantidad)

    def set_precio(self, precio):
        self._precio = float(precio)

    def __str__(self):
        return f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: {self._precio:.2f}"


# ------- Clase Inventario -------
class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print("❌ Error: Ya existe un producto con este ID.")
                return
        self.productos.append(producto)
        print("✅ Producto agregado correctamente.")

    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                print("✅ Producto eliminado.")
                return
        print("❌ No se encontró un producto con ese ID.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                print("✅ Producto actualizado.")
                return
        print("❌ No se encontró un producto con ese ID.")

    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print("🔎 Resultados de búsqueda:")
            for p in resultados:
                print(p)
        else:
            print("❌ No se encontraron productos con ese nombre.")

    def mostrar_productos(self):
        if not self.productos:
            print("📦 Inventario vacío.")
        else:
            print("📋 Lista de productos:")
            for p in self.productos:
                print(p)


# ------- Menú principal -------
def menu():
    inventario = Inventario()

    while True:
        print("\n=== Sistema de Gestión de Inventarios ===")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_producto = input("Ingrese el ID: ")
            nombre = input("Ingrese el nombre: ")
            try:
                cantidad = int(input("Ingrese la cantidad: "))
                precio = float(input("Ingrese el precio: "))
            except ValueError:
                print("❌ Error: La cantidad y el precio deben ser numéricos.")
                continue
            producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar_producto(producto)

        elif opcion == "2":
            id_producto = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = input("Ingrese el ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (dejar vacío si no se cambia): ")
            precio = input("Nuevo precio (dejar vacío si no se cambia): ")

            nueva_cantidad = int(cantidad) if cantidad else None
            nuevo_precio = float(precio) if precio else None

            inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio)

        elif opcion == "4":
            nombre = input("Ingrese el nombre a buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_productos()

        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            break

        else:
            print("❌ Opción no válida. Intente nuevamente.")


# ------- Punto de entrada -------
if __name__ == "__main__":
    menu()
