import textract
import re


class DocReader:
    pattern = r"(?P<heading>\w+)\s*-\s*\n\s*(?P<content>.*?)(?=(?:\n[^\n]+?\s*-\s*)|\s*$)"
    prompt_pattern = r"(?P<prompt>[^:]+)\s*:\s*(?P<image>[^\n]+)"
    title = "Caption Title - "
    story = "Story - "
    lesson = "The Lesson - "
    prompts_and_images = "Prompts - "

    def read_doc_using_regex(self, file_path):
        print("Extracting data from: " + str(file_path) + ".....................")
        text = textract.process(file_path).decode('utf-8')
        matches = re.finditer(self.pattern, text, re.DOTALL)
        result = {}
        for match in matches:
            heading = match.group('heading').strip()
            heading = re.sub(r'\s+', ' ', heading)
            content = match.group('content').strip()
            if heading.lower() == "prompts":
                prompt_matches = re.finditer(self.prompt_pattern, content)
                prompts_and_images = []
                for prompt_match in prompt_matches:
                    prompts_and_images.append([
                        prompt_match.group("prompt").strip(), prompt_match.group("image").strip()
                    ])
                result[heading] = prompts_and_images
            else:
                content = re.sub(r'\s+', ' ', content)
                result[heading] = content
        print("Data Extracted!!\n\n")
        return result

    def read_doc(self, file_path):
        print("Extracting data from: " + str(file_path) + ".....................")
        text = textract.process(file_path).decode('utf-8')
        text = re.sub(r'\s+', ' ', text)

        title_start_idx = text.find(self.title) + len(self.title)
        title_end_idx = text.find(self.story, title_start_idx)
        story_start_idx = title_end_idx + len(self.story)
        story_end_idx = text.find(self.lesson, story_start_idx)
        lesson_start_idx = story_end_idx + len(self.lesson)
        lesson_end_idx = text.find(self.prompts_and_images, lesson_start_idx)
        prompts_start_idx = lesson_end_idx + len(self.prompts_and_images)

        title = text[title_start_idx: title_end_idx].strip()
        story = text[story_start_idx: story_end_idx].strip()
        lesson = text[lesson_start_idx: lesson_end_idx].strip()
        prompts = text[prompts_start_idx: ].strip()

        pattern = re.compile(r'(.+?)\s*:\s*(\S+)\s*')
        matches = pattern.findall(prompts)
        prompts_and_images = [[description.strip(), filename.strip()] for description, filename in matches]

        print("Data Extracted!!\n\n")
        return {
            "Title": title,
            "Story": story,
            "Lesson": lesson,
            "Prompts": prompts_and_images
        }
