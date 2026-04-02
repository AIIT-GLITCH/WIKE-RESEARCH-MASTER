"""
RX EXIT — Free Prescription Drug Cost Engine
Finds every legal way to pay less for your medication.

AIIT-THRESI Research Initiative | 2026
Rhet Dillard Wike | Council Hill, Oklahoma

---

The average American pays 3-10x more for prescription drugs than
patients in any other developed country. The drugs are identical.
The molecules are identical. The factories are sometimes identical.

The price difference is not R&D. It is not manufacturing cost.
It is information asymmetry maintained by deliberate complexity.

GoodRx exists. Cost Plus Drugs exists. Patient Assistance Programs
exist at every major pharmaceutical company. Medicare Extra Help
covers millions who are not enrolled. 340B pharmacies serve
communities that don't know they qualify.

The information is there. It is scattered intentionally.

This app collects it. Finds the cheapest legal source for your
specific medication. Generates the PAP application letter.
Points you to the 340B pharmacy down the street.

The drug costs the same to make whether you pay $3 or $300.
You should pay $3.

— AIIT-THRESI | April 2, 2026
"""

from flask import Flask, render_template, jsonify, request, Response, stream_with_context
from datetime import datetime
import json, os
import anthropic

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

_DRUGS = None
def get_drugs():
    global _DRUGS
    if _DRUGS is None:
        with open(os.path.join(DATA_DIR, 'drugs.json')) as f:
            _DRUGS = json.load(f)
    return _DRUGS

PAP_PROGRAMS = {
    "Pfizer": {"name": "Pfizer RxPathways", "url": "https://www.pfizerrxpathways.com", "phone": "1-844-989-PATH"},
    "AstraZeneca": {"name": "AZ&Me Prescription Savings", "url": "https://www.azandme.com", "phone": "1-800-292-6363"},
    "Eli Lilly": {"name": "Lilly Cares Foundation", "url": "https://www.lillycares.com", "phone": "1-800-545-5979"},
    "Novo Nordisk": {"name": "Novo Nordisk Patient Assistance", "url": "https://www.novonordiskus.com/patient-assistance", "phone": "1-866-310-7549"},
    "Sanofi": {"name": "Sanofi Patient Connection", "url": "https://www.sanofius.com/patient-support", "phone": "1-888-847-4877"},
    "AbbVie": {"name": "myAbbVie Assist", "url": "https://www.myabbvieassist.com", "phone": "1-800-222-6885"},
    "Bristol-Myers Squibb": {"name": "BMS Patient Assistance Foundation", "url": "https://www.bmspaf.org", "phone": "1-800-736-0003"},
    "Merck": {"name": "Merck Patient Assistance Program", "url": "https://www.merckhelps.com", "phone": "1-800-727-5400"},
    "Johnson & Johnson": {"name": "J&J Patient Assistance", "url": "https://www.jnjpatientassistance.com", "phone": "1-800-652-6227"},
    "Roche/Genentech": {"name": "Genentech Access Solutions", "url": "https://www.gene.com/patients/patient-assistance", "phone": "1-888-249-4918"},
    "Amgen": {"name": "Amgen Safety Net Foundation", "url": "https://www.amgensupportivecaregivesback.com", "phone": "1-888-762-6436"},
    "Gilead": {"name": "Gilead Advancing Access", "url": "https://www.gileadadvancingaccess.com", "phone": "1-800-226-2056"},
}

@app.route('/')
def index():
    drugs = get_drugs()
    featured = []
    for key, d in drugs.items():
        if d.get('_meta'): continue
        best_price = None
        if d.get('cost_plus'):
            best_price = d['cost_plus']
        elif d.get('goodrx_low'):
            best_price = d['goodrx_low']
        if best_price and d.get('retail_avg', 0) > 20:
            savings_pct = round((1 - best_price / d['retail_avg']) * 100)
            featured.append({
                'key': key,
                'name': d['name'],
                'condition': d['condition'],
                'retail': d['retail_avg'],
                'best': best_price,
                'best_source': 'Cost Plus' if d.get('winner') == 'cost_plus' else ('GoodRx' if d.get('winner') == 'goodrx' else 'Multiple'),
                'goodrx_low': d.get('goodrx_low'),
                'cost_plus': d.get('cost_plus'),
                'winner': d.get('winner', 'goodrx'),
                'savings_pct': savings_pct,
                'walmart_4': d.get('walmart_4', False)
            })
    featured.sort(key=lambda x: -x['savings_pct'])
    return render_template('index.html', featured=featured, pap_programs=PAP_PROGRAMS, total_drugs=len([k for k in drugs if k != '_meta']))

@app.route('/api/drug/<key>')
def drug_info(key):
    drugs = get_drugs()
    drug = drugs.get(key.lower())
    if not drug:
        return jsonify({'error': 'Drug not found'}), 404
    return jsonify(drug)

@app.route('/api/lookup', methods=['POST'])
def drug_lookup():
    data = request.get_json()
    drug_name = data.get('drug', '').strip()
    insurance = data.get('insurance', 'unknown')
    income = data.get('income', 'unknown')

    prompt = f"""You are a prescription drug cost expert helping a patient find the cheapest legal way to get their medication. Be specific, accurate, and direct. No fluff.

Drug requested: {drug_name}
Insurance status: {insurance}
Approximate household income: {income}

Provide a complete cost breakdown in this format:

## {drug_name} — Every Way to Pay Less

**Is a generic available?**
[Yes/No — and generic name if yes]

**Cost Plus Drugs (costplusdrugs.com)**
[Price if available, or "Not yet available — checking costplusdrugs.com directly recommended"]
[Note: Cost Plus = manufacturing cost + 15% markup + $3 dispensing fee. This beats insurance for most generics.]

**GoodRx**
[Typical low price range at major pharmacies — Kroger, Costco, Walmart usually lowest]
[GoodRx tip: always compare pharmacies — same drug can vary 4x]

**Patient Assistance Program**
[Manufacturer name + program name + phone + income eligibility threshold]
[NeedyMeds.org has every PAP in one place — search there too]

**Medicare Extra Help / Low Income Subsidy**
[If relevant: estimated copay with Extra Help, eligibility note]
[$0 premium + $1-$10 copays for qualifying seniors/disabled — millions eligible but not enrolled]

**340B Pharmacy**
[If relevant: explain 340B — federally qualified health centers, rural health clinics serve patients at dramatically reduced cost]
[Find nearest 340B: hrsa.gov/opa/eligibility-and-registration/health-centers]

**State Programs**
[Any relevant state pharmaceutical assistance programs if applicable]

**Walmart / OTC options**
[If drug has OTC equivalent or Walmart $4 list equivalent]

**The Bottom Line**
[One paragraph: what this specific person should do RIGHT NOW based on their insurance status and income. Be direct. Give the phone number or URL they need first.]

**What to say to your doctor**
[Specific language to use: "I'd like to discuss a generic alternative" / "Can you write for the 90-day supply" / "Is there a therapeutic equivalent that costs less?"]

Keep all prices as monthly 30-day supply unless otherwise noted. Cite specific numbers where you know them — don't guess. If you're uncertain about a price, say so and direct to the source."""

    return Response(
        stream_with_context(_stream(prompt)),
        mimetype='text/plain'
    )

@app.route('/api/pap-letter', methods=['POST'])
def pap_letter():
    data = request.get_json()
    prompt = f"""Generate a complete Patient Assistance Program application letter for prescription medication.

Patient details:
- Name: {data.get('name', '[PATIENT NAME]')}
- Address: {data.get('address', '[ADDRESS]')}
- Phone: {data.get('phone', '[PHONE]')}
- Date of birth: {data.get('dob', '[DATE OF BIRTH]')}
- Medication needed: {data.get('drug', '[MEDICATION NAME]')}
- Prescribing doctor: {data.get('doctor', '[DOCTOR NAME]')}
- Doctor phone/fax: {data.get('doctor_contact', '[DOCTOR CONTACT]')}
- Insurance status: {data.get('insurance', '[INSURANCE STATUS]')}
- Approximate annual household income: {data.get('income', '[INCOME]')}
- Household size: {data.get('household_size', '[HOUSEHOLD SIZE]')}
- Manufacturer/program: {data.get('manufacturer', '[MANUFACTURER]')}
- Today's date: {datetime.now().strftime('%B %d, %Y')}

Write a complete, professional PAP application letter that:
1. States the patient's need clearly and without excess
2. Confirms income eligibility (most PAPs cover up to 400% of federal poverty level)
3. Lists the medication, dose, and prescribing physician
4. Requests enrollment in the patient assistance program
5. Authorizes release of relevant medical/financial information

After the letter, add:
**WHAT TO ATTACH:**
- [list exactly what documents to include]

**WHERE TO SEND:**
- [manufacturer program address if known, otherwise direct to needymeds.org or the manufacturer's program page]

**WHAT HAPPENS NEXT:**
- [realistic timeline and what to expect]

Keep it one page. Professional, direct, complete."""

    return Response(
        stream_with_context(_stream(prompt)),
        mimetype='text/plain'
    )

@app.route('/api/insurance-check', methods=['POST'])
def insurance_check():
    data = request.get_json()
    prompt = f"""A person is paying too much for their prescription drugs. Help them figure out if they're leaving money on the table.

Their situation:
- Age: {data.get('age', 'unknown')}
- Insurance: {data.get('insurance', 'none')}
- Monthly drug costs: {data.get('monthly_cost', 'unknown')}
- Medications: {data.get('medications', 'unknown')}
- Annual income (approximate): {data.get('income', 'unknown')}
- State: {data.get('state', 'unknown')}

Check all of these and tell them what applies:

**Medicare Extra Help (Low Income Subsidy)**
[Eligibility: income under ~$22,000 single / $30,000 couple. If eligible: $0 premiums, $1-$10 copays. Apply at SSA.gov or call 1-800-772-1213]

**Medicaid**
[If income is low enough, they may qualify for full Medicaid drug coverage. Check their state's eligibility.]

**State Pharmaceutical Assistance Programs**
[Most states have additional programs layered on top of Medicare. Name specific programs for their state if possible.]

**Manufacturer Coupons / Copay Cards**
[Brand-name drugs often have copay assistance cards that reduce cost to $0-$10/month — but these usually DON'T work with Medicaid/Medicare. Note this clearly.]

**GoodRx vs. Insurance**
[For generics especially, GoodRx often beats insurance copays. They should compare both every time they fill.]

**Open Enrollment / Plan Switch**
[If they're on Medicare Part D, they can switch plans during open enrollment Oct 15 - Dec 7. Different plans cover different drugs at different tiers.]

Give them a priority action list — what to do first, second, third. Be specific about phone numbers and websites."""

    return Response(
        stream_with_context(_stream(prompt)),
        mimetype='text/plain'
    )

def _stream(prompt):
    client = anthropic.Anthropic()
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield text

if __name__ == '__main__':
    print("RX EXIT — Free Prescription Drug Cost Engine")
    print("Running on http://localhost:5004")
    app.run(debug=True, port=5004)
