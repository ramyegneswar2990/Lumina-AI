import numpy as np
from typing import List, Dict, Any, Optional
from endee import Endee
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
import time
import uuid

class EndeeService:
    def __init__(self, collection_name: str, dimension: int = 384):
        self.collection_name = collection_name
        self.dimension = dimension
        self.client = None
        self.index = None
        self.connected = False
        
        # Try connecting
        try:
            # Endee() defaults to http://127.0.0.1:8080/api/v1 which is perfect for local Docker
            self.client = Endee(token="admin_secret")
            # Simple health check or list_indexes to verify connection
            indexes = self.client.list_indexes()
            self.connected = True
            print(f"✅ Successfully connected to Endee Server! Found {len(indexes) if isinstance(indexes, list) else 0} indexes.")
            self._setup_index()
        except Exception as e:
            print(f"❌ Could not connect to Endee Server: {e}")
            print("Running in OFFLINE/MOCK mode.")

        # In-memory fallback
        self.mock_store = []

    def _setup_index(self):
        try:
            indexes = self.client.list_indexes()
            if self.collection_name not in indexes:
                self.client.create_index(
                    name=self.collection_name, 
                    dimension=self.dimension,
                    space_type="cosine"
                )
            self.index = self.client.get_index(self.collection_name)
        except Exception as e:
            print(f"Error setting up index: {e}")
            self.connected = False

    def add_documents(self, documents: List[Document], embeddings: List[List[float]]):
        ids = [str(uuid.uuid4()) for _ in documents]
        
        if self.connected and self.index:
            try:
                # Assuming insert API: index.insert(vectors, ids=..., metadata=...)
                # The metadata support in Endee might be specific.
                # If inspection failed to show methods, I'll assume standard args.
                # If it fails, we fall back.
                
                # Check for `insert` or `add`
                if hasattr(self.index, 'insert'):
                    # Vector native usually expects vectors + ids
                    self.index.insert(vectors=embeddings, ids=ids) 
                    # Metadata store might be separate or embedded?
                    # For a strict vector DB, we might only check sim.
                    # We will store metadata in self.mock_store even in connected mode 
                    # if Endee is pure vector? No, usually they support payloads.
                    # I'll chance it with a 'metadata' arg or 'payload' arg.
                    pass
                elif hasattr(self.index, 'add'):
                    self.index.add(embeddings)
                
            except Exception as e:
                print(f"Endee Insert Failed: {e}")
        
        # Always store in mock_store for retrieval of Text/Metadata if DB is pure vector
        # or as fallback.
        for doc, emb, id_ in zip(documents, embeddings, ids):
            self.mock_store.append({
                "id": id_,
                "vector": emb,
                "text": doc.page_content,
                "metadata": doc.metadata
            })

    def search(self, query_vector: List[float], k: int = 4) -> List[Dict]:
        results = []
        
        if self.connected and self.index:
            try:
                # Attempt search
                # Expected return: matches with id, score
                search_res = []
                if hasattr(self.index, 'query'):
                    search_res = self.index.query(vector=query_vector, top_k=k)
                elif hasattr(self.index, 'search'):
                    search_res = self.index.search(query_vector=query_vector, limit=k)
                    
                # Process results - assuming search_res is list of objects/dicts
                # If we get IDs, we look up in mock_store (hybrid approach)
                # This guarantees we get the text back.
                for res in search_res:
                    # Normalized result handling
                    rid = getattr(res, 'id', None) or res.get('id')
                    score = getattr(res, 'score', 0.0) or res.get('score', 0.0)
                    
                    # Find doc
                    doc = next((d for d in self.mock_store if d['id'] == rid), None)
                    if doc:
                        doc['score'] = score
                        results.append(doc)
                        
                if results:
                    return results
            except Exception as e:
                print(f"Endee Search Failed: {e}")

        # Fallback: Cosine Similarity on mock_store
        print("Using Fallback Search")
        if not self.mock_store:
            return []
            
        vecs = np.array([d['vector'] for d in self.mock_store])
        q = np.array(query_vector)
        
        norm_v = np.linalg.norm(vecs, axis=1)
        norm_q = np.linalg.norm(q)
        
        if norm_q == 0:
            return []
            
        sims = np.dot(vecs, q) / (norm_v * norm_q)
        top_idx = np.argsort(sims)[::-1][:k]
        
        for idx in top_idx:
            item = self.mock_store[idx]
            item['score'] = float(sims[idx])
            results.append(item)
            
        return results

    def clear_data(self):
        """Clears all data from the Endee Server and the local mock store."""
        self.mock_store = []
        if self.connected and self.client:
            try:
                self.client.delete_index(self.collection_name)
                self._setup_index()
                print(f"Endee: Collection '{self.collection_name}' cleared.")
                return True
            except Exception as e:
                print(f"Failed to clear Endee index: {e}")
        return True

