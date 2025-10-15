"""
Simple chunking test - no complex dependencies
Just chunks one markdown file and saves output to show you where it goes
"""

import json
from pathlib import Path

def simple_chunk(text: str, chunk_size: int = 2048, overlap: int = 100) -> list:
    """Simple text chunking without Docling."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]
        
        chunks.append({
            "index": len(chunks),
            "start_char": start,
            "end_char": min(end, len(text)),
            "content": chunk_text,
            "char_count": len(chunk_text)
        })
        
        start += (chunk_size - overlap)
    
    return chunks


def main():
    """Chunk one Inngest document and save output."""
    
    print("=" * 70)
    print("SIMPLE DOCUMENT CHUNKING TEST")
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
    content = doc_path.read_text(encoding='utf-8')
    
    # Extract title
    title = doc_path.stem
    for line in content.split('\n')[:10]:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    print(f"📝 Title: {title}")
    print(f"📊 Size: {len(content):,} characters")
    
    # 2. Chunk the document
    print(f"\n✂️  Chunking with:")
    print(f"   - Chunk size: 2048 chars")
    print(f"   - Overlap: 100 chars")
    
    chunks = simple_chunk(content, chunk_size=2048, overlap=100)
    
    print(f"\n✅ Created {len(chunks)} chunks")
    
    # 3. Save chunks to output directory
    output_dir = Path("output/chunks")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as JSON
    json_file = output_dir / f"{doc_path.stem}_chunks.json"
    
    chunk_data = {
        "source": str(doc_path),
        "title": title,
        "total_chars": len(content),
        "num_chunks": len(chunks),
        "chunks": chunks
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(chunk_data, f, indent=2, ensure_ascii=False)
    
    # Save as readable text
    txt_file = output_dir / f"{doc_path.stem}_chunks.txt"
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"Document: {title}\n")
        f.write(f"Source: {doc_path}\n")
        f.write(f"Total chunks: {len(chunks)}\n")
        f.write("=" * 70 + "\n\n")
        
        for chunk in chunks:
            f.write(f"CHUNK {chunk['index']}\n")
            f.write(f"Characters: {chunk['start_char']} - {chunk['end_char']}\n")
            f.write(f"Length: {chunk['char_count']}\n")
            f.write("-" * 70 + "\n")
            f.write(chunk['content'])
            f.write("\n" + "=" * 70 + "\n\n")
    
    # 4. Show output locations
    print("\n" + "=" * 70)
    print("✅ CHUNKING COMPLETE!")
    print("=" * 70)
    print(f"\n📁 OUTPUT LOCATIONS:")
    print(f"\n1. JSON Format (for programs):")
    print(f"   {json_file.absolute()}")
    print(f"   Size: {json_file.stat().st_size:,} bytes")
    
    print(f"\n2. Text Format (human-readable):")
    print(f"   {txt_file.absolute()}")
    print(f"   Size: {txt_file.stat().st_size:,} bytes")
    
    # 5. Show statistics
    print(f"\n📊 STATISTICS:")
    total_chars = sum(c['char_count'] for c in chunks)
    avg_chunk_size = total_chars / len(chunks)
    print(f"   Total chunks: {len(chunks)}")
    print(f"   Total characters: {total_chars:,}")
    print(f"   Average chunk size: {avg_chunk_size:.0f} chars")
    
    # 6. Preview first chunk
    print(f"\n📝 FIRST CHUNK PREVIEW:")
    print("-" * 70)
    print(chunks[0]['content'][:300] + "...")
    print("-" * 70)
    
    print(f"\n💡 Next step: Use these chunks for embedding and storing in Qdrant")
    print(f"   The chunks are now ready in: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
