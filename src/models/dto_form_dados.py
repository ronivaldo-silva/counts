from dataclasses import dataclass
from typing import Optional

@dataclass
class DTO_FormDados:
    cpf: Optional[str] = None
    id: Optional[int] = None
    nome: Optional[str] = None
    senha: Optional[str] = None
