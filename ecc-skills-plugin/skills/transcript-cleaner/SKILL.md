---
name: transcript-cleaner
description: Clean, compress and extract intelligence from raw transcripts. Use this skill whenever the user pastes or uploads a raw transcript, voice memo transcription, meeting recording transcript, or dictated notes. Trigger on any large block of conversational text that looks like speech-to-text output, or when the user says "clean this", "clean up this transcript", "transcript", "here's a recording", "I dictated this", "voice memo", or pastes text with verbal filler patterns (um, uh, like, you know, sort of, kind of, I mean, basically, right). Also trigger when the user uploads a .txt, .md, or .doc file that contains transcript-style content. If in doubt about whether pasted text is a transcript, treat it as one — undertriggering is worse than overtriggering here.
---

# Transcript Cleaner

## Purpose

Transform raw, verbose transcripts into clean, tight, usable text. Remove verbal filler, redundant emphasis, false starts, and conversational padding while preserving meaning, intent, tone, and critically — any commitments, admissions, quotes, or leverage-relevant statements made by counterparties.

## When This Skill Triggers

- User pastes a block of raw conversational text
- User uploads a transcript file
- User says "clean this up", "here's a transcript", "voice memo", "recording", "dictated"
- Text contains obvious speech-to-text patterns (filler words, repetition, incomplete sentences)

## Processing Pipeline

### Step 1: Detect and Classify

Read the input and determine:

1. **Source type**: Meeting (multi-speaker), voice memo (single speaker), dictated notes (instruction-style), phone call, or unknown
2. **Speaker count**: Single or multi-speaker
3. **Context**: Business negotiation, internal team, personal notes, legal/formal, general
4. **Length**: Short (<500 words), medium (500-2000), long (2000+)

### Step 2: Clean

Apply these transformations in order:

**REMOVE:**
- Filler words: um, uh, ah, like (when filler), you know, I mean, basically, essentially, sort of, kind of, right (when filler), yeah yeah, so so, look look
- False starts: "I was going to — what I mean is..."  → keep only the completed thought
- Redundant emphasis: "It's really really important, like genuinely critical" → "It's critical"
- Verbal padding: "The thing is that...", "What I'm trying to say is...", "At the end of the day...", "To be perfectly honest with you..."
- Conversational scaffolding: "So anyway...", "But yeah...", "I don't know, maybe..."
- Repeated points: When the same idea is stated 2-3 times with slight variation, keep the clearest version
- Backchannel: "mm-hmm", "yeah", "right right", "okay okay" (when not substantive agreement)
- Self-corrections where the correction is clear: "Tuesday — sorry, Wednesday" → "Wednesday"

**PRESERVE:**
- The speaker's actual meaning and intent
- Tone and register (don't make casual speech formal or vice versa)
- Technical terms, names, numbers, dates, amounts
- Conditional language that signals uncertainty ("I think", "probably", "maybe") — only remove when clearly just verbal filler, not genuine hedging
- Humour, sarcasm, personality — don't flatten the voice

**NEVER EDIT:**
- Direct quotes from counterparties in negotiations
- Commitments ("I'll do X by Y", "We can waive that", "We'll come back to you")
- Admissions ("We haven't done X", "That was our mistake", "The AC hasn't been serviced")
- Concessions ("We can be flexible on...", "I'll check with...", "We'd be open to...")
- Legal or contractual language
- Anything that could serve as normative leverage (their own stated values, promises, standards)

### Step 3: Structure

For **short transcripts** (<500 words):
- Output the cleaned text as a single block
- No headers needed

For **medium transcripts** (500-2000 words):
- Clean transcript with speaker labels if multi-speaker
- Brief summary (3-5 sentences) at the top

For **long transcripts** (2000+ words):
- Summary at top (5-8 sentences)
- Key decisions / action items (if any exist)
- Full cleaned transcript below
- If negotiation context is detected: separate section flagging commitments, admissions, and leverage points with the original verbatim language

### Step 4: Output Format

**Default output** (no special request from user):

```
## Summary
[Concise summary of what was discussed / dictated]

## Action Items
[Only if action items exist — omit section entirely if none]

## Key Quotes & Commitments
[Only if negotiation/business context detected — verbatim quotes preserved]

## Cleaned Transcript
[The cleaned text]
```

For short transcripts, skip the headers and just output the cleaned text directly.

**If user asks for "just clean it"**: Output only the cleaned transcript, no summary or extras.

**If user asks for summary only**: Output only the summary.

## Compression Targets

Aim for these reduction ratios as a guide (not a hard rule):

| Source Type | Typical Reduction |
|------------|------------------|
| Dictated notes | 15-25% shorter |
| Voice memo (single speaker) | 25-40% shorter |
| Meeting recording | 30-50% shorter |
| Casual conversation | 40-60% shorter |

If the cleaned version isn't materially shorter than the original, the cleaning wasn't aggressive enough. Re-read and cut harder.

## Quality Checks

Before outputting, verify:

- [ ] No meaning has been lost or altered
- [ ] No names, numbers, dates, or amounts changed
- [ ] Counterparty quotes/commitments preserved verbatim
- [ ] The cleaned version reads naturally, not like a robot edited it
- [ ] Speaker attribution is maintained in multi-speaker transcripts
- [ ] Tone matches the original speaker's voice

## Edge Cases

- **Heavily accented or garbled speech-to-text**: Flag unclear sections with [unclear] rather than guessing
- **Code-switching / mixed languages**: Preserve both languages, clean filler in both
- **Legal recordings**: Flag with warning that this may require professional transcription for legal use
- **Emotional content**: Preserve emotional markers that carry meaning ("I was furious" stays; "I was like, you know, really really upset about it" → "I was really upset about it")

## What This Skill Does NOT Do

- It does not fabricate content that wasn't in the transcript
- It does not rewrite in a different voice or style (formal/informal conversion)
- It does not translate
- It does not add analysis or opinion unless explicitly asked
- It does not change the speaker's position or soften/harden their statements
