# Math Q&A Engine - Complete Setup Guide

A comprehensive mathematics question-answering system with vector search, conversation memory, and web enrichment capabilities.

## Architecture Overview

![System Architecture](https://via.placeholder.com/800x600/2196F3/FFFFFF?text=Math+Q%26A+Architecture)

The system consists of:
- **Backend API**: FastAPI server with math solving capabilities
- **Frontend**: React-based user interface
- **Vector Database**: Qdrant for similarity search
- **MCP Server**: Web search enrichment service
- **Database**: MongoDB for conversation storage

---

## Prerequisites

- Python 3.8+
- Node.js 16+
- Docker
- Git

## Required API Keys

You'll need the following API keys:
- **OpenAI API Key** (for GPT-4o-mini)
- **MongoDB URI** (MongoDB Atlas or local)
- **Serper API Key** (for web search)

---

## 🚀 Quick Start

### 1. Clone All Repositories

```bash
# Backend
git clone https://github.com/saiganeshreddy7/math_qa_engine.git
cd math_qa_engine

# Frontend (in separate terminal)
git clone https://github.com/saiganeshreddy7/maths_qa_engine_frontend.git
cd maths_qa_engine_frontend

# MCP Server (in separate terminal)
git clone https://github.com/saiganeshreddy7/web-search-enrichment-mcp.git
cd web-search-enrichment-mcp
```

---

## 🔧 Backend Setup

### Step 1: Install Dependencies

```bash
cd math_qa_engine

# Using pip (recommended: use uv for faster installation)
pip install -r requirements.txt

# Or using uv (faster)
uv pip install -r requirements.txt
```

### Step 2: Environment Configuration

Create `.env` file in backend directory:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
MONGO_URI=your_mongodb_uri_here
SERPER_API_KEY=your_serper_api_key_here
```

### Step 3: Setup Vector Database (Qdrant)

#### Pull and Run Qdrant Docker Container

```bash
# Pull Qdrant image
docker pull qdrant/qdrant

# Run Qdrant (update path as needed)
docker run -p 6333:6333 -p 6334:6334 \
    -v /Users/saiganeshreddykodekandla/Documents/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

#### Verify Qdrant is Running

Open browser and check: http://localhost:6333/dashboard

### Step 4: Setup Dataset and Vector Embeddings

#### Download GSM8K Dataset

Download the GSM8K dataset (1000 records):
[GSM8K Dataset](https://drive.google.com/file/d/1M-C2PVukhQKDCMaRpkgfcF2AwQPvpA8y/view?usp=sharing)

#### Download and Run Upsert Scripts

Download upsert scripts:
[Upsert Scripts](https://drive.google.com/drive/folders/1u4D0fHU1NBgvNu9DssKrzpuN4ngYYJPx?usp=sharing)

```bash
# Run the upsert script (requires fast internet for model download)
python upsert_script.py

# This will download sentence-transformers model and populate Qdrant
# Check Qdrant dashboard to verify data is uploaded
```

**✅ Vector Database Ready**

---

## 🌐 MCP Server Setup

### Step 1: Install MCP Dependencies

```bash
cd web-search-enrichment-mcp

# Install requirements
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create `.env` file in MCP directory:

```bash
# .env
SERPER_API_KEY=your_serper_api_key_here
```

### Step 3: Start MCP Server

```bash
# Start MCP server
python -m servers.mcp_server_http
```

### Step 4: Test MCP Server

In another terminal:

```bash
# Test MCP server
python -m clients.client_http_test
```

If test passes, keep MCP server running.

---

## 🛡️ Configure Guardrails

Configure Guardrails with OpenAI API key:

```bash
# Configure guardrails
guardrails configure

# Enter your OpenAI API key when prompted
```

---

## ▶️ Start Backend Server

Ensure Docker (Qdrant) and MCP server are running, then:

```bash
cd math_qa_engine

# Start FastAPI server
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Verify Backend

- Check Swagger UI: http://localhost:8000/docs
- Test health endpoint: http://localhost:8000/health

---

## 🎨 Frontend Setup

### Step 1: Install Dependencies

```bash
cd maths_qa_engine_frontend

# Install npm packages
npm install
```

### Step 2: Start Frontend

```bash
# Start React development server
npm start
```

Frontend will be available at: http://localhost:3000

---

## ✅ Final Verification Checklist

Before using the system, ensure all components are running:

### Required Services Status:

- [ ] **Docker (Qdrant)**: http://localhost:6333/dashboard ✅
- [ ] **MCP Server**: Running on specified port ✅  
- [ ] **Backend API**: http://localhost:8000/docs ✅
- [ ] **Frontend**: http://localhost:3000 ✅

### Test the Complete System:

1. Open frontend at http://localhost:3000
2. Ask a math question (e.g., "What is 15 + 25?")
3. Verify response includes:
   - Proper math formatting
   - Step-by-step solution
   - LaTeX rendering

---

## 📝 Usage

### Basic Math Questions
```
User: "What is the integral of x^2 from 0 to 1?"
System: Returns formatted solution with LaTeX math
```

### Word Problems
```
User: "John has 15 apples and gives 7 to Mary. How many apples does John have left?"
System: Provides step-by-step solution
```

### Conversation Memory
The system remembers previous questions in the same conversation session.

---

## 🔧 Troubleshooting

### Common Issues:

**Qdrant Connection Failed:**
- Ensure Docker is running
- Check port 6333 is not blocked
- Verify volume path exists

**MCP Server Not Responding:**
- Check Serper API key is valid
- Ensure MCP server is running on correct port
- Test with client_http_test.py

**Backend Startup Errors:**
- Verify all environment variables are set
- Check MongoDB connection
- Ensure Guardrails is configured

**Frontend Not Loading:**
- Check if npm install completed successfully
- Verify backend API is running
- Check browser console for errors

## 📄 License

MIT License - see individual repositories for details.



