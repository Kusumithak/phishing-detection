
from features import extract_features
from risk_score import explain_dom_risk

tests = [
    ("Password field", """
        <input type="password">
    """, 10),

    ("External form", """
        <form action="https://other.example/login"></form>
    """, 30),

    ("Missing form action", """
        <form><input type="text"></form>
    """, 5),

    ("Multiple iframes", """
        <iframe src="/a"></iframe>
        <iframe src="/b"></iframe>
        <iframe src="/c"></iframe>
    """, 10),

    ("External iframe", """
        <iframe src="https://other.example/frame"></iframe>
    """, 10),

    ("Many scripts", """
        """ + "".join("<script></script>" for _ in range(16)) + """
    """, 5),

    ("Many external links", """
        """ + "".join(
            f'<a href="https://site{i}.example/">Link</a>'
            for i in range(21)
        ) + """
    """, 5),
]

url = "https://example.com"

for name, html, expected in tests:
    features = extract_features(url, html)
    report = explain_dom_risk(features)
    actual = report["dom_risk_score"]

    status = "PASS" if actual == expected else "FAIL"

    print(
        f"{status}: {name} | "
        f"Expected: {expected} | Actual: {actual}"
    )

    if actual != expected:
        print("Features:", features)
