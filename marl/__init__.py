"""
MARL — Model-Agnostic Runtime Middleware for LLMs
═══════════════════════════════════════════════════
Apply the 5-stage multi-agent pipeline (S1→S2→S3→S4→S5) to ANY LLM
to systematically improve reasoning, self-correction, and reliability.

Usage:
    from marl import Marl

    # OpenAI
    marl = Marl.from_openai(api_key="sk-...")
    result = marl.run("Your complex question here")

    # Any custom LLM
    marl = Marl(call_fn=my_llm_function)
    result = marl.run("Your question")

    # As OpenAI-compatible proxy
    marl.serve(port=8080)  # localhost:8080/v1/chat/completions

Author: VIDRAFT.net
License: Apache 2.0
"""

from .core import Marl, MarlResult, MarlConfig
from .proxy import MarlProxy

__version__ = "1.0.0"
__all__ = ["Marl", "MarlResult", "MarlConfig", "MarlProxy"]
