from features import extract_features
from risk_score import calculate_dom_risk

sample_url = "https://example.com"

sample_html = """
<html>
<body>
    <form action="https://other.example/login">
        <input type="password">
    </form>
    <iframe src="https://example.com/frame"></iframe>
</body>
</html>
"""

features = extract_features(sample_url, sample_html)
score = calculate_dom_risk(features)

print("Extracted Features:", features)
print("DOM Risk Score:", score)