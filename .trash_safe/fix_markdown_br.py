import re

with open('components/ChatView.tsx', 'r') as f:
    text = f.read()

# Since we might not want to install rehype-raw, we just replace <br> with \n directly in the text before rendering
tgt = """        <ReactMarkdown
          remarkPlugins={[remarkGfm]}"""
repl = """        <ReactMarkdown
          remarkPlugins={[remarkGfm]}"""

tgt_main = """  if (thinkStart !== -1) {
    const thinkEnd = content.indexOf('</think>');
    if (thinkEnd !== -1) {
      thinkContent = content.substring(thinkStart + 7, thinkEnd);
      mainContent = content.substring(thinkEnd + 8);
    } else {
      thinkContent = content.substring(thinkStart + 7);
      mainContent = '';
    }
  }"""
repl_main = """  if (thinkStart !== -1) {
    const thinkEnd = content.indexOf('</think>');
    if (thinkEnd !== -1) {
      thinkContent = content.substring(thinkStart + 7, thinkEnd);
      mainContent = content.substring(thinkEnd + 8);
    } else {
      thinkContent = content.substring(thinkStart + 7);
      mainContent = '';
    }
  }
  
  if (mainContent) {
    mainContent = mainContent.replace(/<br\\s*\\/?>/gi, '\\n');
  }"""

if tgt_main in text:
    text = text.replace(tgt_main, repl_main)

with open('components/ChatView.tsx', 'w') as f:
    f.write(text)

