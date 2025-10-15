"""
Command-line interface for RAG system.

Provides commands for:
- Document ingestion (single and batch)
- Querying the knowledge base
- Managing collections
- System status and health checks

Usage:
    python -m src.cli ingest document <file>
    python -m src.cli ingest batch <directory>
    python -m src.cli query "<question>"
    python -m src.cli collections list
    python -m src.cli health
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint

# CLI app
cli = typer.Typer(
    name="rag-cli",
    help="RAG System Command-Line Interface",
    add_completion=False,
)

# Sub-commands
ingest_app = typer.Typer(help="Document ingestion commands")
collections_app = typer.Typer(help="Collection management commands")

cli.add_typer(ingest_app, name="ingest")
cli.add_typer(collections_app, name="collections")

# Rich console for output
console = Console()


# ============================================================================
# INGEST COMMANDS
# ============================================================================

@ingest_app.command("document")
def ingest_document(
    file_path: str = typer.Argument(..., help="Path to document file"),
    collection: Optional[str] = typer.Option(None, "--collection", "-c", help="Target collection name"),
    language: Optional[str] = typer.Option(None, "--language", "-l", help="Programming language (for code files)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress"),
):
    """
    Ingest a single document into the RAG system.
    
    Example:
        python -m src.cli ingest document myfile.pdf
        python -m src.cli ingest document code.py --collection python_code --language python
    """
    file = Path(file_path)
    
    if not file.exists():
        console.print(f"[red]Error:[/red] File not found: {file_path}")
        raise typer.Exit(code=1)
    
    console.print(Panel(
        f"[bold]Document Ingestion[/bold]\n"
        f"File: [cyan]{file.name}[/cyan]\n"
        f"Size: [yellow]{file.stat().st_size / 1024:.1f} KB[/yellow]\n"
        f"Collection: [green]{collection or 'auto-detect'}[/green]",
        title="RAG System",
        border_style="blue"
    ))
    
    # Run ingestion with progress
    asyncio.run(_ingest_document_async(file_path, collection, language, verbose))


async def _ingest_document_async(
    file_path: str,
    collection: Optional[str],
    language: Optional[str],
    verbose: bool
):
    """Async implementation of document ingestion."""
    
    try:
        # Import here to avoid circular dependencies
        from src.ingestion.ingest import DocumentIngestionPipeline
        from src.storage import initialize_chroma, close_chroma
        import os
        
        # Initialize services
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("Initializing services...", total=None)
            
            await initialize_chroma()
            
            progress.update(task, description="✓ Services initialized")
        
        # Create pipeline
        pipeline = DocumentIngestionPipeline()
        
        # Process document with progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            
            task = progress.add_task("[cyan]Processing document...", total=5)
            
            # Stage 1: Parse
            progress.update(task, description="[cyan]Parsing document", completed=1)
            if verbose:
                console.print("  → Extracting content with Docling...")
            
            # Stage 2: Chunk
            progress.update(task, description="[yellow]Chunking content", completed=2)
            if verbose:
                console.print("  → Splitting into semantic chunks...")
            
            # Stage 3: Embed
            progress.update(task, description="[magenta]Generating embeddings", completed=3)
            if verbose:
                console.print("  → Creating vector embeddings...")
            
            # Actually process the document
            result = await pipeline.process_document(
                file_path=file_path,
                collection_name=collection,
                metadata={
                    "language": language,
                    "source": "cli",
                }
            )
            
            # Stage 4: Store
            progress.update(task, description="[green]Storing in database", completed=4)
            if verbose:
                console.print("  → Saving to Chroma...")
            
            # Stage 5: Complete
            progress.update(task, description="[bold green]✓ Complete", completed=5)
        
        # Show results
        console.print("\n[bold green]✓ Document ingested successfully![/bold green]\n")
        
        result_table = Table(show_header=False, box=None)
        result_table.add_column("Property", style="cyan")
        result_table.add_column("Value", style="white")
        
        result_table.add_row("Document ID", result.get("document_id", "N/A"))
        result_table.add_row("Chunks Created", str(result.get("chunks_count", 0)))
        result_table.add_row("Collection", result.get("collection", "default"))
        result_table.add_row("Processing Time", f"{result.get('duration_seconds', 0):.2f}s")
        
        console.print(result_table)
        
        # Cleanup
        await close_chroma()
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {e}")
        import traceback
        if verbose:
            console.print(traceback.format_exc())
        raise typer.Exit(code=1)


@ingest_app.command("batch")
def ingest_batch(
    directory: str = typer.Argument(..., help="Directory containing documents"),
    pattern: str = typer.Option("*", "--pattern", "-p", help="File pattern (e.g., '*.pdf')"),
    collection: Optional[str] = typer.Option(None, "--collection", "-c", help="Target collection"),
    max_files: int = typer.Option(100, "--max", "-m", help="Maximum files to process"),
):
    """
    Batch ingest multiple documents from a directory.
    
    Example:
        python -m src.cli ingest batch ./documents
        python -m src.cli ingest batch ./pdfs --pattern "*.pdf" --collection research
    """
    dir_path = Path(directory)
    
    if not dir_path.exists() or not dir_path.is_dir():
        console.print(f"[red]Error:[/red] Directory not found: {directory}")
        raise typer.Exit(code=1)
    
    # Find files
    files = list(dir_path.glob(pattern))[:max_files]
    
    if not files:
        console.print(f"[yellow]No files found matching pattern: {pattern}[/yellow]")
        raise typer.Exit(code=0)
    
    console.print(Panel(
        f"[bold]Batch Ingestion[/bold]\n"
        f"Directory: [cyan]{directory}[/cyan]\n"
        f"Pattern: [yellow]{pattern}[/yellow]\n"
        f"Files found: [green]{len(files)}[/green]\n"
        f"Collection: [green]{collection or 'auto-detect'}[/green]",
        title="RAG System",
        border_style="blue"
    ))
    
    # Run batch ingestion
    asyncio.run(_ingest_batch_async(files, collection))


async def _ingest_batch_async(files: List[Path], collection: Optional[str]):
    """Async implementation of batch ingestion."""
    
    try:
        from src.ingestion.ingest import DocumentIngestionPipeline
        from src.storage import initialize_chroma, close_chroma
        import os
        
        # Initialize services
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Initializing services...", total=None)
            await initialize_chroma()
        
        # Process files
        pipeline = DocumentIngestionPipeline()
        
        completed = 0
        failed = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            
            batch_task = progress.add_task("[cyan]Processing files...", total=len(files))
            
            for file_path in files:
                try:
                    progress.update(batch_task, description=f"[cyan]Processing {file_path.name}")
                    
                    await pipeline.process_document(
                        file_path=str(file_path),
                        collection_name=collection,
                        metadata={"source": "cli_batch"}
                    )
                    
                    completed += 1
                    progress.update(batch_task, advance=1)
                    
                except Exception as e:
                    console.print(f"  [red]✗ Failed: {file_path.name} - {e}[/red]")
                    failed += 1
                    progress.update(batch_task, advance=1)
        
        # Show summary
        console.print("\n[bold]Batch Ingestion Complete[/bold]\n")
        
        summary_table = Table(show_header=False, box=None)
        summary_table.add_column("Status", style="cyan")
        summary_table.add_column("Count", style="white")
        
        summary_table.add_row("✓ Completed", f"[green]{completed}[/green]")
        summary_table.add_row("✗ Failed", f"[red]{failed}[/red]")
        summary_table.add_row("Total", str(len(files)))
        summary_table.add_row("Success Rate", f"{(completed/len(files)*100):.1f}%")
        
        console.print(summary_table)
        
        # Cleanup
        await close_chroma()
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(code=1)


# ============================================================================
# QUERY COMMAND
# ============================================================================

@cli.command("query")
def query_command(
    question: str = typer.Argument(..., help="Question to ask"),
    collection: Optional[str] = typer.Option(None, "--collection", "-c", help="Search in specific collection"),
    top_k: int = typer.Option(5, "--top-k", "-k", help="Number of results to retrieve"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed results"),
):
    """
    Query the RAG system with a natural language question.
    
    Example:
        python -m src.cli query "What is machine learning?"
        python -m src.cli query "Explain Python decorators" --collection python_code -k 10
    """
    console.print(Panel(
        f"[bold]Query[/bold]\n"
        f"Question: [cyan]{question}[/cyan]\n"
        f"Collection: [green]{collection or 'all'}[/green]\n"
        f"Top-K: [yellow]{top_k}[/yellow]",
        title="RAG System",
        border_style="blue"
    ))
    
    asyncio.run(_query_async(question, collection, top_k, verbose))


async def _query_async(question: str, collection: Optional[str], top_k: int, verbose: bool):
    """Async implementation of query."""
    
    try:
        from src.storage import initialize_chroma, close_chroma, get_chroma_client
        from src.ingestion.embedder import EmbeddingGenerator
        import os
        
        # Initialize
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Initializing...", total=None)
            await initialize_chroma()
        
        # Generate query embedding
        console.print("\n[cyan]Searching knowledge base...[/cyan]")
        
        embedder = EmbeddingGenerator()
        query_embedding = await embedder.embed_query(question)
        
        # Search
        chroma_client = get_chroma_client()
        results = chroma_client.search(
            collection_name=collection or "default",
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Display results
        console.print(f"\n[bold green]✓ Found {len(results)} results[/bold green]\n")
        
        for idx, result in enumerate(results, 1):
            console.print(f"[bold cyan]Result {idx}[/bold cyan]")
            console.print(f"[dim]Score: {result.get('score', 0):.4f}[/dim]")
            console.print(f"[dim]Source: {result.get('metadata', {}).get('source', 'N/A')}[/dim]\n")
            
            # Show content
            content = result.get("document", "")
            if len(content) > 200 and not verbose:
                content = content[:200] + "..."
            
            console.print(Panel(content, border_style="dim"))
            console.print()
        
        # Cleanup
        await close_chroma()
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(code=1)


# ============================================================================
# COLLECTIONS COMMANDS
# ============================================================================

@collections_app.command("list")
def list_collections():
    """
    List all available collections.
    
    Example:
        python -m src.cli collections list
    """
    asyncio.run(_list_collections_async())


async def _list_collections_async():
    """Async implementation of list collections."""
    
    try:
        from src.storage import initialize_chroma, close_chroma, get_chroma_client
        
        await initialize_chroma()
        chroma_client = get_chroma_client()
        
        collections = chroma_client.list_collections()
        
        if not collections:
            console.print("[yellow]No collections found[/yellow]")
            return
        
        console.print(f"\n[bold]Collections ({len(collections)})[/bold]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Name", style="cyan")
        table.add_column("Documents", justify="right", style="yellow")
        table.add_column("Category", style="green")
        
        for coll in collections:
            table.add_row(
                coll.get("name", "N/A"),
                str(coll.get("count", 0)),
                coll.get("metadata", {}).get("category", "general")
            )
        
        console.print(table)
        
        await close_chroma()
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(code=1)


# ============================================================================
# HEALTH COMMAND
# ============================================================================

@cli.command("health")
def health_check():
    """
    Check system health and service status.
    
    Example:
        python -m src.cli health
    """
    asyncio.run(_health_check_async())


async def _health_check_async():
    """Async implementation of health check."""
    
    try:
        from src.storage import initialize_chroma, get_chroma_client, close_chroma
        from src.storage.neo4j_client import initialize_neo4j_async, get_neo4j_client, close_neo4j_async, Neo4jConfig
        import os
        
        console.print("\n[bold]System Health Check[/bold]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Service", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Details", style="dim")
        
        # Check Chroma
        try:
            await initialize_chroma()
            chroma_client = get_chroma_client()
            if chroma_client and chroma_client._initialized:
                table.add_row("Chroma", "[green]✓ Connected[/green]", "Vector database")
            else:
                table.add_row("Chroma", "[yellow]⚠ Not initialized[/yellow]", "Vector database")
        except Exception as e:
            table.add_row("Chroma", "[red]✗ Error[/red]", str(e))
        
        console.print(table)
        
        # Cleanup
        try:
            await close_chroma()
        except:
            pass
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(code=1)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    cli()
