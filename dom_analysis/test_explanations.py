
from features import extract_features
from risk_score import explain_dom_risk

url = "https://shop.example"

html = """
<html>
<body>
    <form action="https://other.example/collect" method="post">
        <input type="password" name="password">
        <button type="submit">Continue</button>
    </form>
</body>
</html>
"""

features = extract_features(url, html)
report = explain_dom_risk(features)

print("DOM RISK SCORE:", report["dom_risk_score"], "/ 100")
print("ASSESSMENT:", report["assessment"])

for reason in report["reasons"]:
    print("\nIndicator:", reason["indicator"])
    print("Evidence:", reason["evidence"])
    print("Explanation:", reason["explanation"])
    print("Recommendation:", reason["recommendation"])

print("\nLimitations:", report["limitations"])
