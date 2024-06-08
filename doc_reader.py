import textract
import re


class DocReader:
    pattern = r"(?P<heading>\w+)\s*-\s*\n\s*(?P<content>.*?)(?=(?:\n[^\n]+?\s*-\s*)|\s*$)"

    def read_doc(self, file_path):
        print("Extracting data from: " + str(file_path) + ".....................")
        text = textract.process(file_path).decode('utf-8')
        matches = re.finditer(self.pattern, text, re.DOTALL)
        result = {}
        for match in matches:
            heading = match.group('heading').strip()
            heading = re.sub(r'\s+', ' ', heading)
            content = match.group('content').strip()
            content = re.sub(r'\s+', ' ', content)
            result[heading] = content
        print("Data Extracted!!\n\n")
        return result
