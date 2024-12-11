import chromadb
import uuid
import pandas as pd

class SkillsPortfolio:
    def __init__(self, file_path="app/resource/skills_portfolio_data.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="skill_portfolios")

    def load_skills_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Tech Stacks"],
                               metadatas={"URLs": row["Portfolio URL"]},
                               ids=[str(uuid.uuid4())])
                
    def query(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

