#pip install diffusers
#pip install torch
#pip install googletrans
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from googletrans import Translator, constants
from pprint import pprint
import torch

def init():
    global translator
    translator = Translator()
    repo_id = "stabilityai/stable-diffusion-2-base"
    global pipe
    pipe = StableDiffusionPipeline.from_pretrained(repo_id, torch_dtype=torch.float16, revision="fp16")

    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")

def sd(prompt):

    image = pipe("tatar_style "+translator.translate(prompt).text, num_inference_steps=25).images[0]
    image.save("a.png")



init()


# sd("Антон")
