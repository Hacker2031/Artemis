# Guia de Implantação Técnica - Artemis ERP

Este documento estabelece o protocolo de configuração, instalação e execução do ecossistema Artemis ERP. O cumprimento rigoroso destas etapas é indispensável para a integridade operacional do sistema.

## 1. Requisitos de Sistema e Dependências

Para a operação estável do software, o ambiente de hospedagem deve possuir as seguintes especificações mínimas:

*   Interpretador Python: Versão 3.10 ou superior.
*   Sistema de Gestão de Base de Dados (SGBD): MySQL Server 8.0+.
*   Interface de Administração: MySQL Workbench (homologada para gestão de schemas).
*   Acesso à Internet: Necessário para a comunicação com as APIs do Google Gemini (Módulo Cronos).

---

## 2. Configuração da Camada de Dados (MySQL)

O Artemis ERP utiliza uma arquitetura relacional estruturada no MySQL. O ficheiro de dump da base de dados encontra-se localizado na raiz do projeto (ficheiro com extensão `.sql`).

### 2.1. Criação do Schema e Utilizador
1.  Aceda ao **MySQL Workbench** e estabeleça conexão com a instância local.
2.  Execute o comando SQL para criação do repositório:
    ```sql
    CREATE DATABASE artemis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```
3.  Certifique-se de que o utilizador administrativo possui as credenciais configuradas no `settings.py`:
    *   **Utilizador:** `root`
    *   **Palavra-passe:** `Artemis2025!`
    *   **Host:** `localhost`
    *   **Porta:** `3306`

### 2.2. Importação do Dump SQL
1.  No MySQL Workbench, aceda ao menu superior: `Server` > `Data Import`.
2.  Selecione a opção `Import from Self-Contained File`.
3.  Aponte para o ficheiro SQL localizado na raiz da pasta do projeto Artemis.
4.  Em `Default Target Schema`, selecione `artemis_db`.
5.  Clique em `Start Import`. Este processo restaurará toda a estrutura de tabelas, constrangimentos e dados iniciais necessários para a operação.

---

## 3. Preparação do Ambiente Virtual e Dependências (OPCIONAL)

A isolação de bibliotecas é opcional para evitar conflitos de versões no interpretador global.

### 3.1. Inicialização do Virtual Environment (VENV)
No terminal, posicionado na raiz do projeto, execute:
```powershell
# Criação do ambiente
python -m venv venv

# Ativação (Windows)
.\venv\Scripts\activate

# Ativação (Linux/macOS)
source venv/bin/activate
```

---

## 3. Preparação do Django

Para instalar as bibliotecas necessárias execute primeiro "cd artemis" para entrar na pasta do projecto.

Depois digite "python -m pip install -r requirements.txt"



---

## 4. Executando o Servidor

Para iniciar o ERP, utilize o comando:

```bash
python manage.py runserver  0.0.0.0:8000

```
*certifique-se que está dentro da pasta artemis (Artemis/artemis)*, que foi explicado no passo anterior. Caso contrário, receberá "no such file or directory". Yebo?
O sistema estará acessível através do navegador no endereço:
**http://127.0.0.1:8000**

E para qualquer outro dispositivo através do endereço IP do host, apontando para a porta 8000: **http://192.xxx.xxx.xxx:8000** (certifique-se de liberar a porta 8000 na firewall)
---

##  Módulo Cronos (IA)
Para que as funcionalidades de IA funcionem corretamente, certifique-se de que a sua `GOOGLE_API_KEY` está configurada no arquivo `.env` na raiz do projeto.


***IMPORTANTE!!!***

Este projecto e as suas dependências são, na sua integridade, propriedade da *WAGYUU Squad*. Qualquer uso sem a devida autorização dos proprietários poderá resultar em graves confrontos legislativos. Obrigado.