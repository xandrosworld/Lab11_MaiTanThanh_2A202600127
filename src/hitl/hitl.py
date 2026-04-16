"""
Lab 11 - Part 4: Human-in-the-Loop Design
  TODO 12: Confidence Router
  TODO 13: Design 3 HITL decision points
"""
from dataclasses import dataclass


HIGH_RISK_ACTIONS = [
    "transfer_money",
    "close_account",
    "change_password",
    "delete_data",
    "update_personal_info",
]


@dataclass
class RoutingDecision:
    """Result of the confidence router."""

    action: str
    confidence: float
    reason: str
    priority: str
    requires_human: bool


class ConfidenceRouter:
    """Route agent responses based on confidence and risk level."""

    HIGH_THRESHOLD = 0.9
    MEDIUM_THRESHOLD = 0.7

    def route(
        self,
        response: str,
        confidence: float,
        action_type: str = "general",
    ) -> RoutingDecision:
        """Route a response based on confidence score and action type."""
        if action_type in HIGH_RISK_ACTIONS:
            return RoutingDecision(
                action="escalate",
                confidence=confidence,
                reason=f"High-risk action: {action_type}",
                priority="high",
                requires_human=True,
            )

        if confidence >= self.HIGH_THRESHOLD:
            return RoutingDecision(
                action="auto_send",
                confidence=confidence,
                reason="High confidence",
                priority="low",
                requires_human=False,
            )

        if confidence >= self.MEDIUM_THRESHOLD:
            return RoutingDecision(
                action="queue_review",
                confidence=confidence,
                reason="Medium confidence - needs review",
                priority="normal",
                requires_human=True,
            )

        return RoutingDecision(
            action="escalate",
            confidence=confidence,
            reason="Low confidence - escalating",
            priority="high",
            requires_human=True,
        )


hitl_decision_points = [
    {
        "id": 1,
        "name": "High-Value Transaction Approval",
        "trigger": "Transfer request above the auto-approval threshold or to a risky new beneficiary.",
        "hitl_model": "human-in-the-loop",
        "context_needed": "Customer identity, amount, destination account, fraud signals, and recent transaction history.",
        "example": "A user asks to transfer 250,000,000 VND to a newly added account late at night.",
    },
    {
        "id": 2,
        "name": "Sensitive Account Recovery",
        "trigger": "Password reset, phone-number change, or account recovery request with incomplete verification.",
        "hitl_model": "human-in-the-loop",
        "context_needed": "KYC status, OTP or identity-check results, registered contact channels, and the conversation transcript.",
        "example": "A customer wants to change their phone number and reset password but cannot complete OTP verification.",
    },
    {
        "id": 3,
        "name": "Policy Ambiguity or Safety Dispute",
        "trigger": "The assistant is low-confidence or guardrails disagree on whether a response is safe and accurate.",
        "hitl_model": "human-as-tiebreaker",
        "context_needed": "User prompt, draft answer, guardrail flags, confidence score, and the relevant policy excerpt.",
        "example": "A customer asks whether a suspicious transfer can be reversed immediately and the assistant is unsure about the exact rule.",
    },
]


def test_confidence_router():
    """Test ConfidenceRouter with sample scenarios."""
    router = ConfidenceRouter()

    test_cases = [
        ("Balance inquiry", 0.95, "general"),
        ("Interest rate question", 0.82, "general"),
        ("Ambiguous request", 0.55, "general"),
        ("Transfer $50,000", 0.98, "transfer_money"),
        ("Close my account", 0.91, "close_account"),
    ]

    print("Testing ConfidenceRouter:")
    print("=" * 80)
    print(f"{'Scenario':<25} {'Conf':<6} {'Action Type':<18} {'Decision':<15} {'Priority':<10} {'Human?'}")
    print("-" * 80)

    for scenario, conf, action_type in test_cases:
        decision = router.route(scenario, conf, action_type)
        print(
            f"{scenario:<25} {conf:<6.2f} {action_type:<18} "
            f"{decision.action:<15} {decision.priority:<10} "
            f"{'Yes' if decision.requires_human else 'No'}"
        )

    print("=" * 80)


def test_hitl_points():
    """Display HITL decision points."""
    print("\nHITL Decision Points:")
    print("=" * 60)
    for point in hitl_decision_points:
        print(f"\n  Decision Point #{point['id']}: {point['name']}")
        print(f"    Trigger:  {point['trigger']}")
        print(f"    Model:    {point['hitl_model']}")
        print(f"    Context:  {point['context_needed']}")
        print(f"    Example:  {point['example']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_confidence_router()
    test_hitl_points()
