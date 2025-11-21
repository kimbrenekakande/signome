# Signome: Microbiome Study Curator

> **Note**
> 🚧 **Work in Progress**
>
> This project is currently under active development. Features and documentation may change as we continue to build and improve the application. We welcome contributions and feedback!

---

A tool for curating and analyzing microbiome studies, with a focus on extracting and processing information from research papers and related documents.

## Project Overview

Signome is designed to help researchers and scientists in the field of microbiome studies by automating the process of extracting, processing, and analyzing research data from various sources. The application currently provides functionality for web scraping, document conversion, and text embedding.

## Current Implementation

The current implementation is built using Python with the following key components:

### Core Dependencies

- **langgraph**: For creating and managing the workflow of data processing
- **crawl4ai**: Web crawling and content extraction
- **chromadb**: Vector database for storing and querying document embeddings
- **langchain**: Framework for working with language models and text processing
- **pydantic**: Data validation and settings management
- **playwright**: Browser automation for web scraping
- **textual**: Terminal UI framework for the application interface

## Workflow Overview

Signome processes microbiome research data through a structured pipeline:

1. **Input**

   - Accepts research paper URLs or documents
   - Uses Crawl4ai for content extraction

2. **Parallel Processing**

   - **Text Content**: Extracts and processes markdown
   - **Images**: Generates descriptions via `images.json`
   - **Documents**: Handles PDFs and ZIP files
   - **Metadata**: Captures supplementary data

3. **Content Unification**

   - Combines all content into a single markdown format
   - Processes through Ollama for embeddings
   - Stores in ChromaDB for efficient retrieval

4. **Analysis**
   - **Metadata Extraction**: Automatically identifies and extracts key study information
   - **Signature Detection**: Analyzes content for microbial signatures and patterns
   - **Experiment Analysis**: Processes experimental data and results
   - **BugSigDB Integration**: Formats findings for compatibility with BugSigDB
   - **LLM-Powered Insights**: Applies language models to generate contextual understanding

### Task Management with Rav

The project uses [Rav](https://github.com/ravsolutions/rav) for task automation. The `rav.yaml` file defines all available tasks and their configurations. This makes it easy to run common development tasks without remembering complex command-line arguments.

## Future Development

We are planning to enhance the application with a modern web interface and API using:

- **Next.js**: For building a responsive and user-friendly web interface
- **FastAPI**: For creating a robust backend API to support the frontend

This will make the tool more accessible to non-technical users and provide better integration capabilities with other research tools.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- UV package manager
- Ollama for local language model support
- Rav task runner (included in project dependencies)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Configure your environment variables in a `.env` file

## Usage

This project uses Rav as a task runner. The following commands are available:

```bash
# Start the development server
rav run dev

# List all available commands
rav list
```

Common Rav tasks include:

- `rav run dev`: Start the development server
- `rav run build`: Build the application for production
- `rav run test`: Run tests

## Note

This README was generated with the assistance of AI to ensure accuracy and completeness.
