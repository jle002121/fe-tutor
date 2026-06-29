# Spec: FE Mechanical Exam Tutor

## Objective
A terminal-based interactive tutor that teaches FE Mechanical exam topics,
quizzes Jacob with realistic practice problems, and tracks progress against
his 11-week study plan (target: August/September 2026 exam, first-time pass).

The tutor must mirror his proven study philosophy:
- Concept first → handbook location → practice problem → timed solve
- Never memorize; always know where to look
- Problem-driven: passive reading doesn't count

## Requirements

### 1. Startup & Dashboard
1.1 On launch, show a dashboard with:
    - Current week number and dates (auto-calculated from Jun 9 start)
    - Current week's primary topic(s)
    - Hours studied this week (tracked in progress.json)
    - Topic readiness summary (✅ Strong, 🟡 Moderate, 🔴 Weak) per his baseline
    - Days until target exam (Aug 25, 2026 placeholder — updatable)

### 2. Topic Menu
2.1 List all 14 FE Mechanical topics with question count ranges and his baseline status
2.2 Mark the current week's topic(s) with a "▶ THIS WEEK" indicator
2.3 User selects a topic by number

### 3. Study Mode (per topic)
3.1 Show topic overview: subtopics, handbook page, question count range
3.2 Present 3–5 key concept explanations written for the FE exam context
3.3 Show exactly where in the FE Reference Handbook 10.6 to find each formula
    (page numbers from the study plan's navigation map)
3.4 After each concept, offer: "Got it [g] | Quiz me on this [q] | Next concept [n]"

### 4. Quiz Mode
4.1 Serve a practice problem with:
    - Problem text
    - Answer choices (A/B/C/D)
    - A visible countdown timer (2-minute target per problem — FE pacing)
4.2 After the user answers:
    - Show correct/incorrect immediately
    - Show full worked solution step-by-step
    - Show which handbook page/formula was used
    - Difficulty level (easy/medium/hard)
4.3 Problems come from an embedded problem bank (see Problem Bank below)
4.4 Problems are sourced/tagged from journey2pe.com topic categories
4.5 Skip hard problems during study (flag them, serve easy/medium by default)
    — user can toggle "include hard" in settings
4.6 Never repeat a problem in the same session; track seen problems in progress.json

### 5. Problem Bank
5.1 Minimum 8 problems per topic (14 topics × 8 = 112+ problems minimum)
5.2 Each problem has: id, topic_id, subtopic, difficulty (easy/medium/hard),
    question, choices (A-D), answer, solution, handbook_page, source
5.3 Problems cover the NCEES subtopics verbatim from the spec
5.4 Problems are realistic FE-style: numbers, units, multiple-choice, 2-min solve time
5.5 All 14 topics must have problems: Math, Prob/Stats, Ethics, Econ, E&M, Statics,
    Dynamics, MOM, Materials, Fluids, Thermo, Heat Transfer, MIC, Mech Design

### 6. Progress Tracking
6.1 After each quiz session, save to progress.json:
    - Topic attempted, problems seen (IDs), correct/incorrect, time per problem
    - Session date and duration
6.2 Show a running accuracy % per topic
6.3 Flag topics where accuracy < 70% as needing review (override their baseline if needed)
6.4 Show problems answered wrong — offer to retry them in next session
6.5 Track total study hours (user confirms session length on exit)

### 7. Exam Strategy Reminders
7.1 On exit, show one rotating exam tip from the strategy section:
    - 2-minute rule, flag-and-move, unit-check-first, handbook navigation speed
7.2 Before a quiz session, remind the user of the difficulty strategy
    (Easy: <90s, Medium: 2-3 min, Hard: flag and move)

### 8. Handbook Navigator
8.1 A dedicated "Find it fast" mode: user types a topic keyword,
    tutor instantly shows the handbook page number and what to look for there
8.2 Covers all 14 sections from the navigation map

### 9. Week-by-Week Mode
9.1 "This week" shortcut: immediately enters study+quiz for the current week's topic
9.2 Tracks hours logged per week toward the 13 hr/week target
9.3 Shows a weekly progress bar (hours logged / 13 target)

### 10. Configuration
10.1 All config in config.json: exam_date, study_start_date, weekly_hour_target
10.2 User can set/update exam date from within the tutor
10.3 Settings persist between sessions

## Edge Cases
- Week 10 and 11 are full practice exam weeks — tutor enters "exam simulation mode":
  serve 110 questions timed across 5h 20min (no feedback until the end)
- Topics 3 (Ethics) and 4 (Economics): limited math — quiz mode adapts to
  concept/scenario questions rather than calculation problems
- If no progress.json exists on first launch, initialize with baseline scores from
  the study plan (Strong/Moderate/Weak mapping)
- Handle week overflow (if past week 11, show "Exam week — good luck!" mode)
- Problem timer: if user takes >4 minutes, auto-flag the problem as "over-time"

## Constraints
- Pure Python 3, single file (fe_tutor.py) plus problems.json and progress.json
- No external dependencies beyond Python stdlib (use only: json, time, datetime,
  os, sys, textwrap, random — no pip installs required)
- Terminal-only: plain text formatting using ASCII (no rich/curses required)
- All problems embedded in problems.json — no network calls required during quiz
  (journey2pe.com problems are sourced and embedded at build time)
- Must run with: python3 fe_tutor.py
- Problem bank: 8+ problems per topic, written in authentic FE exam style

## Definition of Done
- [ ] Dashboard shows correct week, topic, and days-to-exam on launch
- [ ] All 14 topics accessible from main menu with correct metadata
- [ ] Study mode presents concepts + handbook page refs for at least 3 topics
- [ ] Quiz mode presents a problem, accepts A/B/C/D input, shows correct answer + solution
- [ ] Timer counts up during quiz and flags problems over 2 minutes
- [ ] Progress saves to progress.json and loads correctly on next launch
- [ ] Handbook navigator returns correct page for at least 10 topic keywords
- [ ] Problem bank has 8+ problems for every single topic (14 × 8 = 112 minimum)
- [ ] "This week" shortcut works and shows the correct current week topic
- [ ] No external dependencies — runs with python3 fe_tutor.py on a fresh machine
