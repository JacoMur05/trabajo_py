import datetime

class Usuario:
    def __init__(self, id_usuario, nombre, documento, telefono, otro_contacto):
        self.id = id_usuario
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono
        self.otro_contacto = otro_contacto

    def __str__(self):
        return f"[{self.id}] {self.nombre} - Doc: {self.documento} | Tel: {self.telefono} | Otro: {self.otro_contacto}"


class Mesa:
    def __init__(self, id_mesa, numero_mesa, capacidad, ubicacion):
        self.id = id_mesa
        self.numero_mesa = numero_mesa
        self.capacidad = capacidad
        self.ubicacion = ubicacion

    def __str__(self):
        return f"Mesa #{self.numero_mesa} (ID: {self.id}) - Capacidad: {self.capacidad} pers. - Ubicación: {self.ubicacion}"


class Reserva:
    def __init__(self, id_reserva, fecha_hora, usuario, mesa, num_comensales, observaciones=""):
        self.id = id_reserva
        self.fecha_hora = fecha_hora
        self.usuario = usuario
        self.mesa = mesa
        self.num_comensales = num_comensales
        self.observaciones = observaciones

    def __str__(self):
        return (f"Reserva ID: {self.id}\n"
                f"  - Fecha/Hora: {self.fecha_hora}\n"
                f"  - Cliente: {self.usuario.nombre}\n"
                f"  - Mesa: #{self.mesa.numero_mesa} ({self.mesa.ubicacion})\n"
                f"  - Comensales: {self.num_comensales}\n"
                f"  - Observaciones: {self.observaciones if self.observaciones else 'Ninguna'}")


class SistemaReservas:
    def __init__(self):
        self.usuarios = {}
        self.mesas = {}
        self.reservas = []
        self.usuario_actual = None
        self._contador_usuario = 1
        self._contador_reserva = 1
        
        # Cargar algunas mesas por defecto para probar
        self._cargar_mesas_iniciales()

    def _cargar_mesas_iniciales(self):
        mesas_def = [
            Mesa(1, 101, 2, "Ventana"),
            Mesa(2, 102, 4, "Interior"),
            Mesa(3, 103, 6, "Terraza"),
            Mesa(4, 104, 8, "Salón Principal")
        ]
        for m in mesas_def:
            self.mesas[m.id] = m

    def crear_cuenta(self):
        print("\n--- FORMULARIO: CREAR CUENTA ---")
        nombre = input("Nombre completo: ").strip()
        documento = input("Documento de identidad: ").strip()
        telefono = input("Teléfono (# Tel): ").strip()
        otro_contacto = input("Otro contacto: ").strip()

        if not nombre or not documento:
            print("Error: El nombre y documento son obligatorios.")
            return

        usuario = Usuario(self._contador_usuario, nombre, documento, telefono, otro_contacto)
        self.usuarios[documento] = usuario
        self._contador_usuario += 1
        print(f"\n¡Cuenta creada exitosamente! Tu ID de Usuario es {usuario.id}.")

    def iniciar_sesion(self):
        print("\n--- INICIAR SESIÓN ---")
        documento = input("Ingrese su Documento: ").strip()
        if documento in self.usuarios:
            self.usuario_actual = self.usuarios[documento]
            print(f"\n¡Bienvenido/a, {self.usuario_actual.nombre}!")
        else:
            print("\nError: Usuario no encontrado. Por favor cree una cuenta primero.")

    def llenar_formulario_reserva(self):
        if not self.usuario_actual:
            print("\nDebes iniciar sesión primero para realizar una reserva.")
            return

        print("\n--- FORMULARIO: RESERVA ---")
        fecha_hora = input("Fecha y Hora (ej. 2026-10-25 20:00): ").strip()
        
        print("\nMesas Disponibles:")
        for mesa in self.mesas.values():
            print(f"  {mesa}")
            
        try:
            id_mesa = int(input("\nSeleccione el ID de la Mesa: "))
            if id_mesa not in self.mesas:
                print("Mesa no válida.")
                return
            
            num_comensales = int(input("Número de comensales (# Comensales): "))
            observaciones = input("Observaciones (opcional): ").strip()

            mesa_seleccionada = self.mesas[id_mesa]
            
            if num_comensales > mesa_seleccionada.capacidad:
                print(f"Advertencia: El número de comensales excede la capacidad de la mesa ({mesa_seleccionada.capacidad} pers.).")

            reserva = Reserva(
                id_reserva=self._contador_reserva,
                fecha_hora=fecha_hora,
                usuario=self.usuario_actual,
                mesa=mesa_seleccionada,
                num_comensales=num_comensales,
                observaciones=observaciones
            )
            
            self.reservas.append(reserva)
            self._contador_reserva += 1
            print("\n¡Reserva registrada con éxito!")
            print(reserva)

        except ValueError:
            print("Error: Ingrese valores numéricos válidos para la mesa y comensales.")

    def ver_mis_reservas(self):
        if not self.usuario_actual:
            print("\nDebes iniciar sesión para ver tus reservas.")
            return

        mis_reservas = [r for r in self.reservas if r.usuario.id == self.usuario_actual.id]
        print(f"\n--- RESERVAS DE {self.usuario_actual.nombre.upper()} ---")
        if not mis_reservas:
            print("No tienes reservas registradas.")
        else:
            for r in mis_reservas:
                print(r)
                print("-" * 30)

    def menu(self):
        while True:
            estado_usuario = f" (Sesión: {self.usuario_actual.nombre})" if self.usuario_actual else " (Sin sesión)"
            print(f"\n==========================================")
            print(f"  SISTEMA DE RESERVA DE MESAS{estado_usuario}")
            print(f"==========================================")
            print("1. Crear Cuenta")
            print("2. Iniciar Sesión")
            print("3. Llenar Formulario de Reserva")
            print("4. Ver Mis Reservas")
            print("5. Cerrar Sesión")
            print("6. Salir")
            
            opcion = input("Seleccione una opción (1-6): ").strip()

            if opcion == "1":
                self.crear_cuenta()
            elif opcion == "2":
                self.iniciar_sesion()
            elif opcion == "3":
                self.llenar_formulario_reserva()
            elif opcion == "4":
                self.ver_mis_reservas()
            elif opcion == "5":
                self.usuario_actual = None
                print("\nSesión cerrada.")
            elif opcion == "6":
                print("\n¡Gracias por usar el sistema!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    sistema = SistemaReservas()
    sistema.menu()