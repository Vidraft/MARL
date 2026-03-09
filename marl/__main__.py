"""
MARL CLI — Command-line interface

Usage:
    # Run as proxy
    python -m marl proxy --port 8080 --backend openai --model gpt-5.2

    # Run single query
    python -m marl run "Your question here" --backend ollama --model llama3.1

    # Test connection
    python -m marl test --backend openai
"""

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="marl",
        description="🌀 MARL — Model-Agnostic Runtime Middleware for LLMs"
    )
    sub = parser.add_subparsers(dest="command")

    # ── proxy ──
    p_proxy = sub.add_parser("proxy", help="Start OpenAI-compatible proxy server")
    p_proxy.add_argument("--port", type=int, default=8080)
    p_proxy.add_argument("--host", default="0.0.0.0")
    p_proxy.add_argument("--backend", default="openai",
                         choices=["openai", "anthropic", "ollama", "friendli", "custom"])
    p_proxy.add_argument("--model", default=None)
    p_proxy.add_argument("--api-key", default=None)
    p_proxy.add_argument("--base-url", default=None, help="For custom backend")

    # ── run ──
    p_run = sub.add_parser("run", help="Run single MARL query")
    p_run.add_argument("prompt", help="The question/task")
    p_run.add_argument("--backend", default="openai",
                       choices=["openai", "anthropic", "ollama", "friendli", "custom"])
    p_run.add_argument("--model", default=None)
    p_run.add_argument("--api-key", default=None)
    p_run.add_argument("--base-url", default=None)
    p_run.add_argument("--trace", action="store_true", help="Show full agent trace")

    # ── test ──
    p_test = sub.add_parser("test", help="Test backend connection")
    p_test.add_argument("--backend", default="openai",
                        choices=["openai", "anthropic", "ollama", "friendli", "custom"])
    p_test.add_argument("--model", default=None)
    p_test.add_argument("--api-key", default=None)
    p_test.add_argument("--base-url", default=None)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    from .core import Marl, MarlConfig

    marl = _build_marl(args)

    if args.command == "proxy":
        marl.serve(host=args.host, port=args.port)

    elif args.command == "run":
        config = MarlConfig(include_trace=args.trace)
        marl.config = config
        print("🌀 MARL running S1→S2→S3→S4→S5 pipeline...\n")
        result = marl.run(args.prompt)
        if args.trace:
            print(result.full_output)
        else:
            print(result.answer)
        print(f"\n⏱️ {result.elapsed:.1f}s | Fixes: {len(result.fixes)}")

    elif args.command == "test":
        print("🔍 Testing backend connection...")
        try:
            resp = marl.call_fn("Say OK", "", 10, 0)
            if resp and not resp.startswith("[ERROR"):
                print(f"✅ Connected! Response: {resp[:50]}")
            else:
                print(f"❌ Error: {resp}")
        except Exception as e:
            print(f"❌ Failed: {e}")


def _build_marl(args) -> "Marl":
    from .core import Marl
    backend = args.backend
    api_key = args.api_key or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY") or ""
    model = args.model

    if backend == "openai":
        return Marl.from_openai(api_key=api_key, model=model or "gpt-5.2")
    elif backend == "anthropic":
        key = args.api_key or os.getenv("ANTHROPIC_API_KEY", "")
        return Marl.from_anthropic(api_key=key, model=model or "claude-sonnet-4-20250514")
    elif backend == "ollama":
        return Marl.from_ollama(model=model or "llama3.1")
    elif backend == "friendli":
        key = args.api_key or os.getenv("FRIENDLI_TOKEN", "")
        return Marl.from_friendli(token=key, model=model or "deppfs281rgffnk")
    elif backend == "custom":
        base_url = args.base_url or "http://localhost:8000/v1"
        return Marl.from_openai_compatible(base_url=base_url, api_key=api_key,
                                            model=model or "default")
    else:
        raise ValueError(f"Unknown backend: {backend}")


if __name__ == "__main__":
    main()
