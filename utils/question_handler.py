# utils/question_handler.py

from utils.document_fetcher import fetch_documentation, parse_documentation

CDP_DOCS = {
    'segment': 'https://segment.com/docs/?ref=nav',
    'mparticle': 'https://docs.mparticle.com/',
    'lytics': 'https://docs.lytics.com/',
    'zeotap': 'https://docs.zeotap.com/home/en-us/'
}

def handle_question(question):
    for cdp, url in CDP_DOCS.items():
        if cdp in question.lower():
            html_content = fetch_documentation(url)
            if html_content:
                doc_text = parse_documentation(html_content)
                # Simple keyword search for demonstration purposes
                if 'set up a new source' in question.lower():
                    return extract_relevant_info(doc_text, 'set up a new source')
                elif 'create a user profile' in question.lower():
                    return extract_relevant_info(doc_text, 'create a user profile')
                elif 'build an audience segment' in question.lower():
                    return extract_relevant_info(doc_text, 'build an audience segment')
                elif 'integrate my data' in question.lower():
                    return extract_relevant_info(doc_text, 'integrate my data')
    return "Sorry, I couldn't find the information you are looking for."

def extract_relevant_info(doc_text, keyword):
    # This is a placeholder for a more sophisticated extraction logic
    start_idx = doc_text.lower().find(keyword)
    if start_idx != -1:
        end_idx = start_idx + 300  # Extract 300 characters for context
        return doc_text[start_idx:end_idx]
    return "Relevant information not found in the documentation."