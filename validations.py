from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import subprocess
import json
from backend.database import get_db
from backend.models.validation import ValidationResult
from backend.soda_core.generate_checks import generate_checks_yml

router = APIRouter()

@router.post("/run-validation/{table_name}")
def run_validation(table_name: str, db: Session = Depends(get_db)):
    """Runs Soda Core validation on a given table and stores results."""
    
    # Generate Soda Core checks.yml
    checks_file = generate_checks_yml(table_name)

    # Run Soda Core validation
    command = f"soda scan -d soda_analysis_db -c backend/soda_core/config.yml {checks_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Parse Soda Core output
    output_lines = result.stdout.split("\n")
    validation_results = []
    
    for line in output_lines:
        if "FAILED" in line or "PASSED" in line:
            parts = line.split()
            check_name = parts[0]  # Extract check name
            status = parts[-1]  # Extract PASSED/FAILED

            validation_result = ValidationResult(
                table_name=table_name,
                check_name=check_name,
                check_status=status,
                check_value=None  # Can extract from Soda output
            )
            db.add(validation_result)
            validation_results.append(validation_result)

    db.commit()
    
    return {"message": "Validation completed", "output": [v.check_name for v in validation_results]}


@router.get("/history/")
async def get_validation_history(db: Session = Depends(get_db)):
    """Fetch past validation results."""
    validations = db.query(ValidationResult).all()
    return [{"id": v.id, "table": v.table_name, "check": v.check_name, "status": v.check_status, "timestamp": v.timestamp} for v in validations]
