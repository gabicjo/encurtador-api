# Encurtador de Links API

API REST para encurtamento de URLs desenvolvida em Flask.

## Descrição

API simples e eficiente para criar URLs encurtadas, com suporte a códigos personalizados e статистика de cliques. Ideal para aplicações que precisam gerenciar links longos de forma organizada.

## Tecnologias Utilizadas

- **Python 3.12** - Linguagem de programação
- **Flask** - Framework web micro
- **Flask-CORS** - Suporte a CORS
- **SQLite** - Banco de dados leve
- **pytest** - Framework de testes

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd "Encurtador de links API"
```

2. Crie e ative um ambiente virtual (opcional mas recomendado):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate   # Windows
```

3. Instale as dependências:
```bash
pip install flask flask-cors
```

## Como Rodar

```bash
python app.py
```

O servidor estará disponível em `http://localhost:9284`

## Estrutura de Pastas

```
Encurtador de links API/
├── app.py                    # Ponto de entrada da aplicação
├── source/
│   ├── routes/              # Blueprints das rotas API
│   │   ├── encurtar_route.py
│   │   ├── redirect_route.py
│   │   └── stats_routes.py
│   ├── services/            # Lógica de negócio
│   │   ├── encurtar_service.py
│   │   ├── redirect_service.py
│   │   └── stats_service.py
│   ├── models/               # Modelos de banco de dados
│   │   ├── main_model.py
│   │   ├── encurtar_model.py
│   │   └── redirect_model.py
│   └── error_handler.py      # Exceções personalizadas
├── tests/                   # Arquivos de teste
└── AGENTS.md               # Instruções para agentes
```

## Como Usar

### Criar URL encurtada

**Endpoint:** `POST /encurtar`

**Request:**
```json
{
  "url": "https://exemplo.com/pagina/muito/longa"
}
```

**Response:**
```json
{
  "url": "http://localhost:9284/abc123xyz"
}
```

### Criar URL com código personalizado

**Endpoint:** `POST /encurtar`

**Request:**
```json
{
  "url": "https://exemplo.com",
  "code": "meulink"
}
```

**Regras:**
- Código deve ter no mínimo 3 caracteres
- Código deve ser único

**Response:**
```json
{
  "url": "http://localhost:9284/meulink"
}
```

### Redirecionar URL

**Endpoint:** `GET /<codigo>`

Acessar `http://localhost:9284/abc123xyz` redireciona para a URL original.

### Ver estatísticas de uma URL

**Endpoint:** `GET /stats/<codigo>`

**Response:**
```json
{
  "url_original": "https://exemplo.com",
  "clicks": 42
}
```

## Exemplos com cURL

```bash
# Criar URL encurtada
curl -X POST http://localhost:9284/encurtar \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# Criar URL com código personalizado
curl -X POST http://localhost:9284/encurtar \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com", "code": "gogle"}'

# Ver estatísticas
curl http://localhost:9284/stats/gogle
```

## Executando Testes

```bash
pytest -v
```

## Licença

MIT License