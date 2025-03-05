import subprocess
import json
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.uploaded_file import UploadedFile
from backend.models.validation import Validation
from backend.soda_core.generate_checks import generate_checks_yml

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    """Upload a CSV file, store metadata, and run Soda Core validation."""
    file_location = f"backend/uploads/{file.filename}"

    # Save file locally
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Store file metadata in DB
    uploaded_file = UploadedFile(filename=file.filename)
    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)

    # Get table name (assuming it's the same as filename without extension)
    table_name = file.filename.split(".")[0]

    # Generate Soda Core checks.yml
    checks_path = generate_checks_yml(table_name)

    # Run Soda Core validation
    command = f"soda scan -d soda_analysis_db -c backend/soda_core/config.yml {checks_path}"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Parse Soda Core output
    soda_output = process.stdout
    status = "Failed" if "FAILED" in soda_output else "Passed"

    # Save validation results
    validation = Validation(asset_id=uploaded_file.id, status=status, details=json.loads(soda_output))
    db.add(validation)
    db.commit()

    return {"message": "File uploaded and validated!", "status": status}
