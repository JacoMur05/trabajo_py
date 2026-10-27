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
        return f"Mesa {self.numero_mesa} ➔ Capacidad: {self.capacidad} personas | Ubicación: {self.ubicacion}"


class Reserva:
    def __init__(self, id_reserva: int, fecha: datetime.date, hora: datetime.time, usuario: Usuario, mesa: Mesa, num_comensales: int, observaciones: str = "", estado: str = "Confirmada"):
        self.id = int(id_reserva)
        self.fecha = fecha
        self.hora = hora
        self.usuario = usuario
        self.mesa = mesa
        self.num_comensales = int(num_comensales)
        self.observaciones = str(observaciones)
        self.estado = estado

    def __str__(self):
        return (f"Reserva #{self.id} [{self.estado}]\n"
                f"  • Fecha: {self.fecha.strftime('%Y-%m-%d')}\n"
                f"  • Hora: {self.hora.strftime('%H:%M')}\n"
                f"  • Cliente: {self.usuario.nombre} (Doc: {self.usuario.documento})\n"
                f"  • Mesa: Mesa {self.mesa.numero_mesa} ({self.mesa.ubicacion})\n"
                f"  • Personas: {self.num_comensales}\n"
                f"  • Notas: {self.observaciones if self.observaciones else 'Ninguna'}")


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

    def _mesa_disponible(self, numero_mesa: int, fecha: datetime.date, hora: datetime.time, id_reserva_ignorar: int = None) -> bool:
        for r in self.reservas:
            if r.estado == "Confirmada" and r.mesa.numero_mesa == numero_mesa and r.fecha == fecha and r.hora == hora:
                if id_reserva_ignorar is None or r.id != id_reserva_ignorar:
                    return False
        return True

    def crear_cuenta(self):
        limpiar_pantalla()
        print("==========================================")
        print("        ✨ REGISTRO DE NUEVO USUARIO")
        print("==========================================")
        nombre = input("Nombre completo: ").strip()
        documento = input("Documento de identidad: ").strip()
        telefono = input("Teléfono de contacto: ").strip()
        otro_contacto = input("Otro teléfono o correo (opcional): ").strip()

        if not nombre or not documento:
            print("\n💡 Por favor, completa al menos tu nombre y documento para registrarte.")
            input("\nPresiona Enter para continuar...")
            return

        usuario = Usuario(self._contador_usuario, nombre, documento, telefono, otro_contacto)
        self.usuarios[documento] = usuario
        self._contador_usuario += 1
        self.usuario_actual = usuario

        print(f"\n🎉 ¡Bienvenido/a, {usuario.nombre}! Tu cuenta se ha creado con éxito.")
        input("\nPresiona Enter para continuar...")

    def iniciar_sesion(self):
        limpiar_pantalla()
        print("==========================================")
        print("             🔑 INICIAR SESIÓN")
        print("==========================================")
        documento = input("Ingresa tu Documento de Identidad: ").strip()
        if documento in self.usuarios:
            self.usuario_actual = self.usuarios[documento]
            print(f"\n🎉 ¡Hola de nuevo, {self.usuario_actual.nombre}! Sesión iniciada correctamente.")
        else:
            print("\n🔍 No encontramos una cuenta asociada a ese documento. Te invitamos a registrarte primero.")
        input("\nPresiona Enter para continuar...")

    def llenar_formulario_reserva(self):
        if not self.usuario_actual:
            limpiar_pantalla()
            print("\n🔒 Para realizar una reserva, primero debes iniciar sesión o crear una cuenta.")
            input("\nPresiona Enter para continuar...")
            return

        while True:
            limpiar_pantalla()
            print("==========================================")
            print("          🍽️ NUEVA RESERVA DE MESA")
            print("==========================================")

            # 1. Fecha
            fecha_input = input("¿Qué día te gustaría venir? (AAAA-MM-DD | Ej: 2026-10-25): ").strip()
            try:
                fecha_obj = datetime.datetime.strptime(fecha_input, "%Y-%m-%d").date()
            except ValueError:
                print("\n📅 Ups, la fecha ingresada no parece válida. Por favor usa el formato AAAA-MM-DD.")
                input("\nPresiona Enter para reintentar...")
                continue

            # 2. Hora
            hora_input = input("¿A qué hora? (HH:MM formato 24h | Ej: 20:00): ").strip()
            try:
                hora_obj = datetime.datetime.strptime(hora_input, "%H:%M").time()
            except ValueError:
                print("\n⏰ El formato de hora no es correcto. Recuerda ingresarlo como HH:MM (24h).")
                input("\nPresiona Enter para reintentar...")
                continue

            # Validación de tiempo pasado
            fecha_hora_comb = datetime.datetime.combine(fecha_obj, hora_obj)
            if fecha_hora_comb < datetime.datetime.now():
                print("\n⏳ ¡Vaya! Esa fecha y hora ya quedaron en el pasado. Elige un momento futuro.")
                input("\nPresiona Enter para reintentar...")
                continue

            # 3. Número de Mesa
            print("\n--- 🪑 MESAS DISPONIBLES EN EL RESTAURANTE ---")
            for mesa in self.mesas.values():
                print(f"  • {mesa}")
            print("---------------------------------------------")

            try:
                num_mesa = int(input("\nSelecciona el número de mesa que prefieres (ej: 1, 2, 3, 4): "))
            except ValueError:
                print("\n🔢 Por favor ingresa únicamente el número de la mesa.")
                input("\nPresiona Enter para reintentar...")
                continue

            if num_mesa not in self.mesas:
                print(f"\n🔍 No encontramos la Mesa {num_mesa} en la lista. Elige una de las opciones disponibles.")
                input("\nPresiona Enter para reintentar...")
                continue

            # Ocupación
            if not self._mesa_disponible(num_mesa, fecha_obj, hora_obj):
                print(f"\n🗓️ La Mesa {num_mesa} ya está reservada para el {fecha_obj} a las {hora_obj.strftime('%H:%M')}. ¡Intenta con otra mesa u otro horario!")
                input("\nPresiona Enter para reintentar...")
                continue

            mesa_seleccionada = self.mesas[num_mesa]

            # 4. Comensales
            try:
                num_comensales = int(input("¿Cuántas personas asistirán?: "))
                if num_comensales <= 0:
                    print("\n👥 Debe asistir al menos 1 persona.")
                    input("\nPresiona Enter para reintentar...")
                    continue
            except ValueError:
                print("\n🔢 Por favor indica el número de personas con un valor numérico.")
                input("\nPresiona Enter para reintentar...")
                continue

            if num_comensales > mesa_seleccionada.capacidad:
                print(f"\n💡 La Mesa {mesa_seleccionada.numero_mesa} es para {mesa_seleccionada.capacidad} personas máx. Como son {num_comensales}, te recomendamos elegir una mesa más amplia.")
                input("\nPresiona Enter para reintentar...")
                continue

            # 5. Observaciones
            observaciones = input("¿Alguna solicitud u observación especial? (opcional): ").strip()

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

            print("\n🎉 ¡TU RESERVA HA SIDO CONFIRMADA!")
            print("=" * 40)
            print(reserva)
            print("=" * 40)
            input("\nPresiona Enter para volver al menú principal...")
            break

    def ver_mis_reservas(self):
        limpiar_pantalla()
        if not self.usuario_actual:
            print("\n🔒 Inicia sesión para revisar tus reservas.")
            input("\nPresiona Enter para continuar...")
            return

        mis_reservas = [r for r in self.reservas if r.usuario.id == self.usuario_actual.id]
        print("==========================================")
        print(f"    📋 MIS RESERVAS - {self.usuario_actual.nombre.upper()}")
        print("==========================================")
        if not mis_reservas:
            print("Aún no tienes reservas registradas. ¡Te esperamos pronto!")
        else:
            for r in mis_reservas:
                print(r)
                print("-" * 35)
        input("\nPresiona Enter para continuar...")

    def editar_reserva(self):
        limpiar_pantalla()
        if not self.usuario_actual:
            print("\n🔒 Inicia sesión para modificar tus reservas.")
            input("\nPresiona Enter para continuar...")
            return

        reservas_activas = [r for r in self.reservas if r.usuario.id == self.usuario_actual.id and r.estado == "Confirmada"]
        if not reservas_activas:
            print("\n💡 No tienes reservas activas para modificar en este momento.")
            input("\nPresiona Enter para continuar...")
            return

        print("==========================================")
        print("           ✏️ MODIFICAR RESERVA")
        print("==========================================")
        for r in reservas_activas:
            print(r)
            print("-" * 35)

        try:
            id_res = int(input("\nIngresa el ID (#) de la reserva que deseas modificar (o 0 para volver): "))
        except ValueError:
            print("\n🔢 Por favor ingresa un número de ID válido.")
            input("\nPresiona Enter para continuar...")
            return

        if id_res == 0:
            return

        reserva = next((r for r in reservas_activas if r.id == id_res), None)
        if not reserva:
            print(f"\n🔍 No encontramos ninguna reserva activa con el ID #{id_res}.")
            input("\nPresiona Enter para continuar...")
            return

        print(f"\n--- Modificando Reserva #{reserva.id} ---")
        print("(Si no deseas cambiar un dato, simplemente presiona Enter)\n")

        # 1. Nueva Fecha
        fecha_str = input(f"Nueva fecha [{reserva.fecha.strftime('%Y-%m-%d')}]: ").strip()
        if fecha_str:
            try:
                nueva_fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                print("\n📅 Formato de fecha no válido. No se guardaron los cambios.")
                input("\nPresiona Enter para continuar...")
                return
        else:
            nueva_fecha = reserva.fecha

        # 2. Nueva Hora
        hora_str = input(f"Nueva hora [{reserva.hora.strftime('%H:%M')}]: ").strip()
        if hora_str:
            try:
                nueva_hora = datetime.datetime.strptime(hora_str, "%H:%M").time()
            except ValueError:
                print("\n⏰ Formato de hora no válido. No se guardaron los cambios.")
                input("\nPresiona Enter para continuar...")
                return
        else:
            nueva_hora = reserva.hora

        if datetime.datetime.combine(nueva_fecha, nueva_hora) < datetime.datetime.now():
            print("\n⏳ La fecha y hora no pueden ser en el pasado.")
            input("\nPresiona Enter para continuar...")
            return

        # 3. Nueva Mesa
        print("\n--- 🪑 MESAS DISPONIBLES ---")
        for m in self.mesas.values():
            print(f"  • {m}")
        mesa_str = input(f"Número de Mesa [{reserva.mesa.numero_mesa}]: ").strip()
        if mesa_str:
            try:
                nueva_mesa_num = int(mesa_str)
            except ValueError:
                print("\n🔢 El número de mesa no es válido.")
                input("\nPresiona Enter para continuar...")
                return
        else:
            nueva_mesa_num = reserva.mesa.numero_mesa

        if nueva_mesa_num not in self.mesas:
            print(f"\n🔍 La Mesa {nueva_mesa_num} no existe.")
            input("\nPresiona Enter para continuar...")
            return

        if not self._mesa_disponible(nueva_mesa_num, nueva_fecha, nueva_hora, id_reserva_ignorar=reserva.id):
            print(f"\n🗓️ La Mesa {nueva_mesa_num} está ocupada el {nueva_fecha} a las {nueva_hora.strftime('%H:%M')}.")
            input("\nPresiona Enter para continuar...")
            return

        nueva_mesa = self.mesas[nueva_mesa_num]

        # 4. Comensales
        comensales_str = input(f"Cantidad de personas [{reserva.num_comensales}]: ").strip()
        if comensales_str:
            try:
                nuevos_comensales = int(comensales_str)
            except ValueError:
                print("\n🔢 Cantidad de personas no válida.")
                input("\nPresiona Enter para continuar...")
                return
        else:
            nuevos_comensales = reserva.num_comensales

        if nuevos_comensales <= 0:
            print("\n👥 Debe asistir al menos 1 persona.")
            input("\nPresiona Enter para continuar...")
            return

        if nuevos_comensales > nueva_mesa.capacidad:
            print(f"\n💡 La Mesa {nueva_mesa.numero_mesa} admite máximo {nueva_mesa.capacidad} personas.")
            input("\nPresiona Enter para continuar...")
            return

        # 5. Observaciones
        obs_str = input(f"Observaciones [{reserva.observaciones}]: ").strip()
        nuevas_obs = obs_str if obs_str else reserva.observaciones

        reserva.fecha = nueva_fecha
        reserva.hora = nueva_hora
        reserva.mesa = nueva_mesa
        reserva.num_comensales = nuevos_comensales
        reserva.observaciones = nuevas_obs

        print("\n✨ ¡TU RESERVA SE HA ACTUALIZADO CON ÉXITO!")
        print("=" * 40)
        print(reserva)
        print("=" * 40)
        input("\nPresiona Enter para volver al menú...")

    def cancelar_reserva(self):
        limpiar_pantalla()
        if not self.usuario_actual:
            print("\n🔒 Inicia sesión para cancelar reservas.")
            input("\nPresiona Enter para continuar...")
            return

        reservas_activas = [r for r in self.reservas if r.usuario.id == self.usuario_actual.id and r.estado == "Confirmada"]
        if not reservas_activas:
            print("\n💡 No tienes reservas activas para cancelar.")
            input("\nPresiona Enter para continuar...")
            return

        print("==========================================")
        print("           ❌ CANCELAR RESERVA")
        print("==========================================")
        for r in reservas_activas:
            print(r)
            print("-" * 35)

        try:
            id_res = int(input("\nIngresa el ID (#) de la reserva que deseas cancelar (o 0 para volver): "))
        except ValueError:
            print("\n🔢 ID no válido.")
            input("\nPresiona Enter para continuar...")
            return

        if id_res == 0:
            return

        reserva = next((r for r in reservas_activas if r.id == id_res), None)
        if not reserva:
            print(f"\n🔍 No se encontró una reserva activa con el ID #{id_res}.")
        else:
            reserva.estado = "Cancelada"
            print(f"\n👍 Tu Reserva #{reserva.id} ha sido cancelada correctamente (queda guardada en tu historial con estado 'Cancelada').")

        input("\nPresiona Enter para continuar...")

    def menu(self):
        while True:
            limpiar_pantalla()
            opciones = {}
            idx = 1

            if not self.usuario_actual:
                print("==========================================")
                print("  🍽️ BIENVENIDO AL SISTEMA DE RESERVAS")
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
                print("==========================================")
                print(f"  🍽️ MENÚ PRINCIPAL (Sesión: {self.usuario_actual.nombre})")
                print("==========================================")

                print(f"{idx}. Reservar una Mesa")
                opciones[str(idx)] = "reserva"
                idx += 1

                mis_reservas = [r for r in self.reservas if r.usuario.id == self.usuario_actual.id]
                if len(mis_reservas) > 0:
                    print(f"{idx}. Ver Mis Reservas")
                    opciones[str(idx)] = "ver_reservas"
                    idx += 1

                reservas_activas = [r for r in mis_reservas if r.estado == "Confirmada"]
                if len(reservas_activas) > 0:
                    print(f"{idx}. Modificar Reserva")
                    opciones[str(idx)] = "editar_reserva"
                    idx += 1

                    print(f"{idx}. Cancelar Reserva")
                    opciones[str(idx)] = "cancelar_reserva"
                    idx += 1

                print(f"{idx}. Cerrar Sesión")
                opciones[str(idx)] = "cerrar_sesion"
                idx += 1

                print(f"{idx}. Salir")
                opciones[str(idx)] = "salir"

            opcion = input("\nSelecciona una opción: ").strip()

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
                elif accion == "editar_reserva":
                    self.editar_reserva()
                elif accion == "cancelar_reserva":
                    self.cancelar_reserva()
                elif accion == "cerrar_sesion":
                    self.usuario_actual = None
                    print("\n👋 Has cerrado sesión. ¡Hasta pronto!")
                    input("\nPresiona Enter para continuar...")
                elif accion == "salir":
                    print("\n¡Gracias por visitarnos! Que tengas un excelente día. 😊")
                    break
            else:
                print("\n💡 Opción no válida, por favor intenta de nuevo.")
                input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    sistema = SistemaReservas()
    sistema.menu()