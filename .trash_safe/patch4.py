import re

with open('components/ChatView.tsx', 'r') as f:
    text = f.read()

target2 = '              <AgentMessageContent content={msg.content || \'\'} />'
ui = '''              <AgentMessageContent content={msg.content || ''} />
              {msg.suggestions && msg.suggestions.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
                  {msg.suggestions.map((sug, i) => (
                    <button 
                      key={i} 
                      onClick={() => onSuggestionClick && onSuggestionClick(sug)}
                      className="text-xs px-3 py-1.5 rounded-full bg-blue-50 dark:bg-blue-900/40 text-blue-600 dark:text-blue-300 border border-blue-200 dark:border-blue-700/50 hover:bg-blue-100 dark:hover:bg-blue-800/60 transition-colors text-left flex items-center gap-1.5"
                    >
                      <svg viewBox="0 0 24 24" fill="none" className="w-3 h-3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                      {sug}
                    </button>
                  ))}
                </div>
              )}'''
if target2 in text:
    text = text.replace(target2, ui)
else:
    print('Target 2 not found')

with open('components/ChatView.tsx', 'w') as f:
    f.write(text)

