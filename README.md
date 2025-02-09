# goit-pythonweb-hw-06

# Run PostgreSQL in Docker

```bash
docker run --name db-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

```

# Run migrations

```bash
alembic revision --autogenerate -m "Add description"

alembic upgrade head
```

# Init Db

```bash
python seeds.py
```

# Run Queries

```bash
python my_select.py
```
