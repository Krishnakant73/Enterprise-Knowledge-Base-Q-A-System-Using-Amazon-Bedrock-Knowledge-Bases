# 📊 Enterprise Knowledge Base Q&A System  
### 🚀 Production-Ready RAG Application using Amazon Bedrock Knowledge Bases

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-WebApp-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/AWS-Bedrock-orange?style=for-the-badge&logo=amazonaws" />
  <img src="https://img.shields.io/badge/RAG-KnowledgeBase-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Deployment-AWS%20EC2-purple?style=for-the-badge&logo=amazonaws" />
  <img src="https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge" />
</p>

---

## 📌 Project Overview

Traditional enterprise search systems often fail because they rely on **keyword matching**, making it difficult for employees to find the right information from internal documents.

At the same time, standard Large Language Models (LLMs) can generate **hallucinated answers** when asked about proprietary or private company knowledge that is not part of their training data.

This project solves both problems by building a **production-ready Retrieval-Augmented Generation (RAG) Question-Answering System** using **Amazon Bedrock Knowledge Bases**.

The application allows employees to ask natural language questions about internal enterprise documents and receive:

- ✅ **Accurate grounded answers**
- ✅ **Citation-backed responses**
- ✅ **Relevant source snippets**
- ✅ **Enterprise-friendly semantic search**

---

# 🎯 Business Problem

Enterprises often store important internal knowledge in:

- HR policies
- employee handbooks
- reimbursement guidelines
- onboarding manuals
- cloud security documentation
- compliance documents
- internal SOPs

Searching these documents manually is time-consuming and inefficient.

### This project provides:
> A secure AI-powered enterprise assistant that helps employees retrieve answers from private company documents using semantic retrieval and grounded LLM generation.

---

# ✨ Key Features

## 🔍 Semantic Enterprise Search
- Uses **Amazon Bedrock Knowledge Bases**
- Retrieves relevant chunks from internal company documents
- Better than traditional keyword-based search

## 🧠 RAG-Powered Answer Generation
- Combines **retrieval + LLM generation**
- Answers are grounded in enterprise documents
- Reduces hallucination significantly

## 📄 Citation-Backed Responses
- Shows **source document references**
- Displays retrieved evidence snippets
- Improves trust and explainability

## 💬 Multi-Turn Chat Interface
- Supports conversational Q&A
- Maintains recent session history
- Enables contextual follow-up questions

## 🎨 Modern Streamlit UI
- Beautiful clean enterprise dashboard
- Chat-style interface
- Answer cards + expandable citations
- Easy to use and deployment friendly

## ☁️ AWS Deployment Ready
- Compatible with **AWS EC2**
- Uses **IAM / AWS credentials**
- Production-oriented modular architecture

---

# 🏗️ System Architecture

```text
Employee / User
        ↓
Streamlit Web Interface
        ↓
Application Layer
        ↓
Amazon Bedrock Knowledge Base Retrieval
        ↓
Retrieved Enterprise Document Chunks
        ↓
Prompt Engineering Layer
        ↓
Amazon Bedrock Foundation Model
        ↓
Grounded Answer Generation
        ↓
Citation Formatting + UI Rendering
```

---

## ⚙️ Tech Stack

### 🖥 Frontend
- Streamlit

### ⚙️ Backend
- Python

### 🤖 AI / RAG Layer
- Amazon Bedrock Knowledge Bases
- Amazon Bedrock Foundation Models
- Retrieval-Augmented Generation (RAG)

### ☁️ Cloud / Deployment
- AWS EC2
- IAM Role / AWS Credentials

### 📦 Supporting Libraries
- boto3
- botocore
- python-dotenv
- logging

---

## 📂 Project Structure
```markdown
Enterprise Knowledge Base Q&A System/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
│
├── config/
│   └── settings.py
│
├── services/
│   ├── bedrock_kb_service.py
│   ├── answer_generator.py
│   ├── citation_formatter.py
│   ├── memory_manager.py
│   └── prompt_manager.py
│
├── utils/
│   └── logger.py
│
└── logs/
```

---

## 🧠 How It Works
```
User asks a question
        ↓
Query is sent to Amazon Bedrock Knowledge Base
        ↓
Relevant document chunks are retrieved semantically
        ↓
Retrieved chunks are passed into a grounded prompt
        ↓
Amazon Bedrock model generates answer
        ↓
Answer is displayed with source citations
```

---

## 🔐 Environment Variables

Create a file named:

```bash
.env
```

Add the following:

```bash
AWS_REGION=us-east-1
KNOWLEDGE_BASE_ID=your_knowledge_base_id_here
BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

TOP_K_RESULTS=3
MAX_CHAT_HISTORY=10
MAX_CONTEXT_CHARS=1500

TEMPERATURE=0.2
MAX_OUTPUT_TOKENS=1024

LOG_LEVEL=INFO
LOG_DIR=logs
LOG_FILE=app.log
```

---

## 🛠️ Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Krishnakant73/Enterprise-Knowledge-Base-Q-A-System-Using-Amazon-Bedrock-Knowledge-Bases
cd Enterprise Knowledge Base Q&A System
```

### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configure AWS Credentials

You must configure AWS access before running the app.

#### Option A — Local Development

Use AWS CLI:
```bash
aws configure
```

Provide:
- AWS Access Key ID
- AWS Secret Access Key
- Default region
- Output format

#### Option B — AWS EC2 Deployment (Recommended)

Attach an IAM Role to the EC2 instance with permissions for:
- Amazon Bedrock
- Amazon Bedrock Knowledge Bases

This is the preferred secure production approach.

### 5️⃣ Run the Application
```bash
streamlit run app.py
```

### 6️⃣ Open in Browser
```bash
http://localhost:8501
```

---

## 💬 Example Questions

You can ask questions like:

- "What is the employee leave policy?"
- "How does travel reimbursement work?"
- "What are the internal cloud security guidelines?"
- "What is the process for onboarding new employees?"
- "What does the company policy say about remote work?"

---

## 📄 Example Output
**User Question:**
> What is the leave policy?

**AI Response:**
> Employees are entitled to annual leave, casual leave, and sick leave as defined in the HR policy document. The policy also mentions approval requirements and carry-forward conditions. [Source 1]

**Citations:**
- Source 1 → `hr_policy.pdf`
- Source 2 → `employee_handbook.pdf`

---

## 🔍 Why Amazon Bedrock Knowledge Bases?

Amazon Bedrock Knowledge Bases provide a managed RAG pipeline, making it easier to build production-grade enterprise QA systems without manually handling:

- embeddings
- vector stores
- chunking pipelines
- retrieval orchestration
**Benefits:**
- Managed semantic retrieval
- Private enterprise data support
- Better grounding
- Faster production deployment

---

## 🧠 Prompt Engineering Strategy

This project uses structured prompts to ensure:

- Grounded enterprise answers
- No hallucination
- Professional business tone
- Citation-aware responses
- Safe fallback when information is missing

### Prompt Rules:
- Use only retrieved document context
- Do not invent facts
- Say when information is insufficient
- Format answers clearly and professionally

---

## 📈 Production-Ready Engineering Practices

This project follows clean engineering standards:

### ✅ Modular Architecture
- Retrieval logic separated
- Prompt logic separated
- Memory separated
- Logging separated
### ✅ Config-Driven Design
- No hardcoded KB IDs or region values
- All important settings managed through .env
### ✅ Logging
- Logs to both console and file
- Easier debugging and monitoring
### ✅ Error Handling
- AWS exceptions handled properly
- Safe fallbacks for failures
### ✅ EC2 Ready
- Can run directly on AWS EC2
- Works with IAM roles

---

## ☁️ AWS EC2 Deployment Guide

### Step 1 — Launch EC2 Instance

**Recommended:**
- Ubuntu 22.04
- t2.micro / t3.micro (for demo)
- Open inbound port 8501

### Step 2 — Connect to EC2
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3 — Install Python & Git
```bash
sudo apt update
sudo apt install python3-pip python3-venv git -y
```

### Step 4 — Clone Repository
```bash
git clone https://github.com/Krishnakant73/Enterprise-Knowledge-Base-Q-A-System-Using-Amazon-Bedrock-Knowledge-Bases
cd Enterprise Knowledge Base Q&A System
```

### Step 5 — Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 6 — Create .env
```bash
nano .env
```

Paste your environment values.

### Step 7 — Run the App
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Step 8 — Open in Browser
```bash
http://your-ec2-public-ip:8501
```

---

## 🔐 IAM Permissions Required

Your EC2 role / AWS credentials should allow access to:

- `bedrock:InvokeModel`
- `bedrock:Retrieve`
- `bedrock:RetrieveAndGenerate` (optional)
- Bedrock Knowledge Base permissions

---

## 🚀 Future Improvements

This project can be extended with:

- 📂 Multi-document source filtering
- 🧠 Conversation-aware retrieval
- 📊 Confidence scoring
- 📁 Document upload pipeline
- 🏢 Multi-department knowledge bases
- 🔐 Authentication & role-based access
- 🐳 Docker deployment
- 🔁 CI/CD integration
- 📡 CloudWatch monitoring

---

## 🎯 Ideal Use Cases

This system is ideal for:

- HR Policy Q&A
- Employee Handbook Assistant
- Internal IT Support Knowledge Assistant
- Compliance Document Search
- Cloud Security Documentation Assistant
- Enterprise SOP Assistant

---

## 📚 Learning Outcomes

This project demonstrates practical experience in:

- Retrieval-Augmented Generation (RAG)
- Amazon Bedrock Knowledge Bases
- Enterprise AI application design
- Prompt engineering
- Streamlit app development
- Cloud deployment on AWS EC2
- Production-ready modular Python architecture

---

## 👨‍💻 Author

Krishnakant Rajbhar
AI / ML Engineer | GenAI Enthusiast | Cloud AI Builder

---

## 🤝 Contribution

Contributions are welcome.
Feel free to fork, improve, and extend this project.

---

## 📄 License

This project is intended for educational and portfolio use.
You may customize it further based on your deployment or enterprise needs.

---

## ⭐ Support

If you found this project useful:

- ⭐ Star this repository
- 🍴 Fork it
- 📢 Share it on LinkedIn
- 🧠 Use it as a strong portfolio project
