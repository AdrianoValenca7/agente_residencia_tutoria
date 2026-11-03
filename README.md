# TutorIA — Agente Inteligente de Preparação para Concursos Públicos

O **TutorIA** é um agente inteligente desenvolvido para auxiliar pessoas que estão se preparando para concursos públicos. A proposta é oferecer um ambiente de apoio aos estudos, ajudando o candidato a organizar sua rotina, compreender conteúdos, praticar questões e acompanhar seu próprio desenvolvimento.

O projeto utiliza inteligência artificial para oferecer orientações e atividades de estudo adaptadas às necessidades e ao desempenho do estudante.

## 👥 Integrantes — Grupo 03

- **Adriano Valença**
- **Caio Lucas Laurindo**
- **Josielly Santos**
- **Yasmin Marcelly**
- **Hallysson Silva**

## 🎯 Objetivo do projeto

O TutorIA busca tornar a preparação para concursos públicos mais organizada, direcionada e eficiente.

Muitos candidatos enfrentam dificuldades para distribuir as disciplinas ao longo da semana, identificar seus principais pontos fracos e transformar os erros cometidos em oportunidades de aprendizagem.

A proposta é utilizar um agente de inteligência artificial para apoiar esse processo, oferecendo acompanhamento e atividades de acordo com as informações fornecidas pelo estudante.

## 💡 Funcionalidades propostas

O projeto prevê os seguintes módulos:

- **Planejamento de estudos:** criação de cronogramas personalizados conforme disponibilidade, disciplinas e dificuldades do estudante.
- **Explicação de conteúdos:** apoio na compreensão de assuntos cobrados em concursos públicos.
- **Geração de questões:** elaboração de questões originais inspiradas no estilo das bancas examinadoras.
- **Correção comentada:** análise das respostas, explicação dos erros e comentários sobre as alternativas.
- **Caderno de erros:** registro dos assuntos e dificuldades identificados durante os exercícios.
- **Revisão direcionada:** recomendação de revisões com base no desempenho do estudante.

> **Estado atual do MVP:** o módulo de planejamento de estudos está implementado. Os demais módulos fazem parte da evolução planejada do projeto.

## 🧠 Como o TutorIA funciona?

O funcionamento proposto segue um ciclo de acompanhamento:

1. **Compreender:** coleta informações sobre o concurso, disciplinas, disponibilidade e dificuldades do estudante.
2. **Planejar:** utiliza inteligência artificial para elaborar um planejamento de estudos.
3. **Executar:** orienta o estudante na realização das atividades propostas.
4. **Observar:** considera os resultados e as dificuldades apresentadas.
5. **Ajustar:** utiliza as informações obtidas para orientar melhorias no planejamento.

## 🏗️ Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento da aplicação.
- **Streamlit:** criação da interface interativa.
- **Google Gemini API:** integração com o modelo de inteligência artificial.
- **Google GenAI SDK:** comunicação com os modelos Gemini.
- **JSON:** armazenamento de informações e dados da aplicação.
- **Git e GitHub:** controle de versão e gerenciamento do código-fonte.

## 📁 Estrutura do projeto

```text
agente_residencia_tutoria/
│
├── agente/
│   ├── __init__.py
│   └── instrucoes.py
│
├── dados/
│   └── .gitkeep
│
├── modulos/
│   ├── __init__.py
│   └── planejador.py
│
├── servicos/
│   ├── __init__.py
│   └── armazenamento.py
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Instalação e execução

### 1. Pré-requisitos

- Python instalado.
- Git instalado.
- Uma chave de API do Google Gemini.

### 2. Clonar o repositório

```bash
git clone https://github.com/AdrianoValenca7/agente_residencia_tutoria.git
```

### 3. Entrar na pasta do projeto

```bash
cd agente_residencia_tutoria
```

### 4. Criar um ambiente virtual

```bash
python -m venv .venv
```

### 5. Ativar o ambiente virtual

No Windows:

```powershell
.venv\Scripts\Activate
```

### 6. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 7. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto, utilizando o `.env.example` como referência.

Configure sua chave de API e o modelo Gemini utilizado pela aplicação:

```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-3.5-flash-lite
```

**Importante:** não compartilhe sua chave de API e não envie o arquivo `.env` para o GitHub.

### 8. Executar a aplicação

```bash
streamlit run app.py
```

Após a execução, o Streamlit disponibilizará o endereço local para acessar a aplicação pelo navegador.

## 🔐 Segurança e responsabilidade

O projeto adota alguns cuidados importantes:

- A chave de API deve permanecer em variável de ambiente.
- Arquivos com informações locais dos estudantes não devem ser enviados ao repositório.
- O estudante mantém a supervisão sobre seu planejamento.
- O sistema deve informar quando não possuir informações suficientes para responder.
- As questões geradas pela inteligência artificial são originais e inspiradas no estilo das bancas, não devendo ser apresentadas como questões oficiais.

## 🚀 Próximos passos

Entre as evoluções previstas estão:

- Desenvolver os módulos de explicação, questões e correção.
- Implementar o caderno de erros e as revisões direcionadas.
- Ampliar o acompanhamento do desempenho do estudante.
- Aprimorar a personalização das recomendações.
- Realizar testes funcionais e avaliar a qualidade das respostas do agente.

## 📌 Considerações finais

O TutorIA propõe utilizar a inteligência artificial como ferramenta de apoio à preparação para concursos públicos, oferecendo uma experiência de estudo mais organizada, personalizada e orientada à evolução do estudante.

**TutorIA — Estude com estratégia. Evolua com inteligência.**