📦 Sistema de Gestão de Estoque & ERP

Um sistema web completo para controle de estoque, focado em usabilidade, segurança e inteligência de dados. Desenvolvido com a stack moderna do Django.

📸 Visão Geral

O sistema resolve o problema de planilhas desorganizadas, oferecendo uma interface limpa para controle de entradas, saídas e análise financeira.

✨ Funcionalidades Principais

📊 Dashboard Executivo: KPIs em tempo real, gráficos de distribuição e alertas visuais de estoque baixo.

📦 Gestão de Produtos: Cadastro completo com Upload de Fotos, categorização e cálculo automático de Margem de Lucro (%).

🔄 Controle de Movimentações: Entradas e Saídas com validação de saldo (impede venda sem estoque).

🛡️ Segurança: Sistema de Login/Logout, criptografia de senhas e níveis de acesso.

📂 Relatórios: Geração de PDFs prontos para impressão com resumo financeiro.

🎨 UX/UI Profissional:

Menu lateral escuro (Estilo SaaS).

Notificações flutuantes (Toast) para feedback de ações.

Confirmação de exclusão com modais animados (SweetAlert2).

🛠️ Tecnologias

Backend: Python, Django Framework

Banco de Dados: SQLite (Dev) / PostgreSQL (Prod)

Frontend: HTML5, Tailwind CSS, Chart.js (Gráficos), SweetAlert2 (Alertas)

Admin: Django Jazzmin (Tema Dark/Azul Personalizado)

Extras: Pillow (Imagens), xhtml2pdf (Relatórios)

🚀 Como Rodar Localmente

Clone o repositório:

git clone [https://github.com/SEU-USUARIO/gestao-estoque.git](https://github.com/SEU-USUARIO/gestao-estoque.git)
cd gestao-estoque


Crie um ambiente virtual:

python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows


Instale as dependências:

pip install -r requirements.txt


Configure o Banco de Dados:

python manage.py migrate
python manage.py createsuperuser


Rode o servidor:

python manage.py runserver


Acesse: http://127.0.0.1:8000

🌐 Deploy

O projeto está configurado para deploy no Render.com utilizando gunicorn e whitenoise para arquivos estáticos.

Conecte o repo no Render.

Build Command: ./build.sh

Start Command: gunicorn setup.wsgi:application

Desenvolvido por [Seu Nome] 🚀
