"""
TIMESHARE EXIT — Free Exit Engine
Helps people get out of timeshares using information that should always have been free.

Exit companies charge $4,000–$15,000 to do things you can do yourself.
This app gives you everything they know — for free.

AIIT-THRESI Research Initiative | 2026
Rhet Dillard Wike | Council Hill, Oklahoma

---

The timeshare industry deploys decoherence deliberately.
High-pressure 90-minute sales presentations. Sleep deprivation from travel.
Manufactured scarcity. Emotional manipulation. Documents signed before
the buyer is coherent enough to read them.

Then, when the buyer wants out, a second predator class emerges — exit companies
charging thousands of dollars to provide information that is public law.

Every person trapped in a timeshare is paying maintenance fees on something
they can't use, can't sell, and didn't fully understand when they signed.

The information needed to exit is free. The law is public. The letters are simple.
The deed-back programs exist and are not advertised on purpose.

This app makes the exit free.

— AIIT-THRESI | April 1, 2026
"""

from flask import Flask, render_template, jsonify, request, Response, stream_with_context
from datetime import datetime, timedelta
import json
import os
import anthropic

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# ─── State data (cached) ─────────────────────────────────────────────────────

_STATES = None

def get_states():
    global _STATES
    if _STATES is None:
        with open(os.path.join(DATA_DIR, 'states.json')) as f:
            _STATES = json.load(f)
    return _STATES

# ─── Deed-back contact info ───────────────────────────────────────────────────

DEEDBACK_PROGRAMS = {
    "wyndham": {
        "name": "Wyndham Destinations / Club Wyndham",
        "program": "Certified Exit Program",
        "phone": "1-855-812-5046",
        "url": "https://www.wyndhamvacations.com/owner-services",
        "notes": "Most accessible deed-back program in the industry. Requires: loan paid in full, maintenance fees current. Call and ask specifically for the Certified Exit Program.",
        "eligibility": ["Loan paid in full", "All maintenance fees current", "Account in good standing"]
    },
    "hilton": {
        "name": "Hilton Grand Vacations",
        "program": "HGV Transitions Program",
        "phone": "1-800-448-2736",
        "url": "https://www.hiltongrandvacations.com/en/owner",
        "notes": "Formal program for owners experiencing hardship or life changes. Ask for 'HGV Transitions' when you call.",
        "eligibility": ["Loan paid in full", "Fees current", "Financial hardship or major life change often required"]
    },
    "marriott": {
        "name": "Marriott Vacations Worldwide",
        "program": "Internal Deed-Back Review",
        "phone": "1-800-845-5279",
        "url": "https://www.marriottvacationsworldwide.com/owners",
        "notes": "Does not advertise the program prominently. Ask the owner services line directly about 'deed-back' or 'voluntary surrender.' Eligibility is case-by-case.",
        "eligibility": ["Loan paid in full", "Fees current", "Reviewed case-by-case"]
    },
    "disney": {
        "name": "Disney Vacation Club",
        "program": "Resale / Surrender Review",
        "phone": "1-800-500-3990",
        "url": "https://disneyvacationclub.disney.go.com",
        "notes": "DVC has a Right of First Refusal on resales. For surrender, contact Member Services directly and explain your situation. They have a process but it is not publicized.",
        "eligibility": ["Loan paid in full", "Fees current", "Case-by-case review"]
    },
    "bluegreen": {
        "name": "Bluegreen Vacations",
        "program": "Deed-Back / Surrender Request",
        "phone": "1-800-456-2582",
        "url": "https://www.bluegreenvacations.com/owner-care",
        "notes": "Contact Owner Care directly and request deed-back. Bluegreen has honored these requests for owners in financial hardship.",
        "eligibility": ["Loan paid in full", "Fees current or hardship demonstrated"]
    },
    "westgate": {
        "name": "Westgate Resorts",
        "program": "Owner Services Review",
        "phone": "1-888-808-7410",
        "url": "https://www.westgateresorts.com/owners",
        "notes": "Westgate is one of the more difficult companies for deed-backs. Persist through Owner Services and document every call (date, time, representative name).",
        "eligibility": ["Loan paid in full", "Fees current", "Written request recommended"]
    },
    "diamond": {
        "name": "Diamond Resorts / Sunterra",
        "program": "Owner Advocacy Team",
        "phone": "1-866-610-3201",
        "url": "https://www.diamondresorts.com",
        "notes": "Now part of Hilton Grand Vacations. Route through HGV Transitions program.",
        "eligibility": ["Same as HGV Transitions after 2021 acquisition"]
    },
    "other": {
        "name": "Other / Independent Resort",
        "program": "Direct Negotiation",
        "phone": "Contact resort owner services",
        "url": "",
        "notes": "Most resorts have an internal process even if not advertised. Call the main owner services line. Use the phrase 'deed-back' or 'voluntary surrender.' Ask to speak with a supervisor. Put your request in writing via certified mail to create a paper trail.",
        "eligibility": ["Varies — always ask. Many resorts would rather accept a deed-back than pursue a collection."]
    }
}

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    states = get_states()
    state_list = sorted([(k, v['name']) for k, v in states.items()], key=lambda x: x[1])
    return render_template('index.html', state_list=state_list)


@app.route('/api/state/<state_code>')
def state_info(state_code):
    states = get_states()
    state = states.get(state_code.upper())
    if not state:
        return jsonify({'error': 'State not found'}), 404
    return jsonify(state)


@app.route('/api/deedback/<company_key>')
def deedback_info(company_key):
    info = DEEDBACK_PROGRAMS.get(company_key.lower())
    if not info:
        return jsonify(DEEDBACK_PROGRAMS['other'])
    return jsonify(info)


@app.route('/api/generate-letter', methods=['POST'])
def generate_letter():
    data = request.get_json()
    letter_type = data.get('type', 'rescission')

    if letter_type == 'rescission':
        prompt = _build_rescission_prompt(data)
    elif letter_type == 'deedback':
        prompt = _build_deedback_prompt(data)
    elif letter_type == 'ag_complaint':
        prompt = _build_ag_prompt(data)
    else:
        return jsonify({'error': 'Unknown letter type'}), 400

    return Response(
        stream_with_context(_stream_letter(prompt)),
        mimetype='text/plain'
    )


@app.route('/api/scam-check', methods=['POST'])
def scam_check():
    data = request.get_json()
    company = data.get('company', '').strip()
    details = data.get('details', '').strip()

    prompt = f"""You are an expert on timeshare exit scams. A person is asking you to evaluate whether a company or offer they encountered is legitimate or a scam.

Company/offer name: {company}
Details they provided: {details}

Analyze this for scam indicators. Be direct and specific. Format your response as:

VERDICT: [LIKELY SCAM / WARNING SIGNS PRESENT / APPEARS LEGITIMATE / INSUFFICIENT INFO]

KEY RED FLAGS:
- [list any red flags you see]

WHAT LEGITIMATE COMPANIES DO:
- Never charge large upfront fees before delivering results
- Are transparent about their exact process
- Are licensed attorneys or work with licensed attorneys
- Do not cold-call or send unsolicited mailers
- Do not promise guaranteed outcomes or specific timeframes
- Accept credit cards (giving you chargeback rights)

RECOMMENDATION:
[1-2 sentences on what this person should do]

If the company name is well-known as a scam (many exit companies are), name that clearly.
Keep the response focused and under 300 words."""

    return Response(
        stream_with_context(_stream_letter(prompt)),
        mimetype='text/plain'
    )


def _stream_letter(prompt):
    client = anthropic.Anthropic()
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield text


def _build_rescission_prompt(d):
    return f"""You are a consumer rights expert helping someone cancel their timeshare during the legal rescission period. Generate a formal, professional rescission letter.

Details provided:
- Purchaser name(s): {d.get('names', '[PURCHASER NAME(S)]')}
- Address: {d.get('address', '[ADDRESS]')}
- Phone: {d.get('phone', '[PHONE]')}
- Email: {d.get('email', '[EMAIL]')}
- Purchase date: {d.get('purchase_date', '[PURCHASE DATE]')}
- Resort/Developer name: {d.get('resort', '[RESORT/DEVELOPER NAME]')}
- Contract/Membership number: {d.get('contract_num', '[CONTRACT NUMBER]')}
- Amount paid: {d.get('amount_paid', '[AMOUNT PAID]')}
- State where timeshare is located: {d.get('state', '[STATE]')}
- Rescission address (from contract): {d.get('rescission_address', '[RESCISSION ADDRESS FROM CONTRACT]')}
- Today's date: {datetime.now().strftime('%B %d, %Y')}

Generate a complete, properly formatted rescission/cancellation letter. Include:
1. Date
2. Sender's full info
3. Recipient (resort/developer) full info
4. RE: line with contract number
5. Clear statement of intent to rescind
6. All required legal elements
7. List all attachments to include (copy of contract, proof of payment)
8. Signature block for ALL purchasers who signed the original contract
9. A bold note at the bottom: "SEND VIA USPS CERTIFIED MAIL WITH RETURN RECEIPT. THE POSTMARK DATE — NOT DELIVERY DATE — IS WHAT MATTERS."

After the letter, add a section titled "SENDING INSTRUCTIONS" with step-by-step certified mail instructions.

Be specific, professional, and legally sound. This letter may be time-critical."""


def _build_deedback_prompt(d):
    return f"""You are a consumer rights expert helping someone request a voluntary deed-back of their timeshare from the resort developer. Generate a formal, professional deed-back request letter.

Details provided:
- Owner name(s): {d.get('names', '[OWNER NAME(S)]')}
- Address: {d.get('address', '[ADDRESS]')}
- Phone: {d.get('phone', '[PHONE]')}
- Email: {d.get('email', '[EMAIL]')}
- Resort/Developer name: {d.get('resort', '[RESORT/DEVELOPER NAME]')}
- Contract/Membership number: {d.get('contract_num', '[CONTRACT NUMBER]')}
- Year purchased: {d.get('year_purchased', '[YEAR]')}
- Loan status: {d.get('loan_status', '[PAID IN FULL / OUTSTANDING BALANCE]')}
- Current on maintenance fees: {d.get('fees_current', '[YES/NO]')}
- Reason for deed-back request: {d.get('reason', '[REASON]')}
- Today's date: {datetime.now().strftime('%B %d, %Y')}

Generate a complete, properly formatted deed-back request letter. Include:
1. Date and full contact info header
2. RE: line identifying the property and contract number
3. Clear, professional request for voluntary surrender/deed-back
4. Brief statement of reason (financial hardship, life change, inability to use)
5. Statement that owner is current on fees (if applicable) and loan is paid
6. Request for written confirmation and timeline
7. Professional closing

After the letter, add a section titled "NEXT STEPS" with:
- Who to address this letter to
- How to send it (certified mail)
- What to do if ignored (follow-up calls, escalation)
- Reminder to document all calls (date, time, representative name, what was said)

Keep tone professional and non-confrontational — the goal is cooperation."""


def _build_ag_prompt(d):
    return f"""You are a consumer rights expert helping someone file a complaint with their state Attorney General about timeshare fraud or misrepresentation during a sales presentation.

Details provided:
- Complainant name: {d.get('names', '[YOUR NAME]')}
- Address: {d.get('address', '[ADDRESS]')}
- Resort/Company name: {d.get('resort', '[RESORT/COMPANY NAME]')}
- State where timeshare is located: {d.get('state', '[STATE]')}
- Purchase date: {d.get('purchase_date', '[DATE]')}
- What happened / misrepresentations made: {d.get('description', '[DESCRIPTION OF WHAT HAPPENED]')}
- Amount paid or owed: {d.get('amount_paid', '[AMOUNT]')}
- Today's date: {datetime.now().strftime('%B %d, %Y')}

Generate a clear, factual complaint narrative (not a letter — a statement of facts) that this person can use when filing:
1. With their state Attorney General
2. With the FTC at ftc.gov/complaint
3. With the CFPB at consumerfinance.gov/complaint

Structure it as:
COMPLAINT SUMMARY (2-3 sentences)

FACTS IN CHRONOLOGICAL ORDER
- [date]: [what happened]

MISREPRESENTATIONS MADE
- [specific false or misleading statements]

HARM SUFFERED
- [financial harm, stress, ongoing obligation]

RELIEF REQUESTED
- [contract cancellation, refund, investigation]

Also provide a short paragraph at the end explaining what to file where and why filing with multiple agencies increases pressure."""


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("TIMESHARE EXIT — Free Exit Engine")
    print("Running on http://localhost:5003")
    app.run(debug=True, port=5003)
