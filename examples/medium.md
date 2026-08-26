## Problem
Notify customers by email when their invoice is 7 days overdue, so they pay faster and support gets fewer where-is-my-invoice tickets.

## Goals & Non-Goals
| **Goal** | **Description** |
| --- | --- |
| Reduce where-is-my-invoice tickets | Decrease the number of support requests for missing invoices. |
| Improve payment speed | Encourage customers to pay their invoices on time. |

| **Non-Goal** | **Description** |
| --- | --- |
| Notify customers about every invoice status update | This feature is focused on overdue invoices only. |
| Automate email notifications for all customer interactions | The goal is to reduce where-is-my-invoice tickets, not automate all customer emails. |

## Target users
Customer with an outstanding invoice that can become overdue.

## Requirements
* Send a notification email to customers 7 days before their invoice is due.
* Include a clear subject line and body with relevant information (invoice number, amount, etc.).
* Allow customers to respond to the email or click a link to view their invoice online.

## Assumptions I made
* The target user is a customer who has an outstanding invoice that can become overdue.
* Success will be measured by reducing where-is-my-invoice tickets and improving payment speed.
* This feature should not apply to invoices with specific types (e.g., prepaid or paid in full) or scenarios (e.g., invoices sent for goods already delivered).

## Success metrics
1. Reduction in where-is-my-invoice tickets by 20% within the next 6 weeks.
2. Increase in on-time payments by 15% within the next 3 months.

## Open questions
* Are there any specific types of invoices or scenarios for which this feature should not apply?
* How will we measure success beyond just reducing where-is-my-invoice tickets and improving payment speed?

## Risks
1. Customers may mark emails as spam, leading to reduced notification effectiveness.
2. Over-reliance on email notifications could lead to decreased phone or in-person support usage.
3. Technical issues with email delivery or formatting could impact the feature's success.