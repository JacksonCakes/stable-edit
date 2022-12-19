# Stable Edit
An easy to use web app implementation of text guided image inpainting. (Replace any object or scene you want!)

### Sample Demo
<img src="https://user-images.githubusercontent.com/51978507/208395247-8d21c092-6318-4798-b073-c30e3c827069.mp4">

### Setup Tutorial
Easiest setup by running in colab 

1. Click the link <a href="https://colab.research.google.com/drive/164x0t9KAVgxA6OqXoBDeUBWxCBDjABuI?usp=sharing"> <img alt="Open in Colab" src="https://colab.research.google.com/assets/colab-badge.svg" /></a>  
2. Click **Runtime** -> **Hardware Accelerator** change runtime to **GPU** for better speed up in generation.
3. Run the cell in sequence
4. Once the cell with "Run web app" is running, enter your huggingface [access token](https://huggingface.co/docs/hub/security-tokens)
5. Click the generated url from previous cell:
<img src="https://user-images.githubusercontent.com/51978507/208403425-8ddca635-93b7-4eef-93c6-28ab2edcedc6.png" width = 500>
5. Done!


### Settings

| Name      | Description | Default|
| ----------- | ----------- |-----------|
| Steps     | Number of steps to generate the image. Higher steps usually lead to a higher quality image at the expense of slower inference.| 50 |
| Guidance   | Higher guidance scale encourages to generate images that are closely linked to the text `prompt`, usually at the expense of lower image quality.| 7.5 |   
| Brush / Eraser   |Brush to draw mask on the region to replace/ Eraser to erase the mask |  |   
| Seed  |Change the seed num to get different result for same prompt, same seed num will generate same result for same prompt| 0 |  
| Negative prompt  |The prompt or prompts not to guide the image generation.| |  

### To-do

- [ ] Add support for stable-diffusion v2 from [StabilityAI](https://github.com/Stability-AI/stablediffusion)
- [ ] Support for multiple images generation at once
- [ ] Optimize the inference performance with [xformers](https://github.com/facebookresearch/xformers) & TensorRT
- [ ] Support for exemplar guidance from [paint-by-example](https://github.com/Fantasy-Studio/Paint-by-Example)

### Credit
Huge thanks to runway-ml for the inpainting model, [huggingface](https://github.com/huggingface/diffusers) for providing an easy to use inpainting pipeline.
