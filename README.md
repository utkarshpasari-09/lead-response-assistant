# Lead Response Assistant

## Overview

This project implements a Lead Response Assistant that helps convert incoming
customer enquiries into structured, professional draft replies.

The goal is not to automate decisions, but to assist teams in preparing safe,
consistent responses while avoiding assumptions or speculative claims.

---

## Problem Statement

Customer enquiries often arrive with incomplete information.
Responding too quickly can lead to incorrect assumptions or overpromising.

This system demonstrates how an AI-assisted workflow can:

- Understand the context of an enquiry
- Ask relevant clarification questions
- Suggest safe next steps
- Avoid hallucinated technical conclusions

---

## Workflow Design

The assistant follows a controlled reasoning pipeline:

Customer Message
↓
Prompt-Constrained Interpretation
↓
Clarification-First Response Strategy
↓
Safe Draft Generation (No Assumptions)
↓
Human Review Before Sending




The model is guided using strict system instructions that prevent:
- Diagnosing issues without inspection
- Making guarantees or commitments
- Adding information not present in the enquiry

---

## Reliability Approach

To ensure predictable and safe behaviour:

- Responses are clarification-first, not solution-first
- The assistant never claims certainty without evidence
- The system generates drafts, not automated replies
- Human review remains part of the workflow

This design reduces hallucination risk and keeps the assistant aligned with
real operational use cases.

---

## Example Use Cases

The assistant generalises across enquiry types such as:

- Property or maintenance concerns
- Inspection requests
- Early-stage customer enquiries
- Situations where information is incomplete

---

## Limitations

- Cannot validate physical conditions or technical causes
- Depends entirely on the information provided by the customer
- Designed as a drafting aid, not a diagnostic tool

---

## Future Improvements

With more time, the system could be extended to include:

- Retrieval-Augmented Generation (RAG) using internal knowledge bases
- Intent classification models for routing enquiries
- Audit logging for response traceability
- Feedback loops to refine tone and accuracy

---

## How to Run Locally

1. Clone the repository
git clone <repo-url>
cd lead-response-assistant


2. Create virtual environment

python -m venv venv
venv\Scripts\activate


3. Install dependencies

pip install -r requirements.txt



4. Add your API key to a `.env` file
GROQ_API_KEY=your_key_here

5. Run the application

streamlit run app.py

