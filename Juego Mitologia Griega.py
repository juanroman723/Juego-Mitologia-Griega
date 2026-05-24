from __future__ import annotations #Permite usar anotaciones de tipo para clases que aún no han sido definidas y evitar errores
from abc import ABC, abstractmethod #Libreria para utilizar la abstracción en las clases
import json #Libreria para guardar el progreso del juego en un archivo JSON
import random #Libreria para generar números aleatorios
from tkinter import * #Libreria para crear la interfaz gráfica del juego

#COLORES Y ESTILOS PARA LA INTERFAZ GRÁFICA
BG_DARK = "#0d0d0d"
BG_PANEL = "#1a1610"
BG_CARD = "#211e14"
GOLD = "#c9a84c"
GOLD_LIGHT = "#e8c96e"
GOLD_DIM = "#7a6430"
RED_HP = "#c0392b"
BLUE_MANA = "#2980b9"
GREEN_WIN = "#27ae60"
TEXT_WHITE = "#f0ead6"
TEXT_DIM = "#8a7d5a"
BORDER = "#3a3020"

class SerMitico(ABC): #Clase base abstracta para representar a los seres miticos del juego
    _total_creados = 0 #Atributo de clase para contar el total de seres miticos creados
    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int) -> None:
        self.__nombre: str = nombre
        self.__vida: int = max(0, vida)
        self.__vida_maxima: int = vida
        self.ataque: int = ataque
        self.defensa: int = defensa
        self.v = random.randint(-20, 20) #Variación aleatoria para hacer cada ser mitico único
        SerMitico._total_creados += 1

    @property
    def nombre(self) -> str:
        return self.__nombre
      
    @property
    def vida(self) -> int:
        return self.__vida
    
    @property
    def vida_maxima(self) -> int:
        return self.__vida_maxima

    @vida.setter
    def vida(self, valor) -> None:
        self.__vida = max(0, valor)
    
    @vida_maxima.setter
    def vida_maxima(self, valor) -> None:
        self.__vida_maxima = max(1, valor)
        self.__vida = min(self.__vida, self.__vida_maxima)

    @abstractmethod #Método abstracto para definir el ataque de cada ser mitico
    def atacar(self, enemigo: SerMitico) -> tuple[str, int, bool]:
        pass
    
    @abstractmethod #Método abstracto para definir el poder especial de cada ser mitico
    def usar_habilidad(self) -> int:
        pass

    def recibir_daño(self, cantidad) -> int:
        daño_real = max(0, cantidad - self.defensa)
        self.vida -= daño_real
        return daño_real
    
    def esta_vivo(self) -> bool:
        return self.vida > 0
    
    @staticmethod #Método estático para calcular el daño de un ataque, teniendo en cuenta el ataque del atacante y la defensa del defensor
    def calcular_daño(atacante: "SerMitico", defensor: "SerMitico") -> int:
        base = atacante.ataque - defensor.defensa
        variacion = random.randint(-10, 10)
        daño = max(0, base + variacion)

        return daño
    
    @classmethod #Método de clase para obtener el total de seres miticos creados
    def total_creados(cls) -> int:
        return cls._total_creados
    
    def __repr__(self) -> str: #Método para representar el objeto de manera formal, mostrando su tipo y atributos principales
        return f"{type(self).__name__}(nombre={self.nombre}, vida={self.vida}, ataque={self.ataque}, defensa={self.defensa})"
    
    def __str__(self): #Método para representar el objeto como una cadena de texto, mostrando su nombre, vida, ataque y defensa
        return f"{self.nombre} (Vida: {self.vida} | Ataque: {self.ataque} | Defensa: {self.defensa})"

#Dioses
class Dios(SerMitico):
    def __init__ (self, nombre: str, vida: int, ataque: int, defensa: int, poder_especial: str, mana: int) -> None:
        super().__init__(nombre, vida, ataque, defensa)
        self.poder_especial: str = poder_especial
        self.mana: int = mana
        self.mana_maximo: int = mana

    def atacar(self, enemigo: SerMitico) -> tuple[str, int, bool]:
        daño: int = SerMitico.calcular_daño(self, enemigo) 
        critico: bool = random.random() < 0.2        
        if critico:
           daño *= 2
        return self.nombre, daño, critico
    
    def usar_habilidad(self) -> int:
        if self.mana >=25:
            self.mana -= 25
            return random.randint(self.ataque + 15, self.ataque + 30)
        else:
            print(f"{self.nombre} no tiene suficiente maná para usar su habilidad {self.poder_especial}")
            return 0
    
    def __str__(self) -> str: #Método para representar el objeto como una cadena de texto, mostrando su nombre, vida, ataque, defensa, poder especial y maná
        return (super().__str__() + f" | Poder Especial: {self.poder_especial} | Maná: {self.mana}")
    
    def __repr__(self) -> str: #Método para representar el objeto de manera formal, mostrando su tipo y atributos principales, incluyendo el poder especial y el maná
        return (super().__repr__() + f", poder_especial={self.poder_especial}, mana={self.mana}")
    
class Zeus(Dios):
    def __init__ (self) -> None:
        super().__init__("Zeus", 100+self.v, 70+self.v, 25+self.v, "Rayo Divino", 200+self.v)

class Ares(Dios):
    def __init__ (self) -> None:
        super().__init__("Ares", 130+self.v, 65+self.v, 40+self.v, "Furia de Guerra", 150+self.v)
        
class Poseidon(Dios):
    def __init__ (self) -> None:
        super().__init__("Poseidon", 120+self.v, 75+self.v, 30+self.v, "Oleada Marina", 180+self.v)

class Hades(Dios):
    def __init__ (self) -> None:
        super().__init__("Hades", 110+self.v, 80+self.v, 35+self.v, "Sombra del Inframundo", 160+self.v)

class Atenea(Dios):
    def __init__ (self) -> None:
        super().__init__("Atenea", 90+self.v, 60+self.v, 50+self.v, "Escudo de Sabiduría", 170+self.v)

#Criaturas
class Criatura(SerMitico):
    def __init__ (self, nombre: str, vida: int, ataque: int, defensa: int, habilidad: str, multiplicador: float) -> None:
        super().__init__(nombre, vida, ataque, defensa)
        self.habilidad: str = habilidad
        self.multiplicador: float = multiplicador

    def atacar(self, enemigo: SerMitico) -> tuple[str, int, bool]:
        daño: int = SerMitico.calcular_daño(self, enemigo)
        critico: bool = random.random() < 0.2        
        if critico:
           daño *= 2
        return self.nombre, daño, critico
    
    def usar_habilidad(self) -> int:   
        return int(random.randint(self.ataque + 15, self.ataque + 30))
    
    def __str__(self): #Método magico para representar el objeto como una cadena de texto
        return (f"{self.nombre} (Vida: {self.vida} | Ataque: {self.ataque} | Defensa: {self.defensa} | "
        f"Habilidad: {self.habilidad} | Multiplicador de puntos: {self.multiplicador})")
    
    def __repr__(self): #Método magico para representar el objeto de manera formal, mostrando su tipo y atributos principales
        return super().__repr__() + f", habilidad={self.habilidad}, multiplicador={self.multiplicador}"
    
class Minotauro(Criatura):
    def __init__ (self):
        super().__init__("Minotauro", 150+self.v, 55+self.v, 45+self.v, "Embestida", 1.5)
    
class Medusa(Criatura):
    def __init__ (self):
        super().__init__("Medusa", 90+self.v, 70+self.v, 25+self.v, "Petrificación", 1.2)
    
class Ciclope(Criatura):
    def __init__ (self):
        super().__init__("Ciclope", 130+self.v, 60+self.v, 40+self.v, "Mazazo", 1.0)

class Hidra(Criatura):
    def __init__ (self):
        super().__init__("Hidra", 170+self.v, 65+self.v, 40+self.v, "Multi-cabezas", 2.0)
    
class Escila(Criatura):
    def __init__ (self):
        super().__init__("Escila", 150+self.v, 65+self.v, 35+self.v, "Mordedura", 1.8)
    
#Item
class Item: #Nueva clase para representar los items que el jugador puede usar durante el combate
    def __init__(self,nombre: str, tipo: str, valor: int) -> None:
        self.nombre: str = nombre
        self.tipo: str = tipo
        self.valor = valor
    
    def usar(self, dios: Dios) -> str: #Método para usar el item, dependiendo de su tipo, puede curar, restaurar maná o aumentar el ataque del dios
        if self.tipo == "Curación":
            dios.vida = min(dios.vida + self.valor, dios.vida_maxima)
            return f"Usaste {self.nombre} y recuperaste {self.valor} puntos de vida"
        
        elif self.tipo == "Maná": 
            dios.mana = min(dios.mana + self.valor, dios.mana_maximo)
            return f"Usaste {self.nombre} y recuperaste {self.valor} puntos de maná"
        
        elif self.tipo == "Ataque":
            dios.ataque += self.valor
            dios.ataque = min(dios.ataque, 200) #Limitar el ataque máximo a 200
            return f"Usaste {self.nombre} y aumentaste tu ataque en {self.valor} puntos"
        
        return f"Usaste {self.nombre}"
    
    def __repr__(self) -> str: #Método para representar el objeto de manera formal, mostrando su tipo y atributos principales
        return f"Item(nombre={self.nombre}, tipo={self.tipo}, valor={self.valor})"
    
    def __str__(self) -> str: #Método para representar el objeto como una cadena de texto, mostrando su nombre, tipo y valor
        return f"{self.nombre} | {self.tipo} | {self.valor}"

#Inventario
class Inventario:
    def __init__(self):
        self.items: list[Item] = [] #Composición: Inventario contiene una lista de items, cada item es un objeto de la clase Item
    
    def agregar_items(self, item: Item):
        if len(self.items) < 5:
            self.items.append(item)
            print(f"{item.nombre} ha sido agregado al inventario")
        else:
            print("El inventario está lleno, no puedes agregar más items")

    def usar_item(self, indice: int, dios: Dios) -> str:
        if 0 <= indice < len(self.items):
            item = self.items.pop(indice)
            return item.usar(dios)
        else:
            return("Índice inválido, no se pudo usar el item")

    def eliminar_item(self, indice: int) -> str:
        if 0 <= indice < len(self.items):
            eliminado = self.items.pop(indice)
            print(f"{eliminado.nombre} ha sido eliminado del inventario")
        else:
            print("Índice inválido, no se pudo eliminar el item")
    
    def mostrar_inventario(self) -> None:
        if not self.items:
            print("El inventario está vacío")
            return
        print("Inventario:")
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item}")
    
    def __len__(self): #Método mágico para obtener la cantidad de items en el inventario
        return len(self.items)
    
    def __str__(self): #Método mágico para representar el inventario como una cadena de texto, mostrando la cantidad de items y su descripción
        if not self.items:
            return "Inventario vacío"
        
        texto = "Inventario:\n"
        for i, item in enumerate(self.items, start=1):
            texto += f"{i}. {item}\n"
        return texto.n ()
    
    def __repr__(self): #Método mágico para representar el objeto de manera formal, mostrando su tipo y la lista de items que contiene
        return f"Inventario(items={self.items})"
    
    
#Jugador
class Jugador: #Nueva clase para representar al jugador, que tiene un nombre, un dios seleccionado, un nivel, un score, una cantidad de victorias y un inventario de items
    def __init__(self, nombre_jugador: str, dios: Dios, nivel: int = 1, score: int = 0, victorias: int = 0) -> None: #Metodo constructor para inicializar los atributos del jugador
        self.nombre_jugador = nombre_jugador
        self.dios = dios
        self.nivel = nivel
        self.score = score
        self.victorias = victorias
        self.inventario = Inventario() #Composición: el jugador tiene un inventario que puede contener items
    
    def subir_nivel(self) -> str | None: #Método para subir de nivel, cada vez que el jugador sube de nivel, su dios mejora sus atributos y se restaura su vida y maná, el nivel máximo es 10
        if self.nivel <10:
            self.nivel += 1
            self.dios.vida_maxima += 20
            self.dios.ataque += 10
            self.dios.defensa += 5
            self.dios.mana_maximo += 20
            self.dios.vida = self.dios.vida_maxima  
            return f"¡Felicidades {self.nombre_jugador}, has subido al nivel {self.nivel}!"
    
    def actualizar_score(self, puntos: int): #Método para actuzalizar el score del jugador
        self.score += puntos
        if self.score < 0:
            self.score = 0
        return self.score

    def to_dict(self) -> dict: #Método para convertir el objeto jugador en un diccionario, para poder guardarlo en un archivo JSON
        return {
            "nombre_jugador": self.nombre_jugador,
            "nivel": self.nivel,
            "score": self.score,
            "victorias": self.victorias,
            "inventario": [item.nombre 
            for item in self.inventario.items]
        }

    def __repr__(self) -> str: #Método mágico para representar el objeto de manera formal, mostrando su tipo y atributos principales
        return (f"Jugador(nombre_jugador={self.nombre_jugador}, nivel={self.nivel}, score={self.score}," 
                f"victorias={self.victorias}, inventario={self.inventario})")
    
    def __str__(self) -> str: #Método mágico para representar el objeto como una cadena de texto
        return (f"Jugador: {self.nombre_jugador} | Nivel: {self.nivel} | Score: {self.score} | "
                f"Victorias: {self.victorias} | Inventario: {self.inventario}")
    
class GestorPuntajes: #Nueva clase para gestionar los puntajes de los jugadores, guardando su progreso en un archivo JSON y mostrando el top 10 de jugadores con mejor score
    def __init__(self, archivo: str = "puntajes.json"): #Metodo constructor para inicializar el atributo archivo y cargar los puntajes desde el archivo JSON
        self.archivo = archivo
        self.tabla = self.cargar()

    def cargar(self) -> list[dict]: #Método para cargar los puntajes desde el archivo JSON, si el archivo no existe o no se puede leer, devuelve una lista vacía
        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except:
            return []

    def guardar(self, jugador: Jugador) -> None: #Método para guardar los puntajes del jugador en el archivo JSON
        for j in self.tabla: #Buscar si el jugador ya existe en la tabla, si existe, actualizar su nivel, score, victorias e inventario si es mayor que el registrado, si no existe, agregarlo a la tabla
            if j["nombre_jugador"] == jugador.nombre_jugador:
                j["nivel"] = max(j["nivel"], jugador.nivel)
                j["score"] = max(j["score"], jugador.score)
                j["victorias"] = max(j["victorias"], jugador.victorias)
                j["inventario"] = [item.nombre for item in jugador.inventario.items]
                break
        else:
            self.tabla.append(jugador.to_dict()) 
        with open(self.archivo, "w", encoding="utf-8") as archivo: #Guardar la tabla de puntajes actualizada en el archivo JSON, utilizando la función json.dump para escribir la lista de diccionarios en el archivo con una indentación de 4 espacios para mejorar su legibilidad
            json.dump(self.tabla, archivo, indent=4)

    def ordenar_score_desc(self) -> list[dict]: #Método para ordenar la tabla de puntajes por nivel de forma descendente, utilizando una función lambda como clave de ordenamiento
        return sorted(self.tabla, key=lambda x: x["score"], reverse=True)

    def mostrar_top10(self) -> None: #Método para mostrar el top 10 de jugadores con mejor score, ordenando la tabla por nivel de forma descendente y mostrando solo los primeros 10 jugadores
        print("Top 10 Jugadores:")

        for i, jugador in enumerate(self.ordenar_score_desc()[:10], start=1): #Enumerar la lista de jugadores ordenada por score de forma descendente
            print(f"{i}. {jugador['nombre_jugador']} - Score: {jugador['score']} - Nivel: {jugador['nivel']} -" 
                  f"Victorias: {jugador['victorias']}")
    
    def __repr__(self) -> str: #Método mágico para representar el objeto de manera formal, mostrando su tipo y atributos principales
        return f"GestorPuntajes(archivo={self.archivo}, tabla={self.tabla})"
    
    def __str__(self) -> str: #Método mágico para representar el objeto como una cadena de texto, mostrando el nombre del archivo y la cantidad de jugadores registrados en la tabla
        return f"Gestor de Puntajes - Archivo: {self.archivo} | Total Jugadores: {len(self.tabla)}"

#Maquina
class Maquina: #Nueva clase para representar a la máquina que genera los enemigos de forma aleatoria durante el combate
    def obtener_enemigo(self) -> Criatura: #Método para obtener un enemigo de forma aleatoria, utilizando la función random.choice para seleccionar una criatura de la lista de criaturas disponibles
        return random.choice([Minotauro(), Medusa(), Ciclope(), Hidra(), Escila()])
    def __repr__(self) -> str: #Método mágico para representar el objeto de manera formal, mostrando su tipo
        return f"Maquina()"
    def __str__(self) -> str: #Método mágico para representar el objeto como una cadena de texto
        return "Máquina Generadora de Enemigos"
    
class MotorCombate: #Nueva clase para representar el motor de combate, que se encarga de ejecutar la lógica del juego, manejando los turnos de ataque entre el jugador y la máquina, y actualizando el estado del jugador después de cada combate
    def __init__(self, jugador: Jugador, maquina: Maquina, gestor: GestorPuntajes) -> None:
        self.jugador = jugador
        self.maquina = maquina
        self.gestor = gestor
        self.max_combates = 10
        self.combates_realizados = 0

    def generar_item_random(self) -> Item: #Método para generar un item de forma aleatoria, utilizando la función random.choice para seleccionar un item de la lista de items disponibles
        posibles= [Item("Poción", "Curación", 75), 
                   Item("Cristal de maná", "Maná", 50),
                   Item("Espada de divina", "Ataque", 25),]
        return random.choice(posibles)
    
    def combate(self, dios: Dios, criatura: Criatura) -> bool: #Método para ejecutar el combate entre el jugador y la máquina, manejando los turnos de ataque y actualizando el estado del jugador después de cada acción
        turno = 1
        while dios.esta_vivo() and criatura.esta_vivo():
            print (f"\n Turno #{turno}")
            print(f"{dios} vs {criatura}")
            print(f"{dios.nombre} - Vida: {dios.vida}/{dios.vida_maxima} | Maná: {dios.mana}")
            print(f"{criatura.nombre} - Vida: {criatura.vida}/{criatura.vida_maxima}")
            turno += 1

            try: 
                accion_dios = input("¿Qué ataque hará el Dios: \n (1) Atacar  \n (2) Usar poder \n (3) Usar item \n Ingresa el numero: ")
            except: 
                print("Entrada invalida")
                continue

            if accion_dios == "1":
                _, daño, critico = dios.atacar(criatura)
                daño_real = criatura.recibir_daño(daño)
                print(f"{dios.nombre} hizo {daño_real} de daño")
                if critico:
                    print("GOLPE CRITICO x2")

            elif accion_dios == "2":
                daño = dios.usar_habilidad()
                daño_real = criatura.recibir_daño(daño)
                print (f"{dios.nombre} usó su habilidad {dios.poder_especial} e hizo {daño_real} de daño")
            
            elif accion_dios == "3":
                print (self.jugador.inventario)
                if len(self.jugador.inventario) > 0:
                    try:
                        opcion = int(input("Selecciona el número del item que deseas usar: "))
                        self.jugador.inventario.usar_item(opcion - 1, dios)
                    except (ValueError, IndexError):
                        print("Opción inválida")
                        continue
                else:
                    print("Accion invalida")
                    continue
            else: 
                print("Accion incorrecta")
                continue

            if criatura.esta_vivo():
                accion_criatura = random.choice(["atacar", "habilidad"])

                if accion_criatura == "atacar":
                    _, daño, critico = criatura.atacar(dios)
                    daño_real = dios.recibir_daño(daño)
                    print(f"{criatura.nombre} hizo {daño_real} de daño")

                    if critico:
                        print("GOLPE CRITICO x2")

                else:
                    daño = criatura.usar_habilidad()
                    daño_real = dios.recibir_daño(daño)
                    print (f"{criatura.nombre} usó su habilidad {criatura.habilidad} e hizo {daño_real} de daño")

        return dios.esta_vivo()
            
    def ejecutar_partida(self): #Método para ejecutar la partida completa, manejando los combates entre el jugador y la máquina, y actualizando el estado del jugador después de cada combate
        while self.combates_realizados < self.max_combates:
            print(f"\n Combate #{self.combates_realizados + 1   } ")
            self.jugador.dios.vida = self.jugador.dios.vida_maxima #Restaurar la vida del dios al máximo después de cada combate
            self.jugador.dios.mana = self.jugador.dios.mana_maximo #Restaurar el maná del dios al máximo después de cada combate
            enemigo = self.maquina.obtener_enemigo()
            victoria = self.combate(self.jugador.dios, enemigo)
            self.combates_realizados += 1

            if victoria: 
                print("GANASTE EL COMBATE")
                self.jugador.victorias += 1
                mensaje = self.jugador.subir_nivel()

                if mensaje:
                    print(mensaje)

                puntos = int((enemigo.vida_maxima + enemigo.ataque) * enemigo.multiplicador)
                self.jugador.actualizar_score(puntos)

                print(f"Has ganado {puntos} puntos. Score actual: {self.jugador.score}")

                if self.jugador.nivel % 3 == 0:
                    item_ganado = self.generar_item_random()
                    self.jugador.inventario.agregar_items(item_ganado)
                    print(f"¡Has ganado un nuevo item: {item_ganado.nombre}!")

            else:
                print("PERDISTE EL COMBATE")
                print("GAME OVER")

                puntos = int((enemigo.vida_maxima + enemigo.ataque) * enemigo.multiplicador * 0.5)
                self.jugador.actualizar_score(-puntos)

                print(f"Has perdido {puntos} puntos. Score actual: {self.jugador.score}")
                break

            print(f"Estado actual del jugador: {self.jugador}")

        if self.combates_realizados == self.max_combates:
            print("¡Felicidades, has completado todos los combates!")

        print("\n¡Partida finalizada!")
        self.gestor.guardar(self.jugador)
        self.gestor.mostrar_top10()
        print(f"Total de seres míticos creados durante esta partida: {SerMitico.total_creados()}") #Uso de @classmethod para mostrar el total de seres miticos
        print(f"Gracias por jugar, {self.jugador.nombre_jugador}. Tu puntaje final es: {self.jugador.score}")
        def __repr__(self) -> str: #Método mágico para representar el objeto de manera formal, mostrando su tipo y atributos principales
            return f"MotorCombate(jugador={self.jugador}, maquina={self.maquina}, gestor={self.gestor})"
        def __str__(self) -> str: #Método mágico para representar el objeto como una cadena de texto, mostrando el estado actual del jugador y la cantidad de combates realizados
            return (f"Motor de Combate - Jugador: {self.jugador.nombre_jugador} | Combates Realizados: {self.combates_realizados} | "
                    f"Estado del Jugador: {self.jugador}")

#Main
if __name__ == "__main__": #Punto de entrada del programa, donde se inicializa el gestor de puntajes, se muestra el top 10 de jugadores, se solicita al usuario que seleccione su dios y se inicia la partida
    gestor = GestorPuntajes()
    print("MITOLOGIA GRIEGA - JUEGO DE COMBATE")
    gestor.mostrar_top10()
    while True:
        print("¡Bienvenido al Juego de Mitología Griega! Selecciona tu Dios para comenzar la aventura: ")
        try:
            opcion = int(input("1. Zeus \n2. Ares \n3. Poseidon \n4. Hades \n5. Atenea \nIngresa el numero de tu elección: "))
        except ValueError:
            print("Entrada inválida")
            continue

        if opcion == 1:
            dios = Zeus()

        elif opcion == 2:
            dios = Ares()

        elif opcion == 3:
            dios = Poseidon()

        elif opcion == 4:
            dios = Hades()

        elif opcion == 5:
            dios = Atenea()

        else:
            print("Opción inválida")
            continue

        nombre = input("Ingresa tu nombre de jugador: ")
        jugador = Jugador(nombre_jugador=nombre, dios=dios)
        item_inicial = Item("Poción de Inicio", "Curación", 50)
        jugador.inventario.agregar_items(item_inicial)

        print(f"¡Bienvenido {jugador.nombre_jugador}! Has seleccionado a {jugador.dios.nombre} como tu Dios y comienzas con {item_inicial.nombre}. "
              f"¡Buena suerte en tu aventura!")
        maquina = Maquina()
        
        motor = MotorCombate(jugador, maquina, gestor)
        motor.ejecutar_partida()
        break
