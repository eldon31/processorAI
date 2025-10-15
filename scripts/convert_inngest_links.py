"""
Convert Inngest documentation web links to markdown documents using Docling.
Reads URLs from Docs/inngest_overall/links.txt and creates markdown files in the same directory.
"""

import sys
from pathlib import Path
import asyncio
import re
from urllib.parse import urlparse

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from docling.document_converter import DocumentConverter


def url_to_filename(url: str) -> str:
    """
    Convert URL to a clean filename.
    
    Examples:
        https://www.inngest.com/docs/events -> events.md
        https://www.inngest.com/docs/features/events-triggers -> features_events-triggers.md
    """
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    
    # Remove 'docs/' prefix if present
    if path.startswith('docs/'):
        path = path[5:]
    elif path == 'docs':
        path = 'index'
    
    # Replace slashes with underscores
    filename = path.replace('/', '_') if path else 'index'
    
    # Add .md extension
    if not filename.endswith('.md'):
        filename = f"{filename}.md"
    
    return filename


async def convert_url_to_markdown(url: str, output_dir: Path) -> bool:
    """
    Convert a single URL to markdown using Docling.
    
    Args:
        url: URL to convert
        output_dir: Directory to save the markdown file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Converting: {url}")
        
        # Initialize converter
        converter = DocumentConverter()
        
        # Convert the URL
        result = converter.convert(url)
        
        # Get markdown content
        markdown_content = result.document.export_to_markdown()
        
        # Create filename from URL
        filename = url_to_filename(url)
        output_path = output_dir / filename
        
        # Save to file
        output_path.write_text(markdown_content, encoding='utf-8')
        
        print(f"✅ Saved: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to convert {url}: {e}")
        return False


async def main():
    """Main function to convert all links."""
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    links_file = base_dir / "Docs" / "inngest_overall" / "links.txt"
    output_dir = base_dir / "Docs" / "inngest_overall"
    
    # Check if links file exists
    if not links_file.exists():
        print(f"❌ Links file not found: {links_file}")
        return
    
    # Read all URLs
    print(f"Reading links from: {links_file}")
    urls = []
    with open(links_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and line.startswith('http'):
                urls.append(line)
    
    print(f"\n📚 Found {len(urls)} URLs to convert\n")
    print("=" * 60)
    
    # Convert each URL
    successful = 0
    failed = 0
    failed_urls = []
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processing...")
        success = await convert_url_to_markdown(url, output_dir)
        
        if success:
            successful += 1
        else:
            failed += 1
            failed_urls.append(url)
        
        # Small delay to avoid overwhelming the server
        await asyncio.sleep(0.5)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"\n📊 Conversion Summary:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 Output directory: {output_dir}")
    
    if failed_urls:
        print(f"\n⚠️  Failed URLs:")
        for url in failed_urls:
            print(f"   - {url}")
    
    print("\n🎉 Done!")


if __name__ == "__main__":
    asyncio.run(main())
