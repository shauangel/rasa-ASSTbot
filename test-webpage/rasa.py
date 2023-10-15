import requests


if __name__ == "__main__":
    rasa_webhook = "http://0.0.0.0:5005/webhooks/rest/webhook"
    start = 1
    prefix = ""
    while(start):
        msg = input("Please input here: ")
        myReq = {
            "sender": "tester",
            "message": msg
        }
        print(myReq)
        rasaRp = requests.post(rasa_webhook, json=myReq)
        print("-"*10 + "Send Request" + "-"*10)
        resp = rasaRp.json()
        print(resp)
        # if resp['']