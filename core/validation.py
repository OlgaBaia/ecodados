# core/validation.py
from __future__ import annotations
from datetime import datetime

def normalize_name(nome: str) -> str:
    nome_norm = (nome or "").strip()
    if not nome_norm:
        raise ValueError("Nome não pode ser vazio.")
    return nome_norm

def parse_age(idade_str: str) -> int:
    try:
        idade = int(str(idade_str).strip())
    except (TypeError, ValueError):
        raise ValueError("Idade deve ser um número inteiro válido.")
    if idade < 0:
        raise ValueError("Idade deve ser um inteiro maior ou igual a 0.")
    return idade

def parse_date_br(data_str: str) -> str:
    # Entrada: DD/MM/AAAA → Saída: YYYY-MM-DD
    try:
        dt = datetime.strptime(str(data_str).strip(), "%d/%m/%Y")
    except (TypeError, ValueError):
        raise ValueError("Data deve estar no formato DD/MM/AAAA (ex: 25/12/2025).")
    return dt.strftime("%Y-%m-%d")
