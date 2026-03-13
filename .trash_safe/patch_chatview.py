import re

with open('components/ChatView.tsx', 'r') as f:
    text = f.read()

# Add `suggestions?: string[];` to interface Message
text = text.replace("  isError?: boolean;\n}", "  isError?: boolean;\n  suggestions?: string[];\n}")

# Fix message processing in `handleSubmit` where it receives stream
chunk_processor = '''              if (data.metadata) {
                setMessages(prev => {
                  const newMsgs = [...prev];
                  newMsgs[newMsgs.length - 1].metadata = data.metadata;
                  return newMsgs;
                });
              } else if (data.suggestions) {
                setMessages(prev => {
                  const newMsgs = [...prev];
                  newMsgs[newMsgs.length - 1].suggestions = data.suggestions;
                  return newMsgs;
                });
              } else if (data.content) {'''

text = text.replace('''              if (data.metadata) {
                setMessages(prev => {
                  const newMsgs = [...prev];
                  newMsgs[newMsgs.length - 1].metadata = data.metadata;
                  return newMsgs;
                });
              } else if (data.content) {''', chunk_processor)


# Render suggestions in MessageItem
# Locate `          <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">`
ui_injection = '''          {message.suggestions && message.suggestions.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-3 mb-1">
              {message.suggestions.map((sug, i) => (
                <button 
                  key={i} 
                  onClick={() => {
                    // Find ChatView's setInput value, but wait, it's defined outside!
                    // We need to pass onSuggestionClick down to MessageItem!
                  }}
                  className="text-xs px-3 py-1.5 rounded-full bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-800/50 hover:bg-blue-100 dark:hover:bg-blue-800/40 transition-colors text-left"
                >
                  {sug}
                </button>
              ))}
            </div>
          )}
          
          <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">'''

# Since MessageItem does not take onSuggestionClick, we should just emit window event or add prop.
# Let's add prop to MessageItem: `onSuggestionClick?: (text: string) => void`
text = text.replace("interface MessageItemProps {\n  message: Message;\n}", "interface MessageItemProps {\n  message: Message;\n  onSuggestionClick?: (text: string) => void;\n}")
text = text.replace("const MessageItem = React.memo(({ message }: MessageItemProps) => {", "const MessageItem = React.memo(({ message, onSuggestionClick }: MessageItemProps) => {")

ui_injection_real = '''          {message.suggestions && message.suggestions.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-3 mb-1">
              {message.suggestions.map((sug, i) => (
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

text = text.replace('          <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">', ui_injection_real)

# Now pass the prop in map
text = text.replace('<MessageItem key={message.id} message={message} />', '<MessageItem key={message.id} message={message} onSuggestionClick={(sug) => { setInput(sug); setTimeout(() => handleSubmit(undefined, sug), 100); }} />')

with open('components/ChatView.tsx', 'w') as f:
    f.write(text)

