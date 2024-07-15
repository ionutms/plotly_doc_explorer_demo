"""Web utils module."""

from bs4 import BeautifulSoup
import requests


def check_section_exists(url):
    """check_section_exists"""
    section_id = url.split('#')[-1]
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException:
        pass
    return soup.find(id=section_id) is not None
