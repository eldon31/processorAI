#!/usr/bin/env python3
"""Count actual chunks from existing chunked files"""

import json
from pathlib import Path

collections = [
    'viator_api',
    'fast_mcp_api_python',
    'fast_docs',
    'pydantic_docs',
    'inngest_ecosystem'
]

print('\n📊 ACTUAL CHUNK COUNTS FROM EXISTING FILES\n')
print(f"{'Collection':<30} {'Files':<8} {'Chunks':<10}")
print('=' * 55)

total_files = 0
total_chunks = 0

for coll in collections:
    chunked_path = Path(f'output/{coll}/chunked')
    
    if chunked_path.exists():
        files = list(chunked_path.glob('*.json'))
        chunk_count = sum(
            len(json.load(open(f, encoding='utf-8')))
            for f in files
        )
        total_files += len(files)
        total_chunks += chunk_count
        print(f'{coll:<30} {len(files):<8} {chunk_count:<10}')
    else:
        print(f'{coll:<30} {"N/A":<8} {"N/A":<10}')

print('=' * 55)
print(f'{"TOTAL":<30} {total_files:<8} {total_chunks:<10}')
print()
