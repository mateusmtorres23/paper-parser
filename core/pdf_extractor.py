from pathlib import Path

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

class PdfExtractor:
    def __init__(
            self, 
            model_dict = create_model_dict(),
    ):
        self._model_dict = model_dict
        self.converter = PdfConverter(
            artifact_dict=model_dict
        )

    def extract_pdf_info(self, source_pdf: str | Path) -> tuple[str, dict]:
        rendered = self.converter(str(source_pdf))
        md_text, _, images = text_from_rendered(rendered)
        
        return md_text, images
        