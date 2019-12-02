import requests

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ILwXvguynynBDzXQmVmUQ",
                                                                                "isbns": "1632168146",
                                                                                },
                   verify=False
                   )
print(res.json())
print(res.json().books)

print(res.cookies)


#verify='/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/requests/cacert.pem'