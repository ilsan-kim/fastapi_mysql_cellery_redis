from app.crud.base import CRUDBase
from app.models.paragraph import Paragraph
from app.schemas.paragraph import ParagraphCreate, ParagraphUpdate


class CRUDParagraph(CRUDBase[Paragraph, ParagraphCreate, ParagraphUpdate]):
    pass


paragraph = CRUDParagraph(Paragraph)
