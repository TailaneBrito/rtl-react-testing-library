import requests

def main():
    key = "b334ebcb01e86c61c138ca992d6d8946"
    res = requests.get("http://data.fixer.io/api/latest?access_key=b334ebcb01e86c61c138ca992d6d8946&symbols=BRL",
                       verify=False)


    if res.status_code != 200:
        raise Exception("Error: Api request unsuccessful")
    data = res.json()
    print(res.json())
    #extrating information from json obj
    rate = data["rates"]["BRL"]
    print(f"1 USD is equal to { rate } BRL")

if __name__ == "__main__":
    main()