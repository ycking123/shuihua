import re

with open('components/PersonalView.tsx', 'r') as f:
    text = f.read()

# Replace React imports to include useEffect
text = text.replace("import React, { useState } from 'react';", "import React, { useState, useEffect } from 'react';")

# Locate the start of PersonalView component
match = re.search(r'const PersonalView: React\.FC = \(\) => {.*?\n(\s+)const \[memo, setMemo\]', text, re.DOTALL)
if match:
    indent = match.group(1)
    
    state_injection = indent + "const [profile, setProfile] = useState({ name: '吴志雄', role: '总裁', username: 'X-ESSENCE-001' });\n"
    state_injection += indent + "useEffect(() => {\n"
    state_injection += indent + "  let ignore = false;\n"
    state_injection += indent + "  const fetchProfile = async () => {\n"
    state_injection += indent + "    try {\n"
    state_injection += indent + "      const token = localStorage.getItem('token');\n"
    state_injection += indent + "      if (!token) return;\n"
    state_injection += indent + "      const baseUrl = import.meta.env.DEV ? '/api' : `http://${window.location.hostname}:8000/api`;\n"
    state_injection += indent + "      const res = await fetch(`${baseUrl}/auth/me`, { headers: { 'Authorization': `Bearer ${token}` } });\n"
    state_injection += indent + "      const data = await res.json();\n"
    state_injection += indent + "      if (!ignore && data.nick_name) {\n"
    state_injection += indent + "        setProfile({ name: data.nick_name, role: data.position || '员工', username: data.username });\n"
    state_injection += indent + "      }\n"
    state_injection += indent + "    } catch (e) { console.error('Failed fetching profile', e); }\n"
    state_injection += indent + "  };\n"
    state_injection += indent + "  fetchProfile();\n"
    state_injection += indent + "  return () => { ignore = true; };\n"
    state_injection += indent + "}, []);\n\n"
    
    # insert state and effect
    text = text.replace(match.group(0), "const PersonalView: React.FC = () => {\n" + state_injection + indent + "const [memo, setMemo]")
    
    # Replace hardcoded html
    text = text.replace('>吴志雄<', '>{profile.name}<')
    text = text.replace('>总裁<', '>{profile.role}<')
    text = text.replace('>X-ESSENCE-001<', '>{profile.username}<')
    
    with open('components/PersonalView.tsx', 'w') as f:
        f.write(text)

