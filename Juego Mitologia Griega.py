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

#GUI
class App (tk.Tk): #Nueva clase para representar la aplicación gráfica del juego, utilizando la librería tkinter para crear la interfaz de usuario
    def __init__(self):
        super().__init__()
        self.title("Juego de Mitología Griega")
        self.geometry("900x680")
        self.configure(bg=BG_DARK)
        self.resizable(False, False)
        self.gestor = GestorPuntajes()
        self.__frameactual = None
        self.mostrar_menu()
    
    def cambiar_frame(self, nuevo_frame):
        if self.__frameactual:
            self.__frameactual.destroy()
        self.__frameactual = nuevo_frame
        self.__frameactual.pack(fill="both", expand=True)

    def mostrar_menu(self):
        self.cambiar_frame(PantallaMenu(self))
    
    def iniciar_partida(self, nombre, dios):
        jugador = Jugador(nombre_jugador=nombre, dios=dios)
        item_inicial = Item("Poción de Inicio", "Curación", 50)
        jugador.inventario.agregar_items(item_inicial)
        self.cambiar_frame(PantallaCombate(self, jugador))

#Helpers de Estilo
def label (parent, text, size = 11, color = TEXT_WHITE, bold=False, italic=False):
    weight = "bold" if bold else "normal"
    slant = "italic" if italic else "roman"
    return tk.Label(parent, text=text, bg=parent["bg"] if hasattr(parent,"_w",) else BG_DARK, fg=color, font=("Georgia", size, weight, slant))

def sep (parent, color=GOLD_DIM):
    f = tk.Frame(parent, bg=color, height=1)
    f.pack(fill="x", padx=20, padx=6)
    return f

def gold_btn(parent, text, cmd, width=18):
    b = tk.Button(parent, text = text, command = cmd, bg = BG_CARD, fg= GOLD, activebackground= GOLD_DIM, 
                  activeforeground=BG_DARK, relief="flat", font=("Georgia", 10, "bold"), bd=0, padx=14, pady=8, width=width,
                  highlightthickness=1, highlightbackground=GOLD_DIM, cursor="hand2")
    return b

# Menu principal
DIOSES_INFO = {
    "Zeus": ("Rayo Divino", "100 HP | 70 ATQ | 25 DEF| 200 MANA"),
    "Ares": ("Furia de Guerra", "130 HP | 65 ATQ | 40 DEF| 150 MANA"),
    "Poseidon": ("Oleada Marina", "120 HP | 75 ATQ | 30 DEF| 180 MANA"),
    "Hades": ("Sombra del Inframundo", "110 HP | 80 ATQ | 35 DEF| 160 MANA"),
    "Atenea": ("Escudo de Sabiduría", "90 HP | 60 ATQ | 50 DEF| 170 MANA")
}

DIOSES_CLASES = {
    "Zeus": Zeus,
    "Ares": Ares,
    "Poseidon": Poseidon,
    "Hades": Hades,
    "Atenea": Atenea
}

class PantallaMenu(tk.Frame): #Nueva clase para representar la pantalla del menú principal, donde el jugador puede seleccionar su dios y comenzar la partida
    def __init__(self, master: App):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self._seleccion = tk.StringVar(value="Zeus")
        self.build()
    
    def build(self):
        tk.Label(self, text="JUEGO DE MITOLOGÍA GRIEGA", bg=BG_DARK, fg=GOLD, font=("Georgia", 26, "bold")).pack(pady=(30, 4))
        tk.Label(self, text="- JUEGO DE COMBATE -", bg=BG_DARK, fg=GOLD_DIM, font=("Georgia", 12, "italic")).pack(pady=(0, 16))
    sep(self)

    mid = tk.Frame(self, bg=BG_DARK)
    mid.pack = (fill="x", padx=60)

    tk.Label(mid, text="Nombre del guerrero", bg = BG_DARK, fg=TEXT_DIM, font=("Georgia", 10, "italic")).pack(anchor="w", pady=(10, 2))
    self._entry_nombre = tk.Entry(mid, font=("Georgia",13), bg=BG_CARD, fg=TEXT_WHITE, insertbackground=GOLD, relief="flat", bd=6)
    self._entry_nombre.pack(fill="x", ipady=6)
    sep(self)

    tk.Label(self,text="Elige tu Dios", bg=BG_DARK, fg=GOLD, font=("Georgia", 13, "bold")).pack(pady=(8,10))

    grid = tk.Frame(self, bg=BG_DARK)
    grid.pack()

    self._info_label = tk.Label(self, text="", bg=BG_DARK, fg=TEXT_DIM, font=("Georgia", 10, "italic"))
    self._info_label.pack(pady=6)

    for nombre, (icono, poder, stats) in DIOSES_INFO.items():
        self._card_dios(grid, nombre, icono, poder, stats)

    self._seleccion.set("Zeus")
    self._actualizar_info("Zeus")
    sep(self)

    btns = tk.Frame(self, bg=BG_DARK)
    btns.pack(pady=14)

    gold_btn(btns, "VER TOP 10", self._ver_top10, width=16).pack(side="left", padx=10)
    gold_btn(btns, "Comenzar Partida", self._comenzar, width=20).pack(side="left", padx=10)

    def _card_dios(self, parent, nombre, icono, poder, stats):
        var= self._seleccion
        col = BG_CARD

        frame = tk.Frame(parent, bg=col, bd=0, highlightthickness=1, highlightbackground=GOLD_DIM, cursor="hand2")
        frame.pack(side="left", padx=8, pady=4, ipadx=10, ipady=8)

        tk.Label(frame, text=icono, bg=col, font=("", 22)),pack()
        tk.Label(frame, text=nombre, bg=col, fg=GOLD, font=("Georgia", 10, "bold")).pack()

        def select():
            var.set(nombre)
            self._actualizar_info(nombre)
            for w in parent.winfo_children():
                w.configure(highlightbackground=GOLD_DIM)
            frame.configure(highlightbackground=GOLD, highlightthickness=2)
    
        frame.bind("<Button-1>", lambda e: select())
        for child in frame.winfo_children():
            child.bind("<Button-1>", lambda e:select())

    def _actualizar_info(self, nombre):
        icono, poder, stats = DIOSES_INFO[nombre]
        self._info_label.config(text=f"{icono} {nombre} | {poder} | {stats} | (+/- variacion aleatoria)")
    
    def comenzar(self):
        nombre = self._entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("ATENCION", "INGRESA TU NOMBRE")
            return
        dios_cls = DIOSES_CLASES[self._seleccion.get()]
        self.master.iniciar_partida(nombre, dios_cls())
    
    def _ver_top10(self):
        self.master.mostrar_top10(None)
        
#PANTALLA COMBATE
CRIATURAS_LISTA = [Minotauro, Medusa, Ciclope, Hidra, Escila]
 
class PantallaCombate(tk.Frame):
    MAX_COMBATES = 10
 
    def __init__(self, master: App, jugador: Jugador):
        super().__init__(master, bg=BG_DARK)
        self.master   = master
        self.jugador  = jugador
        self.dios     = jugador.dios
        self.combates = 0
        self.turno    = 1
        self.enemigo  = None
        self.en_combate = False
        self._build()
        self._nuevo_combate()