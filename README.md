# 📦 Sistema de Gestão de Estoque (Django)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38bdf8)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)

Um sistema web completo para controle de estoque de pequenas empresas, focado em simplicidade, agilidade e inteligência de dados. Desenvolvido com **Django** e estilizado com **Tailwind CSS**.

## 📸 Screenshots

<img width="1916" height="911" alt="Screenshot_2" src="https://github.com/user-attachments/assets/90718559-3284-4e63-9161-78a6f7e8873a" />
<img width="1919" height="868" alt="Screenshot_1" src="https://github.com/user-attachments/assets/f9164b5a-5318-441a-a416-240165f22de0" />


## 🚀 Funcionalidades

### 📊 Dashboard Inteligente
- **KPIs em Tempo Real:** Visualização imediata do Total de Produtos, Quantidade de Itens e Valor Monetário em Estoque.
- **Gráficos:** Distribuição de estoque por categoria (Chart.js).
- **Alertas Visuais:** Itens com estoque baixo ou zerado são destacados automaticamente (Amarelo/Vermelho).

### 📦 Gestão de Produtos (CRUD)
- Cadastro completo de produtos com categorização.
- Cálculo automático de **Margem de Lucro (%)** e Lucro Líquido (R$).
- Edição e Exclusão segura de itens.

### 🔄 Controle de Movimentação (Entradas e Saídas)
- Registro de Entradas (Compras/Devoluções) e Saídas (Vendas/Perdas).
- **Validação de Estoque:** O sistema impede vendas se não houver saldo suficiente.
- Atualização automática do saldo do produto.

### 🛡️ Auditoria e Segurança
- **Login Obrigatório:** Acesso restrito a usuários autenticados.
- **Histórico Completo:** Rastreabilidade total. Saiba *quem* movimentou, *quanto* e *quando*.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, Django Framework
* **Banco de Dados:** SQLite (Padrão) / Expansível para PostgreSQL
* **Frontend:** HTML5, Tailwind CSS (via CDN), Chart.js
* **Ícones:** Heroicons (SVG)

## ⚙️ Como Rodar o Projeto Localmente

Pré-requisitos: Python instalado.

### 1. Clone o repositório
```bash
git clone [https://github.com/seu-usuario/gestao-estoque.git](https://github.com/seu-usuario/gestao-estoque.git)
cd gestao-estoque

2. Crie e ative um Ambiente Virtual (Windows)
PowerShell

python -m venv venv
.\venv\Scripts\activate
3. Instale as dependências
Bash

pip install django
# Ou se tiver o requirements.txt:
# pip install -r requirements.txt
4. Configure o Banco de Dados
Bash

python manage.py makemigrations
python manage.py migrate
5. Crie um Superusuário (Admin)
Para acessar o sistema, você precisa criar o primeiro login:

Bash

python manage.py createsuperuser
# Siga as instruções na tela (usuário, email e senha)
6. Inicie o Servidor
Bash

python manage.py runserver
Acesse no navegador: http://127.0.0.1:8000/

📂 Estrutura do Projeto
gestao-estoque/
├── estoque/            # App Principal
│   ├── migrations/     # Histórico do Banco de Dados
│   ├── templates/      # Arquivos HTML (Dashboard, Forms)
│   ├── admin.py        # Configuração do Painel Admin
│   ├── models.py       # Estrutura do Banco de Dados
│   ├── views.py        # Lógica do Sistema (Regras de Negócio)
│   └── forms.py        # Formulários
├── setup/              # Configurações do Projeto Django
│   ├── settings.py     # Configurações Globais
│   └── urls.py         # Rotas e Links
├── db.sqlite3          # Banco de Dados
└── manage.py           # Gerenciador de Comandos
