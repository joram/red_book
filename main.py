#!/usr/bin/env python
import os

import bs4
import requests
from bs4 import Comment

bad_urls = ["24"]
_global_words = None


def urls():
    visited = []
    for line in open("./urls.csv"):
        if "www" in line:
            url = line.split(" ")[0].replace("\n", "")
            if url in bad_urls:
                continue
            if "@" in url:
                continue
            if "-" in url:
                continue
            if url.startswith("http://"):
                url = url.replace("http://", "")
            if url.startswith("https://"):
                url = url.replace("https://", "")
            if "/" in url:
                url = url.split("/")[0]
            if url not in visited:
                visited.append(url)
                yield url


def get_cached_content(url):
    filepath = f"./cache/{url.replace('.', '_').replace('/', '_')}.html"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read()

    if not url.startswith("http"):
        url = f"https://{url}"
    try:
        response = requests.get(url, timeout=5)
    except:
        return None
    if response.status_code != 200:
        return None
    with open(filepath, "w") as f:
        f.write(response.text)

    return open(filepath, "r").read()


def calculate_tfidf(content, limit=3):
    """
    Calculate the tf-idf for each word in a document.
    """
    tfidf = {}
    words = words_from_html(content)
    for word in words:
        if word not in tfidf:
            tfidf[word] = 0
        tfidf[word] += 1

    final_tfidf = {}
    for word in tfidf:
        if tfidf[word] <= limit:
            continue
        final_tfidf[word] = tfidf[word] / global_term_frequency().get(word, 1)

    return final_tfidf


def words_from_html(body):
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    soup = bs4.BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    text = u" ".join(t.strip() for t in visible_texts)
    while "  " in text:
        text = text.replace("  ", " ")
    text = text.lower()
    words = text.split(" ")
    return words


def global_term_frequency():
    global _global_words
    if _global_words is not None:
        return _global_words

    global_words = {}
    i = 0
    with open("./unigram_freq.csv", "r") as f:
        for line in f.readlines():
            term, frequency = line.split(",")
            global_words[term] = int(frequency)

    _global_words = global_words
    return global_words


def top_words(content, count_limit=3, limit=3):
    tfidf = calculate_tfidf(content, limit=count_limit)
    return sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:limit]



global_term_frequency()
for url in urls():
    url = url+"/about"
    content = get_cached_content(url)
    # content = get_cached_content(url)
    if content:
        words = top_words(content, limit=5)
        words = [word[0] for word in words]
        print(url, words)
