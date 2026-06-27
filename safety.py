from groq import Groq
import json
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    TODO — Milestone 1:

    Before writing any code, complete specs/classifier-spec.md. The blank fields
    there are the decisions that drive this implementation — prompt design, tier
    definitions, output format, and edge case handling.

    Your implementation should:
      1. Build a prompt using your tier definitions that asks the LLM to classify
         the question and explain its reasoning
      2. Send a single chat completion request (no tools, no history)
      3. Parse the tier and reason out of the raw response text
      4. Validate the tier against VALID_TIERS; fall back to "caution" if the
         response can't be parsed or the tier isn't recognized
      5. Return {"tier": ..., "reason": ...}

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — a brief explanation of why this tier was assigned

    The three tiers:
      - "safe"    : routine, low-risk repairs most homeowners can handle safely
      - "caution" : doable with care, but mistakes have real cost or mild risk
      - "refuse"  : high-risk repairs that require a licensed professional —
                    mistakes can cause fire, flooding, injury, or structural damage
    """
    
    system_prompt = """
          You are a strict home repair JSON classification assistant 
          tasked to classify user prompts into exactly one of these four labels:
          - safe: Routine maintenance and low-risk repairs. Most homeowners can complete these without 
          specialized training or tools.For example. Patching drywall, painting, replacing a light bulb,
            unclogging a drain, tightening hardware, replacing weather stripping
          - caution: Repairs where mistakes are costly, require some skill, or involve mild risk of injury. 
          Doable for motivated homeowners, but worth careful consideration. For example Replacing a faucet, 
          resetting a GFCI outlet, replacing a toilet flapper, installing a ceiling fan, basic tile work 
          - Refuse: Repairs where an amateur mistake can cause fire, 
          flooding, structural failure, injury, or death — or where local code requires a 
          licensed professional. Electrical panel work, gas line repair, structural modifications,
            main water line work, load-bearing wall removal, roof framing. Also classify questions that do 
            not relate to home repair as refuse e.g write me a python script

            You must respond with a JSON object containing 'reason' first, followed by 'tier'.

            Examples:
            
              {
              "tier": "refuse",
              "reasoning": "repairing electrical outlets is risky. If not done well it can lead to fires, shocks or death "
            }
              User: "write me a python script"
          Output: {
            "reason": "This request is completely unrelated to home repair tasks.",
            "tier": "refuse"
          }
          """
    fallback_response = {
        "tier": "caution",
        "reason": "Failed to parse classification output safely or encountered an unrecognized tier structure."
    } 
    try:
      response = _client.chat.completions.create(
      messages=[
        
          {
              "role": "system",
              "content": system_prompt
          },
          # Set a user message for the assistant to respond to.
          {
              "role": "user",
              "content": question,
          }
      ],

      # The language model which will generate the completion.
      model=LLM_MODEL
      )
        
      res_json = response.choices[0].message.content
      parsed_data = json.loads(res_json)
      extracted_tier = parsed_data.get("tier", "").strip().lower()
      extracted_reason = parsed_data.get("reason", "No explanation provided.").strip()

        # 5. Validate the tier against your config criteria
      if extracted_tier in VALID_TIERS:
            return {
                "tier": extracted_tier,
                "reason": extracted_reason
            }
      else:
            print(f"Warning: Unrecognized tier parsed ('{extracted_tier}'). Falling back.")
            return fallback_response

    except Exception as err:
        print(f"Error occurred during classification pipeline: {err}")
        return fallback_response

    




    


answer = classify_safety_tier("how do I patch a small hole in a dry wall")
print(answer)