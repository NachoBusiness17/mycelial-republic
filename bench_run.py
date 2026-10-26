#!/usr/bin/env python3
"""Benchmark llama-server Q4_K_M 7B at different ngl levels, both backends."""
import subprocess, time, json, urllib.request, urllib.error

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
    except Exception as e:
        return {"error": str(e)}

def wait_server(port, max_wait=60):
    for _ in range(max_wait * 2):
        try:
            r = urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=3)
            if r.status == 200:
                return True
        except:
            pass
        time.sleep(0.5)
    return False

def run_bench(backend_name, exe, ngl):
    port = 9100 + (10 if backend_name == "vulkan-avx2" else 0) + ngl
    subprocess.run(["taskkill", "/F", "/IM", "llama-server.exe"], capture_output=True)
    time.sleep(0.5)

    cmd = [exe, "--model", MODEL, "--port", str(port), "--temp", "0", "--n-predict", str(N_PREDICT)]
    if ngl > 0:
        cmd.extend(["--ngl", str(ngl)])

    print(f"[{backend_name}] ngl={ngl} starting...", flush=True)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if not wait_server(port):
        stderr = proc.stderr.read()[-800:] if proc.stderr else "none"
        print(f"  FAILED to start: {stderr}")
        proc.kill()
        return None

    print(f"  Server ready, sending completion...", flush=True)
    payload = {"model": "default", "prompt": PROMPT, "options": {"n_predict": N_PREDICT, "temperature": 0}, "stream": False}

    try:
        t0 = time.time()
        req = urllib.request.Request(f"http://127.0.0.1:{port}/completion",
                                     data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        resp = urllib.request.urlopen(req, timeout=300)
        data = json.loads(resp.read().decode())
        total_elapsed = time.time() - t0

        timings = data.get("timings", {})
        prompt_tps = timings.get("prompt_per_second", 0)
        gen_tps = timings.get("predicted_per_second", 0)
        prompt_ms = timings.get("prompt_ms", 0)
        predicted_ms = timings.get("predicted_ms", 0)
        prompt_tokens = timings.get("prompt_n", 0)
        gen_tokens = timings.get("predicted_n", 0)

        # VRAM info
        vram = "N/A"
        try:
            info = http_json("GET", f"http://127.0.0.1:{port}/vram")
            if isinstance(info, dict) and "error" not in info:
                vram = str(info)[:120]
        except:
            pass

        result = {
            "backend": backend_name, "ngl": ngl,
            "prompt_tps": round(prompt_tps, 1), "gen_tps": round(gen_tps, 1),
            "prompt_tokens": prompt_tokens, "gen_tokens": gen_tokens,
            "prompt_ms": round(prompt_ms, 1), "predicted_ms": round(predicted_ms, 1),
            "total_elapsed_s": round(total_elapsed, 1), "vram": vram,
        }
        print(f"  prompt={prompt_tps} tok/s gen={gen_tps} tok/s ({total_elapsed:.0f}s total)")
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
    print("backend     | ngl | prompt_t/s | gen_t/s | total_t/s | prompt_ms | gen_ms   | vram")
    print("-" * 95)
    for r in results:
        print(f"{r['backend']:11s} | {r['ngl']:3d} | {r['prompt_tps']:10.1f} | {r['gen_tps']:7.1f} | {r['prompt_tps'] + r['gen_tps']:9.1f} | {r['prompt_ms']:8.0f} | {r['predicted_ms']:7.0f} | {r['vram']}")

    with open("C:/tmp/bench_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to C:/tmp/bench_results.json. {len(results)}/{len(NGLL)*len(BACKENDS)} configs completed.")

if __name__ == "__main__":
    main()