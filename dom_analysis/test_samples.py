
from features import extract_features
from risk_score import explain_dom_risk

samples = [
    {
        "name": "Simple webpage",
        "url": "https://example.com",
        "html": """
        <html>
        <body>
            <h1>Welcome</h1>
            <p>This is a simple webpage.</p>
        </body>
        </html>
        """
    },
    {
        "name": "Normal login form",
        "url": "https://example.com",
        "html": """
        <html>
        <body>
            <form action="/login" method="post">
                <input type="password" name="password">
                <button type="submit">Login</button>
            </form>
        </body>
        </html>
        """
    },
    {
        "name": "Suspicious external form",
        "url": "https://example.com",
        "html": """
        <html>
        <body>
            <form action="https://other.example/collect" method="post">
                <input type="password" name="password">
                <button type="submit">Verify Account</button>
            </form>
        </body>
        </html>
        """
    }
]

for sample in samples:
    features = extract_features(sample["url"], sample["html"])
    report = explain_dom_risk(features)

    print("\n" + "=" * 45)
    print("TEST:", sample["name"])
    print("Features:", features)
    print("Score:", report["dom_risk_score"], "/ 100")
    print("Assessment:", report["assessment"])

    for reason in report["reasons"]:
        print("-", reason["indicator"], ":", reason["evidence"])
