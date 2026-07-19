import requests

GAS_URL = "https://script.google.com/macros/s/AKfycbz8q6-gh1sxYlLlaYAht8z5VoVtTtpoCa_0oPg-Bt2Q4DdgrZfWy-ZnRKBVuMgaoWwl/exec"

def send_block(block):

    print("Mengirim block ke Google Spreadsheet...")

    try:

        response = requests.post(
            GAS_URL,
            json=block.to_dict(),
            timeout=10
        )

        print("Status Code :", response.status_code)
        print("Response    :", response.text)

    except Exception as e:
        print("Google Sheet Error :", e)