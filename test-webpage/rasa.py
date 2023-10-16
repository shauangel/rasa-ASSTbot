import requests


if __name__ == "__main__":
    rasa_webhook = "http://0.0.0.0:5005/webhooks/rest/webhook"
    resp = ""
    prefix = ""
    while(1):
        try:
            if "describe your question" in resp['text']:
                prefix = "my question is:"
        except Exception as e:
            prefix = ""
        print("-" * 10 + "User" + "-" * 10)
        msg = input("Please input here: ")
        myReq = {
            "sender": "tester",
            "message": prefix + msg
        }
        # print(myReq)
        rasaRp = requests.post(rasa_webhook, json=myReq)
        print("-"*10 + "PSAbot" + "-"*10)
        resp = rasaRp.json()
        print(resp)
        # print(resp[0]['text'].replace("<br>", '\n'))
        # if resp['']
