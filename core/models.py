from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Registro:
    nome: str
    idade: int
    data_iso: str  # formato YYYY-MM-DD
