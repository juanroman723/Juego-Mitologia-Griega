from __future__ import annotations
from abc import ABC, abstractmethod
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont

# ─────────────────────────────────────────────
#  COLORES Y ESTILOS
# ─────────────────────────────────────────────
BG_DARK    = "#0d0d0d"
BG_PANEL   = "#1a1610"
BG_CARD    = "#211e14"
GOLD       = "#c9a84c"
GOLD_LIGHT = "#e8c96e"
GOLD_DIM   = "#7a6430"
RED_HP     = "#c0392b"
BLUE_MANA  = "#2980b9"
GREEN_WIN  = "#27ae60"
TEXT_WHITE = "#f0ead6"
TEXT_DIM   = "#8a7d5a"
BORDER     = "#3a3020"

# ─────────────────────────────────────────────
#  LÓGICA DEL JUEGO
# ─────────────────────────────────────────────
class SerMitico(ABC):
    _total_creados = 0
    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int) -> None:
        self.__nombre = nombre
        self.__vida   = max(1, vida)
        self.__vida_maxima = max(1, vida)
        self.ataque   = ataque
        self.defensa  = defensa
        SerMitico._total_creados += 1

    @property
    def nombre(self): return self.__nombre
    @property
    def vida(self): return self.__vida
    @property
    def vida_maxima(self): return self.__vida_maxima

    @vida.setter
    def vida(self, v): self.__vida = max(0, v)
    @vida_maxima.setter
    def vida_maxima(self, v):
        self.__vida_maxima = max(1, v)
        self.__vida = min(self.__vida, self.__vida_maxima)

    @abstractmethod
    def atacar(self, enemigo): pass
    @abstractmethod
    def usar_habilidad(self): pass

    def recibir_daño(self, cantidad):
        real = max(0, cantidad - self.defensa)
        self.vida -= real
        return real

    def esta_vivo(self): return self.vida > 0

    @staticmethod
    def calcular_daño(atacante, defensor):
        return max(0, atacante.ataque - defensor.defensa + random.randint(-10, 10))

    @classmethod
    def total_creados(cls): return cls._total_creados

    def __str__(self):
        return f"{self.nombre} (HP:{self.vida}/{self.vida_maxima} ATK:{self.ataque} DEF:{self.defensa})"


class Dios(SerMitico):
    def __init__(self, nombre, vida, ataque, defensa, poder_especial, mana):
        super().__init__(nombre, vida, ataque, defensa)
        self.poder_especial = poder_especial
        self.mana = mana
        self.mana_maximo = mana

    def atacar(self, enemigo):
        daño = SerMitico.calcular_daño(self, enemigo)
        critico = random.random() < 0.2
        if critico: daño *= 2
        return self.nombre, daño, critico

    def usar_habilidad(self):
        if self.mana >= 25:
            self.mana -= 25
            return random.randint(self.ataque + 15, self.ataque + 30)
        return 0

class Zeus(Dios):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Zeus", 100+v, 70+v, 25+v, "Rayo Divino", 200+v)

class Ares(Dios):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Ares", 130+v, 65+v, 40+v, "Furia de Guerra", 150+v)

class Poseidon(Dios):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Poseidon", 120+v, 75+v, 30+v, "Oleada Marina", 180+v)

class Hades(Dios):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Hades", 110+v, 80+v, 35+v, "Sombra del Inframundo", 160+v)

class Atenea(Dios):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Atenea", 90+v, 60+v, 50+v, "Escudo de Sabiduría", 170+v)


class Criatura(SerMitico):
    def __init__(self, nombre, vida, ataque, defensa, habilidad, multiplicador):
        super().__init__(nombre, vida, ataque, defensa)
        self.habilidad = habilidad
        self.multiplicador = multiplicador

    def atacar(self, enemigo):
        daño = SerMitico.calcular_daño(self, enemigo)
        critico = random.random() < 0.2
        if critico: daño *= 2
        return self.nombre, daño, critico

    def usar_habilidad(self):
        return random.randint(self.ataque + 15, self.ataque + 30)

class Minotauro(Criatura):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Minotauro", 150+v, 55+v, 45+v, "Embestida", 1.5)

class Medusa(Criatura):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Medusa", 90+v, 70+v, 25+v, "Petrificación", 1.2)

class Ciclope(Criatura):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Ciclope", 130+v, 60+v, 40+v, "Mazazo", 1.0)

class Hidra(Criatura):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Hidra", 170+v, 65+v, 40+v, "Multi-cabezas", 2.0)

class Escila(Criatura):
    def __init__(self):
        v = random.randint(-20, 20)
        super().__init__("Escila", 150+v, 65+v, 35+v, "Mordedura", 1.8)


class Item:
    def __init__(self, nombre, tipo, valor):
        self.nombre = nombre
        self.tipo   = tipo
        self.valor  = valor

    def usar(self, dios):
        if self.tipo == "Curación":
            dios.vida = min(dios.vida + self.valor, dios.vida_maxima)
            return f"✦ Usaste {self.nombre}: +{self.valor} HP"
        elif self.tipo == "Maná":
            dios.mana = min(dios.mana + self.valor, dios.mana_maximo)
            return f"✦ Usaste {self.nombre}: +{self.valor} Maná"
        elif self.tipo == "Ataque":
            dios.ataque = min(dios.ataque + self.valor, 200)
            return f"✦ Usaste {self.nombre}: +{self.valor} ATK"
        return f"Usaste {self.nombre}"

    def __str__(self):
        iconos = {"Curación": "❤", "Maná": "◈", "Ataque": "⚔"}
        return f"{iconos.get(self.tipo,'•')} {self.nombre}  [{self.tipo} +{self.valor}]"


class Inventario:
    def __init__(self):
        self.items: list[Item] = []

    def agregar(self, item):
        if len(self.items) < 5:
            self.items.append(item)
            return True
        return False

    def usar_item(self, indice, dios):
        if 0 <= indice < len(self.items):
            return self.items.pop(indice).usar(dios)
        return "Índice inválido"

    def __len__(self): return len(self.items)


class Jugador:
    def __init__(self, nombre_jugador, dios):
        self.nombre_jugador = nombre_jugador
        self.dios      = dios
        self.nivel     = 1
        self.score     = 0
        self.victorias = 0
        self.inventario = Inventario()

    def subir_nivel(self):
        if self.nivel < 10:
            self.nivel += 1
            self.dios.vida_maxima += 20
            self.dios.ataque      += 10
            self.dios.defensa     += 5
            self.dios.mana_maximo += 20
            self.dios.vida = self.dios.vida_maxima
            return f"⬆ ¡Subiste al nivel {self.nivel}!"
        return None

    def actualizar_score(self, puntos):
        self.score = max(0, self.score + puntos)

    def to_dict(self):
        return {
            "nombre_jugador": self.nombre_jugador,
            "nivel": self.nivel,
            "score": self.score,
            "victorias": self.victorias,
            "inventario": [i.nombre for i in self.inventario.items]
        }


class GestorPuntajes:
    def __init__(self, archivo="puntajes.json"):
        self.archivo = archivo
        self.tabla   = self._cargar()

    def _cargar(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def guardar(self, jugador):
        for j in self.tabla:
            if j["nombre_jugador"] == jugador.nombre_jugador:
                j["nivel"]     = max(j["nivel"],     jugador.nivel)
                j["score"]     = max(j["score"],     jugador.score)
                j["victorias"] = max(j["victorias"], jugador.victorias)
                j["inventario"] = [i.nombre for i in jugador.inventario.items]
                break
        else:
            self.tabla.append(jugador.to_dict())
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.tabla, f, indent=4)

    def top10(self):
        return sorted(self.tabla, key=lambda x: x["score"], reverse=True)[:10]


# ─────────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ Mitología Griega — Juego de Combate")
        self.geometry("900x680")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self.gestor = GestorPuntajes()
        self._frame_actual = None
        self.mostrar_menu()

    def cambiar_frame(self, nuevo_frame):
        if self._frame_actual:
            self._frame_actual.destroy()
        self._frame_actual = nuevo_frame
        nuevo_frame.pack(fill="both", expand=True)

    def mostrar_menu(self):
        self.cambiar_frame(PantallaMenu(self))

    def iniciar_partida(self, nombre, dios):
        jugador = Jugador(nombre, dios)
        item_ini = Item("Poción de Inicio", "Curación", 50)
        jugador.inventario.agregar(item_ini)
        self.cambiar_frame(PantallaCombate(self, jugador))

    def mostrar_top10(self, jugador):
        self.cambiar_frame(PantallaTop10(self, jugador))


# ─────────────────────────────────────────────
#  HELPERS DE ESTILO
# ─────────────────────────────────────────────
def label(parent, text, size=11, color=TEXT_WHITE, bold=False, italic=False):
    weight = "bold" if bold else "normal"
    slant  = "italic" if italic else "roman"
    return tk.Label(parent, text=text, bg=parent["bg"] if hasattr(parent,"_w") else BG_DARK,
                    fg=color, font=("Georgia", size, weight, slant))

def sep(parent, color=GOLD_DIM):
    f = tk.Frame(parent, bg=color, height=1)
    f.pack(fill="x", padx=20, pady=6)
    return f

def gold_btn(parent, text, cmd, width=18):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=BG_CARD, fg=GOLD, activebackground=GOLD_DIM,
                  activeforeground=BG_DARK, relief="flat",
                  font=("Georgia", 10, "bold"),
                  bd=0, padx=14, pady=8, width=width,
                  highlightthickness=1, highlightbackground=GOLD_DIM,
                  cursor="hand2")
    return b


# ─────────────────────────────────────────────
#  PANTALLA MENÚ PRINCIPAL
# ─────────────────────────────────────────────
DIOSES_INFO = {
    "Zeus":    ("⚡", "Rayo Divino",         "100 HP | 70 ATK | 25 DEF | 200 Maná"),
    "Ares":    ("⚔",  "Furia de Guerra",     "130 HP | 65 ATK | 40 DEF | 150 Maná"),
    "Poseidon":("🌊", "Oleada Marina",        "120 HP | 75 ATK | 30 DEF | 180 Maná"),
    "Hades":   ("💀", "Sombra del Inframundo","110 HP | 80 ATK | 35 DEF | 160 Maná"),
    "Atenea":  ("🛡",  "Escudo de Sabiduría", " 90 HP | 60 ATK | 50 DEF | 170 Maná"),
}
DIOSES_CLASES = {
    "Zeus": Zeus, "Ares": Ares, "Poseidon": Poseidon,
    "Hades": Hades, "Atenea": Atenea
}

class PantallaMenu(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self._seleccion = tk.StringVar(value="Zeus")
        self._build()

    def _build(self):
        # ── Título
        tk.Label(self, text="⚡  MITOLOGÍA GRIEGA  ⚡",
                 bg=BG_DARK, fg=GOLD,
                 font=("Georgia", 26, "bold")).pack(pady=(30,4))
        tk.Label(self, text="— Juego de Combate —",
                 bg=BG_DARK, fg=GOLD_DIM,
                 font=("Georgia", 12, "italic")).pack(pady=(0,16))
        sep(self)

        # ── Nombre del jugador
        mid = tk.Frame(self, bg=BG_DARK)
        mid.pack(fill="x", padx=60)

        tk.Label(mid, text="Nombre del guerrero", bg=BG_DARK,
                 fg=TEXT_DIM, font=("Georgia", 10, "italic")).pack(anchor="w", pady=(10,2))
        self._entry_nombre = tk.Entry(mid, font=("Georgia", 13),
                                      bg=BG_CARD, fg=TEXT_WHITE,
                                      insertbackground=GOLD,
                                      relief="flat", bd=6)
        self._entry_nombre.pack(fill="x", ipady=6)

        sep(self)

        # ── Selección de dios
        tk.Label(self, text="Elige tu Dios", bg=BG_DARK,
                 fg=GOLD, font=("Georgia", 13, "bold")).pack(pady=(8,10))

        grid = tk.Frame(self, bg=BG_DARK)
        grid.pack()

        self._info_label = tk.Label(self, text="", bg=BG_DARK,
                                     fg=TEXT_DIM, font=("Georgia", 10, "italic"))
        self._info_label.pack(pady=6)

        for nombre, (icono, poder, stats) in DIOSES_INFO.items():
            self._card_dios(grid, nombre, icono, poder, stats)

        # Seleccionar Zeus por defecto visualmente
        self._seleccion.set("Zeus")
        self._actualizar_info("Zeus")

        sep(self)

        # ── Botón Top10 + Comenzar
        btns = tk.Frame(self, bg=BG_DARK)
        btns.pack(pady=14)

        gold_btn(btns, "🏆  Ver Top 10", self._ver_top10, width=16).pack(side="left", padx=10)
        gold_btn(btns, "⚡  Comenzar Partida", self._comenzar, width=20).pack(side="left", padx=10)

    def _card_dios(self, parent, nombre, icono, poder, stats):
        var = self._seleccion
        col = BG_CARD

        frame = tk.Frame(parent, bg=col, bd=0,
                         highlightthickness=1, highlightbackground=GOLD_DIM,
                         cursor="hand2")
        frame.pack(side="left", padx=8, pady=4, ipadx=10, ipady=8)

        tk.Label(frame, text=icono, bg=col, font=("", 22)).pack()
        tk.Label(frame, text=nombre, bg=col, fg=GOLD,
                 font=("Georgia", 10, "bold")).pack()

        def select():
            var.set(nombre)
            self._actualizar_info(nombre)
            # Resaltar seleccionado
            for w in parent.winfo_children():
                w.configure(highlightbackground=GOLD_DIM)
            frame.configure(highlightbackground=GOLD, highlightthickness=2)

        frame.bind("<Button-1>", lambda e: select())
        for child in frame.winfo_children():
            child.bind("<Button-1>", lambda e: select())

    def _actualizar_info(self, nombre):
        icono, poder, stats = DIOSES_INFO[nombre]
        self._info_label.config(
            text=f"{icono} {nombre}  ·  {poder}  ·  {stats}  (±20 variación aleatoria)"
        )

    def _comenzar(self):
        nombre = self._entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("⚠ Atención", "Ingresa tu nombre de guerrero.")
            return
        dios_cls = DIOSES_CLASES[self._seleccion.get()]
        self.master.iniciar_partida(nombre, dios_cls())

    def _ver_top10(self):
        self.master.mostrar_top10(None)


# ─────────────────────────────────────────────
#  PANTALLA COMBATE
# ─────────────────────────────────────────────
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