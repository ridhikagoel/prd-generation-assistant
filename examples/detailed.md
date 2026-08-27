## Problem
One customer invoice becomes exactly 7 days overdue for the designated billing contact on Growth and Enterprise plans.

## Working Hypothesis
We will add email and in-app notifications when a customer invoice becomes exactly 7 days overdue for the designated billing contact on Growth and Enterprise plans.

## Strategy Fit
This feature unlocks the initiative to improve customer support efficiency by reducing where-is-my-invoice support tickets.

## Goals & Non-Goals

| Goal | Description |
| --- | --- |
| Reduce Where-Is-My-Invoice Tickets | Reduce support tickets for overdue invoices by 30% within 60 days. |
| Improve Payment Timeliness | Reduce average days-to-payment for overdue invoices from 12 days to 7 days. |
| Exclude Starter Plan Users | Do not apply notifications or invoicing features to accounts on the Starter plan. |

## Target users
The designated billing contact, a named role stored on the account record.

## Requirements

* Notifications are sent exactly 7 days before an invoice is due.
* Notifications are sent only for invoices that are overdue and have not been paid yet.
* The notification includes a clear subject line and body with relevant payment information.
* In-app notifications are displayed in the billing contact's dashboard.

## Behavior Contract
Not applicable — this feature does not involve variable AI or automated behavior that needs an example-based contract.

## Guardrails
Not applicable

## Assumptions I made
* There is a named role stored on the account record for the designated billing contact.
* The billing contact is the only relevant user for notifications and invoicing features.

## Open questions
How will we handle cases where the billing contact does not have access to their account information?

## Success metrics

- Offline Golden Set: A test dataset of 100 accounts with 50 overdue invoices, where at least one notification is sent exactly 7 days before due date.
- Human Review: The primary owner reviews the first week's data for accuracy and completeness.
- Online Metrics:
  * KPI 1: Number of notifications sent correctly (at least 95% accuracy).
  * KPI 2: Average time-to-payment for overdue invoices (target: <7 days).
  * KPI 3: Reduction in where-is-my-invoice support tickets (target: -30% within 60 days).

## Rollout Plan

* Exposure: 50% of Growth and Enterprise plan users initially.
* Duration: Initial rollout runs for 4 weeks before a go/no-go decision.
* Segments & Ramp Gates:
  * The feature is enabled for all eligible accounts after the initial 4-week period.
  * Further exposure expansion requires review and approval by the primary owner.

## Risk Management

* Detection: The primary owner reviews the first week's data for accuracy and completeness, and checks the notification logs for errors.
* Fallback & Kill Switch: In case of issues, the feature is disabled immediately, and notifications are stopped. A kill switch allows the primary owner to disable the feature manually if needed.
* Owner: The primary owner gets paged if something goes wrong.

## Ownership & Action

* Primary Owner: The senior product manager responsible for this feature.
* Decision Points:
  * After the first week's data review and analysis.
  * After a minimum of 4 weeks' data collection to ensure stability.
  * Quarterly reviews to assess progress toward goals.