
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def extract_features(url, html):
    soup = BeautifulSoup(html, "html.parser")

    page_domain = (urlparse(url).hostname or "").lower()

    forms = soup.find_all("form")
    password_fields = soup.find_all(
        "input", {"type": "password"}
    )
    iframes = soup.find_all("iframe")
    scripts = soup.find_all("script")
    links = soup.find_all("a", href=True)

    external_forms = 0
    missing_form_actions = 0
    hidden_inputs = 0
    external_iframes = 0
    external_links = 0

    # Analyze form destinations
    for form in forms:
        action = form.get("action", "").strip()

        if not action:
            missing_form_actions += 1
            continue

        destination = urlparse(urljoin(url, action))
        destination_domain = (
            destination.hostname or ""
        ).lower()

        if destination_domain and destination_domain != page_domain:
            external_forms += 1

    # Count hidden input fields
    for field in soup.find_all("input"):
        field_type = field.get("type", "").lower()

        if field_type == "hidden":
            hidden_inputs += 1

    # Analyze iframe destinations
    for iframe in iframes:
        src = iframe.get("src", "").strip()

        if not src:
            continue

        destination = urlparse(urljoin(url, src))
        iframe_domain = (
            destination.hostname or ""
        ).lower()

        if iframe_domain and iframe_domain != page_domain:
            external_iframes += 1

    # Analyze links pointing to other domains
    for link in links:
        href = link.get("href", "").strip()

        if not href:
            continue

        destination = urlparse(urljoin(url, href))

        if destination.scheme not in ("http", "https"):
            continue

        link_domain = (destination.hostname or "").lower()

        if link_domain and link_domain != page_domain:
            external_links += 1

    return {
        "form_count": len(forms),
        "password_fields": len(password_fields),
        "iframe_count": len(iframes),
        "script_count": len(scripts),
        "external_forms": external_forms,
        "missing_form_actions": missing_form_actions,
        "hidden_inputs": hidden_inputs,
        "external_iframes": external_iframes,
        "external_links": external_links,
    }
