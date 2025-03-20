# paulragstack
# Paul Graham Essays RAG Search

A lightweight Retrieval Augmented Generation (RAG) system that provides intelligent search and analysis of Paul Graham's essays. Uses semantic search with embeddings and generates AI-powered insights across relevant essays.

![image](https://github.com/user-attachments/assets/3cd84682-867b-44b9-83ff-399d98ac4741)


## Features

- 🔍 Semantic search using sentence transformers
- 💡 AI-generated key insights from multiple relevant essays
- 🎯 Vector similarity search using pgvector
- 🎨 Clean, responsive UI with Next.js and shadcn/ui

## Tech Stack

- **Backend**: FastAPI, sentence-transformers, OpenAI
- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Database**: Supabase (PostgreSQL + pgvector)
- **Infrastructure**: Docker for local development


## Install Docker Desktop
`brew install --cask docker`

## Install Supabase CLI
`brew install supabase/tap/supabase`



## Backend

### Create and activate virtual environment
`python -m venv venv`
`source venv/bin/activate # or venv\Scripts\activate on Windows`

### Install dependencies
`cd backend`
`pip install -r requirements.txt`

### Set up environment variables
`cp .env.example .env`

**Note:** Edit .env with your Supabase and OpenAI credentials


## Frontend Setup

`cd frontend`
### Install dependencies
`npm install`

### Set up shadcn/ui components
`npx shadcn-ui@latest init`
`npx shadcn-ui@latest add button card input`



### Database Setup

`supabase start`
`supabase db reset`


### Run backend
`cd backend`
`uvicorn main:app --reload`

### Run frontend
`cd frontend`
`npm run dev`



## Scrape and process essays:

`python scraper.py`
`python embeddings.py`


Visit `http://localhost:3000` to use the application.

## Usage

1. Enter a search query about any topic from Paul Graham's essays
2. Get relevant essays and AI-generated key insights
3. Click through to read full essays

## Project Structure
![Screenshot 2025-03-20 at 10 33 12](https://github.com/user-attachments/assets/47c0bd3c-623a-4a74-80e2-bde4192dfab6)

## Environment Variables
`SUPABASE_URL=your_supabase_url`
`SUPABASE_KEY=your_supabase_key`
`OPENAI_API_KEY=your_openai_key`



