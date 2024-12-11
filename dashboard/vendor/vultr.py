import requests


def get_account(api_token):
    resp = requests.get(
        url="https://api.vultr.com/v2/account",
        headers={"Authorization": f"Bearer {api_token}"},
        timeout=55,
    )
    resp.raise_for_status()
    return resp.json()


def get_instance(api_token, uuid):
    resp = requests.get(
        url=f"https://api.vultr.com/v2/instances/{uuid}",
        headers={"Authorization": f"Bearer {api_token}"},
        timeout=55,
    )
    resp.raise_for_status()
    return resp.json()


def list_instances(api_token):
    resp = requests.get(
        url="https://api.vultr.com/v2/instances",
        headers={"Authorization": f"Bearer {api_token}"},
        timeout=55,
    )
    resp.raise_for_status()
    return resp.json()
