import re

with open('components/ChatView.tsx', 'r') as f:
    text = f.read()

target = '''                if (data.content) {'''
ui = '''                if (data.suggestions) {
                  setMessages(prev => {
                    const newMsgs = [...prev];
                    newMsgs[newMsgs.length - 1].suggestions = data.suggestions;
                    return newMsgs;
                  });
                } else if (data.content) {'''
if target in text:
    text = text.replace(target, ui)
else:
    print('Target not found')

with open('components/ChatView.tsx', 'w') as f:
    f.write(text)

