# TutorIA — Planejador Adaptativo

Primeiro módulo do TutorIA, desenvolvido com Python, Streamlit e Google Gen AI SDK.

## Funcionalidades
- Coleta do perfil de estudos.
- Geração adaptativa de proposta semanal.
- Validação básica de horários, disciplinas e carga horária.
- Visualização detalhada.
- Aprovação explícita antes do salvamento em JSON.

## Preparação no Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite o arquivo `.env` e coloque sua chave do Google AI Studio em `GEMINI_API_KEY`.

## Executar

```powershell
streamlit run app.py
```

## Observações
- Não publique o arquivo `.env`.
- O JSON é armazenamento local de protótipo, não é adequado para múltiplos usuários sem autenticação e isolamento.
- Revise a proposta antes de aprová-la. A validação automática é básica e não garante que o plano seja pedagogicamente perfeito.
