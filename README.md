# Sistema de Estoque — Flask + SQLAlchemy

Sistema web de controle de estoque com cadastro de produtos, entrada/saída e relatórios. Feito para ser usado em empresas reais.

## Funcionalidades

- Autenticação com login e controle de acesso
- Cadastro de produtos com categorias e unidade de medida
- Entrada e saída de estoque com histórico rastreável
- Saldo calculado em tempo real (nunca armazenado diretamente)
- Alertas automáticos de estoque crítico
- Dashboard de relatórios com KPIs
- Exportação para Excel (.xlsx)
- Filtros e busca em todas as listas
- Paginação no histórico de movimentações
- Testes automatizados com pytest

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Web | Flask 3.x |
| Banco | SQLite (dev) / PostgreSQL (prod) |
| ORM | SQLAlchemy + Flask-Migrate |
| Auth | Flask-Login |
| Excel | openpyxl |
| Testes | pytest + pytest-flask |
| UI | Bootstrap 5 |

## Como rodar

```bash
# 1. Clone e entre na pasta
git clone https://github.com/Abnerrum/Projeto-Estoque
cd estoque

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env

# 5. Crie o banco e popule com dados de exemplo
flask --app run.py seed

# 6. Rode o servidor
python run.py
```

Acesse: http://localhost:5000

Login padrão: `admin@estoque.com` / `admin123`

## Rodar os testes

```bash
pytest tests/ -v
```

## Estrutura do projeto

```
estoque/
├── app/
│   ├── __init__.py          # Application Factory
│   ├── models/
│   │   ├── usuario.py
│   │   ├── produto.py       # inclui Categoria
│   │   └── movimentacao.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── produtos.py
│   │   ├── movimentacoes.py
│   │   └── relatorios.py
│   └── templates/
├── tests/
│   └── test_estoque.py
├── config.py
├── run.py                   # entrypoint + CLI seed
├── requirements.txt
└── .env.example
```

## Deploy em produção

1. Troque `SECRET_KEY` no `.env` por uma chave forte
2. Configure `DATABASE_URL` apontando para PostgreSQL
3. Rode `flask db upgrade` para aplicar migrations
4. Use Gunicorn: `gunicorn "run:app"` atrás de Nginx

## Licença

MIT
