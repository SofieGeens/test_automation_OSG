import xml.dom.minidom


class MissingHeaderFile(FileNotFoundError):
    """Raised when attempting to read a header file where none exists."""


class BrtHeaderReader:
    """
    Reader for a single BrainRT header.

    Attributes:
        path: Path of the BrainRT header file
    """

    def __init__(self, path):
        self.text_data = None
        self.info = None

        self.read_header(path)
        self.info_labels = {"MeasurementInfo":
                                {"StartDateAndTime"},
                            "PatientInfo":
                                {"DateOfBirth"}
                            }
        self.parse_header()

    def read_header(self, path):
        with open(path, 'rb') as handle:
            raw_data = handle.read()
        text_data = raw_data.decode(encoding='utf-8', errors='ignore')
        self.text_data = ''.join([char for char in text_data
                                  if self.is_printable(char)])

    def parse_header(self):
        self.info = {}
        for info_type in self.info_labels:
            type_xml = self.extract_xml(info_type)
            self.info[info_type] = {
                sub_type: self.extract_field(type_xml, sub_type) for sub_type in
                self.info_labels[info_type]}

    def extract_xml(self, info_type):
        start_str = '<{}'.format(info_type)
        start = self.text_data.find(start_str)
        end_str = '</{}>'.format(info_type)
        end = self.text_data.find(end_str)
        end += len(end_str)
        type_data = self.text_data[start:end]
        while '> ' in type_data:
            type_data = type_data.replace('> ', '>')
        return xml.dom.minidom.parseString(type_data)

    @staticmethod
    def extract_field(type_xml, sub_type):
        elements = type_xml.getElementsByTagName(sub_type)
        try:
            return elements[0].firstChild.nodeValue
        except IndexError:
            return None

    @staticmethod
    def is_printable(char):
        return len(repr(char)) == len(char) + 2
