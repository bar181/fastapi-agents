import os
import uvicorn
from fastapi import FastAPI, Request, Response
import requests

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT", "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/o3-mini-high")

if not GEMINI_API_KEY and not OPENROUTER_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY or OPENROUTER_API_KEY in environment.")

# Interfaces/structures in Python
class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

class Tool:
    def __init__(self, name: str, description: str, run_func):
        self.name = name
        self.description = description
        self.run = run_func

# Tools
def calculator_run(expression: str) -> str:
    try:
        # Guard against unsafe characters
        if not all(ch in "0123456789.+-*/() " for ch in expression):
            return "Invalid expression"
        result = eval(expression)
        return str(result)
    except Exception as exc:
        return f"Error: {exc}"

tools = [
    Tool(
        name="Calculator",
        description="Performs arithmetic calculations. Usage: Calculator[expression]",
        run_func=calculator_run
    ),
    # Add more tools here if needed
]

# System prompt
tool_descriptions = "\n".join(f"{t.name}: {t.description}" for t in tools)
system_prompt = (
    "You are a smart assistant with access to these tools:\n"
    f"{tool_descriptions}\n\n"
    "When answering user, you may use tools to gather info or calculate results.\n"
    "Follow this format exactly:\n"
    "Thought: <reasoning>\n"
    "Action: <ToolName>[<input>]\n"
    "Observation: <tool result>\n"
    "...(repeat as needed)...\n"
    "Thought: <final reasoning>\n"
    "Answer: <final answer>\n\n"
    "Only one action at a time, wait for observation before continuing.\n"
    "If answer is known or enough info is gathered, output final Answer.\n"
)

# Case databases
medical_cases = [
    {"symptoms": ["fever", "cough", "headache"], "diagnosis": "Flu"},
    {"symptoms": ["fever", "cough"], "diagnosis": "Common Cold"},
    {"symptoms": ["fever", "rash"], "diagnosis": "Measles"},
    {"symptoms": ["cough", "shortness of breath"], "diagnosis": "Asthma"},
]

legal_cases = [
    {
        "caseType": "contract",
        "signed": False,
        "outcome": "Contract declared void (no signature)",
    },
    {
        "caseType": "contract",
        "signed": True,
        "outcome": "Contract enforced by court",
    },
    {
        "caseType": "criminal",
        "evidence": "weak",
        "outcome": "Not guilty verdict",
    },
    {
        "caseType": "criminal",
        "evidence": "strong",
        "outcome": "Guilty verdict",
    },
    {
        "caseType": "civil",
        "outcome": "Case settled out of court",
    },
]

# Agent class
class Agent:
    def apply_deductive(self, domain: str, user_input: dict):
        if domain == "financial":
            data = user_input.get("data", {})
            exp_return = data.get("expectedReturn")
            risk_level = data.get("riskLevel")
            if exp_return is not None and risk_level is not None:
                if exp_return > 0.05 and risk_level == "low":
                    return "Decision: Invest (high return, low risk)"
                if exp_return < 0 or risk_level == "high":
                    return "Decision: Do Not Invest (insufficient return or high risk)"
                return "Decision: Hold (moderate return/risk)"
            return None

        if domain == "medical":
            symptoms = user_input.get("symptoms", [])
            tests = user_input.get("testResults", {})
            if "fever" in symptoms and "rash" in symptoms:
                return "Diagnosis: Measles (fever + rash)"
            if (
                "fever" in symptoms
                and "cough" in symptoms
                and tests.get("chestXRay") == "patchy"
            ):
                return "Diagnosis: Pneumonia (fever, cough, patchy x-ray)"
            if "chest pain" in symptoms and "shortness of breath" in symptoms:
                return "Diagnosis: Possible Heart Attack (chest pain + breathing issues)"
            return None

        if domain == "legal":
            case_type = user_input.get("caseType")
            if case_type == "contract":
                if user_input.get("signed") is False:
                    return "Legal Outcome: Contract invalid (no signature)"
                if user_input.get("signed") is True and user_input.get("consideration") != False:
                    return "Legal Outcome: Contract likely enforceable"
            if case_type == "criminal":
                if user_input.get("evidence") == "strong":
                    return "Legal Outcome: Likely conviction"
                if user_input.get("evidence") == "weak":
                    return "Legal Outcome: Likely acquittal"
            return None

        return None

    def apply_inductive(self, domain: str, user_input: dict):
        if domain == "financial":
            data = user_input.get("data", {})
            exp_return = data.get("expectedReturn")
            risk_level = data.get("riskLevel")
            if exp_return is None and isinstance(data.get("pastReturns"), list):
                returns = data["pastReturns"]
                if returns:
                    exp_return = sum(returns) / len(returns)
            if risk_level is None and isinstance(data.get("pastReturns"), list):
                returns = data["pastReturns"]
                if len(returns) > 1:
                    mean = exp_return if exp_return is not None else sum(returns) / len(returns)
                    variance = sum((r - mean) ** 2 for r in returns) / len(returns)
                    std_dev = variance ** 0.5
                    if std_dev > 0.1:
                        risk_level = "high"
                    elif std_dev < 0.05:
                        risk_level = "low"
                    else:
                        risk_level = "medium"
            if exp_return is not None and risk_level is not None:
                decision = self.apply_deductive(domain, {"data": {
                    "expectedReturn": exp_return,
                    "riskLevel": risk_level
                }})
                if decision:
                    return decision
            return {
                "estimatedReturn": exp_return,
                "estimatedRisk": risk_level,
                "note": "Inductive estimates (no direct rule applied)",
            }

        if domain == "medical":
            symptoms = user_input.get("symptoms", [])
            best_match = None
            for case_data in medical_cases:
                match_count = sum(1 for s in case_data["symptoms"] if s in symptoms)
                if match_count > 0 and (not best_match or match_count > best_match["matchCount"]):
                    best_match = {
                        "diagnosis": case_data["diagnosis"],
                        "matchCount": match_count,
                    }
            if best_match:
                return f"Possible Diagnosis: {best_match['diagnosis']} (similar cases)"
            return "Diagnosis unclear (no close match)"

        if domain == "legal":
            case_type = user_input.get("caseType")
            for rec in legal_cases:
                if rec.get("caseType") == case_type:
                    matches_signed = (
                        "signed" in rec
                        and rec["signed"] == user_input.get("signed")
                    )
                    matches_evidence = (
                        "evidence" in rec
                        and rec["evidence"] == user_input.get("evidence")
                    )
                    # catch records with no 'signed' or 'evidence'
                    if matches_signed or matches_evidence or (
                        "signed" not in rec and "evidence" not in rec
                    ):
                        return f"Likely Outcome: {rec['outcome']} (similar past case)"
            return "Outcome unclear (no similar cases)"

        return None

    def process_query(self, domain: str, user_input: dict):
        reasoning_type = user_input.get("reasoningType", "both")

        if reasoning_type == "deductive":
            ded = self.apply_deductive(domain, user_input)
            return {
                "result": ded or "No deductive conclusion possible with given info."
            }

        if reasoning_type == "inductive":
            ind = self.apply_inductive(domain, user_input)
            return {
                "result": ind or "No inductive conclusion possible with given info."
            }

        # Default: both
        ded = self.apply_deductive(domain, user_input)
        if ded:
            return {"result": ded, "reasoningUsed": "deductive"}
        ind = self.apply_inductive(domain, user_input)
        return {"result": ind, "reasoningUsed": "inductive"}
# LLM interaction via Gemini
def call_gemini(messages: list[ChatMessage]) -> str:
    if not GEMINI_API_KEY:
        return "Gemini API key not configured."
    try:
        url = GEMINI_ENDPOINT + f"?key={GEMINI_API_KEY}"
        contents = [{"role": m.role, "parts": [{"text": m.content}]} for m in messages]
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.0,
                "topP": 1,
                "topK": 32,
                "maxOutputTokens": 2048,
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
        }
        headers = {"Content-Type": "application/json"}

        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code != 200:
            return f"Gemini API error: {resp.status_code} - {resp.text}"

        data = resp.json()
        candidates = data.get("candidates", [])
        if not candidates:
            return "Gemini API returned no candidates."

        content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        if not isinstance(content, str):
            return "Gemini API response missing or invalid content."

        return content
    except Exception as e:
        return f"Gemini API error: {e}"

# LLM interaction via OpenRouter
def call_openrouter(messages: list[ChatMessage]) -> str:
    if not OPENROUTER_API_KEY:
        return "OpenRouter API key not configured."
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stop": ["Observation:"],
            "temperature": 0.0,
        }
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code != 200:
            return f"OpenRouter API error: {resp.status_code} - {resp.text}"
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content")
        if not isinstance(content, str):
            return "LLM response missing or invalid."
        return content
    except Exception as e:
        return f"OpenRouter API error: {e}"

async def run_agent(query: str) -> str:
    messages = [
        ChatMessage("system", system_prompt),
        ChatMessage("user", query),
    ]

    # If query is JSON with domain key, run agentic reasoning first
    domain = None
    try:
        parsed = eval(query)  # or json.loads(query), but ensuring minimal overhead
        if isinstance(parsed, dict) and "domain" in parsed:
            domain = parsed["domain"]
    except Exception:
        pass

    if domain:
        parsed_input = eval(query)  # or json.loads(query)
        ag = Agent()
        preliminary = ag.process_query(domain, parsed_input)
        sys_msg = (
            "Preliminary agentic reasoning result: "
            f"{preliminary}"
        )
        messages.append(ChatMessage("system", sys_msg))

    # ReAct loop
    for _ in range(10):
        if GEMINI_API_KEY:
            assistant_reply = call_gemini(messages)
        elif OPENROUTER_API_KEY:
            assistant_reply = call_openrouter(messages)
        else:
            return "No API key configured."
        # Must be sync call inside async - in real usage, you'd use an async library or thread
        # For demonstration, it's simpler to keep it sync in this example

        reply = assistant_reply if isinstance(assistant_reply, str) else ""
        messages.append(ChatMessage("assistant", reply))

        # Check if final answer is found
        answer_match = None
        import re
        match = re.search(r"Answer:\s*(.*)$", reply)
        if match:
            answer_match = match.group(1).strip()

        if answer_match:
            return answer_match

        # Check for action
        action_match = re.search(r"Action:\s*([^\[]+)\[([^\]]+)\]", reply)
        if action_match:
            tool_name = action_match.group(1).strip()
            tool_input = action_match.group(2).strip()

            found_tool = None
            for t in tools:
                if t.name.lower() == tool_name.lower():
                    found_tool = t
                    break

            if not found_tool:
                obs = f'Tool "{tool_name}" not found'
            else:
                try:
                    obs = found_tool.run(tool_input)
                except Exception as exc:
                    obs = f"Error: {exc}"

            messages.append(ChatMessage("system", f"Observation: {obs}"))
            continue

        return reply.strip()

    raise ValueError("No final answer produced within step limit.")
