from typing import List
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class IngestionPipeline:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def load_pdf(self, path: str) -> List[Document]:
        try:
            loader = PyPDFLoader(path)
            docs = loader.load()
            return self.text_splitter.split_documents(docs)
        except Exception as e:
            print(f"Error loading PDF {path}: {e}")
            return []

    def load_web(self, urls: List[str]) -> List[Document]:
        try:
            from langchain_community.document_loaders import WebBaseLoader
            from bs4 import BeautifulSoup
            import bs4
            
            # Using custom BeautifulSoup parsing to remove 'noise'
            loader = WebBaseLoader(web_paths=urls)
            docs = loader.load()
            
            cleaned_docs = []
            for doc in docs:
                soup = BeautifulSoup(doc.page_content, 'html.parser')
                
                # REMOVE NOISE: References, Navboxes, Sidebars
                for noise in soup.select('.reflist, .navbox, .infobox, .sitenotice, #catlinks, .reference, .mw-editsection'):
                    noise.decompose()
                
                # Get the cleaned text
                text = soup.get_text(separator=' ', strip=True)
                
                # Filter out lines that look like citations (e.g., [1], ^, Retrieved on)
                lines = [line for line in text.splitlines() if not any(x in line for x in ["Retrieved on", "ISBN", "doi:", "arXiv:"])]
                doc.page_content = "\n".join(lines)
                cleaned_docs.append(doc)

            return self.text_splitter.split_documents(cleaned_docs)
        except Exception as e:
            print(f"Error loading URLs {urls}: {e}")
            return []
            
    def load_csv(self, path: str) -> List[Document]:
        try:
            loader = CSVLoader(path)
            docs = loader.load()
            # CSV rows are usually small, but splitting is safe
            return self.text_splitter.split_documents(docs)
        except Exception as e:
            print(f"Error loading CSV {path}: {e}")
            return []
    
    def load_json(self, data: dict, source_name: str = "API_Response") -> List[Document]:
        """Handles JSON data from REST APIs or files."""
        import json
        try:
            text = json.dumps(data, indent=2)
            doc = Document(page_content=text, metadata={"source": source_name})
            return self.text_splitter.split_documents([doc])
        except Exception as e:
            print(f"Error processing JSON: {e}")
            return []
    
    def process_texts(self, texts: List[str], metadatas: List[dict] = None) -> List[Document]:
        return self.text_splitter.create_documents(texts, metadatas=metadatas)

