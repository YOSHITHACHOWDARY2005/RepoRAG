from app.database import SessionLocal
from app.services.repository_service import ingest_repository


def test_ingest_repository():
    db = SessionLocal()

    try:
        repository = ingest_repository(
            db,
            "https://github.com/pallets/flask"
        )

        assert repository.id is not None
        assert repository.owner == "pallets"
        assert repository.name == "flask"
        assert repository.file_count > 0
        assert repository.status == "completed"

    finally:
        db.close()