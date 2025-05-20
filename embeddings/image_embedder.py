import torch
from PIL import Image
from typing import List
import open_clip
from torchvision import transforms


class ImageEmbedder:
    def __init__(self, model_name="ViT-B-32", pretrained="laion2b_s34b_b79k", device="cpu"):
        self.device = device
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model_name=model_name,
            pretrained=pretrained,
            device=self.device
        )
        self.model.eval()

    def embed_image(self, image_path: str) -> List[float]:
        image = Image.open(image_path).convert("RGB")
        image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image_tensor)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            return image_features.squeeze().cpu().tolist()
