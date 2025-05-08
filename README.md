# Projeto Integrador III - Univesp

Este repositório contém o projeto desenvolvido para o **Projeto Integrador III** da **Univesp**. O principal objetivo deste projeto é construir uma aplicação web que integre diversas tecnologias, incluindo banco de dados, scripts web com **JavaScript**, **Nuvem**, consumo de **APIs**, **Acessibilidade**, controle de versão, Testes e **Análise de dados**.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Colaboradores](#colaboradores)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar o Projeto](#como-executar-o-projeto)

## 📝 Sobre o Projeto

Este projeto tem como foco a criação de uma aplicação web funcional e prática, projetada para exercitar e aplicar os conhecimentos adquiridos durante a formação acadêmica. O sistema proporciona uma interface amigável que permite a realização de operações **CRUD** (Criar, Ler, Atualizar e Deletar), alinhada com as melhores práticas de **Desenvolvimento Web** em **Python** e **Django**.

### Funcionalidades Principais:

- **Criação de Modelos (Models):** Estruturação de dados utilizando o ORM do Django.
- **Manipulação de URLs e Views:** Mapeamento e controle de rotas para diferentes partes do sistema.
- **Autenticação de Usuários:** Login e logout seguros com controle de acesso baseado em perfil.
- **Integração com Banco de Dados:** Uso de banco de dados para armazenamento e recuperação de informações.
- **Cadastro de Professores e Alunos:** Interface separada para gerenciar usuários com diferentes permissões.
- **Agendamento de Aulas:** Professores e alunos podem agendar sessões com data, hora, valor e descrição.
- **Cancelamento de Aulas:** Usuários podem cancelar treinos, mantendo o histórico visível.
- **Edição Segura de Treinos:** Apenas quem criou ou participa do treino pode editá-lo.
- **Filtros Dinâmicos com Bootstrap:** Visualização de aulas passadas, futuras, canceladas ou todas.
- **Templates Responsivos:** Interface construída com Bootstrap 5, focada em usabilidade.
- **Validação de Formulários:** Backend e frontend preparados para evitar erros de entrada de dados.
- **Acessibilidade e Navegação Amigável:** Atalhos de teclado, responsividade e controle de fonte inclusos.
- **Mensagens de Feedback:** Sistema de mensagens que informa ações como sucesso, erro e validações.
- **Análise de dados:** Utilização da biblioteca Bokeh para implementação da Visualização de Dados para relatórios financeiros.

## 👥 Colaboradores

- [Bianca Fileto](https://github.com/bifileto)
- [Caroline Bianca Santos Tancredi Molina](link_do_github)
- [Eduardo Luiz De Oliveira](link_do_github)
- [Gustavo Santos](https://github.com/Gustavo-Santos2)
- [Jonathan De Oliveira](https://github.com/jonathandeoliveira)
- [Marcio Sampaio](https://github.com/marciosampaioabc)
- [Miguel Angelo Tancredi Molina](link_do_github)
- [Vanderson Balieiro](https://github.com/VandersonB)

## 🚀 Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

- **[Python](https://www.python.org/)** - Linguagem de Programação
- **[Django](https://www.djangoproject.com/)** - Framework Web
- **[SQLite](https://www.sqlite.org/index.html)** - Banco de Dados
- **[HTML5](https://developer.mozilla.org/pt-BR/docs/Web/HTML)** - Linguagem de Marcação
- **[CSS3](https://developer.mozilla.org/pt-BR/docs/Web/CSS)** - Estilização
- **[JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)** - Linguagem de Programação para Interatividade
- **[Bootstrap](https://getbootstrap.com/)** - Framework web que utiliza HTML, CSS e JavaScript para Design Responsivo
- **[Bokeh](https://bokeh.org/)** - Biblioteca Python para visualização de dados interativa em navegadores web

## 💻 Pré-requisitos

Antes de começar, certifique-se de que você tem o **Python** instalado em sua máquina. Você pode baixar a versão mais recente [aqui](https://www.python.org/downloads/).

Além disso, será necessário instalar todas as dependências do projeto, que estão listadas no arquivo `requirements.txt`. Veja como fazer isso na seção abaixo.

## ▶️ Como Executar o Projeto

Siga os passos abaixo para executar o projeto localmente:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/jonathandeoliveira/PJI-240.git
   ```

2. **Acesse o diretório do projeto**:
   ```bash
   cd PJI-240
   ```

3. **Crie e ative um ambiente virtual (opcional, mas recomendado)**:
   - No Windows:
     ```bash
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - No Unix/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

4. **Instale as dependências do projeto**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute as migrações do banco de dados**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Inicie o servidor de desenvolvimento**:
   ```bash
   python manage.py runserver
   ```
   * Atenção:
    - A Secret key encontra-se com os desenvolvedores.
    - As funcionalidades podem ser atualizadas.
