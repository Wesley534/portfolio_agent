from __future__ import annotations

import argparse
import hashlib
import logging
import os
import re
from pathlib import Path

from rag.chroma import VectorStore
from rag.embeddings import EmbeddingService

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-6s | %(message)s")
logger = logging.getLogger(__name__)


def split_into_chunks(text: str, max_chars: int = 512) -> list[str]:
    """Split markdown text into overlapping chunks by paragraphs."""
    # Split by double newlines (paragraphs)
    paragraphs = re.split(r"\n\s*\n", text.strip())
    chunks = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(current) + len(para) < max_chars:
            current = f"{current}\n\n{para}" if current else para
        else:
            if current:
                chunks.append(current)
            # If a single paragraph is too long, split by sentences
            if len(para) > max_chars:
                sentences = re.split(r"(?<=[.!?])\s+", para)
                current = ""
                for sent in sentences:
                    if len(current) + len(sent) < max_chars:
                        current = f"{current} {sent}" if current else sent
                    else:
                        if current:
                            chunks.append(current)
                        current = sent
            else:
                current = para

    if current:
        chunks.append(current)

    return [c.strip() for c in chunks if len(c.strip()) > 20]


def process_markdown_file(
    file_path: Path,
    category: str,
    source: str = "",
) -> list[tuple[str, dict, str]]:
    """Process a markdown file into (text, metadata, id) tuples."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title from first H1
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else file_path.stem

    chunks = split_into_chunks(content)
    results = []

    for i, chunk in enumerate(chunks):
        chunk_id = hashlib.md5(f"{file_path.name}:{i}".encode()).hexdigest()
        metadata = {
            "title": title,
            "category": category,
            "source": source or file_path.name,
            "chunk_index": i,
            "total_chunks": len(chunks),
        }
        results.append((chunk, metadata, chunk_id))

    return results


def build_index(knowledge_dir: str, output_dir: str) -> VectorStore:
    """Build the vector index from all markdown files in knowledge directory."""
    knowledge_path = Path(knowledge_dir)
    if not knowledge_path.exists():
        logger.warning("Knowledge directory '%s' does not exist", knowledge_dir)
        return VectorStore(persist_dir=output_dir)

    store = VectorStore(persist_dir=output_dir)

    # Delete existing collection to rebuild
    store.delete_collection()

    all_documents = []
    all_metadatas = []
    all_ids = []

    # Category mapping based on directory structure
    category_map = {
        "projects": "project",
        "certificates": "certificate",
        "case_studies": "case_study",
        "blogs": "blog",
    }

    # Process all markdown files recursively
    md_files = list(knowledge_path.rglob("*.md"))
    logger.info("Found %d markdown files in %s", len(md_files), knowledge_dir)

    for md_file in md_files:
        # Determine category from parent directory
        relative = md_file.relative_to(knowledge_path)
        parent_dir = relative.parent.name
        category = category_map.get(parent_dir, "general")

        results = process_markdown_file(md_file, category=category, source=str(relative))
        for text, metadata, chunk_id in results:
            all_documents.append(text)
            all_metadatas.append(metadata)
            all_ids.append(chunk_id)

    if all_documents:
        store.add_documents(all_documents, all_metadatas, all_ids)
        logger.info("Index built with %d chunks from %d files", len(all_documents), len(md_files))
    else:
        logger.warning("No documents found to index")

    return store


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build RAG index from knowledge base")
    parser.add_argument("--knowledge-dir", default="knowledge", help="Path to knowledge directory")
    parser.add_argument("--output-dir", default="index", help="Path to output index directory")
    args = parser.parse_args()

    store = build_index(args.knowledge_dir, args.output_dir)
    logger.info("Index built successfully with %d documents", store.get_document_count())
