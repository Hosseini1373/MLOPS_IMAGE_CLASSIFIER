from pymongo import MongoClient
import os
from dotenv import load_dotenv

##### This is just a test script to read from MongoDB #####



# Setup logging
import logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Retrieve MongoDB connection key from environment
mongo_key = os.getenv('MONGODB_KEY')

# Connect to the MongoDB client
client = MongoClient(mongo_key)

# Access the database
db = client["MLOPS"]

# Log information about all collections in the database
collections = db.list_collection_names()
logging.info(f"Available collections: {collections}")

# Perform an aggregation to find documents where 'trained' field is False
not_trained_count = db['MLOPS'].aggregate([
    {"$match": {"trained": False}},
    {"$count": "total not trained"}
])

# Log the output of the aggregation
not_trained_result = list(not_trained_count)
logging.info(f"Documents not trained: {not_trained_result}")




# Attempt to find one document to inspect its fields
sample_document = db['MLOPS'].find_one()

if sample_document:
    # Extract keys which are the field names of the document
    field_names = sample_document.keys()
    logging.info(f"Field names in the 'MLOPS' collection: {list(field_names)}")
else:
    logging.info("No documents found in the 'MLOPS' collection.")

# If you want to see all unique fields across all documents, you can use an aggregation query:
unique_fields = db['MLOPS'].aggregate([
    {"$project": {"arrayofkeyvalue": {"$objectToArray": "$$ROOT"}}},
    {"$unwind": "$arrayofkeyvalue"},
    {"$group": {"_id": None, "allKeys": {"$addToSet": "$arrayofkeyvalue.k"}}}
])

# Log all unique fields found in the collection
unique_fields_list = list(unique_fields)
if unique_fields_list:
    logging.info(f"All unique field names in the 'MLOPS' collection: {unique_fields_list[0]['allKeys']}")
else:
    logging.info("No data to display unique fields.")
    
    
    
    
# # Fetch and log all documents from the 'MLOPS' collection
# all_documents = db['MLOPS'].find({})
# for doc in all_documents:
#     logging.info(f"Document: {doc}")

# # You might want to log this data to a file or handle it differently depending on your needs.
