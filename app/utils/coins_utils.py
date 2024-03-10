import re
def extract_name_from_webhook_message(message: str) -> str:
    regex_pattern = r"^(.*?)\s*\("
    result = re.search(regex_pattern, message)
    return result.group(1)
    
    