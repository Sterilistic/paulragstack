from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from supabase import create_client
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI

load_dotenv()

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str
    limit: int = 5

class SearchResponse(BaseModel):
    id: int
    title: str
    url: str
    content: str
    similarity: float
    summary: Optional[str] = None

@app.post("/search")
async def search_essays(query: SearchQuery):
    # Create embedding for the search query
    query_embedding = model.encode(query.query).tolist()
    
    # Perform similarity search using pgvector with lower threshold
    result = supabase.rpc(
        'match_essays',
        {
            'query_embedding': query_embedding,
            'match_threshold': 0.3,
            'match_count': query.limit
        }
    ).execute()
    
    # Generate consolidated insights from all relevant essays
    essays_context = "\n\n".join([
        f"Essay: {essay['title']}\n{essay['content'][:1000]}..."
        for essay in result.data
    ])
    
    insights_prompt = f"""
    Analyze these relevant essays from Paul Graham in relation to the query: "{query.query}"
    Extract and synthesize the key insights, patterns, and advice across all these essays.
    
    {essays_context}
    
    Provide only 3-4 key insights that emerge across these essays, focusing on practical takeaways.
    Format each insight as a bullet point starting with "•". End each insight with a period. Keep each insight short and concise and point out the essay as well for each insight.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert at analyzing Paul Graham's essays and extracting actionable insights."},
            {"role": "user", "content": insights_prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
    # Add insights to the response
    return {
        "essays": result.data,
        "insights": response.choices[0].message.content.strip()
    }

@app.get("/essays")
async def get_essays(limit: int = 10, offset: int = 0):
    result = supabase.table('essays')\
        .select('id, title, url')\
        .range(offset, offset + limit - 1)\
        .execute()
    
    return result.data 

