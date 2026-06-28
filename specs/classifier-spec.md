# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions




**safe:**
```Routine maintenance and low-risk repairs. Most homeowners can complete these without specialized training or tools. | Patching drywall, painting, replacing a light bulb, unclogging a drain, tightening hardware, replacing weather stripping |
```

**caution:**
```
 Repairs where mistakes are costly, require some skill, or involve mild risk of injury. Doable for motivated homeowners, but worth careful consideration. | Replacing a faucet, resetting a GFCI outlet, replacing a toilet flapper, installing a ceiling fan, basic tile work |
```

**refuse:**
```
Repairs where an amateur mistake can cause fire, flooding, structural failure, injury, or death — or where local code requires a licensed professional. | Electrical panel work, gas line repair, structural modifications, main water line work, load-bearing wall removal, roof framing |
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
I want the llm to reason step by step. This output will be sent back in a json t output. If a question is ambigous the llm should output that the question is ambiguous. It should add clarifying questions and ask the user to rephrase the question
```

---

### Output formatoutp

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
The llm should return a structured json formant like this:
{
  "tier": "",
  "reasoning": "repairing electrical outlets is risky. If not done well it can lead to fires, shocks or death "
}


```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
You are a strict home repair JSON classification assistant tasked to classify user prompts into exactly one of these four labels:
- safe: Routine maintenance and low-risk repairs. Most homeowners can complete these without specialized training or tools.For example. Patching drywall, painting, replacing a light bulb, unclogging a drain, tightening hardware, replacing weather stripping
- caution: Repairs where mistakes are costly, require some skill, or involve mild risk of injury. Doable for motivated homeowners, but worth careful consideration. For example Replacing a faucet, resetting a GFCI outlet, replacing a toilet flapper, installing a ceiling fan, basic tile work 
- Refuse: Repairs where an amateur mistake can cause fire, flooding, structural failure, injury, or death — or where local code requires a licensed professional. Electrical panel work, gas line repair, structural modifications, main water line work, load-bearing wall removal, roof framing. Also classify questions that do not relate to home repair as refuse e.g write me a python script

```

**User message:**
```
How do i repair electrical outlets
```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
Caution repair tasks are risky but doable if the right precautions are taken. Refuse are very risky and should be done by a qualified professional. For example. I just spilled water on my electrical outlet. How do I dry it. (caution). the llm should recommend the homeowner to turn off the electricity first. How do i move my electrical outlet(refuse). Its risky and can cause fire. Should be done by a professional
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
The llm will be reprompted. This time with the output. Here is the prompt.

Return a json classification similar to this:
{
  "tier": "",
  "reasoning": "repairing electrical outlets is risky. If not done well it can lead to fires, shocks or death "
}


```
```
User: the response
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
The classification that surprised me is "can I replace an electrical outlet that stopped working" It was classified as refuse because I was not clear enough in my prompt regarding electrical work. The right tier should have been caution since it doesn't involve building out new electrical infranstructure

```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
I included the example on replacing electrical outlets in the caution examples. It fixed the replacing electrical s outlets being classified as refuse 
```
