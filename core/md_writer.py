from pathlib import Path

from .section_extractor import SectionExtractor


class MarkdownWriter:
    def __init__(
            self,
            paper_src: Path | str,
            output_dir: Path | str,
            extractor = SectionExtractor(),
    ) -> None:
        self._paper_src = Path(paper_src)
        self._output_dir = Path(output_dir)
        self._extractor = extractor

    def write_markdown(self, md_text: str, images: dict):
        paper_folder = self._output_dir / self._paper_src.stem
        paper_folder.mkdir(parents=True, exist_ok=True)
        assets = paper_folder / "assets"
        assets.mkdir(parents=True, exist_ok=True)

        for img_name, img_obj in images.items():
            img_path = assets / img_name

            img_obj.save(img_path)

        sections = self._extractor.extract_sections(md_text)

        for section in sections:
            file_path = paper_folder / f"{section.header}.md"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(section.content)
