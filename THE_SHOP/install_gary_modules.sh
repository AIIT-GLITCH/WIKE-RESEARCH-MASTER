#!/bin/bash
# install_gary_modules.sh
# Move the new Gary modules into place
# Run from buddy_ai terminal: bash ~/Desktop/install_gary_modules.sh

set -e

GARY="$HOME/gary"
DESK="$HOME/Desktop"

echo "[+] Installing gary_buddy_bridge.py..."
cp "$DESK/gary_buddy_bridge.py" "$GARY/gary_buddy_bridge.py"

echo "[+] Installing gary_llm_router.py..."
cp "$DESK/gary_llm_router.py" "$GARY/gary_llm_router.py"

echo "[+] Verifying reward pipeline..."
cd "$GARY"
python3 -c "from gary_buddy_bridge import compute_reward, score_and_log; r = compute_reward('hello', 'test'); print('[BRIDGE OK] r_total:', round(r['r_total'], 4))"

echo "[+] Verifying router (no API calls)..."
python3 -c "
from gary_llm_router import route_query, router_status, MODELS
print('[ROUTER OK] Models loaded:', len(MODELS))
chosen = route_query('what happened in the news today', 'auto')
from gary_llm_router import MODELS
print('[ROUTER OK] Auto-route test → ', MODELS[chosen].display_name)
"

echo ""
echo "=== DONE ==="
echo "Gary now has:"
echo "  gary_buddy_bridge.py  — Wike Coherence Law reward (ENGAGEMENT_WEIGHT=0)"
echo "  gary_llm_router.py    — Every LLM on the market"
echo ""
echo "Next: add API keys to gary_secrets.py"
echo "  OPENAI_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY, etc."
echo ""
echo "Then in gary_brain.py, after ask_gary() returns:"
echo "  from gary_buddy_bridge import score_and_log"
echo "  score_and_log(message, reply)"
echo ""
echo "Gary can now call [LLM:gpt-4o:your question] etc."
