import numpy as np
import torch
import open_clip

class TextEmbedder:
    def __init__(self, model_name: str = "ViT-B-32", pretrained: str = "laion2b_s34b_b79k", device: str = "cpu"):
        self.device = device
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model_name=model_name,
            pretrained=pretrained,
            device=self.device
        )
        self.tokenizer = open_clip.get_tokenizer(model_name)
        self.model.eval()

    def embed(self, texts):
        """
        Embed a single text or list of texts.
        Returns 1D numpy array for single input, 2D for list.
        """
        single_input = isinstance(texts, str)

        if single_input:
            texts = [texts]

        with torch.no_grad():
            tokens = self.tokenizer(texts).to(self.device)
            embeddings = self.model.encode_text(tokens)
            embeddings = embeddings.cpu().numpy()

        if single_input:
            return embeddings[0]  

        return embeddings