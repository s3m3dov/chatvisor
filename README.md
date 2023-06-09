# Smartbot

Smart Bot with lots of abilities.

## Dependencies

- Python 3.11
- PostgresSQL
- [langchain](https://github.com/hwchase17/langchain)
- OpenAI
- Stripe
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [colorlog](https://github.com/borntyping/python-colorlog)
- alembic
- SQLAlchemy
- SQLAlchemy-Mixins

## Set-up

### Set-up Notes

- [Poetry Installation](https://python-poetry.org/docs/#installation)
- [Poetry Basic Usage](https://python-poetry.org/docs/basic-usage/)
- [Alembic Basic Usage](https://simplyprashant.medium.com/how-to-use-alembic-for-your-database-migrations-d3e93cacf9e8)
- [Alembic Full Guide](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

### Set-up Steps

Clone repository

```bash
git clone git@github.com:s3m3dov/smartbot.git
```

Use poetry env

```bash
poetry env use python3.11
```

Install dependencies

```bash
poetry install
```

Run migrations

```bash
python -m alembic upgrade head
```

## Run

Start telegram bot

```bash
python start_telegram_bot.py
```

Start API server

```bash
python start_api_server.py
```

Stripe Webhook

```bash
stripe listen --forward-to localhost:8000/stripe/webhook
```