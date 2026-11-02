import json
from pathlib import Path
from datetime import datetime

ARQUIVO = Path(__file__).resolve().parent.parent / "dados" / "planejamento.json"


def salvar_planejamento(dados):
    """Salva o plano somente quando esta função é chamada após aprovação."""
    dados["aprovado_em"] = datetime.now().isoformat(timespec="seconds")
    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
