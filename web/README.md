# PulseQ web interface

A React + Vite + Tailwind CSS interface backed by the existing PulseQ DSA modules through FastAPI. The visual direction is intentionally restrained: warm neutral canvas, deep ink, muted teal, low-contrast borders, and compact operational tables.

## Requirements

- Python 3.10+
- Node.js 18+
- npm

## Start the API

From the repository root:

```bash
python -m pip install -r requirements-web.txt
python api_main.py
```

API health: http://127.0.0.1:8000/api/health  
Interactive API docs: http://127.0.0.1:8000/docs

## Start the React frontend

Open a second terminal:

```bash
cd web
npm install
npm run dev
```

Open http://127.0.0.1:5173

The frontend uses `VITE_API_URL` if set, otherwise it calls `http://127.0.0.1:8000/api`. Copy `.env.example` to `.env.local` to override it.

## Build for production

```bash
cd web
npm run build
npm run preview
```

## What is connected

- Patient directory: create, search/filter, edit and delete.
- Routine queue: enqueue and serve next using the custom linked FIFO queue.
- Emergency queue: enqueue with a demo urgency score and serve highest priority using the custom binary max-heap.
- Doctor directory: add doctors, toggle availability, allocate by specialization and release assignments.
- DSA lab: call the project's manual search and sorting algorithms.
- Dashboard: live counts, next-up queues, recent records and doctor availability.

## Important limitations

The API reuses the in-memory structures from `pulseq/`. Restarting the API clears all data. Run only on your local machine for a class demonstration. Do not enter real patient information. The emergency urgency value is not a clinical triage scale. This project is not a production hospital information system and has no authentication, persistent database, audit logging, or deployment hardening.
