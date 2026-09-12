from app.services.chunking_service import chunk_text


def test_empty_content_returns_no_chunks():
    chunks = chunk_text("")

    assert chunks == []


def test_small_content_creates_one_chunk():
    content = "\n".join(
        f"line {i}"
        for i in range(1, 11)
    )

    chunks = chunk_text(
        content,
        chunk_size=80,
        overlap=20,
    )

    assert len(chunks) == 1
    assert chunks[0].start_line == 1
    assert chunks[0].end_line == 10


def test_large_content_creates_overlapping_chunks():
    content = "\n".join(
        f"line {i}"
        for i in range(1, 201)
    )

    chunks = chunk_text(
        content,
        chunk_size=80,
        overlap=20,
    )

    assert len(chunks) == 3

    assert chunks[0].start_line == 1
    assert chunks[0].end_line == 80

    assert chunks[1].start_line == 61
    assert chunks[1].end_line == 140

    assert chunks[2].start_line == 121
    assert chunks[2].end_line == 200


def test_chunk_indexes_are_sequential():
    content = "\n".join(
        f"line {i}"
        for i in range(1, 201)
    )

    chunks = chunk_text(
        content,
        chunk_size=80,
        overlap=20,
    )

    assert [chunk.chunk_index for chunk in chunks] == [0, 1, 2]


def test_invalid_overlap_raises_error():
    content = "line 1\nline 2"

    try:
        chunk_text(
            content,
            chunk_size=20,
            overlap=20,
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "overlap must be smaller than chunk_size"