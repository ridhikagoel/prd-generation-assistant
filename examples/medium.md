## Problem
- Core Problem: The system fails to notify customers when their invoices are overdue, leading to delayed payments and increased support tickets for missing invoices.
- Working Hypothesis: The feature will notify customers by email when their invoice is 7 days overdue, encouraging faster payment and reducing where-is-my-invoice tickets.
- Strategy Fit: This feature aligns with the broader initiative to improve customer experience and reduce operational costs.

## Goals & Non-Goals
| Goal | Scope Boundary |
| --- | --- |
| Notify customers of overdue invoices | Only applicable for customers with outstanding invoices that can become overdue. |
| Reduce where-is-my-invoice tickets | Focus on reducing ticket volume, not addressing the root cause of missing invoices. |

## Target users
The target user is a customer with an invoice that can become overdue.

## Requirements
* The feature will send a notification email to customers when their invoice is 7 days overdue.
* The email will include a clear subject line and body with instructions on how to pay the outstanding amount.
* The system will automatically update the customer's invoice status to "overdue" in the system.
* The feature will be configurable to exclude specific types of invoices or scenarios.

## Behavior Contract
Not applicable — this feature does not involve variable AI or automated behavior that needs an example-based contract.

## Guardrails
Not applicable

## Assumptions I made
* The target user is a customer with an invoice that can become overdue.
* Success in reducing where-is-my-invoice tickets and improving payment speed will be measured by a combination of ticket volume reduction and payment speed improvement metrics.
* Specific types of invoices or scenarios for which this feature should not apply are not specified.

## Open questions
How will we determine the optimal notification frequency for customers with overdue invoices?
What is the ideal threshold for "overdue" invoice status, and how will it be configured?

## Success metrics
- Offline Golden Set: A test dataset of 100 customer accounts with a mix of overdue and non-overdue invoices.
- Human Review: A manual review by a support team member to verify that the feature is correctly notifying customers and updating their invoice status.
- Online Metrics:
  * Reduction in where-is-my-invoice tickets by 20% within the first 30 days after launch.
  * Average payment speed improvement of 10% compared to baseline performance.

## Rollout Plan
- Exposure: 20% of all customers with outstanding invoices will receive the feature initially.
- Duration: The initial rollout will run for 30 days before a go/no-go decision is made based on performance metrics.
- Segments & Ramp Gates: The feature will be expanded to another 20% of customers if the initial group shows a 15% reduction in where-is-my-invoice tickets and a 5% improvement in payment speed.

## Risk Management
- Detection: The system will log any errors or issues related to notification failures, and support team members will monitor these logs for potential problems.
- Fallback & Kill Switch: If the feature fails to notify customers, it will automatically revert to the previous behavior. A kill switch will be implemented to quickly disable the feature if it causes significant issues.
- Owner: The primary owner of this feature is a senior product manager.

## Ownership & Action
- Primary Owner: Senior Product Manager, Customer Experience Team.
- Decision Points: This PRD will be reviewed after the first 30 days of launch and again after 60 days to assess performance metrics.