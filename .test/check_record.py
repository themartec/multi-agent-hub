import chromadb

# Initialize the persistent client with the path to your local DB directory
client = chromadb.PersistentClient(path="chroma_db")

# Get the existing collection by name (replace with your actual collection name)
collection = client.get_collection(name="e8ddefa1-284b-40f9-955c-339a6a00eecf-base_knowledge_graph")

# Retrieve and print the count of records
count = collection.count()
print(f"The collection has {count} records.")