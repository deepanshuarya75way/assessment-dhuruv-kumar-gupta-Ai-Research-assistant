import math
from collection import Counter
import re

from app.services.embedding_service import EmbeddingService
def get_collection():
    from app.vectorstore.chroma_service import collection
    return collection

class RetrievalService:
    @staticmethod
    def tokenization(text):
        return re.findall(r"\b\w+\b",text.lower())
    @staticmethod
    def sparse_serach(question,documents,ids,top_k=10):
        #here we have used BM25 for sparce search 
        query_tokens=RetrievalService.tokenization(question)
        if not documents or not query_tokens:
            return[]

        tokenized_docs=[
            RetrievalService.tokenization(doc or "")
            for doc in documents
        ]
        total_docs=len(toekinzed_docs)
        doc_length=[len(doc) for doc in tokenized_docs]
        avg_length=sum(doc_length)/total_docs

        doc_frequencies=Counter(token
            for doc in tokenized_docs
            for token in set(docs))
        score=[]

        for token, tokens in enumerate(tokenized_docs)
        term_counts=Counter(tokens)
        score=0
        for term in query_token:
            frequency=term.counts.get(term,0)
            if frequency==0:
                continue

        
            df=doc_frequencies[term]
            idf=math.log(1+(total_docs-df+0.5))

            k1=1.5
            b=0.75

            length=doc_length[index]

            denominator=frequency+k1*(1-b+b*length/avg_length)
            score+=idf*(frequency*(k1+1)/denominator)

    if score>0:
        score.append((ids[index],score))

    scores.sort(key=lambda item:item[1],reverse=True)
    return scores[::top_k]
    

@staticmethod
def search(questions,paper_id,top_k=4):
    collection=get_collection()

    stored=collection.get(where={"papers_id":paper_id},include=["documents"])
    documents=stored.get("documents")
    ids=stored.get("ids") or []

    if not in documents
# here we are performing dense search
        query_embedding=(EmbeddingService.create_query_embedding(question))
        candidate_k=min(len(documents),max(top_k*3,10))

        dense_results=collection.query(
            query_embeddings=[query_embedding],
            n_results=candidate_k,
            where={"paper_id":paper_id},
            include=["documents","distances"]
        )

        dense_ids=dense_results.get("ids",[[]])[0]

#here we are performing sparse search
        sparse_results=RetrievalService.sparse_serach(questions,documents,ids,top_k=candiate_k)

        rrf_scores={}
        rank_constant=60

        for rank, chunk_id in enumerate(dense_ids,start=1):
            rrf_scores[chunk_id]=(
                rrf_scores.get(chunks_id,0)+1/(rank_constant+rank)
            )

        for rank,(chunk_id,_) in enumerate(sparse_results,start=1):
            rrf_score.get(chunk_id,0)+1/(rank_constant+rank)
        
        document_by_id=dict(zip(ids,documents))
        ranked_ids=sorted(rrf_scores,key=rrf_scores.get,reverse=True)

        final_documents=[document_by_id[chunk_id] 
            for chunk_id in ranked_ids[:top_k]
            if chunk_id in document_by_id]
        return final_documents
        
