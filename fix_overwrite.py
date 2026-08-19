import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Rewrite buildNewSrs
old_buildNewSrs = """const buildNewSrs = (item, skillToUpdate, newStatus, newStreak) => {
   let srs = { ...item.srs };
   if (srs.status && typeof srs.status === 'string') {
      const oldStatus = srs.status;
      const oldStreak = srs.streak || 0;
      srs = {};
      SKILLS.forEach(s => {
         srs[s.id] = { status: s.id === 'chiettu' ? oldStatus : 'bat_dau', streak: s.id === 'chiettu' ? oldStreak : 0 };
      });
   } else {
      SKILLS.forEach(s => {
         if (!srs[s.id]) srs[s.id] = { status: 'bat_dau', streak: 0 };
      });
   }
   
   if (skillToUpdate) {
      if (!srs[skillToUpdate]) srs[skillToUpdate] = {};
      srs[skillToUpdate].status = newStatus;
      srs[skillToUpdate].streak = newStreak;
   }
   return srs;
};"""

new_buildNewSrs = """const buildNewSrs = (item, skillToUpdate, newStatus, newLevel) => {
   let srs = { ...item.srs };
   if (srs.status && typeof srs.status === 'string') {
      const oldStatus = srs.status;
      const oldLevel = srs.level || srs.streak || 0;
      srs = {};
      SKILLS.forEach(s => {
         srs[s.id] = { status: s.id === 'chiettu' ? oldStatus : 'bat_dau', level: s.id === 'chiettu' ? oldLevel : 0 };
      });
   } else {
      SKILLS.forEach(s => {
         if (!srs[s.id]) srs[s.id] = { status: 'bat_dau', level: 0 };
      });
   }
   
   if (skillToUpdate) {
      if (!srs[skillToUpdate]) srs[skillToUpdate] = {};
      srs[skillToUpdate].status = newStatus;
      srs[skillToUpdate].level = newLevel;
   }
   return srs;
};"""
content = content.replace(old_buildNewSrs, new_buildNewSrs)


# 2. Rewrite handleMoveAllToReady
old_handleMove = """    const handleMoveAllToReady = async (charObj) => {
      const originalSrs = { ...charObj.srs };
      
      let newSrs = { ...charObj.srs };
      SKILLS.forEach(skill => {
         newSrs = buildNewSrs({srs: newSrs}, skill.id, 'san_sang_thi', 0);
      });
      
      charObj.srs = newSrs;"""

new_handleMove = """    const handleMoveAllToReady = async (charObj) => {
      const originalSrs = { ...charObj.srs };
      
      // Upgrade format if needed
      let newSrs = buildNewSrs({ srs: charObj.srs }, null, null, null);
      
      // ONLY promote bat_dau to san_sang_thi, preserve existing progress!
      SKILLS.forEach(skill => {
         if (newSrs[skill.id].status === 'bat_dau') {
             newSrs[skill.id].status = 'san_sang_thi';
             newSrs[skill.id].level = 0;
         }
      });
      
      charObj.srs = newSrs;"""
content = content.replace(old_handleMove, new_handleMove)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed overwriting bug")
