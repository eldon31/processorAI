"""
Real chunking with Docling HybridChunker
Properly processes markdown with semantic chunking
"""

import json
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

def main():
    """Chunk one Inngest document using real Docling HybridChunker."""
    
    print("=" * 70)
    print("DOCLING HYBRID CHUNKER TEST")
    print("=" * 70)
    
    # 1. Read document
    doc_path = Path("Docs/inngest_overall/getting-started.md")
    
    if not doc_path.exists():
        # Find first available document
        inngest_docs = list(Path("Docs/inngest_overall").glob("*.md"))
        if not inngest_docs:
            print("❌ No Inngest documents found!")
            return
        doc_path = inngest_docs[0]
    
    print(f"\n📄 Reading: {doc_path}")
    print(f"   File size: {doc_path.stat().st_size:,} bytes")
    
    # 2. Convert with Docling
    print(f"\n🔄 Converting document with Docling...")
    converter = DocumentConverter()
    result = converter.convert(str(doc_path))
    
    # Get the DoclingDocument
    doc = result.document
    
    print(f"   ✅ Converted successfully")
    print(f"   Title: {doc.name}")
    print(f"   Pages: {len(list(doc.pages))}")
    
    # Get markdown content
    markdown_content = doc.export_to_markdown()
    print(f"   Markdown length: {len(markdown_content):,} characters")
    
    # 3. Chunk with HybridChunker
    print(f"\n✂️  Chunking with HybridChunker...")
    print(f"   Tokenizer: sentence-transformers/all-MiniLM-L6-v2")
    print(f"   Max tokens: 2048")
    print(f"   Heading split: True")
    
    chunker = HybridChunker(
        tokenizer="sentence-transformers/all-MiniLM-L6-v2",
        max_tokens=2048,
        merge_peers=True,
        heading_as_metadata=True
    )
    
    # Chunk the document
    chunk_iter = chunker.chunk(dl_doc=doc)
    chunks = list(chunk_iter)
    
    print(f"   ✅ Created {len(chunks)} chunks")
    
    # 4. Process chunks
    chunk_data = []
    for i, chunk in enumerate(chunks):
        chunk_info = {
            "index": i,
            "text": chunk.text,
            "meta": {
                "doc_items": [str(item) for item in chunk.meta.doc_items] if hasattr(chunk.meta, 'doc_items') else [],
                "headings": chunk.meta.headings if hasattr(chunk.meta, 'headings') else [],
            },
            "char_count": len(chunk.text),
            "token_count": len(chunk.text.split())  # Approximate
        }
        chunk_data.append(chunk_info)
    
    # 5. Save chunks to output directory
    output_dir = Path("output/chunks")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as JSON
    json_file = output_dir / f"{doc_path.stem}_docling_chunks.json"
    
    output_data = {
        "source": str(doc_path),
        "title": doc.name,
        "converter": "Docling DocumentConverter",
        "chunker": "HybridChunker",
        "config": {
            "tokenizer": "sentence-transformers/all-MiniLM-L6-v2",
            "max_tokens": 2048,
            "merge_peers": True,
            "heading_as_metadata": True
        },
        "num_chunks": len(chunks),
        "total_chars": sum(c["char_count"] for c in chunk_data),
        "chunks": chunk_data
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Save as readable text
    txt_file = output_dir / f"{doc_path.stem}_docling_chunks.txt"
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"Document: {doc.name}\n")
        f.write(f"Source: {doc_path}\n")
        f.write(f"Chunker: Docling HybridChunker\n")
        f.write(f"Total chunks: {len(chunks)}\n")
        f.write("=" * 70 + "\n\n")
        
        for chunk_info in chunk_data:
            f.write(f"CHUNK {chunk_info['index']}\n")
            f.write(f"Characters: {chunk_info['char_count']}\n")
            f.write(f"Tokens (approx): {chunk_info['token_count']}\n")
            if chunk_info['meta']['headings']:
                f.write(f"Headings: {chunk_info['meta']['headings']}\n")
            f.write("-" * 70 + "\n")
            f.write(chunk_info['text'])
            f.write("\n" + "=" * 70 + "\n\n")
    
    # 6. Show output locations
    print("\n" + "=" * 70)
    print("✅ CHUNKING COMPLETE WITH DOCLING!")
    print("=" * 70)
    print(f"\n📁 OUTPUT LOCATIONS:")
    print(f"\n1. JSON Format (with metadata):")
    print(f"   {json_file.absolute()}")
    print(f"   Size: {json_file.stat().st_size:,} bytes")
    
    print(f"\n2. Text Format (human-readable):")
    print(f"   {txt_file.absolute()}")
    print(f"   Size: {txt_file.stat().st_size:,} bytes")
    
    # 7. Show statistics
    print(f"\n📊 STATISTICS:")
    total_chars = sum(c['char_count'] for c in chunk_data)
    total_tokens = sum(c['token_count'] for c in chunk_data)
    avg_chunk_chars = total_chars / len(chunks)
    avg_chunk_tokens = total_tokens / len(chunks)
    
    print(f"   Total chunks: {len(chunks)}")
    print(f"   Total characters: {total_chars:,}")
    print(f"   Total tokens (approx): {total_tokens:,}")
    print(f"   Average chars/chunk: {avg_chunk_chars:.0f}")
    print(f"   Average tokens/chunk: {avg_chunk_tokens:.0f}")
    
    # 8. Preview first chunk with metadata
    print(f"\n📝 FIRST CHUNK PREVIEW:")
    first_chunk = chunk_data[0]
    print("-" * 70)
    if first_chunk['meta']['headings']:
        print(f"Headings: {first_chunk['meta']['headings']}")
        print("-" * 70)
    print(first_chunk['text'][:400] + "...")
    print("-" * 70)
    
    print(f"\n💡 These chunks are now ready for:")
    print(f"   1. Embedding with nomic-ai/nomic-embed-code")
    print(f"   2. Storing in Qdrant vector database")
    print(f"   Chunks saved in: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
