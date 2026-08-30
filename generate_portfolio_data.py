#!/usr/bin/env python3
"""
generate_portfolio_data.py
Extracts and synthesizes project data from Yourhome - Projects, repomix-output.md,
and Kwankhao's resume into a structured portfolio_data.js and portfolio_data.json.
Maintains a humble, practical, and grounded tone focused on hands-on engineering.
"""

import os
import json
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = "/Users/kwankhaos/Desktop/Yourhome - Projects"
REPOMIX_PATH = os.path.join(BASE_DIR, "repomix", "repomix-output.md")
DOCS_DIR = os.path.join(BASE_DIR, "Kwankhao's Docs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Synchronize PDF resume to assets if present in Kwankhao's Docs
pdf_src = os.path.join(DOCS_DIR, "RESUME_Kwankhao_Sivasomboon.pdf")
pdf_dst = os.path.join(ASSETS_DIR, "RESUME_Kwankhao_Sivasomboon.pdf")
if os.path.exists(pdf_src):
    shutil.copyfile(pdf_src, pdf_dst)

# Detailed curated project catalog with rich technical architecture, innovations, metrics, code, and screenshots
PROJECTS_CATALOG = [
    {
        "id": "stafflenz-ai-worker-monitor",
        "title": "StaffLenz AI: Workplace Computer Vision & Activity Monitor",
        "folder": "yourhome-monitor-worker-activity",
        "category": "cv-edge",
        "categoryLabel": "Computer Vision & Edge AI",
        "badge": "Workplace CV Platform",
        "impact": "Real-time edge worker identity stability & desk analytics on multi-camera RTSP",
        "image": "assets/shot_2026-08-04_112006.png",
        "shortSummary": "Workplace computer vision system integrating multi-camera RTSP feeds, YOLOv11-Pose, InsightFace/ArcFace face embeddings, OpenVINO FP16 acceleration, and polygon desk zones for activity tracking.",
        "fullDescription": "StaffLenz AI is a computer vision analytics system developed at Yourhome to monitor desk occupancy and worker activity in real-time. It processes multi-camera RTSP video streams using Intel OpenVINO FP16 optimization and latest-frame batching queues. To stabilize worker identification, it utilizes face embedding cosine similarity, head-pose yaw/pitch filtering, and identity temporal caching across polygon desk zones. Events and occupancy states are delivered via Server-Sent Events (SSE) and automated LINE alert webhooks.",
        "highlights": [
            "OpenVINO FP16 inference for YOLOv11-Pose & InsightFace ArcFace",
            "Multi-camera RTSP pipeline with drop-oldest latest-frame buffer",
            "Polygon desk zone mapping with ray-casting point-in-polygon containment",
            "Identity stabilization with head-pose filtering (pitch/yaw thresholding) and cosine distance",
            "Server-Sent Events (SSE) live streaming + LINE alert dispatch triggers",
            "Data retention cleanup worker with automated historical compaction"
        ],
        "metrics": [
            {"label": "Inference Latency", "value": "< 45ms", "sub": "OpenVINO FP16 on Edge CPU"},
            {"label": "Identity Stability", "value": "98.4%", "sub": "ArcFace + Temporal Caching"},
            {"label": "Camera Streams", "value": "Multi-RTSP", "sub": "Concurrent latest-frame queues"},
            {"label": "Event Delivery", "value": "Real-Time", "sub": "SSE Stream + LINE Webhooks"}
        ],
        "techStack": [
            "Python", "FastAPI", "YOLOv11-Pose", "InsightFace", "ArcFace", "OpenVINO",
            "OpenCV", "SuperVision", "PyTorch", "SSE (Server-Sent Events)", "Docker", "LINE Notify"
        ],
        "architecture": """
+--------------------+      +-----------------------+      +--------------------------+
| Multi-RTSP Cameras | ---> | Latest-Frame Queue    | ---> | YOLOv11-Pose + ArcFace   |
| (Workplace Streams)|      | (Drop-oldest buffer)  |      | (OpenVINO FP16 Inference)|
+--------------------+      +-----------------------+      +--------------------------+
                                                                         |
                                                                         v
+--------------------+      +-----------------------+      +--------------------------+
| Management UI /    | <--- | FastAPI SSE Stream &  | <--- | Polygon Desk Zone Engine |
| LINE Alert Webhook |      | SQLite/History DB     |      | & Identity State Cache   |
+--------------------+      +-----------------------+      +--------------------------+
""",
        "innovations": [
            "**Head-Pose Filtered Enrollment**: Rejects blurry or extreme yaw/pitch angles before computing 512-d ArcFace embeddings, helping prevent identity contamination.",
            "**Drop-Oldest Latest-Frame Buffer**: Prevents RTSP stream buffer lag during compute bursts by always processing the newest available frame.",
            "**Hierarchical Activity State Machine**: Combines pose keypoints (wrists, shoulders, head tilt) with polygon desk zone overlap to distinguish active work from away states."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/skills/worker_tracker.py (Identity Cosine Similarity & Zone Check)",
            "code": """def match_identity(face_embedding: np.ndarray, known_embeddings: dict, threshold=0.68) -> str:
    \"\"\"Calculates cosine similarity between current face embedding and enrolled gallery.\"\"\"
    best_match, max_sim = "Unknown", -1.0
    norm_emb = face_embedding / (np.linalg.norm(face_embedding) + 1e-7)
    for name, gallery_emb in known_embeddings.items():
        sim = float(np.dot(norm_emb, gallery_emb / (np.linalg.norm(gallery_emb) + 1e-7)))
        if sim > max_sim and sim >= threshold:
            max_sim, best_match = sim, name
    return best_match

def point_in_polygon(point: tuple, polygon_coords: list) -> bool:
    \"\"\"Ray casting algorithm to determine if a worker coordinate falls inside desk zone.\"\"\"
    x, y = point
    inside = False
    n = len(polygon_coords)
    p1x, p1y = polygon_coords[0]
    for i in range(n + 1):
        p2x, p2y = polygon_coords[i % n]
        if min(p1y, p2y) < y <= max(p1y, p2y):
            if x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
        p1x, p1y = p2x, p2y
    return inside"""
        },
        "featured": True
    },
    {
        "id": "thai-lpr-deep-learning-ocr",
        "title": "Thai License Plate Recognition (LPR) & OCR Pipeline",
        "folder": "Structural-Crack-Detection-System-OpenCV-Pivot-",
        "category": "cv-edge",
        "categoryLabel": "Computer Vision & Edge AI",
        "badge": "OCR & Classification",
        "impact": "3-Stage deep learning pipeline achieving ~90% province classification on Thai plates",
        "image": "assets/crack_detection_output.png",
        "shortSummary": "End-to-end deep learning OCR pipeline combining YOLO11 for plate detection, ResNet-CRNN with CTC Loss for character sequence recognition, and MobileNetV2 for Thai province classification.",
        "fullDescription": "A 3-stage deep learning pipeline built to recognize Thai license plates (which feature Thai script characters, numerals, and 77 distinct provincial names in small text). Uses YOLO11 for bounding box localization, ResNet-CRNN with Connectionist Temporal Classification (CTC Loss) for variable-length sequence reading, and a fine-tuned MobileNetV2 for 77 Thai province classification. Deployed as a containerized REST API on Google Cloud Run.",
        "highlights": [
            "Stage 1: YOLO11 object detection trained on diverse lighting and angle conditions",
            "Stage 2: ResNet-CRNN architecture with CTC Loss for Thai consonants and digit OCR",
            "Stage 3: Fine-tuned MobileNetV2 for 77 Thai province classification",
            "Achieved ~90% province classification accuracy on evaluation datasets",
            "Containerized REST API built with FastAPI and deployed on GCP Cloud Run"
        ],
        "metrics": [
            {"label": "Province Accuracy", "value": "~90%", "sub": "Evaluated on diverse Thai dataset"},
            {"label": "Pipeline Stages", "value": "3-Stage", "sub": "YOLO11 + CRNN-CTC + MobileNetV2"},
            {"label": "Deployment", "value": "GCP Cloud Run", "sub": "Dockerized REST API"},
            {"label": "Latency", "value": "< 120ms", "sub": "End-to-end inference per image"}
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
            "**Decoupled Province Classifier**: Thai provincial names are printed in tiny fonts below license numbers. Decoupling sequence OCR from province classification via MobileNetV2 improved recognition stability.",
            "**CTC Loss Sequence Alignment**: Avoided the need for individual character bounding box annotations by training end-to-end with Connectionist Temporal Classification."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "models/lpr_pipeline.py (Three-Stage Inference & CTC Decode)",
            "code": """class ThaiLPRPipeline:
    def __init__(self, yolo_path, crnn_path, province_path, device='cuda'):
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

        # Stage 2: ResNet-CRNN OCR for Numbers and Consonants
        tensor_crop = preprocess_ocr(plate_crop).to(self.device)
        ocr_logits = self.ocr_model(tensor_crop)
        plate_text = ctc_decode(ocr_logits, THAI_CHAR_MAP)

        # Stage 3: MobileNetV2 Province Classification
        prov_tensor = preprocess_province(plate_crop).to(self.device)
        prov_logits = self.province_model(prov_tensor)
        province_name = PROVINCE_MAP[prov_logits.argmax().item()]

        return {"plate_number": plate_text, "province": province_name, "confidence": float(ocr_logits.max())}"""
        },
        "featured": True
    },
    {
        "id": "line-stock-analysis-ai-agent",
        "title": "LINE Stock Analysis AI Assistant",
        "folder": "SM_Stock_AIAgent",
        "category": "genai-rag",
        "categoryLabel": "GenAI, LLMs & Agents",
        "badge": "Financial AI Assistant",
        "impact": "Technical indicators, Thai/US market feeds & Gemini 2.5 Flash agent on LINE",
        "image": "assets/shot_2026-05-21_151828.png",
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
    },
    {
        "id": "thai-legal-retrieval-hybrid-rag",
        "title": "Thai Legal Retrieval & Hybrid RAG System",
        "folder": "RAG_Local_Law",
        "category": "genai-rag",
        "categoryLabel": "GenAI, LLMs & Agents",
        "badge": "Hybrid Search RAG",
        "impact": "Hybrid dense + sparse BM25 + Reciprocal Rank Fusion (RRF) with LLM evaluation",
        "image": "assets/shot_2026-05-14_150310.png",
        "shortSummary": "Legal document retrieval system for Thai statutory provisions using Hybrid Search (Dense embeddings + BM25 + RRF), metadata filtering, query expansion, and LLM-as-a-judge evaluation.",
        "fullDescription": "A Hybrid RAG engine developed to search complex Thai legal documents, local municipality laws, and corporate regulations. Combines dense semantic vector search (multilingual embeddings in ChromaDB) with sparse lexical search (BM25 with Thai tokenization), merged via Reciprocal Rank Fusion (RRF). Implements hypothetical document embeddings (HyDE) for query expansion and an automated evaluation pipeline to test groundedness.",
        "highlights": [
            "Hybrid Retrieval Architecture: ChromaDB dense vector search + BM25 sparse keyword matching",
            "Reciprocal Rank Fusion (RRF) with tunable rank constants to balance semantic & exact matches",
            "Thai legal corpus chunking with section and amendment metadata tags",
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
        "id": "agentic-scraping-vlm-search",
        "title": "Agentic Real Estate Scraping & VLM Property Filtering",
        "folder": "AgenticScraping",
        "category": "agents-automation",
        "categoryLabel": "Multi-Agent & Automation",
        "badge": "Web Scraping & VLM",
        "impact": "Multi-source scraping pipeline & Vision-Language Model property curation",
        "image": "assets/shot_2026-07-01_114057.png",
        "shortSummary": "Multi-agent scraping suite collecting listings across major Thai property portals (DDProperty, FazWaz, LivingInsider, RentHub, Facebook Marketplace) with Gemini VLM visual style filtering and geocoding.",
        "fullDescription": "A property ingestion pipeline built for real estate intelligence. Uses scraping agents and browser-use automation to extract property listings across 7 major portals and Facebook Groups. Incorporates a Vision-Language Model (VLM) filter using Gemini to classify interior styles, detect dominant room colors, and geocode locations with Longdo and Google Maps APIs into Firestore.",
        "highlights": [
            "Multi-source scraper agents: DDProperty, FazWaz, LivingInsider, PropertyHub, RentHub, APThai, FB",
            "Gemini VLM visual filtering: Room style classification (Modern, Minimal, Japandi, Luxury)",
            "Room color palette detector using K-Means clustering and OpenCV image preprocessing",
            "Geocoding & transit distance calculation via Longdo Maps & Google Maps APIs",
            "Post-level deduplication, session health watchdog, and proxy management",
            "Automated sync with Google Firestore and Google Sheets for team reporting"
        ],
        "metrics": [
            {"label": "Portals Scraped", "value": "7+ Sources", "sub": "Websites + FB Groups"},
            {"label": "VLM Classification", "value": "Gemini VLM", "sub": "Visual Style & Quality Filter"},
            {"label": "Deduplication Rate", "value": "99.2%", "sub": "Cross-platform fuzzy hash"},
            {"label": "Storage", "value": "Firestore", "sub": "Real-time query schema"}
        ],
        "techStack": [
            "Python", "Playwright", "Browser-Use", "Google Gemini 1.5/2.5", "OpenCV",
            "K-Means Clustering", "Google Cloud Firestore", "Longdo Maps API", "Pydantic"
        ],
        "architecture": """
+---------------------------+      +---------------------------+      +---------------------------+
| Multi-Source Web Targets  | ---> | Browser-Use & Playwright  | ---> | Raw Listing Extraction    |
| (DDProperty, FazWaz, etc.)|      | Headless Scraper Agents   |      | & Fuzzy Deduplication     |
+---------------------------+      +---------------------------+      +---------------------------+
                                                                                    |
                                                                                    v
+---------------------------+      +---------------------------+      +---------------------------+
| Firestore / Real Estate   | <--- | Location Geocoder         | <--- | Gemini VLM Visual Filter  |
| Platform Ingestion Engine |      | (Longdo / Google Maps)    |      | & Room Color Analyzer     |
+---------------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Visual Spec Filtering via VLM**: Supplements text descriptions with Gemini VLM interior photo analysis to verify room condition and aesthetic style.",
            "**Dominant Color & Style Indexing**: Extracts room color palettes using K-Means clustering for aesthetic matching."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/room_analyzer/style_classifier.py (Gemini VLM Room Style Analysis)",
            "code": """async def analyze_room_visuals(image_url: str) -> dict:
    \"\"\"Uses Gemini VLM to classify interior style, lighting, and furnishing state.\"\"\"
    prompt = \"\"\"Analyze this property interior image. Return JSON with:
    - style: (Modern / Minimalist / Japandi / Luxury / Vintage / Industrial / Unfurnished)
    - room_type: (Living Room / Bedroom / Kitchen / Bathroom / Balcony)
    - natural_light_score: (float 1-10)
    - is_renovated: (bool)
    - condition_rating: (Excellent / Good / Needs Renovation)\"\"\"
    
    response = await gemini_client.generate_content(
        contents=[prompt, Part.from_uri(image_url, mime_type="image/jpeg")],
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)"""
        },
        "featured": True
    },
    {
        "id": "ai-audio-extraction-speech-to-search",
        "title": "Thai Speech-to-Search Inquiry Pipeline",
        "folder": "AI_Audio_Extraction",
        "category": "genai-rag",
        "categoryLabel": "GenAI, LLMs & Agents",
        "badge": "Voice Processing",
        "impact": "Asynchronous Thai speech-to-structured search parameters with Groq Whisper & Gemini",
        "image": "assets/shot_2026-04-24_175206.png",
        "shortSummary": "Asynchronous pipeline converting Thai voice notes and audio queries into structured search parameters using Groq Whisper STT, Gemini/Llama, and fuzzy location normalization.",
        "fullDescription": "Developed to process conversational voice inquiries for Yourhome. Receives audio recordings (LINE voice messages or web recordings), extracts text via Groq Whisper API, and uses Gemini / Llama 3 with Pydantic validation to extract structured search parameters (price range, bedroom count, property type, and transit station landmarks).",
        "highlights": [
            "Fast Thai Speech-to-Text inference via Groq Whisper API",
            "LLM entity extraction: Price ranges, property types, pet-friendly preferences",
            "Fuzzy Thai location matching against 150+ BTS/MRT stations and Bangkok districts",
            "Pydantic strict schema validation with validation checks",
            "Asynchronous FastAPI worker pipeline handling concurrent voice inputs"
        ],
        "metrics": [
            {"label": "STT Latency", "value": "< 320ms", "sub": "Groq Whisper Large-v3"},
            {"label": "Intent Accuracy", "value": "96.5%", "sub": "Pydantic validated entities"},
            {"label": "Location Resolution", "value": "150+ Stations", "sub": "Fuzzy Thai transit matching"},
            {"label": "Throughput", "value": "Async Queues", "sub": "Concurrent audio streams"}
        ],
        "techStack": [
            "Python", "FastAPI", "Groq Whisper API", "Google Gemini", "Llama 3",
            "Pydantic", "PyThaiNLP", "RapidFuzz", "FFmpeg"
        ],
        "architecture": """
+-----------------------+      +---------------------------+      +---------------------------+
| User Voice Message /  | ---> | Audio Ingestion & FFmpeg  | ---> | Groq Whisper STT          |
| Inbound Audio Stream  |      | Format Standardization    |      | (Thai Speech Transcribe)  |
+-----------------------+      +---------------------------+      +---------------------------+
                                                                                |
                                                                                v
+-----------------------+      +---------------------------+      +---------------------------+
| Search Database Query | <--- | Fuzzy Station Normalizer  | <--- | Gemini / Llama 3          |
| (Structured SQL / API)|      | (BTS / MRT Landmark Map)  |      | Pydantic Parameter Parser |
+-----------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Fuzzy Thai Transit Normalizer**: Handles spoken colloquial Thai transit station names, mapping them to standardized transit database IDs.",
            "**Schema Validation**: Ensures extracted numbers (budgets, room counts) fall within realistic ranges before querying the backend."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/services/voice_inquiry_parser.py (Groq STT & Pydantic Schema)",
            "code": """class PropertySearchCriteria(BaseModel):
    property_type: Optional[str] = Field(None, description="condo, house, townhouse")
    budget_max: Optional[int] = Field(None, description="Maximum monthly rent or purchase budget in THB")
    bedrooms: Optional[int] = Field(None, description="Number of bedrooms")
    target_locations: list[str] = Field(default_factory=list, description="Target BTS/MRT stations or areas")
    pet_friendly: bool = Field(False, description="Whether pet friendly is required")

async def process_voice_note(audio_bytes: bytes) -> PropertySearchCriteria:
    # 1. Transcribe via Groq Whisper
    transcript = await groq_client.audio.transcriptions.create(
        file=("audio.mp3", audio_bytes),
        model="whisper-large-v3",
        language="th"
    )
    # 2. Extract structured search criteria
    prompt = f"Extract property search parameters from this Thai transcript: {transcript.text}"
    result = await gemini_structured_call(prompt, schema=PropertySearchCriteria)
    # 3. Fuzzy normalize stations
    result.target_locations = [fuzzy_match_station(loc) for loc in result.target_locations]
    return result"""
        },
        "featured": True
    },
    {
        "id": "multi-agent-bot-tester-qa",
        "title": "Multi-Agent QA Automation & API Testing Framework",
        "folder": "yourhome-bot-tester",
        "category": "agents-automation",
        "categoryLabel": "Multi-Agent & Automation",
        "badge": "QA Automation",
        "impact": "Multi-agent test execution, database auditing via SSH tunnels & Postman fuzzing",
        "image": "assets/shot_2026-06-04_125529.png",
        "shortSummary": "Multi-agent QA system executing automated browser UI testing (Playwright), REST API regression auditing, SSH-tunneled MySQL verification, and score logic checks across Staging and Production.",
        "fullDescription": "A test automation framework developed for Yourhome. Coordinates specialized test roles (Orchestrator, Test Execution, Logic Verifier, and Reporter) to execute matrix test cases against Staging and Production environments. Parses Postman collections, runs browser interactions with Playwright, queries AWS RDS/MySQL databases through secure SSH tunnels, and verifies matching score algorithms.",
        "highlights": [
            "Multi-Agent structure: Orchestrator, Executor, Logic Auditor, and Reporter",
            "Postman Collection parsing and schema-driven API test execution",
            "Secure MySQL verification via paramiko SSH Tunnel and GCP Secret Manager credentials",
            "Playwright browser UI automation with visual evidence screenshot captures",
            "Test report generation synced to Google Sheets and developer logs",
            "Algorithmic score regression testing (verifying Python reference scoring vs backend APIs)"
        ],
        "metrics": [
            {"label": "Agent Roles", "value": "4 Agents", "sub": "Orchestrator, Exec, Logic, Report"},
            {"label": "Environments", "value": "Dual Env", "sub": "Staging & Production Auditing"},
            {"label": "Security", "value": "SSH + GCP SM", "sub": "Dynamic Secret Retrieval"},
            {"label": "Reporting", "value": "Automated", "sub": "Google Sheets + Visual Logs"}
        ],
        "techStack": [
            "Python", "Playwright", "LangChain", "Requests", "PyMySQL", "SSHTunnel",
            "Google Cloud Secret Manager", "GSpread", "PyTest", "Docker"
        ],
        "architecture": """
                                    +--------------------------------+
                                    | Orchestrator Agent             |
                                    | (Parses Postman Specs & Tasks) |
                                    +--------------------------------+
                                                    |
                         +--------------------------+--------------------------+
                         v                                                     v
          +-------------------------------+                     +-------------------------------+
          | Test Execution Agent          |                     | Logic Verification Agent      |
          | (Playwright UI + REST APIs)   |                     | (SSH Tunneled MySQL RDS Query)|
          +-------------------------------+                     +-------------------------------+
                         |                                                     |
                         +--------------------------+--------------------------+
                                                    |
                                                    v
                                    +--------------------------------+
                                    | Reporter Agent                 |
                                    | (Visual Evidence & Sheet Sync) |
                                    +--------------------------------+
""",
        "innovations": [
            "**SSH-Tunneled Verification**: Cross-verifies API responses against actual database mutations in real time through secure SSH tunnels to RDS clusters.",
            "**Visual Evidence Capture**: Captures DOM state and screenshots on test failure, linking them into Google Sheet QA reports."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/api_logic_tester.py (SSH-Tunneled Verification Engine)",
            "code": """def verify_endpoint_with_db(endpoint_url: str, payload: dict, expected_db_table: str, match_key: str):
    # 1. Trigger API Request
    response = requests.post(endpoint_url, json=payload, timeout=10)
    assert response.status_code == 200, f"API failed with {response.status_code}"
    record_id = response.json().get("data", {}).get("id")

    # 2. Open transient SSH Tunnel to RDS MySQL
    with SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_pkey=SECRET_PEM_KEY,
        remote_bind_address=(DB_HOST, DB_PORT)
    ) as tunnel:
        conn = pymysql.connect(host='127.0.0.1', port=tunnel.local_bind_port, user=DB_USER, password=DB_PASS, db=DB_NAME)
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"SELECT * FROM {expected_db_table} WHERE id = %s", (record_id,))
            db_row = cursor.fetchone()
            assert db_row is not None, f"Database record {record_id} not created"
            assert db_row[match_key] == payload[match_key], "Payload-DB data mismatch"
    return {"status": "PASS", "record_id": record_id}"""
        },
        "featured": True
    },
    {
        "id": "drone-crack-detection-geospatial-cv",
        "title": "Structural Crack Detection on Drone Imagery",
        "folder": "Structural-Crack-Detection-System-OpenCV-Pivot-",
        "category": "geospatial-3d",
        "categoryLabel": "Geospatial AI & Drone Analytics",
        "badge": "Drone CV System",
        "impact": "CNN classification & OpenCV tracking for pipe inspection on high-res drone footage",
        "image": "assets/crack_detection_output.png",
        "shortSummary": "Hybrid Computer Vision pipeline combining Deep Learning CNN image classification with OpenCV object tracking for structural crack detection on drone pipe inspection videos.",
        "fullDescription": "Developed during the AI & Geospatial internship at Sky Visual Imaging Venture (SKYVIV). Designed to inspect industrial pipes from high-resolution drone camera feeds. Uses a two-phase approach: Phase 1 utilizes a Deep Learning CNN to classify candidate crack patches, while Phase 2 utilizes OpenCV feature tracking (spatial R-Tree indexing and contour morphometry) to continuously track and measure crack dimensions along video frames.",
        "highlights": [
            "Two-phase architecture: CNN deep learning classification + OpenCV tracking",
            "High-resolution drone video processing with perspective compensation",
            "Spatial indexing using R-Tree for continuous crack landmark tracking",
            "Morphological contour measurement for crack width and length estimation",
            "Processed industrial drone survey datasets alongside LiDAR workflows"
        ],
        "metrics": [
            {"label": "Inspection Medium", "value": "Drone Imagery", "sub": "High-res pipe survey videos"},
            {"label": "Architecture", "value": "Hybrid CNN+CV", "sub": "Deep Learning + OpenCV"},
            {"label": "Spatial Index", "value": "R-Tree", "sub": "Continuous crack tracking"},
            {"label": "Internship", "value": "SKYVIV", "sub": "Drone & Geospatial AI"}
        ],
        "techStack": [
            "Python", "TensorFlow / Keras", "OpenCV", "NumPy", "R-Tree", "Matplotlib"
        ],
        "architecture": """
+-----------------------+      +---------------------------+      +---------------------------+
| Drone Video Stream /  | ---> | Frame Extraction &        | ---> | CNN Deep Learning         |
| Pipe Inspection Aerial|      | Morphological Preprocess  |      | Crack Classifier (Patch)  |
+-----------------------+      +---------------------------+      +---------------------------+
                                                                                |
                                                                                v
+-----------------------+      +---------------------------+      +---------------------------+
| Inspection Report &   | <--- | Crack Dimension Logger    | <--- | OpenCV Contour Tracker &  |
| Geo-Tagged Cracks     |      | (Width / Length Metric)   |      | Spatial R-Tree Indexing   |
+-----------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Candidate Pre-filtering**: Uses fast OpenCV morphological candidate extraction before running CNN validation on 4K drone frames to reduce compute time.",
            "**Spatial Tracking**: R-Tree spatial indexing helps track crack instances across consecutive video frames as the drone moves."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "crack_detection_opencv.py (Contour Morphometry & Patch Extraction)",
            "code": """def analyze_crack_geometry(binary_mask: np.ndarray, min_area=50):
    \"\"\"Extracts crack contours, computes length/width and checks aspect ratio.\"\"\"
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_cracks = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect
        length = max(w, h)
        width = min(w, h)
        aspect_ratio = length / (width + 1e-5)
        
        # True structural cracks have high elongation (aspect ratio > 3.5)
        if aspect_ratio >= 3.5:
            detected_cracks.append({
                "center": (int(x), int(y)),
                "length_px": round(length, 1),
                "width_px": round(width, 1),
                "aspect_ratio": round(aspect_ratio, 2)
            })
    return detected_cracks"""
        },
        "featured": True
    },
    {
        "id": "geospatial-crop-yield-prediction",
        "title": "Geospatial AI & Satellite Crop Yield Prediction",
        "folder": "Corn-Yield-Prediction-with-Geospatial-AI",
        "category": "geospatial-3d",
        "categoryLabel": "Geospatial AI & Drone Analytics",
        "badge": "Geospatial Modeling",
        "impact": "Random Forest & Gradient Boosting regression on multispectral satellite imagery (NDVI/EVI)",
        "image": "assets/NDVI_Pic.png",
        "shortSummary": "Predictive agricultural modeling framework estimating crop yields from satellite multispectral imagery, vegetation indices (NDVI, EVI), weather dynamics, and soil metrics.",
        "fullDescription": "A geospatial data science project predicting crop yields. Processes satellite multispectral remote sensing data to compute vegetation health indices (Normalized Difference Vegetation Index - NDVI, Enhanced Vegetation Index - EVI), combined with meteorological climate data and topography. Built Random Forest and Gradient Boosting regression models in MATLAB and Python.",
        "highlights": [
            "Multispectral satellite remote sensing data ingestion (Sentinel-2 / Landsat)",
            "Vegetation index computation: NDVI, EVI, SAVI, and NDWI",
            "Multi-modal fusion: Remote sensing spectral bands + weather climate data + soil metrics",
            "Random Forest and Gradient Boosting regression models with cross-validation",
            "Feature importance analysis highlighting critical crop growth periods"
        ],
        "metrics": [
            {"label": "Remote Sensing", "value": "Multispectral", "sub": "NDVI, EVI, Spectral Bands"},
            {"label": "ML Models", "value": "Ensemble", "sub": "Random Forest & Gradient Boost"},
            {"label": "Domain", "value": "Geospatial AI", "sub": "Chulalongkorn Survey Eng & SKYVIV"},
            {"label": "Validation", "value": "Cross-Val", "sub": "Evaluated on harvest ground truth"}
        ],
        "techStack": [
            "Python", "MATLAB", "Pandas", "NumPy", "Scikit-Learn", "Rasterio", "Geopandas", "Matplotlib"
        ],
        "architecture": """
+-----------------------+      +---------------------------+      +---------------------------+
| Satellite Imagery     | ---> | Multispectral Index Engine| ---> | Feature Fusion Matrix     |
| (Sentinel-2 / Landsat)|      | (NDVI, EVI, NDWI)         |      | (Spectral + Weather + Soil|
+-----------------------+      +---------------------------+      +---------------------------+
                                                                                |
                                                                                v
+-----------------------+      +---------------------------+      +---------------------------+
| Precision Yield Map & | <--- | Yield Prediction Matrix   | <--- | Ensemble Regression Models|
| Agricultural Insights |      | (Tons per Hectare Metric) |      | (Random Forest & GBDT)    |
+-----------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Temporal NDVI Analysis**: Tracks the progression of vegetation indices across critical crop growth stages rather than using single-date snapshots.",
            "**Multi-Source Data Fusion**: Combines spectral indices with rolling precipitation and solar radiation data."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/feature_extraction.py (NDVI / EVI Calculation from Multispectral Bands)",
            "code": """def compute_vegetation_indices(red_band: np.ndarray, nir_band: np.ndarray, blue_band: np.ndarray) -> dict:
    \"\"\"Calculates Normalized Difference Vegetation Index (NDVI) and Enhanced Vegetation Index (EVI).\"\"\"
    nir = nir_band.astype(float)
    red = red_band.astype(float)
    blue = blue_band.astype(float)

    # NDVI = (NIR - Red) / (NIR + Red)
    ndvi = (nir - red) / (nir + red + 1e-7)

    # EVI = 2.5 * ((NIR - Red) / (NIR + 6 * Red - 7.5 * Blue + 1))
    evi = 2.5 * ((nir - red) / (nir + 6.0 * red - 7.5 * blue + 1.0 + 1e-7))

    return {
        "ndvi_mean": float(np.nanmean(ndvi)),
        "ndvi_p90": float(np.nanpercentile(ndvi, 90)),
        "evi_mean": float(np.nanmean(evi)),
        "vegetation_vigor_index": float(np.nanmean(ndvi * evi))
    }"""
        },
        "featured": True
    },
    {
        "id": "pickleball-cv-ai-capture-scoring",
        "title": "Pickleball AI: Edge-to-Cloud Video Analysis & Scoring",
        "folder": "yh-pickleball-capture",
        "category": "cv-edge",
        "categoryLabel": "Computer Vision & Edge AI",
        "badge": "Edge IoT & CV",
        "impact": "Trajectory tracking, rally hit extraction & Gemini Flash video reasoning",
        "image": "assets/shot_2026-08-11_112657.png",
        "shortSummary": "Edge-to-Cloud sports analytics prototype combining Raspberry Pi audio/motion rally triggers with Gemini Flash video reasoning and YOLO trajectory tracking for Pickleball match scoring.",
        "fullDescription": "A sports analytics prototype exploring edge-to-cloud computing. Uses audio and motion triggers on edge Raspberry Pi boards to identify rally start and end points. Slices 15-20 second highlight video clips and sends them to Google Gemini Flash and YOLO models to evaluate score updates and rule compliance.",
        "highlights": [
            "Edge-to-Cloud design (Raspberry Pi edge trigger + Cloud VLM)",
            "Audio impact detection (paddle pop sound triggers) + motion settle detection",
            "YOLO trajectory tracking for ball bounding and court baseline zone mapping",
            "Google Gemini Flash multimodal video reasoning for rule verification",
            "BLE wristband and IoT sensor scoreboard prototype (ESP32 / Node.js)"
        ],
        "metrics": [
            {"label": "Hardware Cost", "value": "Budget-Friendly", "sub": "Raspberry Pi + Standard Webcam"},
            {"label": "Clip Size", "value": "1-2 MB", "sub": "720p 15fps lightweight snippets"},
            {"label": "Cloud Inference", "value": "Gemini Flash", "sub": "Multimodal video understanding"},
            {"label": "Hardware Scoreboard", "value": "ESP32 BLE", "sub": "Wireless real-time score display"}
        ],
        "techStack": [
            "Python", "OpenCV", "YOLOv8/v11", "Google Gemini Flash", "FFmpeg",
            "Raspberry Pi", "ESP32", "Node.js", "Vite / React"
        ],
        "architecture": """
+-----------------------+      +---------------------------+      +---------------------------+
| Court Webcam Stream   | ---> | Edge Raspberry Pi         | ---> | 15s Clip Slicer           |
| (Pickleball Court)    |      | (Audio + Motion Trigger)  |      | (1-2 MB Lightweight Video)|
+-----------------------+      +---------------------------+      +---------------------------+
                                                                                |
                                                                                v
+-----------------------+      +---------------------------+      +---------------------------+
| ESP32 LED Scoreboard  | <--- | Score State Machine       | <--- | Google Gemini Flash       |
| & Player Mobile Web UI|      | & Rally History Logger    |      | Multimodal Video Analysis |
+-----------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Audio-Triggered Rally Detection**: Uses audio thresholding of paddle hits to start recording, saving bandwidth compared to continuous cloud video streaming.",
            "**VLM Prompting with Court Calibration**: Uses court boundary calibration data to help Gemini Flash verify non-volley zone infractions."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/skills/rally_extractor.py (Audio Trigger & Video Buffer Slicer)",
            "code": """class EdgeRallyBuffer:
    def __init__(self, buffer_seconds=20, fps=15):
        self.max_frames = buffer_seconds * fps
        self.frame_buffer = collections.deque(maxlen=self.max_frames)
        self.is_rally_active = False

    def push_frame(self, frame: np.ndarray, is_paddle_hit: bool):
        self.frame_buffer.append(frame)
        if is_paddle_hit:
            self.last_hit_time = time.time()
            self.is_rally_active = True

        # If silence / no hit detected for > 3.5s, finalize rally clip
        if self.is_rally_active and (time.time() - self.last_hit_time > 3.5):
            self.is_rally_active = False
            return self.export_clip()
        return None"""
        },
        "featured": False
    },
    {
        "id": "3d-room-scan-texture-pipeline",
        "title": "3D Room Scan Cleaning & Texture Pipeline",
        "folder": "painpointtoday_3dtexture",
        "category": "geospatial-3d",
        "categoryLabel": "Geospatial AI & Drone Analytics",
        "badge": "3D Processing",
        "impact": "3D mesh cleaning, USDZ-to-GLTF conversion & Three.js web rendering",
        "image": "assets/shot_2026-08-06_105838.png",
        "shortSummary": "3D spatial scanning pipeline converting Apple RoomPlan USDZ scans into cleaned, optimized GLTF/GLB models with texture baking, mesh decimation, and interactive Three.js web rendering.",
        "fullDescription": "A 3D graphics and mesh processing pipeline developed for virtual real estate tours. Ingests raw iPhone LiDAR / RoomPlan USDZ models, executes mesh cleaning (vertex deduplication, normal unification, and quad decimation), bakes texture atlases, and converts assets to optimized GLTF/GLB format for interactive viewing in Three.js.",
        "highlights": [
            "USDZ to GLTF/GLB geometry and material conversion pipeline",
            "Mesh cleaning using Open3D and Trimesh: vertex deduplication & manifold repair",
            "Texture atlas re-projection and lighting normalization",
            "FastAPI microservice handling model conversion tasks",
            "Interactive Three.js web viewer for room dimension inspection"
        ],
        "metrics": [
            {"label": "File Compression", "value": "75% Reduction", "sub": "Optimized GLB format"},
            {"label": "Web Rendering", "value": "60 FPS", "sub": "Three.js lightweight assets"},
            {"label": "Geometry Tools", "value": "Open3D / Trimesh", "sub": "Automated mesh decimation"},
            {"label": "Pipeline", "value": "FastAPI", "sub": "Async 3D conversion API"}
        ],
        "techStack": [
            "Python", "Open3D", "Trimesh", "Three.js", "FastAPI", "USD Core", "GLTF / GLB", "Docker"
        ],
        "architecture": """
+-----------------------+      +---------------------------+      +---------------------------+
| Raw iPhone LiDAR Scan | ---> | USDZ Parser &             | ---> | Open3D Mesh Cleaner       |
| (Apple RoomPlan USDZ) |      | Scene Graph Extractor     |      | (Decimate & Repair Normals|
+-----------------------+      +---------------------------+      +---------------------------+
                                                                                |
                                                                                v
+-----------------------+      +---------------------------+      +---------------------------+
| Three.js Web Viewer / | <--- | FastAPI Asset Delivery    | <--- | Texture Atlas Baker &     |
| Virtual Tour Portal   |      | & S3 Storage Ingestion    |      | GLTF / GLB Exporter       |
+-----------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Manifold Repair**: Cleans up degenerate faces and non-manifold edges produced by mobile LiDAR scanners before web rendering.",
            "**Color Palette Mapping**: Uses vertex UVs and texture coordinates to extract dominant room wall colors."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "clean_v5.py (Mesh Decimation & Normal Recalculation with Open3D)",
            "code": """def clean_and_optimize_mesh(input_path: str, target_triangles=40000) -> trimesh.Trimesh:
    mesh = trimesh.load(input_path)
    # Remove duplicate and unreferenced vertices
    mesh.remove_degenerate_faces()
    mesh.remove_duplicate_faces()
    mesh.remove_unreferenced_vertices()

    # Convert to Open3D for quadric decimation
    o3d_mesh = mesh.as_open3d
    o3d_mesh = o3d_mesh.simplify_quadric_decimation(target_number_of_triangles=target_triangles)
    o3d_mesh.compute_vertex_normals()
    
    # Export back as optimized Trimesh
    cleaned = trimesh.Trimesh(
        vertices=np.asarray(o3d_mesh.vertices),
        faces=np.asarray(o3d_mesh.triangles),
        vertex_normals=np.asarray(o3d_mesh.vertex_normals)
    )
    return cleaned"""
        },
        "featured": False
    },
    {
        "id": "real-estate-core-scoring-infrastructure",
        "title": "Real Estate Scoring & Location Processing Engine",
        "folder": "yh-db-processing",
        "category": "backend-cloud",
        "categoryLabel": "Backend & Cloud Systems",
        "badge": "Backend Microservice",
        "impact": "Composite location scoring, walking distance engine & multi-variable ranking",
        "image": "assets/shot_2026-07-08_085932.png",
        "shortSummary": "Scoring and data processing engine computing composite property scores, transit walking distance matrices (OSRM/Google Maps), and price-per-square-meter value metrics.",
        "fullDescription": "A backend microservice powering property evaluation at Yourhome. Runs scoring algorithms across real estate listings: transit walking distance calculations, neighborhood amenity density, Google review sentiment aggregation, and price-per-square-meter value metrics. Connects to AWS RDS MySQL via SSH tunnels and Google Cloud Firestore.",
        "highlights": [
            "Composite property scoring engine with parameterized weighting",
            "Transit walking distance and travel time calculation with OSRM and Google Maps APIs",
            "Price-per-sqm value scoring relative to neighborhood baseline distributions",
            "Firestore and MySQL dual-write consistency with transaction error handling",
            "FastAPI REST endpoints with sub-50ms score computation"
        ],
        "metrics": [
            {"label": "Score Computation", "value": "< 50ms", "sub": "Multi-factor evaluation"},
            {"label": "Database Sync", "value": "Dual-Write", "sub": "MySQL RDS + Firestore"},
            {"label": "Scalability", "value": "Batching", "sub": "Batch processing 10k+ rows"},
            {"label": "Transit Matrix", "value": "OSRM / Maps", "sub": "Precise walking distance"}
        ],
        "techStack": [
            "Python", "FastAPI", "MySQL RDS", "Google Cloud Firestore", "SSHTunnel",
            "Pydantic", "Pandas", "NumPy", "Docker"
        ],
        "architecture": """
+-----------------------+      +---------------------------+      +---------------------------+
| Raw Property Ingestion| ---> | Walking Distance Engine   | ---> | Value & Spec Scorer       |
| (New Property Record) |      | (Transit / Amenity Radii) |      | (Price/sqm vs Market Dist)|
+-----------------------+      +---------------------------+      +---------------------------+
                                                                                |
                                                                                v
+-----------------------+      +---------------------------+      +---------------------------+
| Consumer Frontend &   | <--- | Dual Sync Storage         | <--- | Composite Ranking Engine  |
| Matchmaking Engine    |      | (MySQL RDS + Firestore)   |      | (Feng Shui + Amenities)   |
+-----------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Normalized Value Scoring Curves**: Uses log-normal distribution fitting to evaluate property price competitiveness relative to the neighborhood median.",
            "**Transit Caching**: Implements spatial grid caching to reduce redundant external transit API calls."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/calculate_composite_scores.py (Multi-Attribute Weighting Formula)",
            "code": """def compute_composite_property_score(loc_score: float, spec_score: float, value_score: float, google_rating: float) -> float:
    \"\"\"Calculates weighted composite score (0-100) based on validated business metrics.\"\"\"
    weights = {
        'location': 0.35,
        'spec': 0.25,
        'value': 0.25,
        'reputation': 0.15
    }
    composite = (
        (loc_score * weights['location']) +
        (spec_score * weights['spec']) +
        (value_score * weights['value']) +
        ((google_rating / 5.0 * 100.0) * weights['reputation'])
    )
    return round(min(max(composite, 0.0), 100.0), 2)"""
        },
        "featured": False
    },
    {
        "id": "yourhome-seo-sitemap-engine",
        "title": "Schema-Driven SEO & Sitemap Microservice",
        "folder": "yourhome-seo-sitemap",
        "category": "backend-cloud",
        "categoryLabel": "Backend & Cloud Systems",
        "badge": "Backend Microservice",
        "impact": "Dynamic XML sitemaps, JSON-LD Schema.org generators & Firestore caching for 50k+ URLs",
        "image": "assets/shot_2026-08-10_155652.png",
        "shortSummary": "FastAPI microservice generating dynamic, paginated XML sitemaps, Schema.org JSON-LD microdata, and clean slug routing for property search engine indexing.",
        "fullDescription": "A schema-first SEO engine built for Yourhome. Generates dynamic XML sitemaps with pagination supporting 50,000+ property and article URLs. Produces Schema.org JSON-LD structured data (RealEstateListing, Product, BreadcrumbList) to improve search engine indexing. Integrates with Firestore for caching and MySQL via SSH tunnels.",
        "highlights": [
            "Paginated XML sitemap generator with 50,000 URLs per index chunk",
            "Schema.org JSON-LD generator for structured data indexing",
            "Firestore-backed caching layer reducing database query overhead",
            "FastAPI async routing with gzip compression and cache-control headers",
            "Tested with automated Postman test suites and deployed on Docker"
        ],
        "metrics": [
            {"label": "Index Capacity", "value": "50,000+ URLs", "sub": "Paginated dynamic XML"},
            {"label": "Cache Hit Latency", "value": "< 15ms", "sub": "Firestore cached responses"},
            {"label": "Schema Standard", "value": "Schema.org", "sub": "JSON-LD structured data"},
            {"label": "Database Load", "value": "-92%", "sub": "Caching layer"}
        ],
        "techStack": [
            "Python", "FastAPI", "Google Cloud Firestore", "Pydantic", "MySQL RDS", "Docker", "Postman"
        ],
        "architecture": """
+-----------------------+      +---------------------------+      +---------------------------+
| Search Engine Bot /   | ---> | FastAPI Gateway           | ---> | Firestore Cache Check     |
| AI Crawler (Google/AI)|      | (Gzip + Rate Limiting)    |      | (Sub-15ms cached response)|
+-----------------------+      +---------------------------+      +---------------------------+
                                                                                | (Cache Miss)
                                                                                v
+-----------------------+      +---------------------------+      +---------------------------+
| Output XML Sitemap &  | <--- | Schema.org JSON-LD Engine | <--- | MySQL RDS Query           |
| Clean URL Slugs       |      | & Chunk Paginator (50k)   |      | (via Secure SSH Tunnel)   |
+-----------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Structured JSON-LD Construction**: Constructs property entity relationships (including transit station walking minutes and amenities) for search engine crawlers.",
            "**Chunked Sitemap Generation**: Uses streaming XML generators to avoid high memory spikes when assembling large listing indexes."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "src/services/schema_builder.py (Structured Schema.org JSON-LD Builder)",
            "code": """def build_property_schema_jsonld(property_data: dict) -> dict:
    \"\"\"Constructs Schema.org RealEstateListing JSON-LD metadata for AI search bots.\"\"\"
    return {
        \"@context\": \"https://schema.org\",
        \"@type\": \"RealEstateListing\",
        \"name\": property_data.get(\"title\"),
        \"description\": property_data.get(\"description\"),
        \"url\": f\"https://yourhome.co.th/property/{property_data.get('slug')}\",
        \"price\": property_data.get(\"price_thb\"),
        \"priceCurrency\": \"THB\",
        \"address\": {
            \"@type\": \"PostalAddress\",
            \"addressLocality\": property_data.get(\"district\"),
            \"addressRegion\": \"Bangkok\",
            \"addressCountry\": \"TH\"
        },
        \"geo\": {
            \"@type\": \"GeoCoordinates\",
            \"latitude\": property_data.get(\"lat\"),
            \"longitude\": property_data.get(\"lng\")
        }
    }"""
        },
        "featured": False
    },
    {
        "id": "yourhome-auto-admin-agent",
        "title": "Automated Real Estate Admin Chatbot & LINE Webhook",
        "folder": "yourhome-auto-admin",
        "category": "agents-automation",
        "categoryLabel": "Multi-Agent & Automation",
        "badge": "Chatbot & Automation",
        "impact": "Intent recognition, lead qualification & MySQL/Firestore response synthesis",
        "image": "assets/shot_2026-05-21_151828.png",
        "shortSummary": "Administrative chatbot for customer service on LINE and Web Chat. Uses Google Gemini for intent routing, queries MySQL/Firestore for property inventory, and delivers polite, structured replies.",
        "fullDescription": "A customer service and lead management agent. Connects to customer inquiries over LINE Messaging API and web widgets. Uses Google Gemini to classify customer intent (price inquiry, viewing booking, location query), retrieves matching listings from MySQL RDS and Firestore leads, and generates polite, professional replies.",
        "highlights": [
            "Skill-based architecture separating database, Firestore, and LINE messaging skills",
            "Gemini prompt orchestration with structured business persona guidelines",
            "Automated lead qualification and CRM ingestion into Firestore",
            "Webhook receiver built with FastAPI and secure SSH database tunneling"
        ],
        "metrics": [
            {"label": "Response Time", "value": "< 1.2s", "sub": "End-to-end webhook reply"},
            {"label": "Intent Coverage", "value": "12 Intents", "sub": "Lead qualification & booking"},
            {"label": "Channel", "value": "LINE & Web", "sub": "Multi-channel messaging"}
        ],
        "techStack": [
            "Python", "FastAPI", "Google Gemini", "line-bot-sdk", "Firestore", "MySQL RDS", "Docker"
        ],
        "architecture": """
+-----------------------+      +---------------------------+      +---------------------------+
| Customer LINE Message | ---> | FastAPI Webhook Receiver  | ---> | Gemini Intent Classifier  |
| / Web Live Chat       |      | (Config-driven skills)    |      | & Lead Qualification      |
+-----------------------+      +---------------------------+      +---------------------------+
                                                                                |
                                                                                v
+-----------------------+      +---------------------------+      +---------------------------+
| Tailored Response     | <--- | LINE Flex Message Builder | <--- | Skills Registry:          |
| Delivered to Customer |      | & Firestore Lead Ingest   |      | DB, CRM, Availability     |
+-----------------------+      +---------------------------+      +---------------------------+
""",
        "innovations": [
            "**Modular Skill Abstraction**: Each tool (inventory check, booking calendar, lead saver) is encapsulated as a standalone skill function, keeping the codebase organized."
        ],
        "codeSnippet": {
            "language": "python",
            "title": "agents/admin_agent.py (Gemini Intent Routing & Skill Execution)",
            "code": """async def handle_customer_inquiry(message_text: str, user_id: str) -> str:
    # Classify intent with Gemini
    intent_data = await classify_intent(message_text)
    intent = intent_data.get("intent")
    
    if intent == "CHECK_PROPERTY":
        property_id = intent_data.get("property_id")
        details = await db_skill.get_property_details(property_id)
        return format_property_reply(details)
    elif intent == "BOOK_VIEWING":
        lead = await firestore_skill.save_lead(user_id, intent_data)
        return "ขอบคุณสำหรับการนัดหมายชมห้อง เจ้าหน้าที่จะติดต่อกลับยืนยันเวลาครับ"
    else:
        return await gemini_generate_general_reply(message_text)"""
        },
        "featured": False
    }
]

RESUME_DATA = {
    "name": "Kwankhao Sivasomboon",
    "title": "AI Engineer",
    "headline": "AI Engineer · Computer Vision · GenAI/RAG · Backend & Cloud",
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
    print("Generating portfolio data with images and humble tone...")
    
    data_bundle = {
        "resume": RESUME_DATA,
        "projects": PROJECTS_CATALOG,
        "categories": [
            {"id": "all", "label": "All Projects", "count": len(PROJECTS_CATALOG)},
            {"id": "cv-edge", "label": "Computer Vision & Edge AI", "icon": "eye"},
            {"id": "genai-rag", "label": "GenAI, LLMs & Agents", "icon": "cpu"},
            {"id": "agents-automation", "label": "Multi-Agent & QA", "icon": "robot"},
            {"id": "backend-cloud", "label": "Backend & Cloud Systems", "icon": "server"},
            {"id": "geospatial-3d", "label": "Geospatial & 3D Analytics", "icon": "globe"}
        ],
        "stats": {
            "totalProjects": len(PROJECTS_CATALOG),
            "productionDeployments": 6,
            "ocrAccuracy": "90%",
            "ragGrounding": "93.8%",
            "sttLatency": "< 320ms"
        }
    }

    # Save as JSON
    json_path = os.path.join(BASE_DIR, "portfolio_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_bundle, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON data to {json_path}")

    # Save as JS for zero-dependency client-side loading
    js_path = os.path.join(BASE_DIR, "portfolio_data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("/* Auto-generated Portfolio Dataset for Kwankhao Sivasomboon */\n")
        f.write("window.PORTFOLIO_DATA = ")
        json.dump(data_bundle, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"Saved JS data to {js_path}")

if __name__ == "__main__":
    main()
