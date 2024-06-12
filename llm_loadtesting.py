import concurrent.futures
import requests
import csv
from io import StringIO

def read_first_column_from_github_csv(repo_url, file_path):
    first_column = []
    response = requests.get(repo_url + '/raw/main/' + file_path)
    if response.status_code == 200:
        csv_data = response.text.strip()
        csv_reader = csv.reader(StringIO(csv_data))
        for row in csv_reader:
            if row:  # Ensure the row is not empty
                first_column.append(row[0])
        return first_column
    else:
        print("Failed to fetch CSV file. Status code:", response.status_code)
        return None

# Example usage:
github_repo_url = 'https://github.com/hrusheekeshsawarkarreverie/LLM_queries'  # Replace with your GitHub repo URL
csv_file_path = 'LLM_queries.csv'  # Replace with the path to your CSV file in the repo

first_column = read_first_column_from_github_csv(github_repo_url, csv_file_path)
if first_column:
    print("First column values:", first_column)

# Define a function to send a POST request
def send_post_request(url, data):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    body = {
        'model':'llama3',
        'prompt':data,
        'stream':False
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return None, str(e)

# The URL for the POST requests
url = "http://0.0.0.0:11434/api/chat"

# List of data payloads for the POST requests
# data_payloads = [
#     {"query": "hello"},
#     {"query": "who are you"},
#     {"query": "i want to eat"},
#     {"query": "how are you"},
#     # Add more data payloads as needed
# ]

final_data_payloads = []
for i in range(2):
    for i in range(1,len(first_column)-1):
        # final_data_payloads.append(data_payloads[0])
        # final_data_payloads.append(data_payloads[1])
        # final_data_payloads.append(data_payloads[2])
        # final_data_payloads.append(data_payloads[3])
        data_payloads = first_column[i]
        final_data_payloads.append(data_payloads)

print(f'hello {len(final_data_payloads)}')
# Function to execute POST requests in parallel
def execute_parallel_post_requests(url, final_data_payloads):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        future_to_data = {executor.submit(send_post_request, url, data): data for data in final_data_payloads}
        for future in concurrent.futures.as_completed(future_to_data):
            data = future_to_data[future]
            try:
                status_code, response_data = future.result()
                results.append((data, status_code, response_data))
            except Exception as exc:
                results.append((data, None, str(exc)))
    return results

# Execute the POST requests and get the results
results = execute_parallel_post_requests(url, final_data_payloads)

# Print the results
for data, status_code, response_data in results:
    print(f"Data: {data}")
    print(f"Status Code: {status_code}")
    print(f"Response Data: {response_data}")
    print()
