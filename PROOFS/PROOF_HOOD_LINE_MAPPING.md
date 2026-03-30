# PROOF: Hood Collapse Line Mapping Is Correct (0.4% Rounding)
## AIIT-THRESI Anomaly Resolution #9

---

## Claim
The apparent discrepancy between code step 890 and transcript line 18,708 is resolved by fractional position mapping with 0.4% rounding error.

## Data

- Hood transcript total lines: 20,940
- Collapse observed at: line 18,708 (manual identification from transcript)
- Code constant: `collapse_point = int(0.89 × N_steps)` where N_steps = 1000

## Proof

**Step 1:** Fractional position of collapse in transcript:
```
18,708 / 20,940 = 0.8934
```

**Step 2:** Code uses 0.89 (2 decimal places):
```
Rounding: 0.8934 → 0.89
```

**Step 3:** Code maps fraction to simulation steps:
```
Step = int(0.89 × 1000) = 890
```

**Step 4:** Mapping back to transcript lines:
```
890 / 1000 × 20,940 = 18,637
```

**Step 5:** Discrepancy:
```
|18,708 - 18,637| = 71 lines
71 / 20,940 = 0.34%
```

The 71-line difference is within the uncertainty of manual collapse identification (the collapse is a transition zone, not a single line).

## Status
Not an anomaly. Fractional mapping with standard rounding.
