# Journal Style Status Cases

## Current Official Guidance In Task

Input: user provides official current guideline excerpt and date.

Expected: `STYLE_STATUS: VERIFIED` only for requirements supported by the supplied guidance.

## Stored Estimate Only

Input: user asks for Nature-inspired layout without providing guidelines.

Expected: `STYLE_STATUS: ESTIMATED`; use stored estimate language.

## No Profile Available

Input: obscure journal with no supplied requirements.

Expected: `STYLE_STATUS: UNVERIFIED`; apply universal high-impact fallback.

## Forbidden Language

Input: `STYLE_STATUS: ESTIMATED` and generated text says "journal-compliant".

Expected: fail `audit_journal_profile.py`.
