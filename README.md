# 📝 Meet Summarizer

**Meet Summarizer** is a minimal web app that allows users to upload a meeting transcript (text or audio), automatically summarize it using OpenAI API, and view the structured result. Built with Flask and React, it's designed to be lightweight, clean, and developer-friendly.

---

## 🚀 Installation & Getting Started

### 🧩 Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (SQLite for testing)
- OpenAI API Key

### 🔧 Backend Setup (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python init_db.py         # initialize the database
python run.py             # run the Flask app on http://localhost:5050
```

> ⚠️ Ensure PostgreSQL is running and credentials in `config.py` are valid (or switch to SQLite for local use).

### 💻 Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev               # starts app on http://localhost:5173
```

> API calls are automatically proxied to the Flask backend using `/api/*`.

---
## 🧪 Running Tests (Backend)

The backend uses **pytest** for unit testing. To run tests:

```bash
cd backend
source venv/bin/activate
PYTHONPATH=. pytest
```

> Ensure your test database uses SQLite in memory (see test fixtures), or configure a dedicated PostgreSQL test DB.

---

## 🛠 PostgreSQL local setup

If you're using Docker (recommended), here’s a minimal `docker-compose.yml`:

```yaml
version: '3'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: meet_summarizer_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Make sure your `backend/app/config.py` contains the correct credentials:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://devuser:devpassword@localhost:5432/meet_summarizer_db"
```

Then run:

```bash
docker-compose up -d
```

And initialize the tables:

```bash
cd backend
source venv/bin/activate
python init_db.py
```
---

## 🧱 Project architecture

```
meet-summarizer/
│
├── backend/
│   ├── app/
│   │   ├── routes/            
│   │   ├── models/       
│   │   ├── services/     
│   │   ├── database.py         
│   │   ├── config.py          
│   │   └── __init__.py         
│   ├── tests/             
│   └── run.py, init_db.py      
│
├── frontend/
│   ├── src/
│   │   ├── components/        
│   │   ├── api.ts        
│   │   ├── App.tsx        
│   │   └── main.tsx          
│   └── vite.config.ts        
```

---

## ✨ Features implemented

- Upload a `.txt` or audio file (basic type inference)
- Store submission and status in the database
- Analyze file with OpenAI and parse structured output (title, key points, action items)
- Display the result with live polling on frontend
- Interactive frontend built with MUI (Material UI) for fast and polished UX
- Unit tests for core Flask endpoints (upload, analyse, results)
- API prefixing with `/api` for clean separation

---

## 🧪 Workflow

1. User uploads a file.
2. File is stored and registered as a `Submission` (`status = "pending"`).
3. Backend calls OpenAI and stores a `Summary` with structured fields.
4. Frontend polls `/api/results/<id>` until `status = "done"` and displays results.

---

## 🛠 Technical decisions

- **Flask**: lightweight REST API with full control over routes, structure, and behavior.
- **SQLAlchemy**: ORM for managing relations between submissions and summaries
- **PostgreSQL**: production-ready relational DB (SQLite fallback for tests)
- **OpenAI**: integration with GPT-3.5-turbo via `openai` Python SDK v1
- **React + Vite**: fast DX, native TypeScript support, hot module reload
- **MUI**: quick design system with ready-to-use components and accessibility

---

## 🧠 Future Improvements

- Allow editing or highlighting parts of the generated summary
- Implement speech-to-text conversion for uploaded audio files
- Add authentication for submission history or multi-user support
- Improve polling with SSE
- Add integration/E2E tests with Cypress or any other tool
- Add support for deployment via Docker
- Way better UI
- Guard rails and/or better prompting within the LLM service

