import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

# Ruta de la base de datos
DB_PATH = Path("X:/Proyectos IA OpenCode/Decompas/vector_db")

# Crear cliente de ChromaDB
client = chromadb.PersistentClient(path=str(DB_PATH))

# Usar embedding function local
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Obtener colección
collection = client.get_collection(
    name="decompas_context",
    embedding_function=ef
)

def buscar_contexto(query, n_results=3):
    """Busca contexto relevante en la base de datos vectorial"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    contextos = []
    for i, doc in enumerate(results['documents'][0]):
        distancia = results['distances'][0][i]
        categoria = results['metadatas'][0][i]['categoria']
        contextos.append({
            "texto": doc,
            "categoria": categoria,
            "relevancia": 1 - distancia  # Convertir distancia a relevancia
        })
    
    return contextos

def obtener_contexto_para_respuesta(query):
    """Obtiene el contexto formateado para incluir en la respuesta"""
    contextos = buscar_contexto(query, n_results=3)
    
    if not contextos:
        return ""
    
    contexto_texto = "Contexto relevante:\n"
    for ctx in contextos:
        if ctx['relevancia'] > 0.3:  # Solo incluir si es relevante
            contexto_texto += f"- {ctx['texto']}\n"
    
    return contexto_texto

# Ejemplo de uso
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "¿Qué servicios ofrece Daniel?"
    
    print(f"Buscando: {query}\n")
    contextos = buscar_contexto(query)
    
    for i, ctx in enumerate(contextos, 1):
        print(f"{i}. [{ctx['categoria']}] (relevancia: {ctx['relevancia']:.2f})")
        print(f"   {ctx['texto']}\n")