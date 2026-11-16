# The "local AI agents 24/7" guys funnel you for free tools

There's a reel going around (Kevin Unk Ai): run a "local sovereign AI stack" — Omarchy, a CLI agent, "Qwen 27B," a "262K cache window," and "Herdr" to get agents working 24/7 while you sleep. Get off the OpenAI and Anthropic APIs. Comment "Ai," join the group, book a Zoom call.

I rebuilt the honest version, and it's actually free. No comment, no call, no group.

**Every piece of that stack is free and open.** Omarchy, Ollama, aider, Qwen, Gemma — all free. The Zoom call and the group are the product; the tools are the free part he's gatekeeping.

**The specs are wrong.** "Qwen 27B" doesn't exist — Qwen ships 7B/14B/32B; the 27B is Gemma. A "262K context window" on a 32B model needs tens of GB of VRAM just for the KV cache, on top of the model — a multi-GPU rig, not a laptop. Citing a model size that isn't real is the tell the specs came from a caption.

**"Agents 24/7 while you sleep" is the fantasy.** A local model with no reviewer ships confident garbage. The people who actually run local agents (me included) pair a local coder with a frontier reviewer to plan and verify — because local alone is great for private, cheap, scoped work, not an autonomous money printer.

**The tool, free:** github.com/warboy176/local-ai-stack
It checks your hardware, tells you what you can really run and how it compares, debunks the pitch, and prints the real Ollama + CLI-agent setup. Installs nothing, sends nothing.

Local AI is genuinely good. Just skip the Zoom call. Buy VRAM, not a course.

Witness me.
