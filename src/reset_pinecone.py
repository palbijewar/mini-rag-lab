from pinecone_client import index


print("Deleting existing vectors...")

index.delete(delete_all=True)

print("All vectors deleted.")

print(index.describe_index_stats())