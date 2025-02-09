import os
import re
from openai import OpenAI
import time


# Directory containing PDF files
pdf_directory = "/Users/wenlongx/Desktop/litreviewpdfs/"

# Set your OpenAI API key
client = OpenAI()

vector_store = client.beta.vector_stores.create(name="documents")

def upload_files(directory):
    pdf_paths = []
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            pdf_paths.append(pdf_path)
    file_streams = [open(path, "rb") for path in pdf_paths]

    print(f"Uploading files: {pdf_paths}")

    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    print("Waiting for file uploads ...")
    # You can print the status and the file counts of the batch to see the result of this operation.
    while file_batch.status != "completed":
        print("Waiting for file uploads ...")
        time.sleep(5)
    print("Succeeded")
    return

# Main function to iterate over PDFs and extract thematic information
def main():
    print("Begin file upload")
    upload_files(pdf_directory)
    print("Finished uploading files!")

    print(f"Vector store ID is: {vector_store.id}")


    global_instructions = "You are a data cleaner research assistant. Use the knowledge base of PDFs to transform PDF data into cleaned, summarized information."

    assistant = client.beta.assistants.create(
        name="assistant",
        instructions=global_instructions,
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
    )

    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    print(f"Assistant ID is: {assistant.id}")

if __name__ == "__main__":
    main()
