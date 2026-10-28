
def explain_dom_risk(features):
    score = 0
    reasons = []

    def add_reason(points, indicator, evidence, explanation, action):
        nonlocal score
        score += points
        reasons.append({
            "indicator": indicator,
            "points": points,
            "evidence": evidence,
            "explanation": explanation,
            "recommendation": action,
        })

    # 1. Password fields
    if features.get("password_fields", 0) > 0:
        add_reason(
            10,
            "Password field detected",
            f"{features['password_fields']} password field(s) found",
            "Password fields are common on login pages but can also collect credentials.",
            "Verify the website domain before entering a password."
        )

    # 2. Forms submitting to another domain
    if features.get("external_forms", 0) > 0:
        add_reason(
            30,
            "External form destination",
            f"{features['external_forms']} form(s) submit to another domain",
            "Sending form data to another domain may expose information, "
            "although legitimate websites can also use external services.",
            "Inspect the destination domain."
        )

    # 3. Forms without an explicit action
    if features.get("missing_form_actions", 0) > 0:
        add_reason(
            5,
            "Missing form action",
            f"{features['missing_form_actions']} form(s) have no explicit action",
            "The form does not specify a submission destination in its action attribute.",
            "Inspect the form behavior."
        )

    # 4. Multiple iframes
    if features.get("iframe_count", 0) > 2:
        add_reason(
            10,
            "Multiple iframes",
            f"{features['iframe_count']} iframe(s) found",
            "Multiple embedded frames may deserve inspection.",
            "Review the iframe sources."
        )

    # 5. External iframes
    if features.get("external_iframes", 0) > 0:
        add_reason(
            10,
            "External iframe source",
            f"{features['external_iframes']} iframe(s) point to another domain",
            "External frames can load third-party content.",
            "Check whether the embedded domain is expected."
        )

    # 6. Large script count
    if features.get("script_count", 0) > 15:
        add_reason(
            5,
            "High script count",
            f"{features['script_count']} script element(s) found",
            "Many scripts are common on modern websites and are a weak signal.",
            "Investigate unfamiliar scripts alongside other indicators."
        )

    # 7. Many external links
    if features.get("external_links", 0) > 20:
        add_reason(
            5,
            "Many external links",
            f"{features['external_links']} links point to other domains",
            "Numerous external links may be legitimate but deserve context.",
            "Inspect unexpected or misleading links."
        )

    score = min(score, 100)

    if score >= 50:
        assessment = "High DOM risk"
    elif score >= 25:
        assessment = "Moderate DOM risk"
    elif score > 0:
        assessment = "Low DOM risk indicators detected"
    else:
        assessment = "No configured DOM indicators detected"

    return {
        "dom_risk_score": score,
        "assessment": assessment,
        "reasons": reasons,
        "limitations": (
            "This is a preliminary rule-based score, not a probability "
            "of phishing. No detected indicators does not prove a page is safe."
        ),
    }


def calculate_dom_risk(features):
    # Preserve compatibility with your existing tests.
    return explain_dom_risk(features)["dom_risk_score"]
