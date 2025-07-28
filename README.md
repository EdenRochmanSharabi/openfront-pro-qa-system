# OpenFront Pro QA System 🎮

An intelligent question-answering system for OpenFront.io that uses AI to provide instant answers about game mechanics, strategies, buildings, maps, and more based on the comprehensive OpenFront Pro website content.

## 🚀 What I Built

I created a **local AI-powered knowledge base** that can answer any question about OpenFront.io using the content from my website. Here's what makes it special:

### ✨ Key Features

- **🤖 AI-Powered Answers**: Uses Google's Gemini AI to understand and answer questions naturally
- **📚 Local Knowledge Base**: Processes all HTML content from the OpenFront Pro website
- **⚡ Smart Caching**: Saves embeddings locally for instant startup after first run
- **🎯 Interactive CLI**: Easy-to-use command-line interface for asking questions
- **📄 Source Attribution**: Shows which files were used to generate answers
- **🔄 Rebuild Capability**: Can update the knowledge base when website content changes

### 🛠️ Technical Implementation

1. **Content Processing**: Parses HTML files using BeautifulSoup, removing scripts/styles
2. **Text Chunking**: Splits content into manageable chunks using RecursiveCharacterTextSplitter
3. **Vector Embeddings**: Creates embeddings using Google's Gemini embedding model
4. **FAISS Vector Store**: Stores embeddings locally for fast similarity search
5. **Retrieval QA**: Uses LangChain to retrieve relevant content and generate answers
6. **CLI Interface**: Interactive command-line tool for easy questioning

## 📦 Files Overview

- `openfront_cli.py` - Main interactive CLI application
- `openfront_qa.py` - Basic script version for single questions
- `requirements.txt` - Python dependencies
- `README.md` - This documentation
- `extracted_content.txt` - Raw extracted website content
- `openfrontpro.com/` - Website HTML files
- `openfront_vectorstore/` - Cached embeddings (created automatically)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd OpenFront-Pro
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:
   - Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the API key in `openfront_cli.py` (line 12)

4. **Run the CLI**:
   ```bash
   python openfront_cli.py
   ```

## 🎯 Usage Examples

### Interactive CLI

```bash
python openfront_cli.py
```

**Example Questions You Can Ask:**
- "How does the gold mechanic work?"
- "What are the best hotkeys?"
- "How do I win consistently?"
- "What's the optimal population ratio?"
- "How do MIRVs work?"
- "What are the best spawn locations on World map?"
- "How do alliances work?"
- "What's the difference between atom and hydrogen bombs?"

### Force Rebuild

If you update your website content, rebuild the knowledge base:

```bash
python openfront_cli.py --rebuild
```

### Single Question Script

For one-off questions without the interactive interface:

```bash
python openfront_qa.py
```

## 🔧 How It Works

### 1. Content Processing
- Scans `./openfrontpro.com/` directory for HTML files
- Uses BeautifulSoup to extract clean text content
- Removes scripts, styles, navigation, and footer elements
- Creates 226 content chunks from 58 HTML files

### 2. Vector Embeddings
- Uses Google's `models/embedding-001` model
- Creates high-dimensional vector representations of content
- Stores embeddings in FAISS vector store for fast similarity search

### 3. Question Answering
- Takes user questions and finds most relevant content chunks
- Uses Gemini 1.5 Pro to generate natural language answers
- Provides source file attribution for transparency

### 4. Smart Caching
- Saves vector store to `./openfront_vectorstore/`
- Subsequent runs load instantly (2 seconds vs 30+ seconds)
- Only rebuilds when forced or when loading fails

## 📊 Performance

| Operation | Time | Description |
|-----------|------|-------------|
| **First Run** | ~30s | Parse HTML → Create chunks → Generate embeddings → Save |
| **Subsequent Runs** | ~2s | Load embeddings from disk → Ready to answer! |
| **Question Response** | ~3-5s | Search vectors → Generate AI answer |

## 🎮 OpenFront.io Content Covered

The system includes knowledge about:

- **Game Mechanics**: Population growth, gold economy, trade routes, attack ratios
- **Buildings**: Cities, ports, defense posts, missile silos, SAM launchers, warships
- **Nuclear Weapons**: Atom bombs, hydrogen bombs, MIRVs
- **Maps**: All 22 maps with spawn strategies and win rate analysis
- **Strategies**: Early game, mid game, late game tactics
- **Alliances**: Diplomatic mechanics and betrayal consequences
- **Hotkeys**: Keyboard shortcuts and efficiency controls
- **Bots**: AI behavior patterns and counter-strategies

## 🔑 API Key Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Replace the key in `openfront_cli.py` line 12:
   ```python
   os.environ["GOOGLE_API_KEY"] = "your-api-key-here"
   ```

## 🛠️ Customization

### Adding New Content
1. Add new HTML files to `./openfrontpro.com/`
2. Run `python openfront_cli.py --rebuild`
3. The system will automatically include new content

### Modifying Chunk Size
Edit `chunk_size=800` in the `RecursiveCharacterTextSplitter` for different granularity

### Changing Models
- Embedding model: `models/embedding-001`
- LLM model: `gemini-1.5-pro`

## 🤝 Contributing

Feel free to contribute improvements:
- Add new question types
- Optimize performance
- Enhance the CLI interface
- Add web interface
- Improve answer quality

## 📝 License

This project is for educational and personal use. Please respect the OpenFront.io game and community guidelines.

## 🙏 Acknowledgments

- **OpenFront.io** - The amazing strategy game that inspired this project
- **Google Gemini AI** - Powerful AI models for embeddings and text generation
- **LangChain** - Framework for building LLM applications
- **FAISS** - Efficient similarity search library

---

**Built with ❤️ for the OpenFront.io community**

*This system demonstrates how AI can transform static website content into an interactive knowledge base, making game information easily accessible and searchable.* 