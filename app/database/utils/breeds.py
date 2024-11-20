from contextlib import contextmanager

import httpx


@contextmanager
def request_session(**settings):
    with httpx.Client(**settings) as session:
        yield session


def breed_to_key(name: str):
    return name.replace(" ", "_").upper()


def get_breeds():
    with request_session() as session:
        breeds = session.get("https://api.thecatapi.com/v1/breeds")
        assert breeds.status_code == 200

    return {
        breed_to_key(name := breed["name"]): name 
        for breed in breeds.json()
    }
