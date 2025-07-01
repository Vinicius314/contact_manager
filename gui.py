import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from storage import carregar_contatos, salvar_contatos

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Contatos")
        self.root.geometry("750x500")
        self.contatos = carregar_contatos()

        # Frame superior (formulário)
        form_frame = ttk.LabelFrame(root, text="Novo Contato")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nome_entry = ttk.Entry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.tel_entry = ttk.Entry(form_frame)
        self.tel_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Data Nasc:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.data_entry = DateEntry(form_frame, date_pattern="dd/mm/yyyy")
        self.data_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Tipo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.tipo_cb = ttk.Combobox(form_frame, values=["Pessoal", "Profissional"], state="readonly")
        self.tipo_cb.grid(row=2, column=1, padx=5, pady=5)
        self.tipo_cb.current(0)

        self.btn_add = ttk.Button(form_frame, text="Adicionar", command=self.adicionar_contato)
        self.btn_add.grid(row=2, column=3, padx=5, pady=5)

        # Treeview (lista de contatos)
        self.tree = ttk.Treeview(root, columns=("Nome", "Email", "Telefone", "Data", "Tipo"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Data", text="Data Nasc.")
        self.tree.heading("Tipo", text="Tipo")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.editar_contato)

        # Botão excluir
        self.btn_excluir = ttk.Button(root, text="Excluir Selecionado", command=self.excluir_contato)
        self.btn_excluir.pack(pady=5)

        self.carregar_lista()

    def adicionar_contato(self):
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        tel = self.tel_entry.get().strip()
        data = self.data_entry.get()
        tipo = self.tipo_cb.get()

        if not nome or not email:
            messagebox.showwarning("Aviso", "Nome e Email são obrigatórios.")
            return

        contato = {
            "nome": nome,
            "email": email,
            "telefone": tel,
            "data_nasc": data,
            "tipo": tipo
        }

        self.contatos.append(contato)
        salvar_contatos(self.contatos)
        self.carregar_lista()
        self.limpar_campos()

    def carregar_lista(self):
        self.tree.delete(*self.tree.get_children())
        for contato in self.contatos:
            self.tree.insert("", "end", values=(
                contato["nome"], contato["email"], contato["telefone"], contato["data_nasc"], contato["tipo"]
            ))

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.tel_entry.delete(0, tk.END)
        self.data_entry.set_date("")
        self.tipo_cb.current(0)

    def excluir_contato(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showinfo("Info", "Selecione um contato para excluir.")
            return
        idx = self.tree.index(selecionado)
        if messagebox.askyesno("Confirmar", "Deseja excluir este contato?"):
            self.contatos.pop(idx)
            salvar_contatos(self.contatos)
            self.carregar_lista()

    def editar_contato(self, event):
        selecionado = self.tree.selection()
        if not selecionado:
            return
        idx = self.tree.index(selecionado)
        contato = self.contatos[idx]

        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, contato["nome"])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, contato["email"])

        self.tel_entry.delete(0, tk.END)
        self.tel_entry.insert(0, contato["telefone"])

        self.data_entry.set_date(contato["data_nasc"])
        self.tipo_cb.set(contato["tipo"])

        self.btn_add.config(text="Salvar", command=lambda: self.salvar_edicao(idx))

    def salvar_edicao(self, idx):
        self.contatos[idx] = {
            "nome": self.nome_entry.get(),
            "email": self.email_entry.get(),
            "telefone": self.tel_entry.get(),
            "data_nasc": self.data_entry.get(),
            "tipo": self.tipo_cb.get()
        }
        salvar_contatos(self.contatos)
        self.carregar_lista()
        self.limpar_campos()
        self.btn_add.config(text="Adicionar", command=self.adicionar_contato)
