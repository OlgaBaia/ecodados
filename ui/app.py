import tkinter as tk
from tkinter import messagebox, ttk

from core.validation import normalize_name, parse_age, parse_date_br
from core.storage import append_record, list_records
from core.models import Registro

PADDING = {"padx": 10, "pady": 8}

def _build_cadastro_tab(tab: ttk.Frame, on_saved_callback) -> None:
    nome_var = tk.StringVar()
    idade_var = tk.StringVar()
    data_var = tk.StringVar()

    # Layout grid responsivo
    tab.columnconfigure(1, weight=1)

    ttk.Label(tab, text="Nome").grid(row=0, column=0, sticky="w", **PADDING)
    nome_entry = ttk.Entry(tab, textvariable=nome_var, width=40)
    nome_entry.grid(row=0, column=1, sticky="ew", **PADDING)

    ttk.Label(tab, text="Idade").grid(row=1, column=0, sticky="w", **PADDING)
    idade_entry = ttk.Entry(tab, textvariable=idade_var, width=12)
    idade_entry.grid(row=1, column=1, sticky="w", **PADDING)

    ttk.Label(tab, text="Data (DD/MM/AAAA)").grid(row=2, column=0, sticky="w", **PADDING)
    data_entry = ttk.Entry(tab, textvariable=data_var, width=16)
    data_entry.grid(row=2, column=1, sticky="w", **PADDING)

    def limpar():
        nome_var.set("")
        idade_var.set("")
        data_var.set("")
        nome_entry.focus_set()

    def salvar():
        try:
            nome = normalize_name(nome_var.get())
            idade = parse_age(idade_var.get())
            data_iso = parse_date_br(data_var.get())
            append_record(Registro(nome, idade, data_iso))
            messagebox.showinfo("Sucesso", "Registro salvo em data/registros.xlsx")
            limpar()
            on_saved_callback()  # atualiza a aba de registros
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    btns = ttk.Frame(tab)
    btns.grid(row=3, column=0, columnspan=2, pady=12)
    ttk.Button(btns, text="Salvar", command=salvar, width=14).pack(side="left", padx=6)
    ttk.Button(btns, text="Limpar", command=limpar, width=14).pack(side="left", padx=6)

    nome_entry.focus_set()

def _build_registros_tab(tab: ttk.Frame):
    tab.rowconfigure(0, weight=1)
    tab.columnconfigure(0, weight=1)

    cols = ("nome", "idade", "data")
    tree = ttk.Treeview(tab, columns=cols, show="headings", height=12)
    for col, w in zip(cols, (300, 80, 120)):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=w, anchor="w")

    yscroll = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)

    tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    yscroll.grid(row=0, column=1, sticky="ns", pady=10)

    actions = ttk.Frame(tab)
    actions.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 10))
    def carregar():
        # limpa
        for item in tree.get_children():
            tree.delete(item)
        # carrega
        for r in list_records():
            tree.insert("", "end", values=(r.nome, r.idade, r.data_iso))

    ttk.Button(actions, text="Atualizar", command=carregar).pack(side="left")

    # carrega inicialmente
    carregar()

    # expõe função pra outras abas chamarem
    return carregar

def run() -> None:
    root = tk.Tk()
    root.title("ECODADOS")
    root.geometry("720x420")
    root.minsize(680, 360)

    style = ttk.Style()
    # Usa o tema nativo se disponível
    try:
        style.theme_use("vista")
    except Exception:
        pass

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab_cadastro = ttk.Frame(notebook)
    tab_registros = ttk.Frame(notebook)
    tab_outros = ttk.Frame(notebook)  # placeholder para novos formulários

    notebook.add(tab_cadastro, text="Cadastro")
    notebook.add(tab_registros, text="Registros")
    notebook.add(tab_outros, text="Outros")

    # monta a aba de registros primeiro para pegar o callback
    atualizar_lista = _build_registros_tab(tab_registros)
    _build_cadastro_tab(tab_cadastro, on_saved_callback=atualizar_lista)

    # placeholder “Outros”
    ttk.Label(tab_outros, text="Aqui você pode criar novos formulários em outras telas.").pack(
        anchor="w", padx=12, pady=12
    )

    root.mainloop()
