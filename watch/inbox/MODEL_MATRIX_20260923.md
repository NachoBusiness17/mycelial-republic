# MODEL MATRIX — 50-call bake-off across the free wall (2026-09-23)

Chore: anchor-note for the Church Committee stone (correct = cites 1976). All calls fired concurrently.

| lane | calls | ok | correct | avg latency | avg tok/s | verdict |
|---|---|---|---|---|---|---|
| nvidia/glm-5.3-flash | 5 | 5 | 5 | 25.6s | 12.8 | **carry** |
| nvidia/deepseek-v4.1 | 5 | 0 | 0 | -s | - | **cut** |
| openrouter-a1/auto | 5 | 5 | 5 | 3.8s | 48.1 | **carry** |
| openrouter-a2/auto | 5 | 5 | 5 | 1.6s | 114.9 | **carry** |
| groq/llama-3.3-70b | 5 | 0 | 0 | -s | - | **cut** |
| groq2/llama-3.3-70b | 5 | 0 | 0 | -s | - | **cut** |
| deepseek/deepseek-chat | 5 | 5 | 5 | 1.1s | 70.4 | **carry** |
| together/deepseek-v3 | 5 | 0 | 0 | -s | - | **cut** |
| zai-lite/glm-4.7-flash | 5 | 1 | 1 | 35.7s | 8.4 | **cut** |
| nous/hermes-4-70b | 5 | 0 | 0 | -s | - | **cut** |

## Sample outputs (first ok call per lane)

### nvidia/glm-5.3-flash
[reasoning only] The user wants an "anchor note" for a verified receipt about the Church Committee's Final Report (S. Rep. 94-755), issued April 1976,

### nvidia/deepseek-v4.1
no ok call

### openrouter-a1/auto
In April 1976, the Church Committee’s Final Report confirmed that COINTELPRO had run over 2,000 covert actions against U.S. citizens, while Project SH

### openrouter-a2/auto
The Church Committee’s Final Report, released in April 1976, exposed COINTELPRO’s 2,000+ covert actions against American citizens and SHAMROCK’s mass 

### groq/llama-3.3-70b
no ok call

### groq2/llama-3.3-70b
no ok call

### deepseek/deepseek-chat
In 1976, the Church Committee’s Final Report (S. Rep. 94-755) exposed COINTELPRO’s 2,000+ covert actions and SHAMROCK’s copying of ~150,000 telegrams 

### together/deepseek-v3
no ok call

### zai-lite/glm-4.7-flash
[reasoning only] 1.  **Analyze the Request:**
    *   **Source Material:** A verified receipt about the Church Committee's Final Report (S. Rep. 94-75

### nous/hermes-4-70b
no ok call
