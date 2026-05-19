# Ground Truth Isolation Pattern

Use this when evaluating generated figure code, benchmark examples, or audit outputs.

## Rule

Do not let the agent that produces a figure also see hidden expected answers for evaluation. Keep benchmark truth, expected audit labels, and pass/fail rubrics separate from the production prompt.

## Figure-Suite Application

- For chart generation tests, provide only data and task prompt to the producer.
- For audit tests, provide figure/caption artifacts without expected findings.
- Compare output to expected findings only in validator or external review.
- Do not leak intended fixes into forward-test prompts.

## Why

Scientific figure quality depends on whether the agent detects unsupported claims, missing uncertainty, bad scales, and reproducibility gaps independently.
