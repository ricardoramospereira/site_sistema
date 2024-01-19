# Nome do Projeto
Site-Sistema

## Status do Projeto
🚧 **Em Desenvolvimento** 🚧  
Este projeto está atualmente em desenvolvimento ativo. Estamos trabalhando para adicionar mais funcionalidades e melhorar a experiência do usuário. Fique à vontade para sugerir mudanças, reportar bugs ou contribuir com o projeto!
## Descrição
Este sistema integrado de site e fórum permite o registro de usuários, gerenciamento de contas, interação em um fórum de perguntas e respostas, e a criação de cartões de visita digitais. Ele oferece funcionalidades avançadas de administração de usuários e segurança de contas.

## Modelos do Banco de Dados

### Modelo `MyUser`
Este modelo representa os usuários do sistema. Ele estende a funcionalidade padrão do usuário do Django, adicionando campos personalizados e gerenciamento de usuários.

- **Campos**:
  - `username`: Nome de usuário único, derivado do email.
  - `email`: Endereço de email, usado como identificador único.
  - `first_name`: Primeiro nome do usuário.
  - `last_name`: Sobrenome do usuário.
  - `is_active`: Indica se o usuário está ativo.
  - `is_staff`: Define se o usuário tem permissões de staff.
  - `date_joined`: Data e hora em que o usuário se juntou.
  - `force_change_password`: Indica se o usuário precisa mudar a senha.

### Modelo `PostagemForum`
Modelo para gerenciar as postagens no fórum.

- **Campos**:
  - `usuario`: Relacionamento com o modelo `MyUser`.
  - `titulo`: Título da postagem.
  - `descricao`: Descrição ou conteúdo da postagem.
  - `data_publicacao`: Data de publicação da postagem.
  - `data_criacao`: Data e hora da criação da postagem.
  - `ativo`: Estado da postagem (ativa ou não).
  - `anexar_imagem`: Imagem anexada à postagem.
  - `slug`: Slug único para a postagem.

### Modelo `PostagemForumImagem`
Modelo para gerenciar imagens anexadas às postagens do fórum.

- **Campos**:
  - `imagem`: Campo de arquivo para o upload da imagem.
  - `postagem`: Relacionamento com o modelo `PostagemForum`.

### Modelo `PostagemForumComentario`
Modelo para gerenciar os comentários nas postagens do fórum.

- **Campos**:
  - `usuario`: Relacionamento com o modelo `MyUser`.
  - `postagem`: Relacionamento com o modelo `PostagemForum`.
  - `parent`: Relacionamento consigo mesmo para estruturar comentários em árvore.
  - `data_criacao`: Data e hora da criação do comentário.
  - `comentario`: Texto do comentário.

Cada modelo é projetado para atender às necessidades específicas do sistema, garantindo flexibilidade e eficiência na gestão de usuários, postagens e interações no fórum.


## Funcionalidades Principais
- **Registro e Aprovação de Usuário**: Cadastro com aprovação por administradores ou colaboradores e envio de senha inicial por e-mail.
- **Recuperação de Senha**: Funcionalidade de 'esqueceu sua senha' que envia um token para o e-mail do usuário para permitir a redefinição da senha.
- **Painel Administrativo**: Acesso exclusivo para administradores e colaboradores para gerenciar usuários e conteúdo do fórum.
- **Fórum de Perguntas e Respostas**: Um espaço interativo para perguntas e discussões entre os usuários.
- **Cartão de Visita Digital**: Personalizável por cada usuário, acessível através de um link único.

## Tecnologias Utilizadas
- **Backend**: Python com Django
- **Frontend**: Bootstrap com customizações em CSS

## Instalação e Configuração
Siga estes passos para configurar o ambiente de desenvolvimento:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/ricardoramospereira/site_sistema.git
   ```

Entre no diretório do projeto:
  ```bash
  cd [nome do diretório]
  ```

2. **Crie e ative um ambiente virtual** (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Linux ou macOS
   venv\Scripts\activate     # No Windows
   ```
   
3. **Instale as dependências**
   ```bash
    pip install -r requirements.txt
   ```

4. **Crie um arquivo .env copiando as informações do _env:**
   ```bash
    cp _env .env
   ```
5. **Execute as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```
6. **Crie um superusuário para acessar o painel administrativo:**
   ```bash
   python manage.py createsuperuser
   ```
7. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```
Versões das Tecnologias
- Python: 3.10.12
- Outras dependências estão listadas no arquivo requirements.txt.

Uso
Depois de instalar e configurar o sistema, você pode acessá-lo através do navegador em http://localhost:8000. Utilize as credenciais do superusuário criado para acessar o painel administrativo.
