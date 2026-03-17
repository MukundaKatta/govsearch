# GOVSEARCH

AI-powered public records search engine for government documents.

GOVSEARCH indexes, searches, and analyzes government documents including legislation, regulations, court rulings, executive orders, budgets, and reports. It provides full-text search with TF-IDF ranking, cross-reference tracking, document summarization, and timeline analysis.

## Features

- **Full-text search** with TF-IDF ranking across government document corpora
- **Document parsing** that extracts sections, citations, and dates from structured government documents
- **Filtering** by date range, agency, document type, and jurisdiction
- **Citation tracking** to find cross-references between documents
- **Timeline analysis** to trace document history and amendments
- **LLM-powered summarization** of lengthy government documents
- **Built-in sample database** with 50+ government documents for demonstration

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Search for documents
govsearch search "environmental regulation"

# Search with filters
govsearch search "budget allocation" --agency EPA --type legislation --after 2023-01-01

# Analyze a specific document
govsearch analyze DOC-001

# Show citation graph for a document
govsearch citations DOC-001

# Build a timeline of related documents
govsearch timeline "Clean Air Act"

# Generate a summary report
govsearch report DOC-001 --format markdown
```

## Project Structure

```
src/govsearch/
  cli.py              - Click-based command-line interface
  models.py           - Pydantic data models
  report.py           - Report generation
  search/
    engine.py          - SearchEngine with TF-IDF ranking
    indexer.py         - DocumentIndexer for government documents
    filters.py         - SearchFilters by date/agency/type/jurisdiction
  documents/
    types.py           - DocumentType enum
    parser.py          - DocumentParser for section/citation extraction
    database.py        - DocumentDatabase with 50+ sample documents
  analyzer/
    summarizer.py      - LLM-powered document summarization
    citation.py        - CitationTracker for cross-references
    timeline.py        - TimelineBuilder for document history
```

## Dependencies

- **pydantic** - Data validation and models
- **click** - CLI framework
- **rich** - Terminal formatting and tables
- **scikit-learn** - TF-IDF vectorization and similarity search

## License

MIT
