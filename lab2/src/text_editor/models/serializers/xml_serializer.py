from xml.etree import ElementTree
from ...interfaces import ISerializer
from ...models.documents.document import Document
from ...models.documents.md_document import MarkdownDocument


class XmlSerializer(ISerializer):
    def serialize(self,
                  data: dict) -> str:
        root = ElementTree.Element('root')
        self._dict_to_xml(root, data)

        return ElementTree.tostring(root, encoding='unicode')

    def deserialize(self,
                    data: str) -> dict:
        root = ElementTree.fromstring(data)

        return self._xml_to_dict(root)

    @property
    def extension(self) -> str:
        return "xml"

    def _dict_to_xml(self,
                     parent: ElementTree.Element,
                     data: dict):
        for key, value in data.items():
            elem = ElementTree.SubElement(parent, key)

            if isinstance(value, dict):
                self._dict_to_xml(elem, value)
            elif isinstance(value, list):
                for item in value:
                    sub_elem = ElementTree.SubElement(elem, 'item')

                    if isinstance(item, dict):
                        self._dict_to_xml(sub_elem, item)
                    else:
                        sub_elem.text = str(item)
            else:
                elem.text = str(value)

    def _xml_to_dict(self,
                     element) -> dict:
        result = {}

        for child in element:
            content = self._xml_to_dict(child) if len(child) else child.text

            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(content)
            else:
                result[child.tag] = list(content.values()) if isinstance(content, dict) and 'item' in content.keys() \
                    else content

        print(result)
        return result


class DocumentToXmlSerializerAdapter(XmlSerializer):
    def __init__(self,
                 document: Document):
        self.__document = document

    def serialize(self,
                  data: Document = None) -> str:
        doc = data if data is not None else self.__document

        return super().serialize(doc.to_dict())

    def deserialize(self,
                    data: str):
        data = super().deserialize(data)

        return MarkdownDocument().from_dict(data)

