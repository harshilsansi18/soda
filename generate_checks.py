from sqlalchemy import inspect
from backend.database import SessionLocal

def get_table_columns(table_name):
    """Fetch column names dynamically from PostgreSQL for a given table."""
    db = SessionLocal()
    try:
        inspector = inspect(db.bind)
        columns = [col["name"] for col in inspector.get_columns(table_name)]
        return columns
    finally:
        db.close()

def generate_checks_yml(table_name):
    """Generate Soda Core `checks.yml` file dynamically."""
    columns = get_table_columns(table_name)
    if not columns:
        raise ValueError(f"Table {table_name} not found in the database!")

    checks_yml = f"checks for {table_name}:\n"
    for column in columns:
        checks_yml += f"  - missing_count({column}) = 0\n"
        checks_yml += f"  - duplicate_count({column}) = 0\n"

    checks_path = f"backend/soda_core/{table_name}_checks.yml"
    with open(checks_path, "w") as file:
        file.write(checks_yml)

    return checks_path
