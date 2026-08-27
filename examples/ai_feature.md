## Problem
The support team spends too much time triaging tickets, leading to delayed responses for urgent cases.

## Working Hypothesis
We will add an AI feature that automatically classifies each new support ticket as Urgent, Normal, or Low priority based on the ticket text, to help the support team triage faster.

## Strategy Fit
This unlocks the broader goal of improving the overall efficiency and effectiveness of the support team's operations.

## Goals & Non-Goals

| Goal | Description |
| --- | --- |
| Reduce TTR for Urgent tickets | Decrease average time-to-first-response for Urgent tickets by 40% within 30 days. |
| Improve triage accuracy | Classify tickets as Urgent, Normal, or Low priority based on ticket text. |
| Exclude language support | Tickets will not be classified in languages other than English. |
| Exclude agent routing | Automatically routing tickets to specific agents is out of scope for this release. |

## Target users
Support agents triaging the ticket queue.

## Requirements

* The AI feature must classify tickets as Urgent, Normal, or Low priority with at least 80% accuracy.
* The feature must handle ticket text in multiple formats (e.g., plain text, HTML).
* The feature must be able to learn from and adapt to changes in ticket volume and content over time.

## Behavior Contract

Good examples:

* "I'm experiencing a critical issue with my account. Please help me resolve it ASAP." - Urgent
* "I'm having trouble with my order. Can you please assist me?" - Normal
* "This is just a minor inquiry about our product features." - Low priority

Bad examples:

* "I'm not sure if this is a bug or a feature request. Can you clarify?" - Plausible but wrong classification
* "This ticket is for a technical issue, but I'm not sure what it is yet." - Incorrect classification as Urgent

Reject example:

* "I'm requesting a refund for a product that's no longer available." - Feature should refuse or escalate this type of request.

## Guardrails

* The AI feature must never classify a ticket as Urgent if the text does not contain relevant keywords (e.g., "critical issue", "urgent matter").
* The feature must always check for and respect user-specific priority settings before making a classification decision.

## Assumptions I made
None — all scope decisions were directly stated or resolved by the clarifying answers above.

## Open questions
How will we ensure that the AI feature is fair and unbiased in its classification decisions?

## Success metrics

* Offline Golden Set: A test dataset of 1,000 tickets with manually classified labels for Urgent, Normal, and Low priority.
* Human Review: A manual review of 100 tickets after launch to verify accuracy and identify areas for improvement.
* Online Metrics:
	+ Average TTR for Urgent tickets within the first 30 days of launch
	+ Classification accuracy rate over time (measured against a baseline)
	+ User satisfaction with the feature, as measured through surveys or feedback forms.

## Rollout Plan

* Exposure: 20% of support agents will have access to the new feature during the initial rollout.
* Duration: The initial rollout will run for 30 days before a go/no-go decision is made based on performance data.
* Segments & Ramp Gates:
	+ The feature must meet its accuracy requirements and user satisfaction targets for at least 14 days before exposure expands further.

## Risk Management

* Detection: An automated review of TTR and classification accuracy rates will trigger alerts if the feature fails to meet its requirements.
* Fallback & Kill Switch: A manual override mechanism will be put in place to quickly disable or adjust the feature if it's not performing as expected.
* Owner: The primary owner for this feature is [Name], who will receive notifications and updates on its performance.

## Ownership & Action

* Primary Owner: [Name]
* Decision Points:
	+ After 30 days of launch, a review of TTR and classification accuracy rates to determine whether the feature should be expanded or adjusted.
	+ After 60 days of launch, a follow-up review to assess user satisfaction and make any necessary adjustments.