import json
import os
from google import genai
from google.genai import types
from agente.instrucoes import INSTRUCAO_PLANEJADOR

MODELO = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


def gerar_planejamento(perfil):
    """Solicita ao Gemini uma proposta estruturada de planejamento."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A chave GEMINI_API_KEY não foi encontrada. Confira o arquivo .env.")

    cliente = genai.Client(api_key=api_key)

    prompt = f"""
Crie uma proposta de planejamento semanal com base neste perfil:
{json.dumps(perfil, ensure_ascii=False, indent=2)}

Retorne somente um JSON válido, sem Markdown, com esta estrutura:
{{
  "titulo": "string",
  "justificativa": "string",
  "estrategia": "string",
  "dias": [
    {{
      "dia": "Segunda",
      "foco": "string",
      "sessoes": [
        {{
          "inicio": "08:00",
          "fim": "09:00",
          "disciplina": "string",
          "atividade": "string",
          "objetivo": "string",
          "observacao": "string"
        }}
      ]
    }}
  ],
  "orientacoes": ["string"]
}}

Regras:
- Use somente os dias informados no perfil.
- Não ultrapasse as horas disponíveis por dia.
- Distribua as disciplinas ao longo da semana.
- Priorize dificuldades e baixo desempenho, sem abandonar as demais disciplinas.
- Inclua revisões se foram solicitadas.
- Cada sessão deve ter horários no formato HH:MM e duração positiva.
- Não prometa aprovação nem resultados garantidos.
- Se faltarem dados para uma decisão, adote uma sugestão conservadora e explique isso nas orientações.
"""

    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_PLANEJADOR,
            response_mime_type="application/json",
            temperature=0.4
        )
    )

    if not resposta.text:
        raise ValueError("O modelo não retornou conteúdo.")

    try:
        return json.loads(resposta.text)
    except json.JSONDecodeError as erro:
        raise ValueError("O Gemini retornou uma resposta que não pôde ser interpretada como JSON.") from erro


import unicodedata

def normalizar_texto(texto):
    texto = texto.strip().lower()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def validar_planejamento(plano, perfil):

    erros = []

    if not isinstance(plano, dict):
        return ["Resposta em formato inválido."]

    campos = [
        "titulo",
        "justificativa",
        "estrategia",
        "dias",
        "orientacoes"
    ]

    for campo in campos:
        if campo not in plano:
            erros.append(f"Campo obrigatório ausente: {campo}.")

    if erros:
        return erros

    dias_permitidos = perfil["dias_disponiveis"]

    disciplinas_permitidas = {
        normalizar_texto(d)
        for d in perfil["disciplinas"]
    }

    if not isinstance(plano["dias"], list) or not plano["dias"]:
        return ["O planejamento não contém dias de estudo."]

    for dia in plano["dias"]:

        nome_dia = dia.get("dia")

        if nome_dia not in dias_permitidos:
            erros.append(
                f"O dia '{nome_dia}' não está disponível."
            )

        sessoes = dia.get("sessoes", [])

        if not isinstance(sessoes, list) or not sessoes:
            erros.append(
                f"Não existem sessões para {nome_dia}."
            )
            continue

        minutos_total = 0
        intervalos = []

        for sessao in sessoes:

            try:
                inicio_h, inicio_m = map(
                    int, sessao["inicio"].split(":")
                )

                fim_h, fim_m = map(
                    int, sessao["fim"].split(":")
                )

                inicio = inicio_h * 60 + inicio_m
                fim = fim_h * 60 + fim_m

            except (KeyError, ValueError, AttributeError):
                erros.append(
                    f"Horário inválido em {nome_dia}."
                )
                continue

            if inicio < 0 or fim > 1440 or fim <= inicio:
                erros.append(
                    f"Intervalo inválido em {nome_dia}."
                )
                continue

            minutos_total += fim - inicio

            intervalos.append((inicio, fim))

            disciplina = normalizar_texto(
                str(sessao.get("disciplina", ""))
            )

            if disciplina not in disciplinas_permitidas:
                erros.append(
                    f"Disciplina '{sessao.get('disciplina', '')}' "
                    f"não consta no perfil informado."
                )

            if not sessao.get("atividade"):
                erros.append(
                    f"Sessão sem atividade em {nome_dia}."
                )

            if not sessao.get("objetivo"):
                erros.append(
                    f"Sessão sem objetivo em {nome_dia}."
                )

        limite = int(
            float(perfil["horas_por_dia"]) * 60
        )

        if minutos_total > limite:
            erros.append(
                f"A carga de {nome_dia} ultrapassa "
                f"o limite informado."
            )

        intervalos.sort()

        for indice in range(1, len(intervalos)):

            if intervalos[indice][0] < intervalos[indice - 1][1]:
                erros.append(
                    f"Existem sessões sobrepostas em {nome_dia}."
                )

    return list(dict.fromkeys(erros))