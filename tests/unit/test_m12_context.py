from models.llamacpp import LlamaCppCaps
from models.ollama import OllamaCaps
from agent.compaction_v2 import savings
def test_exact_context_and_savings():assert LlamaCppCaps.context({'n_ctx':8192})==8192;assert OllamaCaps.context({'context_length':4096})==4096;assert savings(1000,400)['saved']==600
