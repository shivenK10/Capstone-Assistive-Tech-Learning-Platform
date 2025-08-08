import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelLoader:
    def __init__(self, base_model_name: str, quantize: bool = False, device: str | None = None):
        self.base_model_name = base_model_name
        self.quantize = quantize
        if device:
            self.device = device
        elif torch.cuda.is_available():
            self.device = "cuda"
        elif torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"

    def load_model(self) -> tuple[torch.nn.Module, AutoTokenizer, str]:
        tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
        if not tokenizer.pad_token:
            tokenizer.pad_token = tokenizer.eos_token

        load_kwargs = {"attn_implementation": "eager"}
        if self.quantize:
            load_kwargs["torch_dtype"] = torch.float16

        model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            **load_kwargs
        ).to(self.device)
        model.eval()
        return model, tokenizer, self.device
