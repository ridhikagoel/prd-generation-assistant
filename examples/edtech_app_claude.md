## Problem
- **Core Problem:** Job seekers preparing for role-specific interviews lack personalized, adaptive practice that keeps them engaged through their prep journey.
- **Working Hypothesis:** AI-generated interview questions that adapt to the learner's performance will drive higher engagement and retention than static interview prep materials.
- **Strategy Fit:** Not stated — if this is part of a broader edtech or job-placement strategy, that context was not provided.

## Goals & Non-Goals

| **Goals** | **Non-Goals** |
|-----------|---------------|
| Drive weekly active usage and 7-day/30-day retention through adaptive interview prep | Optimize for job offer outcomes in the MVP (tracked as signal, not the tuning target) |
| Support 10–15 high-demand job roles with AI-generated questions and study materials | Support open-ended generation for any role or subject a user types in |
| Adapt question difficulty based on learner performance over time | Provide live human coaching or mock interviews with real people |
| Ship on iOS and Android | Ship a web client in the MVP |
| | Build peer/community features or employer-side B2B functionality |

## Target users
Job seekers preparing for interviews in high-demand roles — specifically new graduates entering the workforce and working professionals switching roles. Both segments need structured interview practice for roles they are targeting (e.g. software engineer, data analyst, product manager, sales development rep).

## Requirements
- Support 10–15 curated high-demand job roles at launch, selected based on job market demand data.
- Generate mock interview questions with model answers for each supported role.
- Provide supporting study materials for each role: study notes, flashcards, and practice questions covering fundamentals the role screens on.
- Track learner performance on practice questions and adapt the difficulty of generated interview questions accordingly (easier if struggling, harder if performing well).
- Deliver the experience on iOS and Android mobile apps; no web client in MVP.
- Do not generate interview prep content for roles outside the curated set in the MVP.
- Track weekly active users, session frequency, 7-day retention, and 30-day retention as primary engagement metrics.
- Track learning outcome signals (offers received, interview success self-reports) as secondary data, not optimization targets.

## Behavior Contract

**GOOD examples:**

1. **Input:** User selects "Software Engineer (Backend)" role, marks themselves as "early career," completes 3 easy algorithm practice questions with 2/3 correct.  
   **Output:** Next session surfaces a medium-difficulty mock interview question on API design with a model answer and a supporting study note on REST vs. GraphQL tradeoffs.  
   **Why good:** Adapts difficulty upward appropriately; links interview question to a relevant fundamental the role screens on.

2. **Input:** User selects "Product Manager" role, struggles on 4 consecutive case-study practice questions (scores below 50% on rubric).  
   **Output:** App surfaces an easier behavioral interview question ("Tell me about a time you prioritized features") with a structured model answer, plus a flashcard deck on prioritization frameworks (RICE, MoSCoW).  
   **Why good:** Adapts difficulty downward to prevent discouragement; offers supporting material to rebuild fundamentals before re-attempting harder content.

3. **Input:** User preparing for "Data Analyst" role completes a mock interview question on SQL joins with high accuracy, then requests more practice.  
   **Output:** App generates a harder SQL mock question involving window functions, with a model answer and a study note linking to when window functions are preferred over joins.  
   **Why good:** Progression respects demonstrated mastery; generated content stays within the role's scope.

**BAD examples:**

1. **Input:** User selects "Sales Development Rep" role and completes 5 practice questions with 100% accuracy.  
   **Output:** App continues surfacing easy cold-calling questions identical in difficulty to prior sessions.  
   **Why bad:** Fails to adapt difficulty upward despite strong performance; risks boring the user and hurting retention.

2. **Input:** User preparing for "Software Engineer (Frontend)" role asks for React interview questions.  
   **Output:** App generates a question about Vue.js lifecycle hooks with a model answer referencing Vue documentation.  
   **Why bad:** Content mismatch — user requested React for a frontend engineering role, but app generated content for a different framework, breaking trust.

3. **Input:** User selects "Product Manager" role, has completed zero practice questions so far (first session).  
   **Output:** App immediately surfaces an extremely difficult case-study question requiring market-sizing and P&L analysis with minimal scaffolding.  
   **Why bad:** No performance data exists yet to justify hard difficulty; risks overwhelming a new user before they're calibrated, damaging early retention.

**REJECT examples:**

1. **Input:** User types "Help me prepare for an interview at [Specific Company Name]" and requests insider questions from that company's interview loop.  
   **Output:** App should refuse and display: "I can't provide company-specific interview questions or insider information. I can help you prepare for [Role Type] interviews in general."  
   **Why reject:** Legal and ethical risk — cannot scrape or simulate proprietary interview content from specific employers.

2. **Input:** User requests interview prep for "Cryptocurrency Day Trader" or another role outside the curated MVP set of 10–15 roles.  
   **Output:** App should refuse and display: "This role isn't supported yet. Supported roles: [list]. More roles coming soon."  
   **Why reject:** Out of scope for MVP — open-ended role generation is explicitly excluded; attempting it anyway would produce low-quality results and set wrong expectations.

## Guardrails
- **No hallucinated company-specific content:** The app must never generate questions it claims are "used by [Company X]" or simulate proprietary interview processes from named employers — all content is role-generic.
- **Difficulty floor and ceiling:** Adaptive difficulty must respect minimum and maximum bounds appropriate for the role — never generate a question so trivial it's insulting, or so advanced it assumes expertise the target user (job seeker, not expert) wouldn't have.
- **Role boundaries enforced:** If a user requests content for a role outside the curated MVP set of 10–15, the app must explicitly refuse and surface the list of supported roles, rather than attempting to generate content it wasn't designed for.
- **Performance tracking consent:** Any data used to adapt question difficulty (practice question scores, session behavior) must be tied to the user's account with clear notice that performance tracking drives personalization — no silent behavioral profiling.

## Assumptions I made
- **Adaptation algorithm not specified:** The requirement states difficulty "adapts based on performance" but does not define the threshold (e.g., how many questions wrong triggers easier content, or how much easier). I assume a reasonable implementation would use a rolling window of recent performance rather than a single-question trigger, but the exact logic is not defined here.
- **Study content sourcing:** The feature describes "supporting study notes, flashcards, and practice questions" but does not specify whether these are AI-generated, human-authored, or pulled from a third-party content library. I assume they are AI-generated to match the stated AI-personalization capability, but this is not confirmed.
- **Role selection criteria:** "Curated set of 10–15 high-demand job roles" does not define the selection process — I assume this is based on job-market demand data (LinkedIn, BLS, Glassdoor trending roles), but the specific roles beyond the four examples given (SWE, data analyst, PM, SDR) are not listed.
- **Rollout plan:** No rollout percentage, duration, or ramp gates were specified — the plan below is a standard conservative mobile app rollout, not a product decision from the feature idea.

## Open questions
- What is the acceptable latency for generating a new interview question when the user requests one? (Affects model choice and caching strategy.)
- Should the app allow users to manually override the adaptive difficulty (e.g., "I want hard questions even though I'm struggling"), or is difficulty fully automated?
- How do we define "performing well" vs. "struggling" concretely — what score threshold on practice questions triggers a difficulty shift, and over how many questions?
- Do we track whether users report receiving job offers and attribute that to app usage, or only passively collect self-reported outcome data without in-app prompts?

## Success metrics
- **Offline Golden Set:** A labeled dataset of 50–100 interview questions per role (500–1,500 questions total across 10–15 roles), each human-reviewed for relevance, appropriate difficulty level, and alignment with real interview practices for that role. Model-generated questions would be spot-checked against this set before launch.
- **Human Review:** Before launch, a hiring manager or interview coach for each supported role reviews a sample of 10 generated questions and model answers per role, checking for accuracy, realism, and absence of biased or inappropriate content. Post-launch, support tickets and user-reported question quality issues are reviewed weekly.
- **Online Metrics:**
  - **7-day retention ≥ 40%** (percentage of new users who return within 7 days of first session). Industry benchmark for interview-prep apps is 30–40%; we need at least 40% to validate engagement.
  - **30-day retention ≥ 20%** (percentage of new users still active 30 days after first session). Typical interview prep cycles are 2–6 weeks, so 20% sustained usage indicates the adaptive content is keeping learners engaged through their prep window.
  - **Weekly Active Users (WAU) / Monthly Active Users (MAU) ratio ≥ 0.5** (measures session frequency — how many monthly users come back each week). A ratio below 0.5 would indicate one-and-done usage rather than repeated practice.
  - **Minimum detectable effect:** With typical mobile app sample sizes (10K+ users in first month), a 5-percentage-point shift in 7-day retention or a 0.05 shift in WAU/MAU is statistically significant and actionable; smaller changes are likely noise.

## Rollout Plan
- **Exposure:** Launch to 10% of new app installs (iOS and Android combined) in the first week, with the remaining 90% seeing a wait-list or feature-unavailable screen.
- **Duration:** Run the 10% exposure for 7 days to capture one full week of 7-day retention data before deciding whether to expand.
- **Segments & Ramp Gates:**
  - If 7-day retention in the test group is ≥ 40% and no critical bugs or content-quality issues surface in support tickets, expand to 50% of new installs.
  - After 14 days total (7 days at 50%), if 7-day retention holds ≥ 40% and WAU/MAU ≥ 0.5, expand to 100%.
  - If 7-day retention falls below 35% at any stage, pause expansion and investigate (content quality, onboarding friction, or performance issues).

## Risk Management
- **Detection:** Monitor 7-day retention, WAU/MAU ratio, and session length daily via the app analytics dashboard (e.g., Mixpanel, Amplitude). Set up alerts for 7-day retention dropping below 35% or WAU/MAU below 0.4 for 3 consecutive days. Review user-reported question quality issues in support tickets weekly; if more than 5% of active users report "irrelevant" or "incorrect" questions in a given week, escalate immediately.
- **Fallback & Kill Switch:** The feature can be disabled via a feature flag in under 5 minutes, reverting users to a static question bank (pre-generated, human-reviewed questions for each role) with no adaptive difficulty. This fallback content must be prepared and tested before launch. If the AI generation endpoint fails or times out, the app automatically serves static content and logs the failure for engineering review.
- **Owner:** Mobile product lead (or named PM if available) is accountable for monitoring metrics and deciding whether to pause, ramp, or kill the feature. Engineering oncall is paged for generation-service outages or >5-second question-generation latency.

## Ownership & Action
- **Primary Owner:** Mobile product team lead (or the PM specifically assigned to job-seeker retention initiatives, if org structure defines one).
- **Decision Points:**
  - **Day 7:** Review 7-day retention data from the initial 10% rollout. Decision: expand to 50%, hold at 10% for more data, or roll back.
  - **Day 14:** Review 7-day retention and WAU/MAU from the 50% cohort. Decision: expand to 100% or pause.
  - **Day 30:** Review 30-day retention and any secondary learning-outcome signals (self-reported offers, interview success). Decision: declare MVP success and plan next role expansion, or iterate on content quality and re-test.
