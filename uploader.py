import requests
import json

def upload_screenshot():
    apiHost = "https://api.aboo.se/file"
    files = {
        "file": ("temp_file_name.png", open("temp_file_name.png", "rb"))
    }
    #We dont need any header information for this call
    response = requests.post(apiHost, files=files)
    if(not response.status_code == 201):
        return False
    readResponse = json.loads(response.text)
    url = readResponse["data"]["file"]["url"]["minimal"]
    _id = readResponse["data"]["file"]["metadata"]["id"]
    return (url, _id)

if __name__ == "__main__":
    print(upload_screenshot())