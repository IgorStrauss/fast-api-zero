from http import HTTPStatus

from bs4 import BeautifulSoup


def test_read_root_deve_retornar_ola_mundo(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_path_html_titulo_da_pagina_deve_retornar_MarquesIgor(client):
    response = client.get("/path-html")

    assert response.status_code == HTTPStatus.OK

    soup = BeautifulSoup(response.text, "html.parser")

    title_tags = soup.find_all("title")
    assert len(title_tags) == 1
    assert title_tags[0].text == "MarquesIgor"


def test_path_html_deve_retornar_html(client):
    response = client.get("/path-html")

    assert response.status_code == HTTPStatus.OK

    soup = BeautifulSoup(response.text, "html.parser")

    h1_tags = soup.find_all("h1")

    expected_h1_tags = 2

    assert len(h1_tags) == expected_h1_tags

    def normalize_text(text):
        return text.replace("\n", "").replace(" ", "").strip()

    assert normalize_text(h1_tags[0].text) == "MarquesIgor"
    assert normalize_text(h1_tags[1].text) == "CursoFastAPIZerocomDunossauro!"
