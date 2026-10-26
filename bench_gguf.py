#!/usr/bin/env python3
"""Benchmark llama-server Q4_K_M 7B at different ngl levels, both backends."""
import subprocess, time, json, sys, os, signal, urllib.request, urllib.error

MODEL = r"C:/Users/foste/.ollama/models/blobs/sha256-2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730"
PROMPT = "The quick brown fox jumps over the lazy dog. " * 15
N_PREDICT = 128
NGLL = [0, 33, 66, 99]
BACKENDS = {
    "cpu-avx2": r"C:/Users/foste/.lmstudio/extensions/backends/llama.cpp-win-x86_64-avx2-2.28.2/llama-server.exe",
    "vulkan-avx2": r"C:/Users/foste/.lmstudio/extensions/backends/llama.cpp-win-x86_64-vulkan-avx2-2.28.2/llama-server.exe",
}

def http_json(method, url, data=None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    if body:
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except Exception as e:
        return {"error": str(e)}

def run_bench(backend_name, exe, ngl):
    port = 9100 + (10 if backend_name == "vulkan-avx2" else 0) + ngl
    subprocess.run(["taskkill", "/F", "/IM", "llama-server.exe"], capture_output=True)
    time.sleep(0.5)
    
    cmd = [exe, "--model", MODEL, "--port", str(port), "--temp", "0", "--n-predict", str(N_PREDICT)]
    if ngl > 0:
        cmd.extend(["--ngl", str(ngl)])
    
    print(f"[{backend_name}] ngl={ngl} starting...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    loaded = False
    for _ in range(40):
        try:
            r = urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=3)
            if r.status == 200:
                loaded = True
                break
        except:
            pass
        time.sleep(0.5)
    
    if not loaded:
        stderr = proc.stderr.read()[-800:] if proc.stderr else "none"
        print(f"  FAILED to start: {stderr}")
        proc.kill()
        return None
    
    print(f"  Server ready, sending completion...")
    payload = {"model": "default", "prompt": PROMPT, "options": {"n_predict": N_PREDICT, "temperature": 0}, "stream": False}
    
    try:
        t0 = time.time()
        data = http_json("POST", f"http://127.0.0.1:{port}/completion", payload)
        total_elapsed = time.time() - t0
        
        if "error" in data:
            print(f"  Request error: {data['error']}")
            return None
        
        eval_count = data.get("evaluation_count", 0)
        eval_dur_us = data.get("evaluation_duration", 0)
        prompt_eval_count = data.get("prompt_eval_count", 0)
        prompt_eval_dur_us = data.get("prompt_eval_duration", 0)
        
        gen_time = eval_dur_us / 1e6
        gen_tps = eval_count / gen_time if gen_time > 0 else 0
        prompt_time = prompt_eval_dur_us / 1e6
        prompt_tps = prompt_eval_count / prompt_time if prompt_time > 0 else 0
        
        vram = "N/A"
        try:
            info = http_json("GET", f"http://127.0.0.1:{port}/vram")
            if isinstance(info, dict) and "error" not in info:
                vram = str(info)[:100]
        except:
            pass
        
        result = {
            "backend": backend_name, "ngl": ngl,
            "prompt_tps": round(prompt_tps, 1), "gen_tps": round(gen_tps, 1),
            "prompt_tokens": prompt_eval_count, "gen_tokens": eval_count,
            "prompt_eval_ms": round(prompt_eval_dur_us / 1000, 1),
            "eval_ms": round(eval_dur_us / 1000, 1),
            "total_elapsed_s": round(total_elapsed, 1), "vram": vram,
        }
        print(f"  prompt={prompt_tps} tok/s gen={gen_tps} tok/s (total {total_elapsed:.0f}s)")
        return result
    except Exception as e:
        print(f"  Exception: {e}")
        return None
    finally:
        proc.kill()
        time.sleep(1)

def main():
    results = []
    for backend_name, exe in BACKENDS.items():
        for ngl in NGLL:
            r = run_bench(backend_name, exe, ngl)
            if r:
                results.append(r)
            else:
                print(f"  [{backend_name}] ngl={ngl}: FAILED")
    
    print("\n\n=== BENCHMARK TABLE ===")
    print("backend     | ngl | prompt_t/s | gen_t/s | total_t/s | eval_ms | vram")
    print("-" * 85)
    for r in results:
        print(f"{r['backend']:11s} | {r['ngl']:3d} | {r['prompt_tps']:10.1f} | {r['gen_tps']:7.1f} | {r['prompt_tps'] + r['gen_tps']:9.1f} | {r['eval_ms']:7.1f} | {r['vram']}")
    
    with open("C:/tmp/bench_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved. {len(results)}/{len(NGLL)*len(BACKENDS)} configs completed.")

if __name__ == "__main__":
    main()