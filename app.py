
from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from modulos.planejador import (
    gerar_planejamento,
    validar_planejamento
)

from servicos.armazenamento import salvar_planejamento


st.set_page_config(
    page_title="TutorIA | Planejador",
    page_icon="📚",
    layout="wide"
)


st.title("📚 TutorIA")
st.subheader("Planejador Adaptativo de Estudos")

st.write(
    "Monte uma rotina de estudos adaptada ao seu concurso, "
    "disponibilidade e desempenho."
)


if "proposta" not in st.session_state:
    st.session_state.proposta = None

if "perfil_atual" not in st.session_state:
    st.session_state.perfil_atual = None


with st.form("form_planejamento"):

    st.markdown("### 1. Sobre seu objetivo")

    concurso = st.text_input(
        "Qual concurso você está se preparando?",
        placeholder="Ex.: Banco do Brasil"
    )

    disciplinas_txt = st.text_area(
        "Quais disciplinas precisa estudar?",
        placeholder="Ex.: Português, Direito Constitucional, História",
        help="Separe as disciplinas por vírgula."
    )

    st.markdown("### 2. Sua disponibilidade")

    dias = st.multiselect(
        "Em quais dias da semana você pode estudar?",
        [
            "Segunda",
            "Terça",
            "Quarta",
            "Quinta",
            "Sexta",
            "Sábado",
            "Domingo"
        ],
        default=[
            "Segunda",
            "Terça",
            "Quarta",
            "Quinta",
            "Sexta"
        ]
    )

    horas_por_dia = st.number_input(
        "Quantas horas por dia?",
        min_value=0.5,
        max_value=12.0,
        value=3.0,
        step=0.5
    )

    periodo_preferido = st.selectbox(
        "Em qual período você prefere estudar?",
        [
            "Manhã",
            "Tarde",
            "Noite",
            "Flexível"
        ],
        help=(
            "O TutorIA utilizará essa preferência "
            "para distribuir os horários de estudo."
        )
    )

    st.markdown("### 3. Seu nível atual")

    nivel = st.selectbox(
        "Como avalia seu nível geral?",
        [
            "Iniciante",
            "Intermediário",
            "Avançado"
        ]
    )

    dificuldades = st.text_area(
        "Quais matérias ou assuntos são mais difíceis?",
        placeholder=(
            "Ex.: interpretação de texto, concordância, "
            "atos administrativos..."
        )
    )

    desempenho = st.text_area(
        "Como está seu desempenho em questões?",
        placeholder=(
            "Ex.: Português 70%, História 55%. "
            "Se ainda não sabe, deixe em branco."
        )
    )

    revisoes = st.selectbox(
        "Deseja incluir revisões no planejamento?",
        [
            "Sim, revisões frequentes",
            "Sim, revisões moderadas",
            "Não incluir por enquanto"
        ]
    )

    enviar = st.form_submit_button(
        "✨ Gerar proposta de planejamento",
        type="primary"
    )


if enviar:

    disciplinas = [
        item.strip()
        for item in disciplinas_txt.split(",")
        if item.strip()
    ]

    if not concurso.strip():
        st.error("Informe o concurso pretendido.")

    elif not disciplinas:
        st.error("Informe pelo menos uma disciplina.")

    elif not dias:
        st.error("Selecione pelo menos um dia disponível.")

    else:

        perfil = {
            "concurso": concurso.strip(),
            "disciplinas": disciplinas,
            "dias_disponiveis": dias,
            "horas_por_dia": horas_por_dia,
            "periodo_preferido": periodo_preferido,
            "nivel": nivel,
            "dificuldades": dificuldades.strip(),
            "desempenho": desempenho.strip(),
            "revisoes": revisoes
        }

        with st.spinner(
            "O TutorIA está elaborando sua proposta..."
        ):

            try:

                proposta = gerar_planejamento(perfil)

                erros = validar_planejamento(
                    proposta,
                    perfil
                )

                if erros:

                    st.error(
                        "A proposta não passou pela validação automática."
                    )

                    for erro in erros:
                        st.write(f"- {erro}")

                    st.session_state.proposta = None
                    st.session_state.perfil_atual = None

                else:

                    st.session_state.proposta = proposta
                    st.session_state.perfil_atual = perfil

                    st.success(
                        "Proposta gerada e validada. "
                        "Revise antes de aprovar."
                    )

            except (RuntimeError, ValueError) as erro:

                st.error(str(erro))

            except Exception as erro:

                st.error(
                    "Ocorreu um erro inesperado ao gerar "
                    "o planejamento."
                )

                st.caption(f"Detalhes técnicos: {erro}")


if st.session_state.proposta:

    proposta = st.session_state.proposta

    st.divider()

    st.header(
        proposta.get(
            "titulo",
            "Sua proposta de estudos"
        )
    )

    st.write(
        proposta.get("justificativa", "")
    )

    st.markdown("### Estratégia recomendada")

    st.write(
        proposta.get("estrategia", "")
    )

    for dia in proposta.get("dias", []):

        with st.expander(
            f"📅 {dia.get('dia', 'Dia')} — {dia.get('foco', '')}",
            expanded=True
        ):

            for sessao in dia.get("sessoes", []):

                st.markdown(
                    f"**{sessao.get('inicio', '')}–"
                    f"{sessao.get('fim', '')} | "
                    f"{sessao.get('disciplina', '')}**"
                )

                st.write(
                    f"Atividade: {sessao.get('atividade', '')}"
                )

                st.write(
                    f"Objetivo: {sessao.get('objetivo', '')}"
                )

                if sessao.get("observacao"):

                    st.caption(
                        sessao["observacao"]
                    )

    st.markdown("### Orientações gerais")

    for orientacao in proposta.get("orientacoes", []):
        st.write(f"- {orientacao}")

    st.warning(
        "Esta é uma proposta gerada por IA. "
        "Confira se os horários e a carga de estudos "
        "fazem sentido para sua rotina."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Aprovar e salvar planejamento",
            type="primary",
            use_container_width=True
        ):

            try:

                salvar_planejamento({
                    "perfil": st.session_state.perfil_atual,
                    "planejamento": proposta
                })

                st.session_state.proposta = None
                st.session_state.perfil_atual = None

                st.success(
                    "Planejamento aprovado e salvo com sucesso!"
                )

            except Exception as erro:

                st.error(
                    "Não foi possível salvar o planejamento."
                )

                st.caption(f"Detalhes técnicos: {erro}")

    with col2:

        if st.button(
            "🗑️ Descartar proposta",
            use_container_width=True
        ):

            st.session_state.proposta = None
            st.session_state.perfil_atual = None

            st.info(
                "Proposta descartada. "
                "Nenhum planejamento foi salvo."
            )
