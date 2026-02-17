# HOW TO USE THE URGENCY MULTIPLIER

## Step-by-Step Instructions

### 1. Open the App
- Go to: http://localhost:8501
- The app should now be running with the updated network

### 2. Select Cities for Testing

**RECOMMENDED TEST SCENARIO:**

**Source Hub**: Select **Ibadan**
**Destination Clinic**: Select **Ilorin**

### 3. Use the Urgency Multiplier Slider

In the left sidebar, you'll see:
- **"Urgency Multiplier"** slider
- Range: 0.1 to 10.0
- Default: 1.0

### 4. Click "Calculate Optimal Route"

After selecting cities and setting urgency, click the blue button:
**"🚀 Calculate Optimal Route"**

### 5. What to Observe

#### The Route (Right Panel):
- **Path**: Ibadan → Ogbomosho → Ilorin
- **Total Distance**: 105 km
- **Route Segments**: 2 hops

#### The Priority Score (Changes with Urgency):

| Urgency | Priority Score | Meaning |
|---------|----------------|---------|
| 0.5x    | ~353.59        | Low priority (standard delivery) |
| 1.0x    | ~176.79        | Normal priority |
| 3.0x    | ~58.93         | Medium priority (elevated) |
| 6.0x    | ~29.47         | High priority (urgent) |
| 10.0x   | ~17.68         | Emergency priority |

**Lower score = Higher priority!**

---

## What the Urgency Multiplier Does

### Formula
```
Priority Score = Distance / (Prevalence × Urgency)
```

### Effect
- **Increasing urgency** → **Decreases priority score** → **Higher priority**
- Routes through high-prevalence areas get MORE attractive
- Supplies reach areas with most malaria cases faster

---

## Try These Test Scenarios

### Test 1: Ibadan → Ilorin
- **Why it works**: Route goes through Ogbomosho (78% prevalence)
- **What changes**: Priority score drops dramatically with higher urgency
- **Route**: Always Ibadan → Ogbomosho → Ilorin (optimal path)

### Test 2: Lagos → Akure
- **Why it works**: Route goes through Ore (82% prevalence - VERY HIGH)
- **What changes**: Priority score changes significantly
- **Route**: Lagos → Ore → Akure (225km)

### Test 3: Lagos → Benin City
- **Route**: Direct (290km, 75% prevalence)
- **What changes**: Priority score reflects urgency level

---

## Understanding the Results

### Why Routes Don't Always Change

The urgency multiplier affects **priority scoring**, not always the route itself.

**The route changes ONLY when**:
- Multiple competitive paths exist
- One path is shorter but lower prevalence
- Another path is longer but higher prevalence
- Urgency tips the balance

**In your network**:
- Most optimal paths go through high-prevalence areas already
- So the route stays the same
- But the **priority score** always changes!

### What ALWAYS Changes

**Priority Score** = How urgently this route should be executed

- **Low urgency (0.5x)**: Score ~350 → "Can wait, standard delivery"
- **High urgency (10.0x)**: Score ~18 → "Emergency! Execute immediately!"

This tells the system how to prioritize this delivery vs. other deliveries.

---

## Quick Reference

### Urgency Levels (from sidebar)
- **0.1-2.0**: Standard delivery (distance matters most)
- **2.1-5.0**: Elevated priority (balance distance & prevalence)
- **5.1-10.0**: Emergency outbreak response (prevalence critical)

### How to Test
1. Select: Ibadan → Ilorin
2. Set urgency to 0.5x
3. Click "Calculate Optimal Route"
4. Note the Priority Score
5. Change urgency to 10.0x
6. Click "Calculate Optimal Route" again
7. Compare the Priority Scores (should be ~20x different!)

---

## Expected Behavior

✅ **Priority Score changes** with urgency (ALWAYS)
✅ **Route may stay the same** (if one path is clearly optimal)
✅ **Lower score = Higher priority** (counterintuitive but correct!)
✅ **High-prevalence routes** are favored at high urgency

❌ **Route doesn't change for every city pair** (this is normal!)
