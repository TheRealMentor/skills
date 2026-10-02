---
name: ste-writing
description: Rewrite or write text so it is clear, short, and hard to misread, using the principles of Simplified Technical English (ASD-STE100). Use this skill whenever the user wants to simplify, clarify, tighten, "unslop", de-jargon, or make text easier to understand, or when they paste a draft (README, PR description, Slack message, email, spec, runbook, docs, UI copy, prompt or agent instructions) and ask for a rewrite, review, or "make this better". Also use it when writing documentation or instructions from scratch for readers who may not be native English speakers, and when text sounds bloated, vague, or AI-generated. Trigger even if the user never says "STE" or "simple English".
---

# STE Writing

Make text easy to understand on the first read. This skill borrows the core ideas of ASD-STE100 (Simplified Technical English) and adapts them for everyday professional writing. It is not a certification checker. The goal is a reader who gets the point fast and cannot misread it.

## Why this works better than a "slop" ban list

Lists of banned phrases ("delve", "tapestry", "in today's fast-paced world") fix symptoms. Text stays hard to read because of structure: long sentences, vague subjects, hidden actors, stacked ideas. STE fixes structure, so apply the structural rules first and only then clean up phrases.

## Workflow

1. **Find the job of the text.** Who reads it, and what must they know or do after reading? If this is unclear and cannot be guessed, ask one short question. Otherwise decide and say what you assumed.
2. **Pick a mode.** Default to **standard**. Use **strict** when the user says "STE", "strict", or the text is a procedure (steps, runbook, install guide, safety text). Use **light** for casual text (Slack, chat, personal email) where tone matters more than rule-following.
3. **Rewrite** with the rules below. Keep every fact, number, name, and caveat. Never invent facts to fill a gap. If the source is ambiguous, keep the ambiguity visible with a short `[check: ...]` note.
4. **Check** with `scripts/ste_check.py` when you can run it. Fix what it flags, but use judgment: a flag is a hint, not a verdict.
5. **Deliver** the rewritten text first. Then add at most 3 short bullets on the main changes, only if the user would learn something. Do not lecture.

## The rules

### Sentences
- One idea per sentence. Standard mode: aim for 20 words or fewer, hard cap 25. Strict mode: 20 for procedures, 25 for descriptions.
- One topic per paragraph. Start the paragraph with the point.
- If a sentence has "and", "which", or "while" joining two separate ideas, split it.
- Put the most important information first. Conditions go before the action: "If the build fails, run `make clean`."
- Do not make the text choppy. Short does not mean a row of 6-word sentences. Keep short connectors ("so", "because", "then", "but") where they show how ideas relate, and keep an average of about 10 to 18 words per sentence in prose. Strict mode accepts choppier text. Standard and light modes should still read like a person wrote them.

### Verbs and voice
- Use the active voice. Name who or what acts: "The service retries the request", not "The request is retried".
- Use the simple tenses: present, past, future. Avoid perfect and progressive forms ("has been running", "is being processed") unless time matters.
- Write instructions as commands: "Open the file." Not "You should open the file" or "The file should be opened".
- Replace noun stacks and nominalizations with verbs: "make a decision" → "decide", "perform validation of" → "validate", "provide an explanation" → "explain".
- Avoid phrasal verbs and idioms when a plain verb exists ("set up" as a noun vs verb is fine; "touch base", "circle back", "bite the bullet" are not).

### Words
- One word, one meaning, used the same way every time. Do not rotate synonyms for style ("user", "customer", "client", "end user" for the same person). Pick one and keep it.
- Prefer the short, common word: "use" not "utilize", "start" not "commence", "help" not "facilitate", "about" not "approximately" when precision is not needed. See `references/plain-swaps.md`.
- Keep technical names exactly as they are (function names, product names, error codes). Define a term the first time it appears if the reader may not know it.
- Do not drop small words (articles, "that") to save space. Compressed text ("Verify config then restart svc") is harder to read for non-native readers and for translation tools.
- Say "can" for ability, "must" for a requirement, "should" for advice. Avoid "may" (permission or possibility? pick one) and "might".

### Structure
- Use a numbered list for steps that must happen in order. Use a short bullet list for parallel items. Use prose for reasoning.
- Put warnings and cautions before the step they apply to, and make them stand out.
- Use a table only to compare items across the same attributes.
- Give numbers, names, and dates instead of vague quantities ("a few", "soon", "significant").

### Tone (this part is what "unslop" tried to do)
- Cut filler openers and closers ("I hope this finds you well", "In conclusion", "It's important to note that").
- Cut empty intensifiers and hedges ("very", "really", "essentially", "basically", "arguably") unless they carry real meaning.
- Do not add enthusiasm, metaphors, or rhetorical questions that the source did not have.
- Keep the author's voice where it matters. A friendly Slack message should still sound friendly after the rewrite, only clearer.

## Mode details

| Mode | Sentence cap | Contractions | Tone changes | Use for |
|---|---|---|---|---|
| light | 25 words (soft) | keep | minimal | Slack, chat, casual email |
| standard | 25 words | allowed | trim filler | PRs, docs, specs, most email |
| strict | 20 words (procedures) | avoid | neutral and direct | runbooks, install steps, safety text, text for translation |

## Edge cases

- **Text with code, logs, or quotes:** leave them unchanged. Rewrite only the prose around them.
- **Text that is already clear:** say so and change little. Do not rewrite for the sake of rewriting.
- **Legal, medical, or contract text:** do not change meaning or defined terms. Offer clearer wording as a suggestion and flag clauses where simplification could change legal effect.
- **Non-English text:** apply the same ideas (short sentences, one idea each, plain words) but do not use the English word lists.
- **Writing from scratch:** draft with the rules from the start, then run the check.

## Self-check before delivering

- Did every fact, number, and name survive?
- Can a reader who is tired and reads English as a second language follow each sentence once?
- Is each sentence's actor clear?
- Did I use the same word for the same thing throughout?
- Did I add anything the source did not say?

## Bundled files

- `scripts/ste_check.py`: reports long sentences, likely passive voice, perfect and progressive tenses, flagged words with plain alternatives, filler phrases, and stacked ideas. Run: `python scripts/ste_check.py file.txt` or pipe text in. Add `--json` for machine-readable output and `--max-words N` to change the cap.
- `references/plain-swaps.md`: plain-word replacements and filler phrases. Read it when rewriting a long or wordy text.
