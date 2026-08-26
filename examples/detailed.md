## Problem
We're solving the problem of customers on Growth and Enterprise plans being unable to track when their invoices are due, leading to unnecessary support tickets. Specifically, we're targeting the designated billing contact for these accounts.

## Goals & Non-Goals
| **Goal** | **Description** |
| --- | --- |
| Reduce where-is-my-invoice support tickets by 30% within 60 days of launch | The primary goal of this feature is to decrease the number of support tickets related to lost or forgotten invoices. |
| Reduce average days-to-payment for overdue invoices from 12 days to 7 days | A secondary goal is to speed up the payment process for overdue invoices. |
| **Non-Goal** | Do not send email and in-app notifications for invoices under $50, as this feature only targets accounts on Growth and Enterprise plans. |
| **Non-Goal** | Modify the invoicing or payment system itself, which is out of scope for this release. |

## Target users
The target user for this feature is the designated billing contact (a named role stored on the account record) for accounts on Growth and Enterprise plans only.

## Requirements
* Send email and in-app notifications when a customer invoice becomes exactly 7 days overdue.
* Only notify designated billing contacts for Growth and Enterprise plan accounts.
* Exclude Starter-plan accounts, as they do not use invoicing and are excluded by definition.

## Assumptions I made
* The "designated billing contact" role is accurately represented in the account record, with a valid email address or other notification method.
* The current average days-to-payment for overdue invoices is 12 days, providing a clear baseline for comparison.

## Success metrics
* Reduce where-is-my-invoice support tickets by 30% within 60 days of launch.
* Reduce average days-to-payment for overdue invoices from 12 days to 7 days.

## Open questions
None — all scope decisions were directly stated or resolved by the clarifying answers above.

## Risks
1. The designated billing contact role may not be accurately represented in the account record, leading to incorrect notifications.
2. The feature's notification system may not effectively reduce support tickets, potentially due to user behavior or other factors.
3. The invoicing and payment system itself may still experience issues that affect the success of this feature.