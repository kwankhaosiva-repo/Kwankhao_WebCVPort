#!/usr/bin/env python3
"""
generate_portfolio_data.py
Synthesizes project data and resume for Kwankhao Sivasomboon.
Separates Personal Projects (with code, architecture, and deep dive)
from Company Work (reformed strictly to non-confidential tech stacks & role contributions).
"""

import os
import json
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "Kwankhao's Docs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Copy PDF resume to assets if exists
pdf_src = os.path.join(DOCS_DIR, "RESUME_Kwankhao_Sivasomboon.pdf")
pdf_dst = os.path.join(ASSETS_DIR, "RESUME_Kwankhao_Sivasomboon.pdf")
if os.path.exists(pdf_src):
    shutil.copyfile(pdf_src, pdf_dst)

# ==============================================================================
# 1. PERSONAL PROJECTS (User's Independent Projects - Full Code & Deep Dive)
# ==============================================================================
PERSONAL_PROJECTS = [
    {
        "id": "thai-lpr-deep-learning-ocr",
        "title": "Thai License Plate Recognition (LPR) & OCR Pipeline",
        "type": "personal",
        "typeLabel": "Personal Project",
        "category": "cv-edge",
        "categoryLabel": "Computer Vision & Deep Learning",
        "badge": "Personal Deep Learning Project",
        "impact": "3-Stage deep learning pipeline achieving ~90% Thai province OCR classification",
        "shortSummary": "End-to-end deep learning OCR pipeline combining YOLO11 for plate detection, ResNet-CRNN with CTC Loss for character sequence recognition, and MobileNetV2 for 77 Thai province classification.",
        "fullDescription": "An end-to-end 3-stage deep learning pipeline built to recognize complex Thai vehicle license plates (featuring Thai script consonants, numerals, and 77 distinct provincial names in small text). Stage 1 uses YOLO11 for plate localization and perspective alignment. Stage 2 employs a custom ResNet-CRNN architecture trained with Connectionist Temporal Classification (CTC Loss) for reading character sequences without per-character bounding boxes. Stage 3 utilizes a fine-tuned MobileNetV2 classifier to identify the 77 Thai provinces.",
        "highlights": [
            "Stage 1: YOLO11 object detection trained on diverse Thai vehicle camera angles",
            "Stage 2: ResNet-CRNN with CTC Loss for Thai alphabet and digit sequence transcription",
            "Stage 3: Fine-tuned MobileNetV2 model for 77 Thai province classification",
            "Achieved ~90% province classification accuracy across test validation datasets",
            "Containerized REST API built with FastAPI and tested on GCP Cloud Run"
        ],
        "metrics": [
            {"label": "Province Accuracy", "value": "~90%", "sub": "77 Thai provinces evaluated"},
            {"label": "Pipeline Stages", "value": "3-Stage", "sub": "YOLO11 + CRNN-CTC + MobileNetV2"},
            {"label": "Inference Latency", "value": "< 120ms", "sub": "End-to-end pipeline per image"},
            {"label": "Framework", "value": "PyTorch", "sub": "Custom CNN-RNN-CTC training"}
        ],
        "techStack": [
            "Python", "PyTorch", "YOLO11", "ResNet-CRNN", "CTC Loss", "MobileNetV2",
            "OpenCV", "FastAPI", "Docker", "GCP Cloud Run"
        ],
        "architecture": """
+-----------------+      +------------------------+      +------------------------+
| Input Image /   | ---> | Stage 1: YOLO11        | ---> | Crop & Perspective     |
| Vehicle Camera  |      | Plate Detection        |      | Warp Correction        |
+-----------------+      +------------------------+      +------------------------+
                                                                     |
                                  +----------------------------------+
                                  |
                                  v
+-------------------------------------------------+      +------------------------+
| Stage 2: ResNet-CRNN + CTC Loss (Text/Numbers)  | ---> | JSON Structured Result |
| Stage 3: MobileNetV2 (77 Province Classifier)   |      | Plate: 1กข 9999 กรุงเทพ |
+-------------------------------------------------+      +------------------------+
""",
        "innovations": [
            "**Decoupled Province Classifier**: Decoupled sequence transcription from province identification, allowing the MobileNetV2 classifier to specialize on subtle font differences in provincial titles.",
            "**CTC Loss Sequence Alignment**: Eliminated the need for character-level bounding box segmentation by training CRNN end-to-end with Connectionist Temporal Classification."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "models/lpr_pipeline.py (Three-Stage PyTorch Inference & CTC Decode)",
            "code": """class ThaiLPRPipeline:
    def __init__(self, yolo_path: str, crnn_path: str, province_path: str, device='cuda'):
        self.detector = YOLO(yolo_path)
        self.ocr_model = CRNN(num_classes=NUM_THAI_CHARS).to(device)
        self.province_model = MobileNetV2(num_classes=77).to(device)
        self.device = device

    def predict(self, image_np: np.ndarray) -> dict:
        # Stage 1: Bounding Box Detection
        results = self.detector(image_np, conf=0.5)
        if not results or len(results[0].boxes) == 0:
            return {"status": "no_plate_found"}

        box = results[0].boxes[0].xyxy[0].cpu().numpy().astype(int)
        plate_crop = image_np[box[1]:box[3], box[0]:box[2]]

        # Stage 2: ResNet-CRNN OCR for Thai Consonants and Numbers
        tensor_crop = preprocess_ocr(plate_crop).to(self.device)
        ocr_logits = self.ocr_model(tensor_crop)
        plate_text = ctc_decode(ocr_logits, THAI_CHAR_MAP)

        # Stage 3: MobileNetV2 77 Province Classification
        prov_tensor = preprocess_province(plate_crop).to(self.device)
        prov_logits = self.province_model(prov_tensor)
        province_name = PROVINCE_MAP[prov_logits.argmax().item()]

        return {
            "plate_number": plate_text,
            "province": province_name,
            "confidence": float(ocr_logits.max().item())
        }"""
        },
        "featured": True
    },
    {
        "id": "thai-legal-retrieval-hybrid-rag",
        "title": "Thai Legal Retrieval & Hybrid RAG System",
        "type": "personal",
        "typeLabel": "Personal Project",
        "category": "genai-rag",
        "categoryLabel": "GenAI, LLMs & Agents",
        "badge": "Personal RAG Project",
        "impact": "Hybrid dense + sparse BM25 + Reciprocal Rank Fusion (RRF) with LLM evaluation",
        "shortSummary": "Legal document retrieval system for Thai statutory provisions using Hybrid Search (Dense embeddings + BM25 + RRF), metadata filtering, query expansion, and LLM-as-a-judge evaluation.",
        "fullDescription": "A Hybrid Retrieval-Augmented Generation (RAG) engine designed to search Thai legal documents, local municipality laws, and corporate regulations. Combines dense semantic vector search (multilingual embeddings in ChromaDB) with sparse lexical search (BM25 with PyThaiNLP tokenization), merged via Reciprocal Rank Fusion (RRF). Implements hypothetical document embeddings (HyDE) for query expansion and an automated evaluation pipeline to test groundedness.",
        "highlights": [
            "Hybrid Retrieval Architecture: ChromaDB dense vector search + BM25 sparse keyword matching",
            "Reciprocal Rank Fusion (RRF) with tunable rank constants to balance semantic & exact matches",
            "Thai legal corpus chunking with section and statutory metadata tags",
            "Query expansion with Gemini/Ollama to generate domain-specific legal synonyms",
            "LLM-as-a-judge evaluation benchmark for faithfulness and answer relevancy",
            "LangChain orchestration with streaming citations"
        ],
        "metrics": [
            {"label": "Retrieval Strategy", "value": "Hybrid RRF", "sub": "Dense Semantic + BM25 Sparse"},
            {"label": "Evaluation Score", "value": "93.8%", "sub": "Context Groundedness (LLM-judge)"},
            {"label": "Vector Store", "value": "ChromaDB", "sub": "Multilingual Semantic Embeddings"},
            {"label": "Inference Latency", "value": "< 480ms", "sub": "Hybrid retrieval + RRF merge"}
        ],
        "techStack": [
            "Python", "LangChain", "ChromaDB", "BM25", "Reciprocal Rank Fusion (RRF)",
            "Google Gemini", "Ollama", "PyThaiNLP", "FastAPI", "Pydantic"
        ],
        "architecture": """
                                    +------------------------------+
                                    | User Thai Legal Query        |
                                    +------------------------------+
                                                  |
                                   +--------------+--------------+
                                   | (Query Expansion & HyDE)    |
                                   v                             v
                    +-----------------------------+ +-----------------------------+
                    | Dense Vector Search         | | Sparse Lexical Search       |
                    | (ChromaDB Multilingual)     | | (BM25 + PyThaiNLP Tokens)   |
                    +-----------------------------+ +-----------------------------+
                                   |                             |
                                   +--------------+--------------+
                                                  |
                                                  v
                                    +------------------------------+
                                    | Reciprocal Rank Fusion (RRF) |
                                    | Rank Score = 1 / (60 + Rank) |
                                    +------------------------------+
                                                  |
                                                  v
                                    +------------------------------+
                                    | Gemini Reasoning + Citation  |
                                    | & Section-grounded Output    |
                                    +------------------------------+
""",
        "innovations": [
            "**Reciprocal Rank Fusion (RRF) for Exact Statutory Numbers**: Addresses vector search's difficulty with exact Thai section numbers by combining dense semantic vectors with BM25 lexical token matching.",
            "**LLM-as-a-Judge Eval**: Implemented an automated test script verifying that claims in the output reference retrieved chunks accurately."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/retriever/hybrid_rrf.py (Reciprocal Rank Fusion Algorithm)",
            "code": """def reciprocal_rank_fusion(dense_results: list, sparse_results: list, k: int = 60) -> list:
    \"\"\"Combines dense and sparse search rankings using Reciprocal Rank Fusion.\"\"\"
    rrf_scores = {}
    doc_lookup = {}

    # Accumulate Dense RRF scores
    for rank, doc in enumerate(dense_results):
        doc_id = doc.metadata.get('section_id', doc.page_content)
        doc_lookup[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank + 1))

    # Accumulate Sparse BM25 RRF scores
    for rank, doc in enumerate(sparse_results):
        doc_id = doc.metadata.get('section_id', doc.page_content)
        doc_lookup[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank + 1))

    # Sort merged documents by combined RRF score descending
    sorted_doc_ids = sorted(rrf_scores.keys(), key=lambda did: rrf_scores[did], reverse=True)
    return [doc_lookup[did] for did in sorted_doc_ids]"""
        },
        "featured": True
    },
    {
        "id": "rag-chain-langchain-retrieval",
        "title": "RAG-Chain: Advanced LangChain Multi-Retrieval Pipeline",
        "type": "personal",
        "typeLabel": "Personal Project",
        "category": "genai-rag",
        "categoryLabel": "GenAI, LLMs & Agents",
        "badge": "Personal RAG Project",
        "impact": "LangChain retrieval chain with Maximal Marginal Relevance (MMR) & strict hallucination guardrails",
        "shortSummary": "Document question-answering RAG pipeline built with LangChain, ChromaDB vector indexing, Maximal Marginal Relevance (MMR) diversity reranking, Google Gemini LLM, and anti-hallucination grounding.",
        "fullDescription": "A modular Retrieval-Augmented Generation pipeline implemented using LangChain and Google Generative AI embeddings. Integrates ChromaDB vector store with Maximal Marginal Relevance (MMR) retrieval to prevent redundant document chunks. Implements structured document chaining (`create_stuff_documents_chain`, `create_retrieval_chain`), base-document context injection, and strict system prompts preventing LLM hallucinations.",
        "highlights": [
            "LangChain modular chain orchestration (`create_retrieval_chain` + `create_stuff_documents_chain`)",
            "Maximal Marginal Relevance (MMR) search type (`fetch_k=20`, `lambda_mult=0.5`) for diverse context retrieval",
            "ChromaDB persistent vector store with Google Generative AI embeddings",
            "Strict hallucination guardrails instructing Gemini to answer exclusively from ground truth context",
            "Metadata-based first-page executive summary extraction and contextual injection"
        ],
        "metrics": [
            {"label": "Reranker", "value": "MMR Search", "sub": "Maximal Marginal Relevance"},
            {"label": "LLM Engine", "value": "Gemini Models", "sub": "Structured prompt chaining"},
            {"label": "Embeddings", "value": "Google GenAI", "sub": "ChromaDB vector store"},
            {"label": "Guardrails", "value": "Strict Grounding", "sub": "Zero-hallucination prompting"}
        ],
        "techStack": [
            "Python", "LangChain", "ChromaDB", "Google Gemini", "GoogleGenerativeAIEmbeddings",
            "PyPDF / Document Loaders", "Pydantic", "FastAPI"
        ],
        "architecture": """
+-----------------------+      +---------------------------+      +---------------------------+
| User Query Inbound    | ---> | ChromaDB Vector Store     | ---> | MMR Search Reranker       |
| (Document Research)   |      | (Google GenAI Embeddings) |      | (Diversity fetch_k=20)    |
+-----------------------+      +---------------------------+      +---------------------------+
                                                                                |
                                                                                v
+-----------------------+      +---------------------------+      +---------------------------+
| Grounded AI Answer    | <--- | Gemini LLM Engine         | <--- | Stuff Documents Chain     |
| with Source Context   |      | (Temperature Controlled)  |      | & Base Info Injection     |
+-----------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Maximal Marginal Relevance (MMR) Diversity**: Prevents context crowding by balancing relevance against similarity to already selected chunks.",
            "**Strict Grounding Prompting**: System prompt strictly enforces answering only from retrieved context or explicitly declaring missing data."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/rag_chain.py (LangChain MMR Retriever & Retrieval Chain Setup)",
            "code": """def build_rag_retrieval_chain(vectorstore: Chroma, llm: ChatGoogleGenerativeAI):
    # 1. MMR Retriever for context diversity
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.5}
    )

    # 2. Strict Grounding Prompt
    system_prompt = (
        "คุณเป็นผู้ช่วยวิจัยอัจฉริยะที่เคร่งครัดเรื่องความถูกต้องของข้อมูล "
        "1. ตอบคำถามโดยใช้ข้อมูลจาก '[ข้อมูลพื้นฐาน]' และ '[เนื้อหาค้นหา]' เท่านั้น\\n"
        "2. หาก 'ไม่พบข้อมูล' ในเนื้อหา ให้ตอบว่า 'ไม่พบข้อมูลในเอกสาร' ห้ามคาดเดาคำตอบเองเด็ดขาด\\n"
        "3. คงคำศัพท์ภาษาอังกฤษสำหรับชื่อเฉพาะและศัพท์เทคนิคไว้เสมอ\\n\\n"
        "[ข้อมูลพื้นฐาน]:\\n{base_info}\\n\\n"
        "[เนื้อหาค้นหา]:\\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    # 3. Assemble End-to-End Chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, question_answer_chain)"""
        },
        "featured": True
    },
    {
        "id": "line-stock-analysis-ai-agent",
        "title": "LINE Stock Analysis AI Assistant",
        "type": "personal",
        "typeLabel": "Personal Project",
        "category": "genai-rag",
        "categoryLabel": "GenAI, LLMs & Agents",
        "badge": "Personal Financial AI",
        "impact": "Technical indicators (RSI, MACD), Thai/US market feeds & Gemini 2.5 Flash on LINE",
        "shortSummary": "Conversational financial assistant on LINE messaging integrating Gemini 2.5 Flash, yfinance market data, technical indicator calculations (RSI, MACD, Bollinger Bands), user profiles, and background scheduled alerts.",
        "fullDescription": "A conversational AI financial assistant operating on the LINE platform. Powered by Google Gemini 2.5 Flash, it analyzes market data across Thai (SET) and US equities. Computes technical indicators (RSI, MACD, Moving Averages, Bollinger Bands), summarizes relevant news sentiment, and tracks user risk profiles stored in PostgreSQL via SQLAlchemy. Implements webhook deduplication and background task scheduling via APScheduler.",
        "highlights": [
            "Integrated Google Gemini 2.5 Flash for financial context synthesis and conversational Q&A",
            "Technical indicator engine: RSI (14), MACD (12, 26, 9), EMA (20/50/200), Bollinger Bands",
            "Data ingestion covering Thai Stock Exchange (SET) and US markets (yfinance)",
            "PostgreSQL & SQLAlchemy ORM for user profiles, watchlists, and conversation memory",
            "Scheduled morning briefings & market close updates via APScheduler",
            "LINE Messaging API webhook deduplication to handle retry events gracefully"
        ],
        "metrics": [
            {"label": "Markets Covered", "value": "Thai & US", "sub": "SET + US Equities"},
            {"label": "Technical Analysis", "value": "6+ Indicators", "sub": "RSI, MACD, EMA, BB, ATR"},
            {"label": "LLM Engine", "value": "Gemini 2.5 Flash", "sub": "Financial Context Prompting"},
            {"label": "Reliability", "value": "Deduplicated", "sub": "Idempotent Webhook Processing"}
        ],
        "techStack": [
            "Python", "Flask / FastAPI", "Google Gemini 2.5 Flash", "line-bot-sdk",
            "PostgreSQL", "SQLAlchemy", "yfinance", "Pandas", "APScheduler", "Docker"
        ],
        "architecture": """
+-------------------+      +-------------------------+      +---------------------------+
| LINE User Inbound | ---> | Webhook Receiver        | ---> | Message Deduplicator      |
| Query / Command   |      | (Flask / FastAPI)       |      | (Idempotency Key Cache)   |
+-------------------+      +-------------------------+      +---------------------------+
                                                                          |
                                                                          v
+-------------------+      +-------------------------+      +---------------------------+
| Gemini 2.5 Flash  | <--- | User Profile & Context  | <--- | Data Engine (yfinance)    |
| Financial Advisor |      | (PostgreSQL Database)   |      | + Technicals (RSI/MACD)   |
+-------------------+      +-------------------------+      +---------------------------+
          |
          v
+----------------------------------------------------+
| Rich Flex Message Response / Scheduled Alert Push  |
+----------------------------------------------------+
""",
        "innovations": [
            "**Structured Context Assembly**: Combines mathematical indicators (RSI momentum, MACD crosses) with news context before passing to Gemini Flash, reducing hallucinations.",
            "**Idempotent Event Deduplication**: Prevents duplicate LLM processing caused by LINE webhook network retries."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/services/market_analyzer.py (Technical Indicator Computation & Prompting)",
            "code": """def calculate_technical_summary(symbol: str, period='6mo') -> dict:
    ticker = yfinance.Ticker(symbol)
    df = ticker.history(period=period)
    if df.empty:
        return None

    # Calculate 14-day RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))

    # Calculate MACD (12, 26, 9)
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    latest = df.iloc[-1]
    return {
        "symbol": symbol.upper(),
        "close_price": round(latest['Close'], 2),
        "rsi": round(latest['RSI'], 2),
        "macd_status": "Bullish Cross" if latest['MACD'] > latest['Signal_Line'] else "Bearish Divergence",
        "ema_50": round(df['Close'].ewm(span=50).mean().iloc[-1], 2),
        "volume": int(latest['Volume'])
    }"""
        },
        "featured": True
    }
]

# ==============================================================================
# 2. COMPANY WORK & INDUSTRY SYSTEMS (Reformed to Tech Stacks & Role Highlights)
# ==============================================================================
COMPANY_PROJECTS = [
    {
        "id": "stafflenz-ai-worker-monitor",
        "title": "StaffLenz AI: Edge Workplace Activity & Desk Zone Analytics",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Yourhome Platform",
        "category": "cv-edge",
        "categoryLabel": "Computer Vision & Edge AI",
        "badge": "Workplace CV Platform",
        "impact": "Real-time edge worker identity stability & desk analytics on multi-camera RTSP",
        "shortSummary": "Edge computer vision analytics platform processing multi-camera RTSP feeds with OpenVINO FP16 acceleration, YOLOv11-Pose keypoints, InsightFace/ArcFace embeddings, polygon desk zones, and real-time Server-Sent Events (SSE).",
        "fullDescription": "Engineered an edge computer vision system at Yourhome for real-time desk occupancy and workplace activity analytics. Implemented multi-camera RTSP ingestion with latest-frame batching buffers and Intel OpenVINO FP16 inference acceleration. Stabilized worker identity recognition using ArcFace face embeddings, head-pose yaw/pitch angle filtering, and temporal caching across polygon desk zones. Built real-time Server-Sent Events (SSE) streaming and automated LINE alert webhook integrations.",
        "highlights": [
            "OpenVINO FP16 inference acceleration for YOLOv11-Pose and InsightFace ArcFace models",
            "Multi-camera RTSP pipeline with drop-oldest latest-frame buffer preventing lag",
            "Polygon desk zone mapping with ray-casting point-in-polygon containment logic",
            "Identity stabilization with head-pose angle filtering and cosine similarity thresholding",
            "Real-time Server-Sent Events (SSE) stream delivery and LINE alert webhook triggers",
            "Automated data retention cleanup worker for historical telemetry compaction"
        ],
        "techStack": [
            "Python", "FastAPI", "YOLOv11-Pose", "InsightFace", "ArcFace", "OpenVINO (FP16)",
            "OpenCV", "SuperVision", "PyTorch", "SSE (Server-Sent Events)", "Docker", "LINE Notify"
        ],
        "featured": True
    },
    {
        "id": "agentic-scraping-vlm-search",
        "title": "Agentic Real Estate Ingestion & VLM Property Filtering",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Yourhome Platform",
        "category": "agents-automation",
        "categoryLabel": "Multi-Agent & Automation",
        "badge": "Web Scraping & VLM",
        "impact": "Multi-source scraping pipeline & Vision-Language Model property curation",
        "shortSummary": "Automated data ingestion pipeline collecting listings across major Thai property portals with Gemini VLM visual style filtering, K-Means color detection, and geocoding.",
        "fullDescription": "Built a multi-agent data ingestion suite at Yourhome extracting property listings across 7 major portals and Facebook Marketplace. Integrated Google Gemini Vision-Language Models (VLM) to analyze room condition, aesthetic styles (Modern, Minimalist, Japandi, Luxury), and K-Means color clustering. Geocoded coordinates via Longdo Maps and Google Maps APIs into Google Cloud Firestore.",
        "highlights": [
            "Multi-source scraping agents with Playwright and Browser-Use automation",
            "Gemini VLM visual filtering for room style and interior quality classification",
            "Room color palette extraction using OpenCV and K-Means clustering",
            "Geocoding and transit distance computation via Longdo Maps and Google Maps APIs",
            "Deduplication hashing and automated data synchronization to Google Cloud Firestore"
        ],
        "techStack": [
            "Python", "Playwright", "Browser-Use", "Google Gemini VLM", "OpenCV",
            "K-Means Clustering", "Google Cloud Firestore", "Longdo Maps API", "Pydantic"
        ],
        "featured": True
    },
    {
        "id": "ai-audio-extraction-speech-to-search",
        "title": "Thai Speech-to-Search Voice Inquiry Pipeline",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Yourhome Platform",
        "category": "genai-rag",
        "categoryLabel": "GenAI, LLMs & Agents",
        "badge": "Voice Processing",
        "impact": "Asynchronous Thai speech-to-structured search parameters with Groq Whisper & Gemini",
        "shortSummary": "Asynchronous pipeline converting Thai voice inquiries into structured search parameters using Groq Whisper STT, Gemini/Llama with Pydantic validation, and fuzzy location normalization.",
        "fullDescription": "Developed an asynchronous voice inquiry processing pipeline for Yourhome. Received Thai voice notes from LINE and web clients, transcribed audio using Groq Whisper API (<320ms latency), and extracted structured search parameters (budgets, property types, bedroom counts, pet policies) using Gemini and Llama 3 with Pydantic validation. Normalized colloquial Thai transit landmarks against 150+ BTS/MRT stations.",
        "highlights": [
            "Sub-350ms Thai Speech-to-Text inference via Groq Whisper API",
            "LLM structured entity extraction with strict Pydantic schema validation",
            "Fuzzy Thai location matching against 150+ Bangkok BTS/MRT stations",
            "Asynchronous FastAPI worker architecture for handling concurrent audio inputs"
        ],
        "techStack": [
            "Python", "FastAPI", "Groq Whisper API", "Google Gemini", "Llama 3",
            "Pydantic", "PyThaiNLP", "RapidFuzz", "FFmpeg"
        ],
        "featured": True
    },
    {
        "id": "multi-agent-bot-tester-qa",
        "title": "Multi-Agent QA Automation & API Auditing Framework",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Yourhome Platform",
        "category": "agents-automation",
        "categoryLabel": "Multi-Agent & Automation",
        "badge": "QA Automation",
        "impact": "Multi-agent test execution, database auditing via SSH tunnels & Postman fuzzing",
        "shortSummary": "Multi-agent QA framework executing browser UI testing (Playwright), REST API regression auditing, SSH-tunneled MySQL verification, and score algorithm validation across environments.",
        "fullDescription": "Engineered an AI-assisted test automation framework at Yourhome coordinating specialized agents (Orchestrator, Executor, Logic Auditor, Reporter). Automated browser regression flows with Playwright, parsed Postman collections, queried AWS RDS MySQL databases through secure SSH tunnels with GCP Secret Manager, and generated automated QA reports synced to Google Sheets.",
        "highlights": [
            "Multi-agent architecture coordinating test tasks, execution, and reporting",
            "Postman Collection parsing and automated API schema testing",
            "Secure MySQL verification via paramiko SSH tunnels and GCP Secret Manager",
            "Playwright browser automation capturing visual failure evidence and logs"
        ],
        "techStack": [
            "Python", "Playwright", "LangChain", "Requests", "PyMySQL", "SSHTunnel",
            "Google Cloud Secret Manager", "GSpread", "PyTest", "Docker"
        ],
        "featured": True
    },
    {
        "id": "3d-room-scan-texture-pipeline",
        "title": "3D Room Scan Mesh Cleaning & Web Viewer Pipeline",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Yourhome Platform",
        "category": "geospatial-3d",
        "categoryLabel": "Geospatial AI & 3D Analytics",
        "badge": "3D Processing",
        "impact": "3D mesh cleaning, USDZ-to-GLTF conversion & Three.js web rendering",
        "shortSummary": "3D spatial scanning pipeline converting iPhone RoomPlan USDZ scans into cleaned, optimized GLTF/GLB models with texture baking, mesh decimation, and interactive Three.js web rendering.",
        "fullDescription": "Developed a 3D asset processing pipeline converting Apple RoomPlan USDZ spatial scans into web-optimized GLTF/GLB models. Implemented Open3D and Trimesh routines for vertex deduplication, normal recalculation, and quadric decimation, reducing asset file sizes by ~75% while maintaining 60 FPS interactive rendering in Three.js.",
        "highlights": [
            "USDZ to GLTF/GLB geometry and material conversion microservice",
            "Mesh cleaning with Open3D and Trimesh: vertex deduplication and normal repair",
            "Texture atlas re-projection and lighting normalization",
            "Interactive Three.js web viewer for room dimension inspection"
        ],
        "techStack": [
            "Python", "Open3D", "Trimesh", "Three.js", "FastAPI", "USD Core", "GLTF / GLB", "Docker"
        ],
        "featured": False
    },
    {
        "id": "real-estate-core-scoring-infrastructure",
        "title": "Real Estate Scoring & Location Analytics Engine",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Yourhome Platform",
        "category": "backend-cloud",
        "categoryLabel": "Backend & Cloud Systems",
        "badge": "Backend Microservice",
        "impact": "Composite location scoring, walking distance engine & multi-variable ranking",
        "shortSummary": "Backend microservice computing composite property evaluation scores, transit walking distance matrices, and price-per-square-meter value distributions.",
        "fullDescription": "Built a backend data processing microservice at Yourhome calculating multi-factor property scores: transit walking distances (OSRM / Google Maps APIs), neighborhood amenity density, and price-per-square-meter value metrics relative to local distributions. Maintained dual-write consistency between AWS RDS MySQL and Google Cloud Firestore.",
        "highlights": [
            "Composite property scoring engine with parameterized weighting",
            "Transit walking distance and travel time calculation with OSRM and Maps APIs",
            "Price-per-sqm value scoring relative to neighborhood baseline distributions",
            "Dual-sync consistency between MySQL RDS and Google Cloud Firestore"
        ],
        "techStack": [
            "Python", "FastAPI", "MySQL RDS", "Google Cloud Firestore", "SSHTunnel",
            "Pydantic", "Pandas", "NumPy", "Docker"
        ],
        "featured": False
    },
    {
        "id": "yourhome-seo-sitemap-engine",
        "title": "Schema-Driven Dynamic SEO & Sitemap Microservice",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Yourhome Platform",
        "category": "backend-cloud",
        "categoryLabel": "Backend & Cloud Systems",
        "badge": "Backend Microservice",
        "impact": "Dynamic XML sitemaps, JSON-LD Schema.org generators & Firestore caching for 50k+ URLs",
        "shortSummary": "FastAPI microservice generating dynamic, paginated XML sitemaps, Schema.org JSON-LD microdata, and clean slug routing for property search engine indexing.",
        "fullDescription": "Designed a schema-first SEO microservice at Yourhome. Generated dynamic paginated XML sitemaps supporting 50,000+ URLs and produced Schema.org JSON-LD structured data (RealEstateListing, Product, BreadcrumbList) for search engine indexing. Implemented Firestore response caching to reduce database overhead.",
        "highlights": [
            "Paginated XML sitemap generator supporting 50,000+ URLs per index chunk",
            "Schema.org JSON-LD metadata generator for real estate listings",
            "Firestore-backed caching layer reducing database load by >90%",
            "FastAPI async routing with gzip compression and cache-control headers"
        ],
        "techStack": [
            "Python", "FastAPI", "Google Cloud Firestore", "Pydantic", "MySQL RDS", "Docker", "Postman"
        ],
        "featured": False
    },
    {
        "id": "yourhome-auto-admin-agent",
        "title": "Automated Customer Service & Inquiry Chatbot",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Yourhome Platform",
        "category": "agents-automation",
        "categoryLabel": "Multi-Agent & Automation",
        "badge": "Chatbot & Automation",
        "impact": "Intent recognition, lead qualification & MySQL/Firestore response synthesis",
        "shortSummary": "Administrative customer inquiry assistant on LINE and Web Chat using Gemini for intent routing, property inventory queries, and CRM lead capture.",
        "fullDescription": "Developed a customer inquiry agent connecting LINE Messaging API and Web Chat. Used Google Gemini for intent classification (price inquiry, viewing booking, location query), queried property listings from MySQL RDS and Firestore leads, and generated polite, structured replies.",
        "highlights": [
            "Skill-based architecture separating database, Firestore, and LINE messaging skills",
            "Gemini prompt orchestration with structured business persona guidelines",
            "Automated lead qualification and CRM ingestion into Firestore",
            "FastAPI webhook receiver with secure SSH database tunneling"
        ],
        "techStack": [
            "Python", "FastAPI", "Google Gemini", "line-bot-sdk", "Firestore", "MySQL RDS", "Docker"
        ],
        "featured": False
    },
    {
        "id": "pickleball-cv-ai-capture-scoring",
        "title": "Pickleball AI: Edge Video Analysis & IoT Scoring Prototype",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Yourhome Platform",
        "category": "cv-edge",
        "categoryLabel": "Computer Vision & Edge AI",
        "badge": "Edge IoT & CV",
        "impact": "Trajectory tracking, rally hit extraction & Gemini Flash video reasoning",
        "shortSummary": "Edge-to-Cloud sports analytics prototype combining Raspberry Pi audio/motion rally triggers with Gemini Flash video reasoning and YOLO trajectory tracking.",
        "fullDescription": "Developed an edge-to-cloud sports analytics prototype. Used audio and motion triggers on Raspberry Pi boards to identify rally start/end points, sliced lightweight video clips, and sent them to Google Gemini Flash and YOLO models to evaluate score updates and rule compliance.",
        "highlights": [
            "Edge-to-Cloud design (Raspberry Pi edge trigger + Cloud VLM)",
            "Audio impact detection (paddle hit triggers) + motion settle detection",
            "YOLO trajectory tracking for ball bounding and court baseline zone mapping",
            "Google Gemini Flash multimodal video reasoning for rule verification"
        ],
        "techStack": [
            "Python", "OpenCV", "YOLOv8/v11", "Google Gemini Flash", "FFmpeg",
            "Raspberry Pi", "ESP32", "Node.js", "Vite / React"
        ],
        "featured": False
    },
    {
        "id": "drone-crack-detection-geospatial-cv",
        "title": "Structural Crack Detection on Drone Aerial Footage",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "SKYVIV (Internship)",
        "category": "geospatial-3d",
        "categoryLabel": "Geospatial AI & 3D Analytics",
        "badge": "Drone CV System",
        "impact": "CNN classification & OpenCV tracking for pipe inspection on high-res drone footage",
        "shortSummary": "Computer Vision pipeline combining Deep Learning CNN image classification with OpenCV object tracking for structural crack detection on drone pipe inspection videos.",
        "fullDescription": "Developed during the AI & Geospatial internship at Sky Visual Imaging Venture (SKYVIV). Designed to inspect industrial pipes from high-resolution drone camera feeds using Deep Learning CNN candidate classification and OpenCV spatial R-Tree indexing for continuous crack landmark tracking.",
        "highlights": [
            "Two-phase architecture: CNN deep learning classification + OpenCV tracking",
            "High-resolution drone video processing with perspective compensation",
            "Spatial indexing using R-Tree for continuous crack landmark tracking",
            "Morphological contour measurement for crack width and length estimation"
        ],
        "techStack": [
            "Python", "TensorFlow / Keras", "OpenCV", "NumPy", "R-Tree", "Matplotlib"
        ],
        "featured": False
    },
    {
        "id": "geospatial-crop-yield-prediction",
        "title": "Geospatial AI & Satellite Crop Yield Prediction",
        "type": "company",
        "typeLabel": "Industry Experience",
        "companyName": "Chulalongkorn / SKYVIV Research",
        "category": "geospatial-3d",
        "categoryLabel": "Geospatial AI & 3D Analytics",
        "badge": "Geospatial Modeling",
        "impact": "Random Forest & Gradient Boosting regression on multispectral satellite imagery (NDVI/EVI)",
        "shortSummary": "Predictive agricultural modeling framework estimating crop yields from satellite multispectral imagery, vegetation indices (NDVI, EVI), weather dynamics, and soil metrics.",
        "fullDescription": "Geospatial data science research predicting crop yields. Processed satellite multispectral remote sensing data to compute vegetation health indices (NDVI, EVI, SAVI), combined with meteorological climate data, evaluated using Random Forest and Gradient Boosting regression models.",
        "highlights": [
            "Multispectral satellite remote sensing data ingestion (Sentinel-2 / Landsat)",
            "Vegetation index computation: NDVI, EVI, SAVI, and NDWI",
            "Multi-modal fusion: Remote sensing spectral bands + weather climate data + soil metrics",
            "Random Forest and Gradient Boosting regression models with cross-validation"
        ],
        "techStack": [
            "Python", "MATLAB", "Pandas", "NumPy", "Scikit-Learn", "Rasterio", "Geopandas", "Matplotlib"
        ],
        "featured": False
    }
]

# Combined projects list
ALL_PROJECTS = PERSONAL_PROJECTS + COMPANY_PROJECTS

STARTUP_LEARNINGS = [
    {
        "icon": "fa-bolt",
        "title": "Fast Adaptation & Rapid Execution",
        "tag": "Agility & Speed",
        "description": "In a fast-paced startup environment, I quickly learned to pick up unfamiliar frameworks and libraries (e.g. OpenVINO, Playwright, Groq, LangChain) and bring working prototypes into production within short turnaround cycles."
    },
    {
        "icon": "fa-book-open-reader",
        "title": "Self-Directed Continuous Learning",
        "tag": "Curiosity & Depth",
        "description": "Thrive on reading official documentation, research papers (YOLO-Pose, ArcFace embeddings, Hybrid RRF), and discovering edge optimization techniques independently without waiting for step-by-step instructions."
    },
    {
        "icon": "fa-cube",
        "title": "Modular & Pure Function Mindset",
        "tag": "Code Quality",
        "description": "Adopted a skill-driven, config-first engineering standard where core math and logic are isolated into deterministic pure functions (no hidden side effects), making unit testing and multi-agent reuse straightforward."
    },
    {
        "icon": "fa-arrows-split-up-and-left",
        "title": "Pragmatic Problem Solving",
        "tag": "Cost & Efficiency",
        "description": "Focused on practical trade-offs between accuracy, compute cost, and latency — such as implementing low-cost edge triggers + cloud VLM instead of maintaining expensive always-on GPU clusters."
    },
    {
        "icon": "fa-users-gear",
        "title": "Cross-Functional Collaboration",
        "tag": "Teamwork & Delivery",
        "description": "Collaborated closely with backend developers and QA to understand business needs, integrate API endpoints, handle edge cases, and ensure clean handover of deployed microservices."
    }
]

RESUME_DATA = {
    "name": "Kwankhao Sivasomboon",
    "title": "AI Engineer",
    "headline": "AI Engineer · Computer Vision · GenAI/RAG · Backend & Cloud",
    "photo": "assets/profile_photo.jpg",
    "contact": {
        "email": "Kwankhaosiva@gmail.com",
        "phone": "(+66) 95-959-6921",
        "linkedin": "https://linkedin.com/in/kwankhao-sivasomboon",
        "github": "https://github.com/Kwankhao-Sivasomboon",
        "location": "Bangkok, Thailand"
    },
    "summary": "AI Engineer with hands-on experience building practical AI-powered systems across computer vision, GenAI/RAG, backend services, and data pipelines. Developed real-time computer vision applications, LLM-powered automation, and deployable APIs using Python, FastAPI, PyTorch, Docker, and GCP. Work spans AI model integration, real-time inference, data processing, and backend engineering.",
    "skills": {
        "programming": ["Python", "SQL", "PostgreSQL", "MySQL", "Pandas", "NumPy", "MATLAB", "JavaScript", "HTML/CSS"],
        "computer_vision": [
            "PyTorch", "YOLOv11 / YOLO11-Pose", "OpenCV", "OpenVINO (FP16)", "InsightFace / ArcFace",
            "ResNet-CRNN", "CTC Loss", "MobileNetV2", "SuperVision", "Contour Analysis"
        ],
        "genai_rag": [
            "Google Gemini (1.5 / 2.5 Flash)", "Groq Whisper STT", "Ollama", "LangChain",
            "Hybrid RAG", "ChromaDB", "BM25", "Reciprocal Rank Fusion (RRF)", "Pydantic",
            "Structured Outputs", "LLM Evaluation"
        ],
        "backend_cloud": [
            "FastAPI", "Pydantic", "REST APIs", "Docker", "Google Cloud Platform (GCP)",
            "Cloud Run", "Cloud Build", "Artifact Registry", "Firestore", "Secret Manager",
            "SSE (Server-Sent Events)", "Git / GitHub Actions", "Linux / Bash"
        ],
        "qa_automation": [
            "Playwright", "Requests", "Multi-Agent Systems", "SSHTunnel", "PyTest", "Postman Collections"
        ],
        "geospatial_3d": [
            "Satellite Remote Sensing (NDVI / EVI)", "Drone Aerial Imagery", "LiDAR Analysis",
            "Three.js 3D Web", "Open3D / Trimesh", "ESP32 BLE IoT"
        ]
    },
    "experience": [
        {
            "role": "AI Engineer",
            "company": "Yourhome Platform",
            "period": "Mar 2026 – Aug 2026",
            "location": "Bangkok, Thailand",
            "achievements": [
                "Developing **StaffLenz AI**, an edge-first computer vision platform for workplace analytics, integrating multi-camera RTSP streams, YOLOv11-Pose, InsightFace/ArcFace, OpenVINO FP16 inference, polygon desk zones, and a latest-frame batching queue for real-time processing.",
                "Improved worker identity stability using face embeddings, head-pose filtering, identity caching, and multi-angle enrollment; connected recognized workers with desk-zone and activity-state logic.",
                "Implemented real-time Server-Sent Events (SSE) event delivery, activity history, retention cleanup, and LINE alert workflows to connect computer vision events with the management dashboard.",
                "Developed an asynchronous Thai speech/text-to-search pipeline using Groq STT, Llama/Gemini, Pydantic validation, and fuzzy location normalization to convert unstructured inquiries into structured search parameters.",
                "Built a config-driven AI-assisted QA framework using Playwright, Gemini, and Python to generate matrix test cases, validate API behavior against database rules via SSH tunnels, and surface backend regressions.",
                "Configured Docker-based CI/CD workflows with Google Cloud Build, Artifact Registry, and Cloud Run to prepare backend and management services for cloud deployment."
            ]
        },
        {
            "role": "AI & Geospatial Intern",
            "company": "Sky Visual Imaging Venture Company Ltd. (SKYVIV)",
            "period": "May 2024 – Jul 2024",
            "location": "Bangkok, Thailand",
            "achievements": [
                "Applied YOLO and OpenCV to drone imagery for structural crack detection in pipe inspection, and analyzed LiDAR and multispectral data for 3D and computer vision workflows.",
                "Developed Random Forest and Gradient Boosting regression models in MATLAB to forecast agricultural crop yield from satellite and drone geospatial data."
            ]
        }
    ],
    "education": [
        {
            "institution": "Chulalongkorn University, Thailand",
            "degree": "B.Eng. Survey Engineering",
            "period": "2021 – 2025",
            "coursework": [
                "Artificial Intelligence for Engineers",
                "Geospatial Data Science and Analysis",
                "Photogrammetry & Remote Sensing",
                "Computer Programming & Algorithms"
            ]
        }
    ],
    "competitions": [
        {
            "name": "Hackathon: Sustainability Waste Management",
            "role": "Team Member & AI Solution",
            "description": "Designed a waste management solution in a sustainability-focused competition."
        },
        {
            "name": "TheChallengerXKrungsri FinTech Case",
            "role": "Team Member & FinTech Proposition",
            "description": "Developed a FinTech value proposition tailored for Gen Z users."
        }
    ]
}

def main():
    print("Generating reformed portfolio dataset...")
    
    data_bundle = {
        "resume": RESUME_DATA,
        "personalProjects": PERSONAL_PROJECTS,
        "companyProjects": COMPANY_PROJECTS,
        "projects": ALL_PROJECTS,
        "startupLearnings": STARTUP_LEARNINGS,
        "typeFilters": [
            {"id": "all", "label": "All Projects", "count": len(ALL_PROJECTS)},
            {"id": "personal", "label": "Personal Projects (Deep Dive & Code)", "count": len(PERSONAL_PROJECTS)},
            {"id": "company", "label": "Company & Industry Experience", "count": len(COMPANY_PROJECTS)}
        ],
        "categories": [
            {"id": "all", "label": "All Categories", "count": len(ALL_PROJECTS)},
            {"id": "cv-edge", "label": "Computer Vision & Edge AI", "icon": "eye"},
            {"id": "genai-rag", "label": "GenAI, LLMs & Agents", "icon": "cpu"},
            {"id": "agents-automation", "label": "Multi-Agent & QA", "icon": "robot"},
            {"id": "backend-cloud", "label": "Backend & Cloud Systems", "icon": "server"},
            {"id": "geospatial-3d", "label": "Geospatial & 3D Analytics", "icon": "globe"}
        ],
        "stats": {
            "totalProjects": len(ALL_PROJECTS),
            "personalProjectsCount": len(PERSONAL_PROJECTS),
            "companyProjectsCount": len(COMPANY_PROJECTS),
            "ocrAccuracy": "~90%",
            "ragGrounding": "93.8%",
            "sttLatency": "< 320ms"
        }
    }

    # Save as JSON
    json_path = os.path.join(BASE_DIR, "portfolio_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_bundle, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON data to {json_path}")

    # Save as JS for client-side loading
    js_path = os.path.join(BASE_DIR, "portfolio_data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("/* Auto-generated Portfolio Dataset for Kwankhao Sivasomboon */\n")
        f.write("window.PORTFOLIO_DATA = ")
        json.dump(data_bundle, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"Saved JS data to {js_path}")

if __name__ == "__main__":
    main()
