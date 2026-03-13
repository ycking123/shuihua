import re

with open('components/ChatView.tsx', 'r') as f:
    text = f.read()

target1 = 'const MessageItem = React.memo(({ msg }: { msg: Message }) => {'
if target1 in text:
    text = text.replace(target1, 'const MessageItem = React.memo(({ msg, onSuggestionClick }: { msg: Message, onSuggestionClick?: (text: string) => void }) => {')
else:
    print('Target 1 not found')

target2 = '          <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">'
ui = '''          {msg.suggestions && msg.suggestions.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-3 mb-1">
              {msg.suggestions.map((sug, i) => (
                <button 
                  key={i} 
                  onClick={() => onSuggestionClick && onSuggestionClick(sug)}
                  className="text-xs px-3 py-1.5 rounded-full bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-800/50 hover:bg-blue-100 dark:hover:bg-blue-800/40 transition-colors text-left"
                >
                  {sug}
                </button>
              ))}
            </div>
          )}
          
          <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">'''
if target2 in text:
    text = text.replace(target2, ui)
else:
    print('Target 2 not found')

target3 = '<MessageItem key={msg.id} msg={msg} />'
if target3 in text:
    text = text.replace(target3, '<MessageItem key={msg.id} msg={msg} onSuggestionClick={(sug) => { setInput(sug); setTimeout(() => handleSubmit(undefined, sug), 100); }} />')
else:
    print('Target 3 not found')


with open('components/ChatView.tsx', 'w') as f:
    f.write(text)

