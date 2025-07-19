# KODA-S

**Offline Cross-Platform AI Code Assistant**  
A fast, lightweight, fully offline AI-powered coding assistant targeting devices from Raspberry Pi ARM boards to Windows and Linux PCs.

---

## 🚀 Project Overview

KODA-S is a local-first AI code assistant combining powerful quantized LLMs with a modern, multi-window web UI. The backend is Python-based with FastAPI and llama-cpp-python for inference. The frontend is React-driven, designed for a smooth VS Code–style developer experience.

Key features:  
- Offline-only operation (no internet required after setup)  
- Cross-platform support: Windows (initial), Linux, ARM (Raspberry Pi)  
- Multi-tier models optimized by RAM and CPU: Super Light, Light, Heavy  
- Perfect memory with vector search for long-term session context  
- Dockable, multi-file UI with live AI streaming responses  

---

## 🎯 Goals

| Tier           | RAM Target  | Device Type                | Model Example (quantized GGUF)        |
|----------------|-------------|----------------------------|---------------------------------------|
| Super Light    | ~1GB        | Raspberry Pi, ARM SBCs     | WizardCoder 1B                        |
| Light          | ~1.5–2GB    | Low-end Windows/Linux PCs  | Qwen 1.5B                            |
| Heavy          | 8GB+        | Desktop, High-end laptops  | Code Llama 7B                        |

---

## 🛠 Tech Stack

- **Backend:**  
  - Python 3.10+  
  - FastAPI for REST + WebSocket APIs  
  - llama-cpp-python for local LLM inference  
  - SQLite + FAISS or Annoy for memory vector search  

- **Frontend:**  
  - React (functional components + hooks)  
  - Golden Layout for dockable multi-window UI  
  - Tailwind CSS for styling  
  - Monaco Editor for code editing  

- **Models:**  
  - GGUF quantized models (GGML-compatible)  
  - Dynamic loading/unloading based on device tier  

- **Packaging (future):**  
  - Tauri for native cross-platform desktop app  

---

## 🏗 Architecture Diagram

    React Frontend
        ⇅ REST + WebSocket
    FastAPI Python Backend
        ⇅ llama-cpp-python (local LLM inference)
        ⇅ SQLite + FAISS/Annoy (long-term memory & vector search)
        ⇅ Local Filesystem (project files)

---

## ⚙️ Development Details

### Backend

- llama-cpp-python: Load quantized GGUF models, run inference with async API.  
- FastAPI: Serve endpoints (/generate, /models, /projects) and WebSocket for streaming tokens.  
- Memory: SQLite stores conversations & project data; FAISS/Annoy for semantic retrieval.  
- Model management: Load/unload multiple models; switch by device tier or preference.  
- Project files: API to browse, read, write files on local disk.

### Frontend

- React + Golden Layout: Build dockable, resizable multi-window UI like VS Code.  
- Monaco Editor: Code editing with syntax highlighting & basic intellisense.  
- Prompt panel: Accept user queries/prompts to AI.  
- Streaming display: Show AI responses token-by-token via WebSocket.  
- Model switcher: UI to select backend model tier.  
- Project explorer: File tree view for code files.

### Models

| Tier        | Model               | Description                             | RAM Usage | Notes                   |
|-------------|---------------------|-----------------------------------------|-----------|-------------------------|
| Super Light | WizardCoder 1B GGUF | Small, coding-focused, ARM-friendly     | ~1GB      | Ideal for Raspberry Pi  |
| Light       | Qwen 1.5B GGUF      | Balanced reasoning, coding, creativity  | 1.5–2GB   | Great for low-end PCs   |
| Heavy       | Code Llama 7B GGUF  | Advanced multi-step reasoning & coding  | 8GB+      | High-end desktops       |

---

## 🗓 Milestones / Roadmap

1. **Backend: FastAPI + llama-cpp-python**  
   - Install dependencies and test model loading  
   - Implement /generate endpoint for inference  
   - Add multi-model support and switching  

2. **Frontend: Minimal React app**  
   - Monaco editor + prompt input + AI output  
   - Connect to backend REST + WebSocket  

3. **Perfect memory**  
   - Integrate SQLite and vector search  
   - Implement session context retrieval  

4. **UI/UX enhancements**  
   - Dockable multi-window layout  
   - Keyboard shortcuts, themes, model panel  

5. **Project file management APIs**  
   - CRUD for local project files  

6. **Packaging**  
   - Windows installer via Tauri  
   - ARM/Linux packaging plan  

---

## 🛠 Setup Instructions (Windows Dev Focus)

### Prerequisites

- Python 3.10+  
- Node.js & npm/yarn  
- Git  

### Backend setup

    python -m venv venv
    venv\Scripts\activate   # Windows
    pip install --upgrade pip
    pip install fastapi uvicorn llama-cpp-python sqlalchemy faiss-cpu

- Download WizardCoder 1B GGUF model into /models.

### Frontend setup

    cd frontend
    npm install
    npm run dev

### Run backend

    uvicorn main:app --reload

---

## 📚 Dev Notes & Tips

- Use prebuilt llama-cpp-python wheels to avoid compiling.  
- Always use quantized GGUF models for low resource use.  
- Use async in FastAPI for smooth UX.  
- Cache models in memory to speed inference.  
- Detect device specs to auto-select model tier.  
- Keep prompts concise to save memory.  
- Stream tokens via WebSocket to frontend.

---

## 🙋‍♂️ Need Help?

Ask for:  
- Starter code snippets  
- Model download & quantization guides  
- Packaging tips for ARM & Windows  
- API specs or UI layouts

---

## 🎉 Let’s build KODA-S: The ultimate offline AI coding assistant for all your devices!

*Build smart. Build local. Build fast.*  
— KODA-S Team
