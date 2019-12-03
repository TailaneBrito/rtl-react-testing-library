import requests

def main():
    key = 'ILwXvguynynBDzXQmVmUQ'
    isbn = '1632168146'
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": key,
                               "isbns": isbn},
                       verify=False
                       )
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    data = res.json()
    book_rating = data["books"][9]
    print(f"1 {isbn} has the {book_rating} on Googlereads!")

if __name__ == "__main__":
    main()


#verify='/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/requests/cacert.pem'