import json

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('function TracNghiemTab(')

before_trac = content[:start_idx]
trac_content = content[start_idx:]

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(before_trac)

with open('src/TracNghiemTab.jsx', 'w', encoding='utf-8') as f:
    f.write('import React, { useState, useEffect } from "react";\n')
    # find where to inject the props
    trac_content = trac_content.replace('function TracNghiemTab({ currentUser, userStats, setUserStats, savedSession, setSavedSession }) {', 'export default function TracNghiemTab({ currentUser, userStats, setUserStats, savedSession, setSavedSession, researchDataObj, getSrsStatus, getSrsLevel }) {')
    f.write(trac_content)

print("Split successful")
