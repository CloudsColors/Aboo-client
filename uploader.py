import requests
import json

class Uploader:

    def __init__(self):
        self._API_HOST = "https://api.aboo.se/file"

    def upload_screenshot(self, filename):
        try:
            files = {
                "file": (filename, open(filename, "rb"))
            }
        except:
            return (False, "Can not find a file with the filename: "+filename, None)
        #We dont need any header information for this call
        response = requests.post(self._API_HOST, files=files)
        if(not response.status_code == 201):
            return (False, "Something went wrong with the POST request", None)
        readResponse = json.loads(response.text)
        url = readResponse["data"]["file"]["url"]["minimal"]
        _id = readResponse["data"]["file"]["metadata"]["id"]
        return (True, url, _id)

if __name__ == "__main__":
    uploader = Uploader()
    print(uploader.upload_screenshot("temp_file_name.png"))