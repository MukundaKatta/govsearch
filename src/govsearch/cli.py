"""Command-line interface for GOVSEARCH."""

from __future__ import annotations

from datetime import date

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from govsearch.analyzer.citation import CitationTracker
from govsearch.analyzer.summarizer import DocumentSummarizer
from govsearch.analyzer.timeline import TimelineBuilder
from govsearch.documents.database import DocumentDatabase
from govsearch.documents.types import DocumentType, Jurisdiction
from govsearch.models import SearchQuery
from govsearch.report import ReportGenerator
from govsearch.search.engine import SearchEngine

console = Console()


def _build_engine() -> SearchEngine:
    """Build a search engine with the sample database."""
    db = DocumentDatabase(load_samples=True)
    return SearchEngine(database=db)


@click.group()
@click.version_option(version="0.1.0", prog_name="govsearch")
def cli() -> None:
    """GOVSEARCH - AI-powered public records search for government documents."""


@cli.command()
@click.argument("query")
@click.option("--type", "doc_type", help="Filter by document type (legislation, regulation, court_ruling, executive_order, budget, report)")
@click.option("--agency", help="Filter by issuing agency")
@click.option("--jurisdiction", help="Filter by jurisdiction (federal, state, local)")
@click.option("--after", "date_from", help="Filter documents published after date (YYYY-MM-DD)")
@click.option("--before", "date_to", help="Filter documents published before date (YYYY-MM-DD)")
@click.option("--max-results", default=10, help="Maximum number of results")
def search(
    query: str,
    doc_type: str | None,
    agency: str | None,
    jurisdiction: str | None,
    date_from: str | None,
    date_to: str | None,
    max_results: int,
) -> None:
    """Search government documents by keyword."""
    engine = _build_engine()

    parsed_type = None
    if doc_type:
        try:
            parsed_type = DocumentType.from_string(doc_type)
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            return

    parsed_jurisdiction = None
    if jurisdiction:
        try:
            parsed_jurisdiction = Jurisdiction(jurisdiction.lower())
        except ValueError:
            console.print(f"[red]Invalid jurisdiction: {jurisdiction}[/red]")
            return

    parsed_from = _parse_date(date_from) if date_from else None
    parsed_to = _parse_date(date_to) if date_to else None

    search_query = SearchQuery(
        query_text=query,
        doc_type=parsed_type,
        agency=agency,
        jurisdiction=parsed_jurisdiction,
        date_from=parsed_from,
        date_to=parsed_to,
        max_results=max_results,
    )

    results = engine.search(search_query)

    if not results:
        console.print(f"[yellow]No results found for '{query}'[/yellow]")
        return

    table = Table(title=f"Search Results: '{query}'", show_lines=True)
    table.add_column("ID", style="cyan", width=10)
    table.add_column("Title", style="bold", width=40)
    table.add_column("Type", width=16)
    table.add_column("Agency", width=20)
    table.add_column("Date", width=12)
    table.add_column("Score", justify="right", width=8)

    for result in results:
        doc = result.document
        table.add_row(
            doc.doc_id,
            doc.title,
            doc.doc_type.display_name,
            doc.agency,
            str(doc.date_published),
            f"{result.score:.4f}",
        )

    console.print(table)
    console.print(f"\n[dim]{len(results)} results shown[/dim]")


@cli.command()
@click.argument("doc_id")
def analyze(doc_id: str) -> None:
    """Analyze a specific document by its ID."""
    engine = _build_engine()
    doc = engine.database.get(doc_id)

    if doc is None:
        console.print(f"[red]Document not found: {doc_id}[/red]")
        return

    summarizer = DocumentSummarizer()
    summary = summarizer.summarize(doc)
    key_points = summarizer.key_points(doc)

    panel = Panel(
        f"[bold]{doc.title}[/bold]\n\n"
        f"[cyan]ID:[/cyan] {doc.doc_id}\n"
        f"[cyan]Type:[/cyan] {doc.doc_type.display_name}\n"
        f"[cyan]Agency:[/cyan] {doc.agency}\n"
        f"[cyan]Jurisdiction:[/cyan] {doc.jurisdiction.value}\n"
        f"[cyan]Status:[/cyan] {doc.status.value}\n"
        f"[cyan]Published:[/cyan] {doc.date_published}\n"
        f"[cyan]Tags:[/cyan] {', '.join(doc.tags)}",
        title="Document Details",
    )
    console.print(panel)

    console.print("\n[bold]Summary[/bold]")
    console.print(summary)

    if key_points:
        console.print("\n[bold]Key Points[/bold]")
        for point in key_points:
            console.print(f"  - {point}")


@cli.command()
@click.argument("doc_id")
def citations(doc_id: str) -> None:
    """Show citation graph for a document."""
    engine = _build_engine()
    doc = engine.database.get(doc_id)

    if doc is None:
        console.print(f"[red]Document not found: {doc_id}[/red]")
        return

    tracker = CitationTracker(engine.database.all_documents())

    outgoing = tracker.get_outgoing_citations(doc_id)
    incoming = tracker.get_incoming_citations(doc_id)

    console.print(f"\n[bold]Citations for {doc.title}[/bold]\n")

    if outgoing:
        table = Table(title="Outgoing References (this document cites)")
        table.add_column("Target", style="cyan")
        table.add_column("Title")
        table.add_column("Context", width=50)
        for cite in outgoing:
            table.add_row(cite.target_doc_id, cite.target_title, cite.context[:50])
        console.print(table)
    else:
        console.print("[dim]No outgoing references found.[/dim]")

    if incoming:
        table = Table(title="\nIncoming Citations (cited by)")
        table.add_column("Source", style="cyan")
        table.add_column("Context", width=60)
        for cite in incoming:
            table.add_row(cite.source_doc_id, cite.context[:60])
        console.print(table)
    else:
        console.print("[dim]No incoming citations found.[/dim]")

    co_cited = tracker.find_co_cited(doc_id)
    if co_cited:
        console.print(f"\n[bold]Co-cited documents:[/bold] {', '.join(co_cited[:5])}")


@cli.command()
@click.argument("topic")
def timeline(topic: str) -> None:
    """Build a timeline of documents related to a topic."""
    engine = _build_engine()
    builder = TimelineBuilder(engine.database.all_documents())

    # Try as doc_id first, then as topic
    doc = engine.database.get(topic)
    if doc:
        events = builder.build_timeline(topic)
        title = f"Timeline: {doc.title}"
    else:
        events = builder.build_topic_timeline(topic)
        title = f"Timeline: {topic}"

    if not events:
        console.print(f"[yellow]No timeline events found for '{topic}'[/yellow]")
        return

    table = Table(title=title, show_lines=True)
    table.add_column("Date", style="cyan", width=12)
    table.add_column("Event", width=14)
    table.add_column("Document", width=10)
    table.add_column("Title", width=40)
    table.add_column("Description", width=40)

    for event in events:
        table.add_row(
            str(event.date),
            event.event_type,
            event.doc_id,
            event.title,
            event.description[:40] + "..." if len(event.description) > 40 else event.description,
        )

    console.print(table)


@cli.command()
@click.argument("doc_id")
@click.option("--format", "fmt", default="markdown", type=click.Choice(["markdown", "text"]))
def report(doc_id: str, fmt: str) -> None:
    """Generate a detailed report for a document."""
    engine = _build_engine()
    doc = engine.database.get(doc_id)

    if doc is None:
        console.print(f"[red]Document not found: {doc_id}[/red]")
        return

    all_docs = engine.database.all_documents()
    tracker = CitationTracker(all_docs)
    builder = TimelineBuilder(all_docs)
    summarizer = DocumentSummarizer()

    generator = ReportGenerator(
        summarizer=summarizer,
        citation_tracker=tracker,
        timeline_builder=builder,
    )

    doc_report = generator.generate_document_report(doc)

    if fmt == "markdown":
        output = generator.format_report_markdown(doc_report)
    else:
        output = generator.format_report_text(doc_report)

    console.print(output)


@cli.command()
def stats() -> None:
    """Show database statistics."""
    engine = _build_engine()
    db = engine.database
    all_docs = db.all_documents()

    console.print(Panel(f"[bold]GOVSEARCH Database Statistics[/bold]"))
    console.print(f"Total documents: [cyan]{db.count()}[/cyan]\n")

    type_table = Table(title="Documents by Type")
    type_table.add_column("Type", style="cyan")
    type_table.add_column("Count", justify="right")
    for dt in DocumentType:
        count = len(db.get_by_type(dt))
        if count > 0:
            type_table.add_row(dt.display_name, str(count))
    console.print(type_table)

    tracker = CitationTracker(all_docs)
    most_cited = tracker.most_cited(5)
    if most_cited:
        console.print("\n[bold]Most Referenced Documents[/bold]")
        for doc_id, count in most_cited:
            doc = db.get(doc_id)
            name = doc.title if doc else doc_id
            console.print(f"  [{count} refs] {name}")


def _parse_date(date_str: str) -> date | None:
    """Parse a date string in YYYY-MM-DD format."""
    try:
        parts = date_str.split("-")
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return None


if __name__ == "__main__":
    cli()
