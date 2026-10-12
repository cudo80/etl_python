# Spotify ETL Pipeline

Este projeto é um pipeline ETL (Extract, Transform, Load) escrito em Python que interage com a API do Spotify. Ele extrai as últimas 50 músicas que você escutou nas últimas 24 horas, realiza verificações de qualidade e transformações de dados, e finalmente carrega essas informações em um banco de dados local SQLite (`my_played_tracks.sqlite`).

## 📌 Como funciona

O pipeline é composto por 3 etapas principais:
1. **Extract (`extract.py`)**: Conecta-se à API do Spotify, utilizando o seu `CLIENT_ID`, `CLIENT_SECRET` e `REFRESH_TOKEN` para gerar um *Access Token* válido de forma dinâmica. Em seguida, busca os dados da rota *"Recently Played"*.
2. **Transform (`transform.py`)**: Valida se o retorno não está vazio, não possui duplicatas e nem valores nulos. Depois, agrega os dados para contar quantas vezes você escutou determinado artista no dia.
3. **Load (`load.py`)**: Cria e insere os dados transformados e originais em duas tabelas diferentes no SQLite (`my_played_tracks` e `fav_artist`).

## ⚙️ Pré-requisitos e Configuração

Para executar este projeto, você precisa gerar credenciais de acesso na plataforma para desenvolvedores do Spotify.

### 1. Obtendo credenciais do Spotify
1. Acesse [Spotify for Developers](https://developer.spotify.com/) e faça login.
2. Crie um novo App.
3. Copie o **Client ID** e **Client Secret**.
4. Você também precisará gerar um **Refresh Token** inicial com o escopo `user-read-recently-played` (você pode fazer isso via Postman ou usando um script simples de autorização web).

### 2. Configurando o Ambiente
Copie o arquivo de exemplo de variáveis de ambiente e preencha com as suas credenciais:

```bash
cp .env.example .env
```
Edite o arquivo `.env` gerado:
```env
SPOTIFY_CLIENT_ID=seu_client_id_aqui
SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIFY_REFRESH_TOKEN=seu_refresh_token_aqui
```

## 🚀 Como Executar Localmente

### Opção 1: Usando Python Virtualenv (Recomendado)

Crie um ambiente virtual e instale as dependências:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Execute o processo principal do pipeline:
```bash
python load.py
```

### Opção 2: Usando Docker

Você pode rodar todo o pipeline dentro de um container Docker, sem se preocupar com dependências instaladas na sua máquina.

1. Construa a imagem:
```bash
docker build -t spotify-etl .
```

2. Execute o container:
```bash
docker run --env-file .env spotify-etl
```

## 🧪 Como rodar os Testes

Este projeto utiliza o `pytest` para testes unitários, fazendo o *mock* das chamadas à API para que não seja necessário se conectar ao Spotify durante os testes.

Para rodar a suíte de testes:
```bash
python -m pytest
```

## 📝 Logs

Todo o projeto utiliza o módulo nativo de `logging` do Python em vez de `print()`. Ao executar o script, os logs serão apresentados na tela e também salvos automaticamente no arquivo `etl_pipeline.log`.
