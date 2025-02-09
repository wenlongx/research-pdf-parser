from openai import OpenAI
import datetime

# Initialize the OpenAI client
client = OpenAI()

# list all of our assistants 
def list_assistants(client, limit=100):
    return client.beta.assistants.list(order='desc', limit=str(limit))

# function that deletes and assistant
def delete_assistant(client, assistant_id):
    try:
        response =client.beta.assistants.delete(assistant_id=assistant_id)
        print(f'Deleted: {assistant_id}!')
        return response 
    except Exception as e:
        print(f'errror deleting {assistant_id}: {e}')

def main():
    # get the list of assistants 
    my_assistants = list_assistants(client)

    # delete all of the assistants that are not in the do_not_delete_ids set
    for assistant in my_assistants.data:
        delete_assistant(client, assistant.id)

if __name__ == "__main__":
    main()