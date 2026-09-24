import re
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

from .models import Section


class SectionExtractor:
    def __init__(
            self,
            parser = MarkdownIt()
    ) -> None:
        self.parser = parser

    def extract_sections(self, md_text: str) -> list[Section]:
        root = self._create_ast(md_text)
        sections = []
        current_section: Section | None = None
    
        for node in root.children:
            if node.type == "heading":
                if current_section:
                    sections.append(current_section)
                header = self._extract_header(node)
                current_section = header
    
            elif node.type == "bullet_list":
                content = self._extract_bullet_list(node)
                if current_section:
                    current_section.content += content
            elif node.type == "paragraph":
                content = self._extract_paragraph(node)
                if current_section:
                    current_section.content += content
    
        if current_section:
            sections.append(current_section)
    
        return sections
    def _extract_header(
            self,
            node: SyntaxTreeNode
    ) -> Section:
        for sub_node in node.walk():
            if sub_node.type == "text":
                header = sub_node.content
                current_section = Section(
                    self._sanitize_header(header), 
                    ""
                )
                return current_section

        raise Exception("No text found in a header")

    def _extract_image(
            self, 
            node:SyntaxTreeNode
    ) -> str:
        attrs = node.attrs

        src = attrs.get("src", "")
        alt = attrs.get("alt", "")
        return f"![{alt}](assets/{src})"

    def _extract_bullet_list(
            self, 
            node: SyntaxTreeNode
    ) -> str:
        content = ""
        for sub_node in node.walk():
                if sub_node.type == "paragraph":
                    content += "\n\n"
                elif sub_node.type == "text":
                    content += sub_node.content
                elif sub_node.type == "image":
                    image_str = self._extract_image(sub_node)
                    content += image_str

        return content

    def _extract_paragraph(
            self, 
            node: SyntaxTreeNode
    ) -> str:
        content = ""
        for sub_node in node.walk():
            if sub_node.type == "text":
                content += f"{sub_node.content}"
            elif sub_node.type == "paragraph":
                content += "\n\n"
            elif sub_node.type == "image":
                image_str = self._extract_image(sub_node)
                content += f"\n\n{image_str}"

        return content

    @staticmethod
    def _sanitize_header(header_name: str) -> str:
        header_name = re.sub(r'[\\/*?:"<>|]+', "-", header_name)
        if header_name:
            return header_name.strip(" -")
        return "no_title"
    
    def _create_ast(self, md_text: str) -> SyntaxTreeNode:
        tokens = self.parser.parse(md_text)

        return SyntaxTreeNode(tokens)