
import requests

from features import extract_features
from risk_score import explain_dom_risk


def analyze_url(url):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "DOMAnalysis/1.0"},
            allow_redirects=True
        )
        response.raise_for_status()

        # Analyze the HTML returned by the webpage
        features = extract_features(
            response.url,
            response.text
        )

        # Generate score and evidence-based explanations
        report = explain_dom_risk(features)

        return {
            "url": response.url,
            "features": features,
            "dom_risk_score": report["dom_risk_score"],
            "assessment": report["assessment"],
            "reasons": report["reasons"],
            "limitations": report["limitations"],
        }

    except requests.RequestException as error:
        return {
            "url": url,
            "error": str(error),
        }


if __name__ == "__main__":
    url = input("Enter a webpage URL: ").strip()

    if not url.startswith(("http://", "https://")):
        print("Please enter a URL starting with http:// or https://")
    else:
        result = analyze_url(url)

        print("\nDOM ANALYSIS REPORT")
        print("-" * 40)

        if "error" in result:
            print("Error:", result["error"])
        else:
            print("URL:", result["url"])
            print("DOM Risk Score:", result["dom_risk_score"], "/ 100")
            print("Assessment:", result["assessment"])

            print("\nDetected indicators:")
            if result["reasons"]:
                for reason in result["reasons"]:
                    print(f"\n- {reason['indicator']} (+{reason['points']})")
                    print("  Evidence:", reason["evidence"])
                    print("  Explanation:", reason["explanation"])
                    print("  Recommendation:", reason["recommendation"])
            else:
                print("No configured DOM indicators detected.")

            print("\nLimitations:", result["limitations"])
