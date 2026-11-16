#!/usr/bin/env python3
"""
Local AI Stack — the honest setup the "comment Ai / book a Zoom call" guys funnel you for.

A viral reel (Kevin Unk Ai) sells a "local sovereign AI stack": Omarchy + a CLI agent + "Qwen 27B" +
a "262K cache window" + "Herdr" to run "agents 24/7 while you sleep" — comment Ai, join the group,
book a Zoom call. The stack is real and worth running. But every piece is FREE and open, the specs in
the pitch are wrong, and "agents while you sleep" is the fantasy. This tool gives you the whole thing
for free: it checks YOUR hardware, tells you what you can actually run and how it really compares, and
prints the real setup commands. No group, no Zoom call, no per-token bill.

Reads your hardware and prints advice. It installs nothing and sends nothing.
"""
import re, shutil, subprocess, sys

# Approx VRAM (GB) to run at a usable Q4_K_M quant, model only (add context/KV cache on top).
MODELS = [
    ("qwen2.5-coder:7b",  5,  "solid autocomplete + simple edits; weakest at multi-file agentic work"),
    ("qwen2.5-coder:14b", 9,  "decent single-file coding; still not frontier for planning/agents"),
    ("gemma2:27b",        17, "good general model (THIS is the real '27B' — it's Gemma, not Qwen)"),
    ("qwen2.5-coder:32b", 20, "the best local coder tier; ~a weak GPT-4o for scoped tasks, not Claude-tier agents"),
    ("llama3.1:70b",      42, "strong, but needs a big GPU or multi-GPU; slow without it"),
]

def vram_gb():
    if not shutil.which("nvidia-smi"):
        return None
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=10).stdout
        mb = [int(x) for x in re.findall(r"\d+", out)]
        return round(max(mb) / 1024, 1) if mb else None
    except Exception:
        return None

def ram_gb():
    try:
        for line in open("/proc/meminfo"):
            if line.startswith("MemTotal"):
                return round(int(line.split()[1]) / 1024 / 1024, 1)
    except Exception:
        pass
    return None

def kv_cache_gb(ctx_tokens, model_gb):
    # rough: KV cache scales with context; ~ (model_gb/20) GB per 32K tokens as a ballpark for a 32B-class model
    return round((ctx_tokens / 32000.0) * max(1.0, model_gb / 20.0) * 4.0, 1)

def main():
    v = vram_gb(); r = ram_gb()
    print("=" * 74)
    print("LOCAL AI STACK — HONEST CHECK   (the setup behind the 'comment Ai' funnel)")
    print("=" * 74)
    print("\nYour hardware: GPU VRAM = %s | system RAM = %s"
          % (("%.1f GB" % v) if v else "no NVIDIA GPU detected", ("%.1f GB" % r) if r else "?"))

    budget = v if v else (r * 0.5 if r else 0)   # CPU-only can use RAM but will be slow
    where = "GPU VRAM" if v else "RAM (CPU-only = much slower)"
    print("Usable model budget: ~%.1f GB of %s\n" % (budget, where))
    print("WHAT YOU CAN ACTUALLY RUN (model only; leave headroom for context):")
    any_ok = False
    for name, need, note in MODELS:
        ok = budget >= need + 1
        any_ok = any_ok or ok
        print("  [%s] %-20s needs ~%2d GB  - %s" % ("x" if ok else " ", name, need, note))
    if not any_ok:
        print("  -> Your box can't comfortably run even a 7B at speed. Local is private + free, but this is")
        print("     the hardware wall the reel skips. A used 24GB GPU is the real cost of 'your own box'.")

    print("\nTHE PITCH, CHECKED:")
    print("  * 'Qwen 27B' does not exist. Qwen ships 7B/14B/32B; the 27B is GEMMA. Citing a model size that")
    print("    isn't real is the tell that the specs came from a caption, not a setup.")
    big = kv_cache_gb(262000, 20)
    print("  * '262K context window' on a 32B model needs roughly ~%s GB of VRAM JUST for the KV cache," % big)
    print("    on top of the ~20 GB model. That's a multi-GPU rig, not a laptop. Run 8K-32K and you're fine.")
    print("  * 'Agents working 24/7 while you sleep' on a local model = unreviewed output. Even pros pair a")
    print("    local coder with a FRONTIER reviewer (plan/verify) or it ships confident garbage. Local alone")
    print("    is great for private, cheap, scoped work - not an autonomous money printer.")

    print("\nTHE REAL SETUP (free, no group, no Zoom call):")
    pick = next((n for n, need, _ in reversed(MODELS) if budget >= need + 1), "qwen2.5-coder:7b")
    print("  1. Install Ollama (runs local models):   curl -fsSL https://ollama.com/install.sh | sh")
    print("  2. Pull a model your box can run:         ollama pull %s" % pick)
    print("  3. A CLI coding agent (free, open):       pipx install aider-chat")
    print("  4. Point the agent at your local model:   aider --model ollama/%s" % pick)
    print("  5. Keep context sane for your VRAM:        OLLAMA_CONTEXT_LENGTH=16384 ollama serve")
    print("  (Omarchy is just a nice Arch/Linux setup - optional. The intelligence is the model, not the OS.)")
    print("\nPrivate, free, no per-token bill - all true. Just skip the Zoom call; the tools are the free part.\n")

if __name__ == "__main__":
    main()
