from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from supabase import create_client

class EssayEmbeddings:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.supabase = create_client(supabase_url, supabase_key)

    def create_embeddings(self, text: str) -> List[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()

    def process_essays(self):
        # Fetch all essays from database
        response = self.supabase.table('essays')\
            .select('id, title, content')\
            .execute()
        
        for essay in response.data:
            # Generate embedding from title + content
            embedding = self.create_embeddings(essay['title'] + ' ' + essay['content'])
            
            # Store embedding in database
            self.supabase.table('essays')\
                .update({'embedding': embedding})\
                .eq('id', essay['id'])\
                .execute()
            
            print(f"Processed essay {essay['id']}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    processor = EssayEmbeddings(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    processor.process_essays() 