"""
Safe Qdrant Upload Script with Duplicate Prevention

This script uploads embeddings to Qdrant with safeguards against duplicates.
"""

import json
import hashlib
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

# Configuration
QDRANT_URL = "http://localhost:6333"
BATCH_SIZE = 100  # Upload in batches of 100 points

def string_to_id(text: str) -> int:
    """Convert string ID to integer using hash (Qdrant requires int IDs for some operations)"""
    return int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2**63)

class QdrantUploader:
    def __init__(self, url: str = QDRANT_URL):
        self.client = QdrantClient(url=url)
        print(f"✓ Connected to Qdrant at {url}")
    
    def create_collection(self, collection_name: str, vector_size: int = 768, recreate: bool = False):
        """
        Create a Qdrant collection if it doesn't exist
        
        Args:
            collection_name: Name of the collection
            vector_size: Dimension of embeddings (768 for nomic-embed-code)
            recreate: If True, delete and recreate collection
        """
        if recreate:
            if self.client.collection_exists(collection_name):
                print(f"⚠️  Deleting existing collection: {collection_name}")
                self.client.delete_collection(collection_name)
        
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            print(f"✓ Created collection: {collection_name} (vector_size={vector_size})")
        else:
            print(f"✓ Collection already exists: {collection_name}")
    
    def check_source_exists(self, collection_name: str, source_file: str) -> bool:
        """
        Check if a source file already has data in the collection
        
        Args:
            collection_name: Name of the collection
            source_file: Source filename to check
            
        Returns:
            True if source file exists in collection
        """
        try:
            result = self.client.scroll(
                collection_name=collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="source",
                            match=MatchValue(value=source_file)
                        )
                    ]
                ),
                limit=1
            )
            return len(result[0]) > 0
        except Exception:
            return False
    
    def delete_source_data(self, collection_name: str, source_file: str):
        """
        Delete all points from a specific source file
        
        Args:
            collection_name: Name of the collection
            source_file: Source filename to delete
        """
        self.client.delete(
            collection_name=collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=source_file)
                    )
                ]
            )
        )
        print(f"  ✓ Deleted existing data for: {source_file}")
    
    def upload_embeddings(
        self,
        embeddings_file: Path,
        collection_name: str,
        mode: str = "upsert",
        check_duplicates: bool = True
    ):
        """
        Upload embeddings from JSONL file to Qdrant
        
        Args:
            embeddings_file: Path to JSONL embeddings file
            collection_name: Target collection name
            mode: 'upsert' (update/insert), 'skip' (skip if exists), 'replace' (delete then insert)
            check_duplicates: Whether to check for existing source files
        """
        print(f"\n{'='*60}")
        print(f"UPLOADING TO QDRANT")
        print(f"{'='*60}")
        print(f"File: {embeddings_file}")
        print(f"Collection: {collection_name}")
        print(f"Mode: {mode}")
        print(f"Check duplicates: {check_duplicates}")
        
        # Load embeddings
        embeddings = []
        with open(embeddings_file, 'r', encoding='utf-8') as f:
            for line in f:
                embeddings.append(json.loads(line))
        
        print(f"✓ Loaded {len(embeddings)} embeddings")
        
        # Check for duplicates by source file
        if check_duplicates and mode in ["skip", "replace"]:
            sources = set()
            for emb in embeddings:
                source = emb.get('metadata', {}).get('source')
                if source:
                    sources.add(source)
            
            print(f"\nChecking {len(sources)} unique source files...")
            
            for source in sources:
                exists = self.check_source_exists(collection_name, source)
                if exists:
                    if mode == "skip":
                        print(f"  ⊘ Skipping: {source} (already exists)")
                        # Remove from upload list
                        embeddings = [e for e in embeddings 
                                    if e.get('metadata', {}).get('source') != source]
                    elif mode == "replace":
                        print(f"  ♻️  Replacing: {source}")
                        self.delete_source_data(collection_name, source)
                else:
                    print(f"  ✓ New source: {source}")
        
        if not embeddings:
            print("\n⚠️  No embeddings to upload (all skipped or deleted)")
            return
        
        # Convert to PointStruct objects
        print(f"\nPreparing {len(embeddings)} points for upload...")
        points = []
        
        for idx, emb in enumerate(embeddings):
            # Extract fields
            chunk_id = emb.get('id', f"chunk_{idx}")
            text = emb.get('text', '')
            vector = emb.get('embedding', [])
            metadata = emb.get('metadata', {})
            
            # Create payload (metadata + text)
            payload = {
                "text": text,
                "source": metadata.get('source', 'unknown'),
                "subdir": metadata.get('subdir', ''),
                "collection": metadata.get('collection', collection_name),
                "chunk_index": metadata.get('chunk_index', idx),
                "indexed_at": datetime.now().isoformat()
            }
            
            # Add any additional metadata fields
            for key, value in metadata.items():
                if key not in payload:
                    payload[key] = value
            
            # Create point with integer ID
            point = PointStruct(
                id=string_to_id(chunk_id),
                vector=vector,
                payload=payload
            )
            points.append(point)
        
        # Upload in batches
        print(f"\nUploading in batches of {BATCH_SIZE}...")
        total_uploaded = 0
        
        for i in range(0, len(points), BATCH_SIZE):
            batch = points[i:i + BATCH_SIZE]
            self.client.upsert(
                collection_name=collection_name,
                points=batch
            )
            total_uploaded += len(batch)
            print(f"  Progress: {total_uploaded}/{len(points)} points uploaded "
                  f"({total_uploaded/len(points)*100:.1f}%)")
        
        # Verify
        collection_info = self.client.get_collection(collection_name)
        print(f"\n{'='*60}")
        print(f"✓ UPLOAD COMPLETED")
        print(f"{'='*60}")
        print(f"Collection: {collection_name}")
        print(f"Total points in collection: {collection_info.points_count}")
        print(f"Points uploaded: {total_uploaded}")
        print(f"{'='*60}\n")

def main():
    """Example usage"""
    uploader = QdrantUploader()
    
    # Example 1: Upload Viator embeddings (upsert mode - updates if exists)
    uploader.create_collection("viator_api", vector_size=768)
    uploader.upload_embeddings(
        embeddings_file=Path("output/viator_api/embeddings/viator_api_embeddings.jsonl"),
        collection_name="viator_api",
        mode="upsert",  # Will update existing points
        check_duplicates=True
    )
    
    # Example 2: Upload FastMCP embeddings (skip mode - don't upload duplicates)
    # uploader.create_collection("create_fast_mcp_with_api", vector_size=768)
    # uploader.upload_embeddings(
    #     embeddings_file=Path("output/fast_mcp_and_api/embeddings/create_fast_mcp_with_api_embeddings.jsonl"),
    #     collection_name="create_fast_mcp_with_api",
    #     mode="skip",  # Will skip if source already exists
    #     check_duplicates=True
    # )
    
    # Example 3: Upload Python SDK embeddings (replace mode - delete old, insert new)
    # uploader.create_collection("python_sdk_and_pydantic", vector_size=768)
    # uploader.upload_embeddings(
    #     embeddings_file=Path("output/python_sdk_and_pydantic/embeddings/python_sdk_and_pydantic_embeddings.jsonl"),
    #     collection_name="python_sdk_and_pydantic",
    #     mode="replace",  # Will delete old data from same source, then insert
    #     check_duplicates=True
    # )

if __name__ == "__main__":
    main()
