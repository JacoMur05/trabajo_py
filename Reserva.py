import datetime
import os

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')


class Usuario:
    def __init__(self, id_usuario: int, nombre: str, documento: str, telefono: str, otro_contacto: str):
        self.id = int(id_usuario)
        self.nombre = str(nombre)
        self.documento = str(documento)
        self.telefono = str(telefono)
        self.otro_contacto = str(otro_contacto)

    def __str__(self):
        return f"[{self.id}] {self.nombre} - Doc: {self.documento} | Tel: {self.telefono}"


class Mesa:
    def __init__(self, id_mesa: int, numero_mesa: int, capacidad: int, ubicacion: str):
        self.id = int(id_mesa)
        self.numero_mesa = int(numero_mesa)
        self.capacidad = int(capacidad)
        self.ubicacion = str(ubicacion)

    def __str__(self):
        return f"Mesa {self.numero_mesa} -> Capacidad: {self.capacidad} personas | Ubicación: {self.ubicacion}"


class Reserva:
    def __init__(self, id_reserva: int, fecha: datetime.date, hora: datetime.time, usuario: Usuario, mesa: Mesa, num_comensales: int, observaciones: str = ""):
        self.id = int(id_reserva)
        self.fecha = fecha
        self.hora = hora
        self.usuario = usuario
        self.mesa = mesa
        self.num_comensales = int(num_comensales)
        self.observaciones = str(observaciones)

    def __str__(self):
        return (f"Reserva #{self.id}\n"
                f"  - Fecha: {self.fecha.strftime('%Y-%m-%d')}\n"
                f"  - Hora: {self.hora.strftime('%H:%M')}\n"
                f"  - Cliente: {self.usuario.nombre} (Doc: {self.usuario.documento})\n"
                f"  - Mesa: Mesa {self.mesa.numero_mesa} ({self.mesa.ubicacion})\n"
                f"  - Comensales: {self.num_comensales}\n"
                f"  - Observaciones: {self.observaciones if self.observaciones else 'Sin observaciones'}")


class SistemaReservas:
    def __init__(self):
        self.usuarios = {}
        self.mesas = {}
        self.reservas = []
        self.usuario_actual = None
        self._contador_usuario = 1
        self._contador_reserva = 1
        self._cargar_mesas_iniciales()

    def _cargar_mesas_iniciales(self):
        mesas_def = [
            Mesa(id_mesa=1, numero_mesa=1, capacidad=2, ubicacion="Ventana"),
            Mesa(id_mesa=2, numero_mesa=2, capacidad=4, ubicacion="Interior"),
            Mesa(id_mesa=3, numero_mesa=3, capacidad=6, ubicacion="Terraza"),
            Mesa(id_mesa=4, numero_mesa=4, capacidad=8, ubicacion="Salón Principal")
        ]
        for m in mesas_def:
            self.mesas[m.numero_mesa] = m

    def crear_cuenta(self):
        limpiar_pantalla()
        print("==========================================")
        print("          FORMULARIO: CREAR CUENTA")
        print("==========================================")
        nombre = input("Nombre completo: ").strip()
        documento = input("Documento de identidad: ").strip()
        telefono = input("Teléfono (# Tel): ").strip()
        otro_contacto = input("Otro contacto: ").strip()

        if not nombre or not documento:
            print("\n🚨 ¡ERROR! El nombre y el documento son obligatorios.")
            input("\nPresione Enter para continuar...")
            return

        usuario = Usuario(self._contador_usuario, nombre, documento, telefono, otro_contacto)
        self.usuarios[documento] = usuario
        self._contador_usuario += 1

        # Sesión iniciada automáticamente al registrarse
        self.usuario_actual = usuario

        print(f"\n✅ ¡Cuenta creada exitosamente! Sesión iniciada como: {usuario.nombre}")
        input("\nPresione Enter para continuar...")

    def iniciar_sesion(self):
        limpiar_pantalla()
        print("==========================================")
        print("             INICIAR SESIÓN")
        print("==========================================")
        documento = input("Ingrese su Documento de Identidad: ").strip()
        if documento in self.usuarios:
            self.usuario_actual = self.usuarios[documento]
            print(f"\n✅ ¡Bienvenido/a, {self.usuario_actual.nombre}!")
        else:
            print("\n🚨 ¡ERROR! Usuario no encontrado. Crea una cuenta primero.")
        input("\nPresione Enter para continuar...")

    def llenar_formulario_reserva(self):
        if not self.usuario_actual:
            limpiar_pantalla()
            print("\n🚨 ¡ERROR! Debes iniciar sesión antes de realizar una reserva.")
            input("\nPresione Enter para continuar...")
            return

        while True:
            limpiar_pantalla()
            print("==========================================")
            print("         FORMULARIO DE RESERVA")
            print("==========================================")

            # 1. Fecha
            fecha_input = input("Ingrese la Fecha (YYYY-MM-DD | Ej: 2026-10-25): ").strip()
            try:
                fecha_obj = datetime.datetime.strptime(fecha_input, "%Y-%m-%d").date()
            except ValueError:
                print("\n🚨 ¡ALARMA DE ERROR! La fecha debe ser válida y en formato YYYY-MM-DD.")
                input("\nPresione Enter para reiniciar el registro limpio...")
                continue

            # 2. Hora
            hora_input = input("Ingrese la Hora (HH:MM formato 24h | Ej: 20:00): ").strip()
            try:
                hora_obj = datetime.datetime.strptime(hora_input, "%H:%M").time()
            except ValueError:
                print("\n🚨 ¡ALARMA DE ERROR! La hora debe ser válida y en formato HH:MM (24 horas).")
                input("\nPresione Enter para reiniciar el registro limpio...")
                continue

            # Validación de fecha u hora en el pasado
            fecha_hora_comb = datetime.datetime.combine(fecha_obj, hora_obj)
            if fecha_hora_comb < datetime.datetime.now():
                print("\n🚨 ¡ALARMA DE ERROR! No puedes hacer reservas en fechas u horas pasadas.")
                input("\nPresione Enter para reiniciar el registro limpio...")
                continue

            # 3. Número de Mesa
            print("\n--- MESAS DISPONIBLES ---")
            for mesa in self.mesas.values():
                print(f"  • {mesa}")
            print("-------------------------")

            try:
                num_mesa = int(input("\nIngrese el número de mesa (ej: 1, 2, 3, 4): "))
            except ValueError:
                print("\n🚨 ¡ALARMA DE ERROR! Debe ingresar un número entero para la mesa.")
                input("\nPresione Enter para reiniciar el registro limpio...")
                continue

            if num_mesa not in self.mesas:
                print(f"\n🚨 ¡ALARMA DE ERROR! La Mesa {num_mesa} no existe.")
                input("\nPresione Enter para reiniciar el registro limpio...")
                continue

            mesa_seleccionada = self.mesas[num_mesa]

            # 4. Cantidad de comensales
            try:
                num_comensales = int(input(f"Ingrese la cantidad de personas (# Comensales): "))
                if num_comensales <= 0:
                    print("\n🚨 ¡ALARMA DE ERROR! Debe ingresar al menos 1 comensal.")
                    input("\nPresione Enter para reiniciar el registro limpio...")
                    continue
            except ValueError:
                print("\n🚨 ¡ALARMA DE ERROR! La cantidad de comensales debe ser un número entero.")
                input("\nPresione Enter para reiniciar el registro limpio...")
                continue

            if num_comensales > mesa_seleccionada.capacidad:
                print(f"\n🚨 ¡ALARMA DE ERROR! NO SE PUEDE RESERVAR:")
                print(f"   Elegiste la Mesa {mesa_seleccionada.numero_mesa} que tiene capacidad para {mesa_seleccionada.capacidad} personas,")
                print(f"   e intentaste ingresar {num_comensales} personas.")
                input("\nPresione Enter para reiniciar el registro limpio...")
                continue

            # 5. Observaciones
            observaciones = input("Observaciones (opcional): ").strip()

            reserva = Reserva(
                id_reserva=self._contador_reserva,
                fecha=fecha_obj,
                hora=hora_obj,
                usuario=self.usuario_actual,
                mesa=mesa_seleccionada,
                num_comensales=num_comensales,
                observaciones=observaciones
            )

            self.reservas.append(reserva)
            self._contador_reserva += 1

            print("\n✅ ¡RESERVA REGISTRADA CON ÉXITO!")
            print("=" * 40)
            print(reserva)
            print("=" * 40)
            input("\nPresione Enter para volver al menú principal...")
            break

    def ver_mis_reservas(self):
        limpiar_pantalla()
        if not self.usuario_actual:
            print("\n🚨 Debes iniciar sesión para ver tus reservas.")
            input("\nPresione Enter para continuar...")
            return

        mis_reservas = [r for r in self.reservas if r.usuario.id == self.usuario_actual.id]
        print("==========================================")
        print(f"    RESERVAS DE {self.usuario_actual.nombre.upper()}")
        print("==========================================")
        for r in mis_reservas:
            print(r)
            print("-" * 35)
        input("\nPresione Enter para continuar...")

    def menu(self):
        while True:
            limpiar_pantalla()
            opciones = {}
            idx = 1

            # Si no ha iniciado sesión, muestra menú restringido
            if not self.usuario_actual:
                print("==========================================")
                print("  SISTEMA DE RESERVA DE MESAS (Sin sesión)")
                print("==========================================")
                print(f"{idx}. Crear Cuenta")
                opciones[str(idx)] = "crear_cuenta"
                idx += 1

                print(f"{idx}. Iniciar Sesión")
                opciones[str(idx)] = "iniciar_sesion"
                idx += 1

                print(f"{idx}. Salir")
                opciones[str(idx)] = "salir"
            else:
                # Menú para usuario con sesión activa
                print("==========================================")
                print(f"  SISTEMA DE RESERVA (Sesión: {self.usuario_actual.nombre})")
                print("==========================================")
                
                print(f"{idx}. Llenar Formulario de Reserva")
                opciones[str(idx)] = "reserva"
                idx += 1

                # Muestra "Ver Mis Reservas" SOLO si el usuario tiene reservas
                mis_reservas = [r for r in self.reservas if r.usuario.id == self.usuario_actual.id]
                if len(mis_reservas) > 0:
                    print(f"{idx}. Ver Mis Reservas")
                    opciones[str(idx)] = "ver_reservas"
                    idx += 1

                print(f"{idx}. Cerrar Sesión")
                opciones[str(idx)] = "cerrar_sesion"
                idx += 1

                print(f"{idx}. Salir")
                opciones[str(idx)] = "salir"

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion in opciones:
                accion = opciones[opcion]
                if accion == "crear_cuenta":
                    self.crear_cuenta()
                elif accion == "iniciar_sesion":
                    self.iniciar_sesion()
                elif accion == "reserva":
                    self.llenar_formulario_reserva()
                elif accion == "ver_reservas":
                    self.ver_mis_reservas()
                elif accion == "cerrar_sesion":
                    self.usuario_actual = None
                    print("\nSesión cerrada.")
                    input("\nPresione Enter para continuar...")
                elif accion == "salir":
                    print("\n¡Gracias por usar el sistema!")
                    break
            else:
                print("\nOpción no válida.")
                input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    sistema = SistemaReservas()
    sistema.menu()