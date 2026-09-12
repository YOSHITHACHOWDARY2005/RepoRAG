from datetime import datetime
import uuid

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    repo_url: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )

    owner: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    branch: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )

    file_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    files = relationship(
        "RepositoryFile",
        back_populates="repository",
        cascade="all, delete-orphan",
    )

    chunks = relationship(
        "CodeChunk",
        back_populates="repository",
        cascade="all, delete-orphan",
    )


class RepositoryFile(Base):
    __tablename__ = "repository_files"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    repository_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    content_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    repository = relationship(
        "Repository",
        back_populates="files",
    )

    chunks = relationship(
        "CodeChunk",
        back_populates="file",
        cascade="all, delete-orphan",
    )


class CodeChunk(Base):
    __tablename__ = "code_chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    repository_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("repository_files.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    start_line: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    end_line: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(768),
        nullable=True,
    )

    chunk_metadata: Mapped[dict | None] = mapped_column(
        "metadata",
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    repository = relationship(
        "Repository",
        back_populates="chunks",
    )

    file = relationship(
        "RepositoryFile",
        back_populates="chunks",
    )