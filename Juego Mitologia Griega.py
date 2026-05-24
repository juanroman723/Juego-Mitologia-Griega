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
    
    # ── Layout ──────────────────────────────
    def _build(self):
        # Encabezado
        top = tk.Frame(self, bg=BG_PANEL,
                       highlightthickness=1, highlightbackground=BORDER)
        top.pack(fill="x", padx=0, pady=0)
 
        self.lbl_titulo = tk.Label(top, text="", bg=BG_PANEL,
                                   fg=GOLD, font=("Georgia", 13, "bold"))
        self.lbl_titulo.pack(side="left", padx=20, pady=8)
 
        self.lbl_score = tk.Label(top, text="", bg=BG_PANEL,
                                  fg=GOLD_DIM, font=("Georgia", 10))
        self.lbl_score.pack(side="right", padx=20)
 
        # Arena (barras de HP/maná + log)
        arena = tk.Frame(self, bg=BG_DARK)
        arena.pack(fill="both", expand=True, padx=16, pady=8)
 
        # Columna izquierda: stats jugador
        self.panel_jugador = self._panel_stats(arena, lado="jugador")
        self.panel_jugador.pack(side="left", fill="y", padx=(0,8))
 
        # Centro: log de batalla
        centro = tk.Frame(arena, bg=BG_PANEL,
                          highlightthickness=1, highlightbackground=BORDER)
        centro.pack(side="left", fill="both", expand=True)
 
        tk.Label(centro, text="— Crónica de Batalla —",
                 bg=BG_PANEL, fg=GOLD_DIM,
                 font=("Georgia", 9, "italic")).pack(pady=(6,2))
 
        self.log = tk.Text(centro, bg=BG_PANEL, fg=TEXT_WHITE,
                           font=("Courier", 9), relief="flat",
                           state="disabled", wrap="word",
                           highlightthickness=0, bd=0)
        self.log.pack(fill="both", expand=True, padx=8, pady=(0,8))
 
        sb = tk.Scrollbar(centro, command=self.log.yview, bg=BG_PANEL)
        sb.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=sb.set)
 
        # Columna derecha: stats enemigo
        self.panel_enemigo = self._panel_stats(arena, lado="enemigo")
        self.panel_enemigo.pack(side="right", fill="y", padx=(8,0))
 
        # Acciones
        self._build_acciones()
 
    def _panel_stats(self, parent, lado):
        f = tk.Frame(parent, bg=BG_CARD, width=190,
                     highlightthickness=1, highlightbackground=BORDER)
        f.pack_propagate(False)
 
        tag = lado
        tk.Label(f, text="JUGADOR" if lado=="jugador" else "ENEMIGO",
                 bg=BG_CARD, fg=GOLD_DIM,
                 font=("Georgia", 8, "bold")).pack(pady=(10,2))
 
        setattr(self, f"lbl_nombre_{tag}",
                tk.Label(f, text="—", bg=BG_CARD, fg=GOLD,
                         font=("Georgia", 12, "bold")))
        getattr(self, f"lbl_nombre_{tag}").pack()
 
        setattr(self, f"lbl_poder_{tag}",
                tk.Label(f, text="", bg=BG_CARD, fg=TEXT_DIM,
                         font=("Georgia", 8, "italic"), wraplength=170))
        getattr(self, f"lbl_poder_{tag}").pack(pady=(0,6))
 
        # HP bar
        tk.Label(f, text="❤  VIDA", bg=BG_CARD, fg=RED_HP,
                 font=("Georgia", 9, "bold")).pack(anchor="w", padx=12)
        setattr(self, f"bar_hp_{tag}", self._barra(f, RED_HP))
        setattr(self, f"lbl_hp_{tag}",
                tk.Label(f, text="", bg=BG_CARD, fg=TEXT_DIM,
                         font=("Courier", 9)))
        getattr(self, f"lbl_hp_{tag}").pack()
 
        if lado == "jugador":
            tk.Label(f, text="◈  MANÁ", bg=BG_CARD, fg=BLUE_MANA,
                     font=("Georgia", 9, "bold")).pack(anchor="w", padx=12, pady=(8,0))
            self.bar_mana = self._barra(f, BLUE_MANA)
            self.lbl_mana = tk.Label(f, text="", bg=BG_CARD, fg=TEXT_DIM,
                                     font=("Courier", 9))
            self.lbl_mana.pack()
 
        tk.Label(f, text="", bg=BG_CARD).pack(pady=4)
 
        for stat in (("⚔ ATK", "atk"), ("🛡 DEF", "def")):
            row = tk.Frame(f, bg=BG_CARD)
            row.pack(fill="x", padx=12, pady=1)
            tk.Label(row, text=stat[0], bg=BG_CARD, fg=TEXT_DIM,
                     font=("Georgia", 9)).pack(side="left")
            setattr(self, f"lbl_{stat[1]}_{tag}",
                    tk.Label(row, text="—", bg=BG_CARD, fg=TEXT_WHITE,
                             font=("Georgia", 9, "bold")))
            getattr(self, f"lbl_{stat[1]}_{tag}").pack(side="right")
 
        return f
 
    def _barra(self, parent, color):
        cont = tk.Frame(parent, bg=BORDER, height=10)
        cont.pack(fill="x", padx=12, pady=2)
        cont.pack_propagate(False)
        fill = tk.Frame(cont, bg=color, height=10)
        fill.place(x=0, y=0, relheight=1.0, relwidth=1.0)
        return fill
    def _build_acciones(self):
        bot = tk.Frame(self, bg=BG_PANEL,
                       highlightthickness=1, highlightbackground=BORDER)
        bot.pack(fill="x", padx=0, pady=0, side="bottom")
 
        btns = tk.Frame(bot, bg=BG_PANEL)
        btns.pack(pady=10)
 
        self.btn_atacar  = gold_btn(btns, "⚔  Atacar",     self._accion_atacar,  14)
        self.btn_poder   = gold_btn(btns, "✨  Usar Poder", self._accion_poder,   16)
        self.btn_item    = gold_btn(btns, "🎒  Usar Ítem",  self._abrir_inventario, 14)
 
        self.btn_atacar.pack(side="left", padx=8)
        self.btn_poder.pack(side="left",  padx=8)
        self.btn_item.pack(side="left",   padx=8)
 
    # ── Lógica de combate ───────────────────
    def _nuevo_combate(self):
        if self.combates >= self.MAX_COMBATES:
            self._fin_partida(completa=True)
            return
        self.combates += 1
        self.turno = 1
        self.dios.vida = self.dios.vida_maxima
        self.dios.mana = self.dios.mana_maximo
        self.enemigo = random.choice(CRIATURAS_LISTA)()
        self.en_combate = True
        self._set_botones(True)
        self.lbl_titulo.config(
            text=f"Combate #{self.combates}/{self.MAX_COMBATES}  ·  Nivel {self.jugador.nivel}  ·  {self.jugador.nombre_jugador}")
        self._actualizar_score()
        self._actualizar_stats()
        self._log(f"\n{'═'*38}", GOLD_DIM)
        self._log(f"  COMBATE #{self.combates}: {self.dios.nombre} vs {self.enemigo.nombre}", GOLD)
        self._log(f"{'═'*38}\n", GOLD_DIM)
 
    def _actualizar_stats(self):
        d = self.dios
        e = self.enemigo
 
        self.lbl_nombre_jugador.config(text=d.nombre)
        self.lbl_poder_jugador.config(text=d.poder_especial)
        self.lbl_hp_jugador.config(text=f"{d.vida} / {d.vida_maxima}")
        self.lbl_atk_jugador.config(text=str(d.ataque))
        self.lbl_def_jugador.config(text=str(d.defensa))
        self.lbl_mana.config(text=f"{d.mana} / {d.mana_maximo}")
        self._set_barra(self.bar_hp_jugador, d.vida, d.vida_maxima)
        self._set_barra(self.bar_mana, d.mana, d.mana_maximo)
 
        if e:
            self.lbl_nombre_enemigo.config(text=e.nombre)
            self.lbl_poder_enemigo.config(text=e.habilidad)
            self.lbl_hp_enemigo.config(text=f"{e.vida} / {e.vida_maxima}")
            self.lbl_atk_enemigo.config(text=str(e.ataque))
            self.lbl_def_enemigo.config(text=str(e.defensa))
            self._set_barra(self.bar_hp_enemigo, e.vida, e.vida_maxima)
 
    def _set_barra(self, bar, actual, maximo):
        pct = max(0.0, min(1.0, actual / maximo)) if maximo else 0
        bar.place(relwidth=pct)
 
    def _actualizar_score(self):
        self.lbl_score.config(
            text=f"Score: {self.jugador.score}  |  Victorias: {self.jugador.victorias}")
 
    def _log(self, msg, color=TEXT_WHITE):
        self.log.configure(state="normal")
        tag = f"c{color}"
        self.log.tag_configure(tag, foreground=color)
        self.log.insert("end", msg + "\n", tag)
        self.log.configure(state="disabled")
        self.log.see("end")
 
    def _set_botones(self, estado):
        s = "normal" if estado else "disabled"
        for b in (self.btn_atacar, self.btn_poder, self.btn_item):
            b.configure(state=s)
 
    # ── Acciones del jugador ────────────────
    def _accion_atacar(self):
        if not self.en_combate: return
        self._log(f"\n── Turno #{self.turno} ──", GOLD_DIM)
        _, daño, critico = self.dios.atacar(self.enemigo)
        real = self.enemigo.recibir_daño(daño)
        msg = f"  {self.dios.nombre} ataca → {real} daño"
        if critico: msg += "  ⚡ CRÍTICO x2"
        self._log(msg, GOLD_LIGHT if critico else TEXT_WHITE)
        self._actualizar_stats()
        self._turno_enemigo()
 
    def _accion_poder(self):
        if not self.en_combate: return
        self._log(f"\n── Turno #{self.turno} ──", GOLD_DIM)
        daño = self.dios.usar_habilidad()
        if daño == 0:
            self._log(f"  ✗ Maná insuficiente para {self.dios.poder_especial}", RED_HP)
            return
        real = self.enemigo.recibir_daño(daño)
        self._log(f"  {self.dios.nombre} usa {self.dios.poder_especial} → {real} daño", GOLD)
        self._actualizar_stats()
        self._turno_enemigo()
 
    def _turno_enemigo(self):
        self.turno += 1
        if not self.enemigo.esta_vivo():
            self._victoria()
            return
 
        accion = random.choice(["atacar", "habilidad"])
        if accion == "atacar":
            _, daño, critico = self.enemigo.atacar(self.dios)
            real = self.dios.recibir_daño(daño)
            msg = f"  {self.enemigo.nombre} contraataca → {real} daño"
            if critico: msg += "  ⚡ CRÍTICO x2"
            self._log(msg, "#e07070" if not critico else RED_HP)
        else:
            daño = self.enemigo.usar_habilidad()
            real = self.dios.recibir_daño(daño)
            self._log(f"  {self.enemigo.nombre} usa {self.enemigo.habilidad} → {real} daño", "#e07070")
 
        self._actualizar_stats()
 
        if not self.dios.esta_vivo():
            self._derrota()
 
    def _victoria(self):
        self.en_combate = False
        self._set_botones(False)
        self.jugador.victorias += 1
        puntos = int((self.enemigo.vida_maxima + self.enemigo.ataque) * self.enemigo.multiplicador)
        self.jugador.actualizar_score(puntos)
        self._log(f"\n  ✦ VICTORIA — +{puntos} pts", GREEN_WIN)
 
        msg = self.jugador.subir_nivel()
        if msg: self._log(f"  {msg}", GOLD)
 
        if self.jugador.nivel % 3 == 0:
            item = random.choice([
                Item("Poción", "Curación", 75),
                Item("Cristal de maná", "Maná", 50),
                Item("Espada Divina", "Ataque", 25),
            ])
            ok = self.jugador.inventario.agregar(item)
            if ok:
                self._log(f"  🎁 Obtuviste: {item.nombre}", GOLD_LIGHT)
 
        self._actualizar_score()
        self.after(1400, self._nuevo_combate)
 
    def _derrota(self):
        self.en_combate = False
        self._set_botones(False)
        puntos = int((self.enemigo.vida_maxima + self.enemigo.ataque) * self.enemigo.multiplicador * 0.5)
        self.jugador.actualizar_score(-puntos)
        self._log(f"\n  ✗ DERROTA — -{puntos} pts", RED_HP)
        self._log("  ═══════  GAME OVER  ═══════", RED_HP)
        self._actualizar_score()
        self.after(2000, self._fin_partida)
 
    def _fin_partida(self, completa=False):
        self.master.gestor.guardar(self.jugador)
        if completa:
            self._log("\n  🏆 ¡Completaste todos los combates!", GOLD)
        self.master.mostrar_top10(self.jugador)
 
    # ── Inventario popup ────────────────────
    def _abrir_inventario(self):
        if not self.en_combate: return
        inv = self.jugador.inventario
        if not inv.items:
            self._log("  ✗ Inventario vacío", TEXT_DIM)
            return
 
        win = tk.Toplevel(self, bg=BG_CARD)
        win.title("Inventario")
        win.geometry("320x280")
        win.resizable(False, False)
        win.grab_set()
 
        tk.Label(win, text="─── Inventario ───", bg=BG_CARD,
                 fg=GOLD, font=("Georgia", 12, "bold")).pack(pady=(14,6))
 
        for i, item in enumerate(inv.items):
            row = tk.Frame(win, bg=BG_CARD)
            row.pack(fill="x", padx=20, pady=3)
            tk.Label(row, text=str(item), bg=BG_CARD, fg=TEXT_WHITE,
                     font=("Courier", 10), anchor="w").pack(side="left", expand=True)
            def usar(idx=i, w=win):
                msg = self.jugador.inventario.usar_item(idx, self.dios)
                self._log(f"  {msg}", GOLD_LIGHT)
                self._actualizar_stats()
                w.destroy()
            tk.Button(row, text="Usar", command=usar,
                      bg=GOLD_DIM, fg=BG_DARK,
                      font=("Georgia", 9, "bold"),
                      relief="flat", padx=8, pady=2,
                      cursor="hand2").pack(side="right")
 
        gold_btn(win, "Cerrar", win.destroy, 12).pack(pady=12)
 
 
# ─────────────────────────────────────────────
#  PANTALLA TOP 10
# ─────────────────────────────────────────────
class PantallaTop10(tk.Frame):
    def __init__(self, master: App, jugador):
        super().__init__(master, bg=BG_DARK)
        self.master  = master
        self.jugador = jugador
        self._build()
 
    def _build(self):
        tk.Label(self, text="🏆  TABLA DE HONOR  🏆",
                 bg=BG_DARK, fg=GOLD,
                 font=("Georgia", 22, "bold")).pack(pady=(30,4))
        tk.Label(self, text="— Los guerreros más gloriosos —",
                 bg=BG_DARK, fg=GOLD_DIM,
                 font=("Georgia", 11, "italic")).pack(pady=(0,16))
        sep(self)
 
        tabla = tk.Frame(self, bg=BG_DARK)
        tabla.pack(padx=80, fill="x")
 
        headers = ["#", "Guerrero", "Score", "Nivel", "Victorias"]
        widths   = [4, 20, 10, 8, 10]
        for col, (h, w) in enumerate(zip(headers, widths)):
            tk.Label(tabla, text=h, bg=BG_DARK, fg=GOLD_DIM,
                     font=("Georgia", 10, "bold"),
                     width=w, anchor="w").grid(row=0, column=col, padx=4, pady=4)
 
        top = self.master.gestor.top10()
        medalles = ["🥇", "🥈", "🥉"]
 
        for i, j in enumerate(top):
            bg = BG_CARD if i % 2 == 0 else BG_PANEL
            medal = medalles[i] if i < 3 else f" {i+1}."
            es_actual = self.jugador and j["nombre_jugador"] == self.jugador.nombre_jugador
            color = GOLD if es_actual else TEXT_WHITE
 
            vals = [medal, j["nombre_jugador"], j["score"], j["nivel"], j["victorias"]]
            for col, (val, w) in enumerate(zip(vals, widths)):
                tk.Label(tabla, text=str(val), bg=bg, fg=color,
                         font=("Courier", 10),
                         width=w, anchor="w").grid(row=i+1, column=col,
                                                    padx=4, pady=2, sticky="w")
 
        if not top:
            tk.Label(tabla, text="(Sin registros aún)", bg=BG_DARK,
                     fg=TEXT_DIM, font=("Georgia", 11, "italic")).grid(
                row=1, column=0, columnspan=5, pady=20)
 
        sep(self)
 
        if self.jugador:
            tk.Label(self, text=f"Partida finalizada  ·  {self.jugador.nombre_jugador}  ·  "
                                f"Score: {self.jugador.score}  ·  Victorias: {self.jugador.victorias}",
                     bg=BG_DARK, fg=TEXT_DIM,
                     font=("Georgia", 10, "italic")).pack(pady=6)
 
        btns = tk.Frame(self, bg=BG_DARK)
        btns.pack(pady=16)
        gold_btn(btns, "⚡  Jugar de nuevo", self.master.mostrar_menu, 18).pack(side="left", padx=10)
        gold_btn(btns, "✕  Salir",          self.master.destroy,      12).pack(side="left", padx=10)
 
 
# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
 