from app.database import SessionLocal
from app.services.embedding_repository_service import embed_all_chunks


db = SessionLocal()

try:
    count = embed_all_chunks(db, batch_size=10)
    print(f"Embedded {count} chunks successfully.")

finally:
    db.close()