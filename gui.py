import customtkinter as ctk
from tkinter import messagebox
from storage import carregar_tarefas, salvar_tarefas

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-do List")
        self.root.geometry("600x500")
        self.tarefas = carregar_tarefas()
        self.filtro = "todas"

        self.entrada = ctk.CTkEntry(root, width=400, height=35, placeholder_text="Digite uma nova tarefa")
        self.entrada.pack(pady=(15, 10))

        self.frame_botoes = ctk.CTkFrame(root)
        self.frame_botoes.pack()

        self.btn_add = ctk.CTkButton(self.frame_botoes, text="Adicionar", command=self.adicionar_tarefa)
        self.btn_add.pack(side="left", padx=5)

        self.btn_remover = ctk.CTkButton(self.frame_botoes, text="Remover", command=self.remover_tarefa)
        self.btn_remover.pack(side="left", padx=5)

        self.btn_subir = ctk.CTkButton(self.frame_botoes, text="🔼", width=40, command=self.mover_para_cima)
        self.btn_subir.pack(side="left", padx=2)

        self.btn_descer = ctk.CTkButton(self.frame_botoes, text="🔽", width=40, command=self.mover_para_baixo)
        self.btn_descer.pack(side="left", padx=2)

        self.btn_limpar = ctk.CTkButton(self.frame_botoes, text="Limpar Tudo", fg_color="red", command=self.limpar_tudo)
        self.btn_limpar.pack(side="left", padx=5)

        self.btn_modo = ctk.CTkButton(root, text="🌗 Alternar Tema", command=self.trocar_tema)
        self.btn_modo.pack(pady=5)

        self.filtro_frame = ctk.CTkFrame(root)
        self.filtro_frame.pack()

        self.btn_todas = ctk.CTkButton(self.filtro_frame, text="Todas", command=lambda: self.definir_filtro("todas"))
        self.btn_todas.pack(side="left", padx=5)

        self.btn_pendentes = ctk.CTkButton(self.filtro_frame, text="Pendentes", command=lambda: self.definir_filtro("pendentes"))
        self.btn_pendentes.pack(side="left", padx=5)

        self.btn_concluidas = ctk.CTkButton(self.filtro_frame, text="Concluídas", command=lambda: self.definir_filtro("concluidas"))
        self.btn_concluidas.pack(side="left", padx=5)

        self.lista = ctk.CTkListbox(root, height=15, width=550, command=self.toggle_conclusao)
        self.lista.pack(pady=10)

        self.carregar_lista()

    def carregar_lista(self):
        self.lista.delete(0, "end")
        for i, t in enumerate(self.tarefas):
            if self.filtro == "pendentes" and t["concluida"]:
                continue
            if self.filtro == "concluidas" and not t["concluida"]:
                continue
            prefixo = "✓ " if t["concluida"] else "• "
            self.lista.insert("end", prefixo + t["texto"])

    def adicionar_tarefa(self):
        texto = self.entrada.get().strip()
        if texto:
            self.tarefas.append({"texto": texto, "concluida": False})
            salvar_tarefas(self.tarefas)
            self.carregar_lista()
            self.entrada.delete(0, "end")

    def remover_tarefa(self):
        idx = self.lista.curselection()
        if idx:
            real_idx = self.get_indice_real(idx[0])
            self.tarefas.pop(real_idx)
            salvar_tarefas(self.tarefas)
            self.carregar_lista()

    def toggle_conclusao(self, idx=None):
        idx = self.lista.curselection()
        if not idx:
            return
        real_idx = self.get_indice_real(idx[0])
        self.tarefas[real_idx]["concluida"] = not self.tarefas[real_idx]["concluida"]
        salvar_tarefas(self.tarefas)
        self.carregar_lista()

    def limpar_tudo(self):
        if messagebox.askyesno("Confirmar", "Deseja remover todas as tarefas?"):
            self.tarefas.clear()
            salvar_tarefas(self.tarefas)
            self.carregar_lista()

    def mover_para_cima(self):
        idx = self.lista.curselection()
        if idx and idx[0] > 0:
            real_idx = self.get_indice_real(idx[0])
            if real_idx > 0:
                self.tarefas[real_idx - 1], self.tarefas[real_idx] = self.tarefas[real_idx], self.tarefas[real_idx - 1]
                salvar_tarefas(self.tarefas)
                self.carregar_lista()
                self.lista.select_set(idx[0] - 1)

    def mover_para_baixo(self):
        idx = self.lista.curselection()
        if idx and idx[0] < len(self.lista.get(0, "end")) - 1:
            real_idx = self.get_indice_real(idx[0])
            if real_idx < len(self.tarefas) - 1:
                self.tarefas[real_idx + 1], self.tarefas[real_idx] = self.tarefas[real_idx], self.tarefas[real_idx + 1]
                salvar_tarefas(self.tarefas)
                self.carregar_lista()
                self.lista.select_set(idx[0] + 1)

    def trocar_tema(self):
        atual = ctk.get_appearance_mode()
        novo = "light" if atual == "Dark" else "dark"
        ctk.set_appearance_mode(novo)

    def definir_filtro(self, tipo):
        self.filtro = tipo
        self.carregar_lista()

    def get_indice_real(self, visivel_idx):
        """Mapeia índice visível para o real na lista original"""
        visiveis = []
        for i, t in enumerate(self.tarefas):
            if self.filtro == "pendentes" and t["concluida"]:
                continue
            if self.filtro == "concluidas" and not t["concluida"]:
                continue
            visiveis.append(i)
        return visiveis[visivel_idx] if visivel_idx < len(visiveis) else 0
