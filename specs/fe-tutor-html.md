# Spec: FE Mechanical Exam Tutor — HTML Web App

## Objective
A single self-contained HTML file that replaces the Python CLI tutor.
Opens in any browser, works fully offline, no server or internet required.
Teaches, quizzes, and tracks progress toward passing the NCEES FE Mechanical exam.

## Constraints
- ONE file: fe_tutor.html — all CSS and JavaScript inline, zero external dependencies
- No CDN links, no imports, no network calls — must work with file:// protocol
- All 112 problems embedded as a JavaScript array
- All topic content (concepts, handbook refs) embedded as JS objects
- Progress stored in localStorage — persists between browser sessions
- Must work in Safari, Chrome, Firefox on macOS

## Requirements

### 1. Layout — Single Page App
1.1 A fixed sidebar (left, ~220px) with:
    - App title "FE Mechanical Tutor"
    - Days to exam countdown (large, prominent)
    - Week number + current week topic name
    - Nav links: Dashboard, This Week, Topics, Handbook, Progress, Settings
1.2 A main content area (right) that swaps content based on nav selection
1.3 Responsive: sidebar collapses on narrow screens

### 2. Dashboard View (default on open)
2.1 Welcome header: "Week N of 11 — [Topic Name]"
2.2 Horizontal topic readiness grid: all 14 topics shown as cards with:
    - Topic name, question count range
    - Status badge: ✅ Strong / 🟡 Moderate / 🔴 Weak (from baseline, overridden by quiz accuracy)
    - Click card → goes to topic detail
2.3 Weekly hours progress bar (logged hours / 13h target)
2.4 Quick-action buttons: "Study This Week's Topic" and "Quiz This Week's Topic"

### 3. Topics View
3.1 List of all 14 topics with name, q_range, baseline status, accuracy if quizzed
3.2 Clicking a topic opens Topic Detail with two tabs: Study | Quiz

### 4. Study Mode (per topic)
4.1 Concept cards shown one at a time with:
    - Concept title
    - Full explanation text (preformatted, monospace for formulas)
    - "📖 Handbook p.XX" badge
4.2 Navigation: Previous / Next buttons + concept counter (1/4)
4.3 "Quiz me on this topic" button at bottom of last concept card
4.4 At least 3 concepts per topic (pulled from TOPICS data)

### 5. Quiz Mode (per topic)
5.1 Problem card showing:
    - Topic + subtopic + difficulty badge (color-coded: green/yellow/red)
    - Question text
    - Four answer buttons (A / B / C / D) as large clickable cards
    - Live elapsed timer (counts up from 0:00, turns orange at 2:00, red at 4:00)
5.2 On answer click:
    - Correct: button turns green, show ✅ with solution panel sliding in below
    - Incorrect: clicked button turns red, correct button turns green, show solution
    - Solution panel shows: full worked solution + "📖 Handbook p.XX"
    - "Next Problem" button appears after answering
5.3 Session stats bar at top: X/Y correct | avg time | streak
5.4 Hard problems excluded by default (toggle in Settings)
5.5 Problems not repeated in same session; seen IDs tracked in localStorage
5.6 Session summary modal on exit: score, accuracy %, topics covered, weak areas

### 6. Handbook Navigator
6.1 Search box — as user types, results filter live (no submit needed)
6.2 Results show: page number (large, bold) + description
6.3 Covers 50+ keywords across all 14 topic sections

### 7. Progress View
7.1 Accuracy % per topic shown as a horizontal bar chart
7.2 Total problems attempted, total correct, overall accuracy
7.3 Recent sessions list (date, topic, score)
7.4 Wrong problems list with "Review" button to re-quiz them
7.5 "Reset All Progress" button (with confirmation)

### 8. Settings View
8.1 Exam date picker (updates days-to-exam countdown live)
8.2 Log study hours for current week (number input + "Add Hours" button)
8.3 Toggle: Include hard problems (default OFF)
8.4 Study start date display (set on first open, not editable — it's your Day 1)

### 9. First Run
9.1 On first open (no localStorage), set study_start to today
9.2 Show a brief welcome modal: "Welcome! Your Week 1 starts today."
9.3 Initialize all progress to zero / baseline defaults

### 10. Visual Design
10.1 Clean, modern look: dark navy sidebar (#1e2a3a), white content area
10.2 Card-based layout with subtle box shadows
10.3 Color system: green (#22c55e) correct, red (#ef4444) incorrect,
     amber (#f59e0b) warning, blue (#3b82f6) primary action
10.4 Smooth transitions on view changes (100ms fade)
10.5 Monospace font for formulas/code sections (system-ui monospace)
10.6 Exam tips rotate in the sidebar footer area

## Definition of Done
- [ ] Opens in browser with double-click, no server needed
- [ ] Dashboard shows Week 1, correct topic, and days-to-exam on first open
- [ ] All 14 topics accessible and clickable
- [ ] Study mode shows concept cards with handbook page refs
- [ ] Quiz mode: clicking an answer reveals correct/incorrect + full solution
- [ ] Timer counts up and changes color at 2:00 and 4:00
- [ ] Progress persists after closing and reopening the browser
- [ ] Handbook navigator filters live as user types
- [ ] Settings: exam date updates countdown; hours logging works
- [ ] No console errors on open; works in Safari and Chrome
