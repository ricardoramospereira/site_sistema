# Selecionando a imagem base Python 3.10 com Alpine por sua leveza e eficiência.
# Prefiro Alpine para manter minhas imagens Docker enxutas e rápidas.
FROM python:3.10-alpine

# Definindo '/app' como diretório de trabalho. Todos os comandos serão executados aqui.
# Isso ajuda a organizar melhor os arquivos dentro do contêiner.
WORKDIR /app

# Primeiro, copio o requirements.txt. Isso é estratégico para aproveitar o cache do Docker.
# Se as dependências não mudarem, o Docker não precisa reinstalá-las, agilizando o build.
COPY requirements.txt .

# Instalando as dependências do projeto. Uso --no-cache-dir para reduzir o tamanho da imagem.
# Sempre tento otimizar o tamanho das minhas imagens Docker.
RUN pip install --no-cache-dir -r requirements.txt

# Agora, copio o restante dos arquivos do projeto. É uma prática comum.
# Isso inclui meu código Python, templates, e arquivos estáticos.
COPY . .

# Configurando o comando padrão para iniciar o servidor Django.
# Optei por rodar na porta 3000 para variar das portas padrões.
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]

# Expondo a porta 3000. É mais uma nota para mim mesmo e outros desenvolvedores,
# já que ajuda a entender rapidamente em qual porta o serviço estará disponível.
EXPOSE 3000
