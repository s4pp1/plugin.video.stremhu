### Conda

A Python környezet kezeléséhez:

- `conda env create -p ./.conda -f environment.yaml` – Létrehozza a környezetet a helyi `.conda` mappába.
- `conda env update -p ./.conda -f environment.yaml --prune` – Frissíti a környezetet és törli a feleslegessé vált csomagokat.

### Kódminőség és típusellenőrzés (Linting & Typing)

- `basedpyright .` – Típusellenőrzés futtatása.
- `ruff check .` – Statikus kódellenőrzés (linter).
- `ruff check . --fix` – Kódhibák automatikus javítása.
- `ruff format .` – Kód formázása.
