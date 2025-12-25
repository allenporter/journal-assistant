class ImageGenTool:
    def generate_image(self, prompt: str) -> str:
        """
        Generates an image based on a text prompt.

        Args:
            prompt (str): The description of the image to generate.

        Returns:
            str: A URL or description of the generated image.
        """
        return f"Image generated for prompt: '{prompt}'. (Mock URL: http://example.com/image.png)"
