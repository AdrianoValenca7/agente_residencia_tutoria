
import json
import os
import unicodedata

from google import genai
from google.genai import types

from agente.instrucoes import INSTRUCAO_PLANEJADOR


MODELO = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


def gerar_planejamento(perfil):
    """Solicita ao Gemini uma proposta estruturada de planejamento."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "A chave GEMINI_API_KEY não foi encontrada. "
            "Confira o arquivo .env."
        )

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

    try:
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
            raise ValueError(
                "O Gemini retornou uma resposta que não pôde "
                "ser interpretada como JSON."
            ) from erro

    except ValueError:
        raise

    except Exception as erro:
        mensagem = str(erro).upper()

        if "503" in mensagem or "UNAVAILABLE" in mensagem:
            raise RuntimeError(
                "O serviço de IA está temporariamente indisponível. "
                "Tente novamente em alguns minutos."
            ) from erro

        if "429" in mensagem or "RESOURCE_EXHAUSTED" in mensagem:
            raise RuntimeError(
                "O limite de solicitações da API foi atingido. "
                "Aguarde um pouco antes de tentar novamente."
            ) from erro

        if "401" in mensagem or "UNAUTHENTICATED" in mensagem:
            raise RuntimeError(
                "A autenticação com o Gemini falhou. "
                "Confira sua chave da API."
            ) from erro

        if "403" in mensagem or "PERMISSION_DENIED" in mensagem:
            raise RuntimeError(
                "A API não autorizou a solicitação. "
                "Confira as permissões e a configuração do projeto."
            ) from erro

        raise RuntimeError(
            "Não foi possível gerar o planejamento. "
            "Verifique a conexão e tente novamente."
        ) from erro


def normalizar_texto(texto):
    """Remove espaços extras, diferenças entre maiúsculas e acentos."""

    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def validar_planejamento(plano, perfil):
    """Verifica se a proposta respeita as informações do perfil."""

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

    dias_permitidos = {
        normalizar_texto(dia)
        for dia in perfil["dias_disponiveis"]
    }

    disciplinas_permitidas = {
        normalizar_texto(disciplina)
        for disciplina in perfil["disciplinas"]
    }

    if not isinstance(plano["dias"], list) or not plano["dias"]:
        return ["O planejamento não contém dias de estudo."]

    dias_encontrados = set()

    for dia in plano["dias"]:

        if not isinstance(dia, dict):
            erros.append("Foi encontrado um dia em formato inválido.")
            continue

        nome_dia = dia.get("dia", "")
        dia_normalizado = normalizar_texto(nome_dia)

        if dia_normalizado not in dias_permitidos:
            erros.append(
                f"O dia '{nome_dia}' não está disponível."
            )

        if dia_normalizado in dias_encontrados:
            erros.append(
                f"O dia '{nome_dia}' aparece mais de uma vez."
            )

        dias_encontrados.add(dia_normalizado)

        sessoes = dia.get("sessoes", [])

        if not isinstance(sessoes, list) or not sessoes:
            erros.append(
                f"Não existem sessões para {nome_dia}."
            )
            continue

        minutos_total = 0
        intervalos = []

        for sessao in sessoes:

            if not isinstance(sessao, dict):
                erros.append(
                    f"Sessão inválida em {nome_dia}."
                )
                continue

            try:
                inicio_h, inicio_m = map(
                    int, sessao["inicio"].split(":")
                )

                fim_h, fim_m = map(
                    int, sessao["fim"].split(":")
                )

                if not (
                    0 <= inicio_h <= 23
                    and 0 <= inicio_m <= 59
                    and 0 <= fim_h <= 23
                    and 0 <= fim_m <= 59
                ):
                    raise ValueError()

                inicio = inicio_h * 60 + inicio_m
                fim = fim_h * 60 + fim_m

            except (KeyError, ValueError, AttributeError):
                erros.append(
                    f"Horário inválido em {nome_dia}."
                )
                continue

            if fim <= inicio:
                erros.append(
                    f"Intervalo inválido em {nome_dia}."
                )
                continue

            minutos_total += fim - inicio
            intervalos.append((inicio, fim))

            disciplina = normalizar_texto(
                sessao.get("disciplina", "")
            )

            if disciplina not in disciplinas_permitidas:
                erros.append(
                    f"Disciplina '{sessao.get('disciplina', '')}' "
                    "não consta no perfil informado."
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
                "o limite informado."
            )

        intervalos.sort()

        for indice in range(1, len(intervalos)):
            if intervalos[indice][0] < intervalos[indice - 1][1]:
                erros.append(
                    f"Existem sessões sobrepostas em {nome_dia}."
                )

    return list(dict.fromkeys(erros))
