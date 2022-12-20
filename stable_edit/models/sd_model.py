from diffusers import StableDiffusionInpaintPipeline
import torch
import torch.nn as nn
class Inpainting_Model(nn.Module):
    def __init__(self,model_cards = "runwayml/stable-diffusion-inpainting",revision="fp16",**kwargs):
        super().__init__()
        is_cuda = torch.cuda.is_available()
        self.access_tokens = kwargs['access_token']
        self.device = "cuda" if  is_cuda else "cpu"
        self.pipeline = StableDiffusionInpaintPipeline.from_pretrained(
                                model_cards,
                                revision=revision,
                                use_auth_token = self.access_tokens,
                                torch_dtype=torch.float16 if is_cuda else torch.float32,
                                ).to(self.device)


    def forward(self,prompt,image,mask,steps=50,guidance_scale=7.5,neg_prompt="",num_samples=1,seed=0):
        generator = torch.Generator(device=self.device).manual_seed(seed)
        output_img = self.pipeline(
        prompt=prompt,
        image=image,
        mask_image=mask,
        width=image.width,
        height=image.height,
        num_inference_steps = steps,
        guidance_scale=guidance_scale,
        negative_prompt = neg_prompt,
        generator=generator,
        num_images_per_prompt=num_samples,
        ).images
        return output_img