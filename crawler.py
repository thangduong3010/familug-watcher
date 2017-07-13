import requests
from bs4 import BeautifulSoup
from app import db
from app import Posts


LABELS = ("Python", "Command", "sysadmin")
URL = "http://www.familug.org/search/label/{}"


def crawler(label=None, latest=False):
    """ Fetch data from `URL`

    :param label: posts' label to search
    :param latest: True to fetch latest posts
    :rtype generator:
    """
    if not latest:
        resp = requests.get(URL.format(label))
    else:
        resp = requests.get("http://www.familug.org")
    soup = BeautifulSoup(resp.text, "html.parser")

    for post in soup.find_all('h3', class_='post-title entry-title'):
        yield (post.text, post.a['href'])


def insert():
    """ Insert data to database
    """
    for label in LABELS:
        for title, url in crawler(label):
            row = Posts(title, label, url)
            db.session.add(row)

    # fetch latest
    label = "Latest"
    for title, url in crawler(latest=True):
        row = Posts(title, label, url)
        db.session.add(row)

    db.session.commit()


def main():
    insert()


if __name__ == "__main__":
    main()
