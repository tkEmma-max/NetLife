from PIL import Image

from .gemini_service import model
from .prompts import ANALYSIS_PROMPT

def analyze_image(image_path):

    image = Image.open(image_path)

    response = model.generate_content(
        [
            ANALYSIS_PROMPT,
            image
        ]
    )

    return response.text