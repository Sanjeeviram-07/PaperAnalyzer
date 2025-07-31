def fetch_paper(url: str) -> str:
    import requests
    response = requests.get(url)
    return response.text
