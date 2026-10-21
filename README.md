# goit-pycore-hw-05

## Setup

The bot (task 4) needs `colorama`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

All commands run from the repo root.

Tasks 1–2 (`caching_fibonacci`, `generator_numbers` / `sum_profit`):

```bash
python main.py
```

Task 3 (log analyzer), optional level as the second argument:

```bash
python -m hws.hw03 assets/hw03.log
python -m hws.hw03 assets/hw03.log error
```

Task 4 (assistant bot with `input_error` decorator):

```bash
python -m hws.hw04
```

`-m` runs a script as a module, so imports of `share.py` from the repo root work without `PYTHONPATH`.

Bot commands: `hello`, `add <name> <phone>`, `change <name> <phone>`, `phone <name>`, `all`, `exit` / `close`.
