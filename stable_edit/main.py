import argparse
import torch
from diffusers import StableDiffusionInpaintPipeline
def get_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True, help='path to image / uploaded image')
    parser.add_argument('--resolution', choices=[256, 512, 1024, 2048], default=256, type=int)
    parser.add_argument('--prompt', type=str, default="A Tree", help='text to fill the masked region')
    parser.add_argument('--num_steps', type=int, default=5)
    parser.add_argument('--guidance_scale', type=float, default=7.5)
    parser.add_argument('--seed', type=int, default=0,help="seed to reproduce exact output")
    parser.add_argument('--num_samples', type=int, default=1,help="number of image to generate")
    parser.add_argument('--output_dir', default='./outputs', type=str,help='output path to save image')

    opt = parser.parse_args()
    return opt

def build_pipeline():
    is_cuda = torch.cuda.is_available()
    device = "cuda" if  is_cuda else "cpu"
    inpainting_pipeline = StableDiffusionInpaintPipeline.from_pretrained(
                            "runwayml/stable-diffusion-inpainting",
                            revision="fp16",
                            torch_dtype=torch.float16 if is_cuda else torch.float32,
                            ).to(device)
    return inpainting_pipeline

def generate_img(opt,inpaint_pipeline,device):
    generator = torch.Generator(device=device).manual_seed(opt.seed)
    output_img = inpaint_pipeline(
    prompt=opt.prompt,
    image=opt.image,
    mask_image=opt.mask_image,
    guidance_scale=opt.guidance_scale,
    generator=generator,
    num_images_per_prompt=opt.num_samples,
    ).images
    return output_img

if __name__ == '__main__':
    opt = get_opt()
    inpaint_pipeline = build_pipeline()
    output_img = generate_img()