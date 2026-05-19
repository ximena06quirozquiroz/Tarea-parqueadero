import tkinter as tk
from tkinter import ttk

class Visualizador:
    def __init__(self, root, bridge):
        self.root = root
        self.bridge = bridge
        self.root.title("Sistema de Parqueadero — En vivo")
        self.root.geometry("1150x780") # Un poco más ancha para que quepa todo
        self.root.configure(bg="#0a0a0c")

        # --- CONFIGURACIÓN DE COLORES NEÓN ---
        self.bg_negro = "#0a0a0c"
        self.morado_neon = "#bc13fe"     
        self.rosado_neon = "#ff007f"     
        self.texto_blanco = "#ffffff"    
        self.gris_oscuro = "#141419"

        self.celdas_widgets = {}
        
        self._setup_ui()
        self.actualizar_grilla()

    def _setup_ui(self):
        # Contenedor principal que llena toda la ventana
        main_container = tk.Frame(self.root, bg=self.bg_negro, padx=10, pady=10)
        main_container.pack(fill="both", expand=True)

        # --- PARTE SUPERIOR: GRILLA DE CELDAS (Sincronizada a 27 puestos) ---
        frame_grilla = tk.LabelFrame(
            main_container, text=" Estado de Celdas (27) ", 
            padx=10, pady=10, bg=self.bg_negro, fg=self.texto_blanco,
            font=("Segoe UI", 12, "bold"), highlightbackground=self.morado_neon, highlightthickness=1, bd=0
        )
        frame_grilla.pack(fill="x", padx=5, pady=5)

        # Configuramos 9 columnas para que los 27 puestos queden en 3 filas (3x9)
        for c in range(9):
            frame_grilla.columnconfigure(c, weight=1)

        for i in range(27):
            fila = i // 9
            col = i % 9
            
            cell_frame = tk.Frame(
                frame_grilla, width=115, height=65, bd=0,
                highlightbackground=self.morado_neon, highlightthickness=1.5, bg=self.gris_oscuro
            )
            cell_frame.grid(row=fila, column=col, padx=5, pady=5, sticky="nsew")
            cell_frame.pack_propagate(False)
            
            lbl_num = tk.Label(cell_frame, text=f"Celda {i+1}", font=("Segoe UI", 9, "bold"), fg=self.texto_blanco, bg=self.gris_oscuro)
            lbl_num.pack(pady=(4, 1))
            
            lbl_placa = tk.Label(cell_frame, text="LIBRE", font=("Segoe UI", 10, "bold"), fg=self.morado_neon, bg=self.gris_oscuro)
            lbl_placa.pack(pady=(0, 4))
            
            self.celdas_widgets[i] = {
                "frame": cell_frame, 
                "placa_label": lbl_placa,
                "num_label": lbl_num
            }

        # --- PARTE INFERIOR: HISTORIAL Y ADMINISTRADORAS ---
        frame_inferior = tk.Frame(main_container, bg=self.bg_negro)
        frame_inferior.pack(fill="both", expand=True, padx=5, pady=5)

        # TABLA DE HISTORIAL (Izquierda)
        frame_historial = tk.LabelFrame(
            frame_inferior, text=" Historial de Eventos ", 
            padx=10, pady=10, bg=self.bg_negro, fg=self.texto_blanco,
            font=("Segoe UI", 11, "bold"), highlightbackground=self.morado_neon, highlightthickness=1, bd=0
        )
        frame_historial.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Forzar estilos visuales de la tabla para ver las letras
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview", 
            background="#141419", 
            fieldbackground="#141419", 
            foreground="#ffffff", 
            rowheight=24, 
            bd=0
        )
        style.configure("Treeview.Heading", background=self.morado_neon, foreground=self.texto_blanco, font=("Segoe UI", 10, "bold"))

        columnas = ("hora", "placa", "celda", "estado")
        self.tabla = ttk.Treeview(frame_historial, columns=columnas, show="headings", height=6)
        
        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("placa", text="Placa")
        self.tabla.heading("celda", text="Celda")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("hora", width=90, anchor="center")
        self.tabla.column("placa", width=120, anchor="center")
        self.tabla.column("celda", width=80, anchor="center")
        self.tabla.column("estado", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_historial, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # PANEL DE ADMINISTRADORAS (Derecha)
        frame_admin = tk.LabelFrame(
            frame_inferior, text=" Administradoras ", 
            padx=15, pady=15, bg=self.bg_negro, fg=self.texto_blanco,
            font=("Segoe UI", 11, "bold"), highlightbackground=self.morado_neon, highlightthickness=1, bd=0
        )
        frame_admin.pack(side="right", fill="y", padx=(5, 0))

        # Texto de los nombres fijos dentro de la caja de Administradoras
        lbl_nombres = tk.Label(
            frame_admin, 
            text="XIMENA\n&\nCAMILA", 
            font=("Impact", 22), 
            fg=self.rosado_neon, 
            bg=self.bg_negro,
            justify="center"
        )
        lbl_nombres.pack(expand=True, pady=10)

        lbl_itm = tk.Label(frame_admin, text="Estudiantes ITM", font=("Segoe UI", 9, "italic"), fg="#666677", bg=self.bg_negro)
        lbl_itm.pack(side="bottom")


    def agregar_evento(self, placa, hora, celda, estado):
        self.tabla.insert("", 0, values=(hora, placa, celda, estado), tags=('neon_row',))
        self.tabla.tag_configure('neon_row', foreground='#ffffff') 
        
        if len(self.tabla.get_children()) > 50:
            ultimo = self.tabla.get_children()[-1]
            self.tabla.delete(ultimo)
            
        try:
            idx = int(celda) - 1
            if 0 <= idx < 27:
                widget = self.celdas_widgets[idx]
                
                if estado == "ENTRADA":
                    widget["frame"].configure(bg=self.rosado_neon, highlightbackground=self.rosado_neon)
                    widget["placa_label"].configure(text=f"OCUPADA\n{placa}", bg=self.rosado_neon, fg=self.texto_blanco, font=("Segoe UI", 9, "bold"))
                    widget["num_label"].configure(bg=self.rosado_neon, fg=self.texto_blanco)
                else:
                    widget["frame"].configure(bg=self.gris_oscuro, highlightbackground=self.morado_neon)
                    widget["placa_label"].configure(text="LIBRE", bg=self.gris_oscuro, fg=self.morado_neon, font=("Segoe UI", 10, "bold"))
                    widget["num_label"].configure(bg=self.gris_oscuro, fg=self.texto_blanco)
        except ValueError:
            pass 

    def actualizar_grilla(self):
        estados = self.bridge.obtener_estado_celdas()
        for i, estado_bit in enumerate(estados):
            if i >= 27: break
            widget = self.celdas_widgets[i]
            if estado_bit == "1":
                widget["frame"].configure(bg=self.rosado_neon, highlightbackground=self.rosado_neon)
                widget["placa_label"].configure(text="OCUPADA", bg=self.rosado_neon, fg=self.texto_blanco, font=("Segoe UI", 9, "bold"))
                widget["num_label"].configure(bg=self.rosado_neon, fg=self.texto_blanco)
            else:
                widget["frame"].configure(bg=self.gris_oscuro, highlightbackground=self.morado_neon)
                widget["placa_label"].configure(text="LIBRE", bg=self.gris_oscuro, fg=self.morado_neon, font=("Segoe UI", 10, "bold"))
                widget["num_label"].configure(bg=self.gris_oscuro, fg=self.texto_blanco)