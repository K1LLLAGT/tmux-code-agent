# Q11 Android IME / Browser Matrix

## Device

- Model: SM-T870
- Android: 13
- API: 33
- Active IME: Samsung Keyboard
- IME component: com.samsung.android.honeyboard/.service.HoneyBoardService

## Browser Matrix

### Chrome

Package: com.android.chrome

#### Editor

- [ ] ASCII typing
- [ ] Uppercase typing
- [ ] Spaces
- [ ] Backspace
- [ ] Enter/newline
- [ ] Punctuation
- [ ] Unicode
- [ ] Paste
- [ ] Selection
- [ ] Copy
- [ ] Autocorrect/composition
- [ ] No duplicated composition
- [ ] Keyboard resize usable

Result: NOT TESTED

#### Terminal

- [ ] ASCII typing
- [ ] Backspace
- [ ] Enter
- [ ] Tab
- [ ] Ctrl+C
- [ ] Ctrl+D
- [ ] Arrow keys
- [ ] Unicode
- [ ] Paste
- [ ] Punctuation
- [ ] No duplicated composition
- [ ] Keyboard resize usable

Result: NOT TESTED

---

### Samsung Browser

Package: com.sec.android.app.sbrowser

#### Editor

- [ ] ASCII typing
- [ ] Uppercase typing
- [ ] Spaces
- [ ] Backspace
- [ ] Enter/newline
- [ ] Punctuation
- [ ] Unicode
- [ ] Paste
- [ ] Selection
- [ ] Copy
- [ ] Autocorrect/composition
- [ ] No duplicated composition
- [ ] Keyboard resize usable

Result: NOT TESTED

#### Terminal

- [ ] ASCII typing
- [ ] Backspace
- [ ] Enter
- [ ] Tab
- [ ] Ctrl+C
- [ ] Ctrl+D
- [ ] Arrow keys
- [ ] Unicode
- [ ] Paste
- [ ] Punctuation
- [ ] No duplicated composition
- [ ] Keyboard resize usable

Result: NOT TESTED

---

### Tor Browser

Package: org.torproject.torbrowser

#### Editor

- [ ] ASCII typing
- [ ] Uppercase typing
- [ ] Spaces
- [ ] Backspace
- [ ] Enter/newline
- [ ] Punctuation
- [ ] Unicode
- [ ] Paste
- [ ] Selection
- [ ] Copy
- [ ] Autocorrect/composition
- [ ] No duplicated composition
- [ ] Keyboard resize usable

Result: NOT TESTED

#### Terminal

- [ ] ASCII typing
- [ ] Backspace
- [ ] Enter
- [ ] Tab
- [ ] Ctrl+C
- [ ] Ctrl+D
- [ ] Arrow keys
- [ ] Unicode
- [ ] Paste
- [ ] Punctuation
- [ ] No duplicated composition
- [ ] Keyboard resize usable

Result: NOT TESTED

## Overall

Status: DEFERRED

Reason: The actual TCA CodeMirror and xterm.js browser surfaces do not yet exist in Milestone 0, so the real IME/browser interaction cannot honestly be exercised yet.
