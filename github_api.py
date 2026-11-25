import json
import urllib.error
import urllib.request


def create_github_repo(name: str, token: str, private: bool = True, description: str = "") -> str:
    url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": name,
        "private": private,
        "description": description,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "gh-init-cli",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["clone_url"]
    except urllib.error.HTTPError as e:
        details = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"GitHub API ({e.code}): {details}") from e