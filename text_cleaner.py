import re

class TextCleaner:
    def clean(self, text: str) -> str:
        text = text.lower()
        text=re.sub(r"\s+"," ",text)
        
        text = re.sub(r"[^\w\s+#.]","",text)
        text=text.strip()
        
        return text