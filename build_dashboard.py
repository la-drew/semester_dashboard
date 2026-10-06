"""Build a self-contained semester dashboard HTML file.

The generated page has no external assets or runtime dependencies. Course data is
kept in the COURSES list below so the dashboard can be regenerated after syllabus
details are reviewed or corrected.
"""

# -----------------------------------------------------------------------------
# Section 1: Standard-library imports
# -----------------------------------------------------------------------------
from __future__ import annotations

import datetime as dt
import json
import hashlib
import re
from pathlib import Path


# -----------------------------------------------------------------------------
# Section 2: Semester and course data
# -----------------------------------------------------------------------------
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def to_iso(value) -> str | None:
    """Return a YYYY-MM-DD string, or None if the value is not a real date.

    Accepts date/datetime objects as well as ISO strings, so a field that
    changes type (or is replaced by a placeholder like "REDACTED") cannot
    break JSON serialization or the browser-side date parsing.
    """
    if isinstance(value, dt.datetime):
        return value.date().isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, str) and ISO_DATE.fullmatch(value.strip()):
        try:
            return dt.date.fromisoformat(value.strip()).isoformat()
        except ValueError:
            return None
    return None


# Semester dates may be None (the page then shows "Dates not set").
SEMESTER = {
    "name": "Fall 2026",
    "start_date": to_iso("2026-08-24"),
    "end_date": to_iso("2026-12-11"),
}

# Stable IDs are derived from syllabus content, so saved checkboxes survive a
# rebuild even if timeline rows are re-ordered.
def item(
    course_id: str,
    date: str,
    kind: str,
    title: str,
    detail: str = "",
    importance: str = "routine",
) -> dict:
    """Create one reading/task with a deterministic persistence key."""
    iso = to_iso(date)
    if iso is None:
        raise ValueError(
            f"Invalid date {date!r} for {course_id} item {title!r}; expected YYYY-MM-DD."
        )
    date = iso
    signature = f"{course_id}|{date}|{kind}|{title}".encode()
    digest = hashlib.blake2s(signature, digest_size=6).hexdigest()
    return {
        "id": f"{course_id}-{date}-{digest}",
        "date": date,
        "type": kind,
        "importance": importance,
        "title": title,
        "detail": detail,
    }


# Each reading below corresponds to an individual line (or chapter group) in a
# weekly schedule. Recommended and optional readings remain visible because the
# requested master timeline includes every reading, not only required books.
COURSES: list[dict] = [
    {
        "id": "ppd554",
        "code": "PPD 554",
        "title": "Foundations of Policy Analysis",
        "color": "#d85b3f",
        "instructor": "REDACTED",
        "meeting": "REDACTED",
        "location": "REDACTED",
        "office_hours": "REDACTED",
        "assistant": "REDACTED",
        "tools": ["Brightspace", "CATME surveys"],
        "grading": [
            {"label": "Participation, discussion boards, quizzes", "percent": 10},
            {"label": "Four lab exercises", "percent": 20},
            {"label": "Issue diagnosis memo", "percent": 15},
            {"label": "Issue diagnosis presentation", "percent": 10},
            {"label": "Policy analysis sentence outline", "percent": 5},
            {"label": "Final group presentation", "percent": 10},
            {"label": "Final communications briefer", "percent": 5},
            {"label": "Final policy analysis paper", "percent": 25},
        ],
        "textbooks": [
            {"title": "A Practical Guide for Policy Analysis: The Eightfold Path to More Effective Problem Solving", "authors": "Eugene Bardach & Eric Patashnik", "note": "7th ed. · Required"},
            {"title": "The CQ Press Writing Guide for Public Policy", "authors": "Andrew Pennock", "note": "2nd ed. · Required"},
        ],
        "timeline": [
            item("ppd554", "2026-08-27", "reading", "Class syllabus", "Required · Course overview"),
            item("ppd554", "2026-08-27", "reading", "What’s Wrong with Policy Education", "Francis Fukuyama (2018) · Required"),
            item("ppd554", "2026-08-27", "reading", "What Do Students Lose When They Stop Writing?", "Dana Goldstein (2026) · Required"),
            item("ppd554", "2026-08-27", "reading", "The Problem with Public Policy Schools", "James Piereson & Naomi Schaefer Riley (2013) · Required"),
            item("ppd554", "2026-08-27", "reading", "A Public Policy Paradox", "Alice Rivlin (1984), pp. 17–22 · Required"),
            item("ppd554", "2026-08-27", "reading", "The Once and Future School of Public Policy", "Aaron Wildavsky (1985), pp. 24–41 · Required"),
            item("ppd554", "2026-08-27", "reading", "The Historical Roots of the Field", "Peter deLeon (2008), pp. 39–57 · Recommended"),
            item("ppd554", "2026-09-03", "task", "Discussion Board #1", "Due in Brightspace"),
            item("ppd554", "2026-09-03", "reading", "How Effective Is Policy Analysis?", "John Hird (2014), pp. 60–84 · Required"),
            item("ppd554", "2026-09-03", "reading", "Professional Roles for Policy Analysts: A Critical Assessment", "Hank Jenkins-Smith (1982), pp. 88–100 · Required"),
            item("ppd554", "2026-09-03", "reading", "Policy Paradox — Introduction", "Deborah Stone (2012), pp. 1–15 · Required"),
            item("ppd554", "2026-09-03", "reading", "What Is Policy Analysis?", "David Weimer & Aidan Vining (2017), pp. 23–38 · Required"),
            item("ppd554", "2026-09-03", "reading", "Analysis of Race as Policy Analysis", "Samuel Myers Jr. (2002), pp. 169–190 · Recommended"),
            item("ppd554", "2026-09-03", "reading", "How Food Banks Use Markets to Feed the Poor", "Canice Prendergast (2017), pp. 145–162 · Recommended"),
            item("ppd554", "2026-09-03", "reading", "The Methodology of Normative Policy Analysis", "Christopher Robert & Richard Zeckhauser (2011), pp. 613–643 · Recommended"),
            item("ppd554", "2026-09-03", "reading", "Policy Analysis as a Profession and a Process", "Michael Munger (2000), pp. 1–17 · Recommended"),
            item("ppd554", "2026-09-03", "reading", "The Need for Simple Methods of Policy Analysis and Planning", "Carl Patton, David Sawicki & Jennifer Clark (2012), pp. 2–20 · Recommended"),
            item("ppd554", "2026-09-10", "task", "Discussion Board #2", "Due in Brightspace"),
            item("ppd554", "2026-09-10", "reading", "Step One: Define the Problem", "Bardach & Patashnik (2024), pp. 1–16 · Required"),
            item("ppd554", "2026-09-10", "reading", "Structuring Policy Problems", "William Dunn (2017), pp. 68–81 · Required"),
            item("ppd554", "2026-09-10", "reading", "Thinking About the Future: Prospective Policy Analysis", "Peter Linquiti (2023), pp. 13–19 · Required"),
            item("ppd554", "2026-09-10", "reading", "Dilemmas in a General Theory of Planning", "Horst Rittel & Melvin Webber (1973), pp. 155–169 · Required"),
            item("ppd554", "2026-09-10", "reading", "Causal Stories and the Formation of Policy Agendas", "Deborah Stone (1989), pp. 281–300 · Required"),
            item("ppd554", "2026-09-10", "reading", "Verifying, Defining, and Detailing the Problem", "Patton, Sawicki & Clark, pp. 140–175 · Recommended"),
            item("ppd554", "2026-09-17", "task", "Policy Interests Write-Up", "Due before class"),
            item("ppd554", "2026-09-17", "reading", "Tradecraft: Professional Writing as Problem Solving", "Juliet Musso, Robert Biller & Robert Myrtle (2000), pp. 635–646 · Required"),
            item("ppd554", "2026-09-17", "reading", "Audiences & Audience-Centered Writing in Public Policy", "Andrew Pennock (2023), ch. 1, pp. 1–12 · Required"),
            item("ppd554", "2026-09-17", "reading", "Generating and Organizing Your Argument", "Andrew Pennock (2023), ch. 2, pp. 15–36 · Required"),
            item("ppd554", "2026-09-17", "reading", "Social Construction of Target Populations", "Anne Schneider & Helen Ingram (1993), pp. 334–347 · Required"),
            item("ppd554", "2026-09-17", "reading", "Case study readings", "Titles provided with the case study · Required"),
            item("ppd554", "2026-09-17", "reading", "What to Do When Stakeholders Matter", "John Bryson (2004), pp. 21–53 · Recommended"),
            item("ppd554", "2026-09-24", "task", "Lab #1: Problem Definition", "Due before class"),
            item("ppd554", "2026-09-24", "reading", "Part II: Assembling Evidence", "Bardach & Patashnik (2024), pp. 97–123 · Required"),
            item("ppd554", "2026-09-24", "reading", "Appendix E: Incorporating Big Data and Rigorous Scientific Evidence", "Bardach & Patashnik (2024), pp. 177–180 · Required"),
            item("ppd554", "2026-09-24", "reading", "Gathering Information for Policy Analysis", "Weimer & Vining (2017), ch. 14, pp. 325–339 · Required"),
            item("ppd554", "2026-09-24", "reading", "Finding and Evaluating Sources", "Wayne Booth et al. (2024), pp. 64–98 · Recommended"),
            item("ppd554", "2026-09-24", "reading", "Module 3: In-Depth Interviews", "Natasha Mack et al. (2012) · Recommended"),
            item("ppd554", "2026-09-24", "reading", "The Politics of Evidence — Introduction", "Justin Parkhurst (2017), pp. 3–14 · Recommended"),
            item("ppd554", "2026-09-24", "reading", "The Promise of Evidence-Based Policymaking", "Commission on Evidence-Based Policymaking · Recommended"),
            item("ppd554", "2026-10-01", "task", "Issue Diagnosis Memo", "Due in Brightspace · 15%", "major"),
            item("ppd554", "2026-10-01", "task", "Lab #2: Assembling Evidence", "Due before class"),
            item("ppd554", "2026-10-01", "reading", "Step 3: Construct the Alternatives", "Bardach & Patashnik (2024), pp. 22–33 · Required"),
            item("ppd554", "2026-10-01", "reading", "Appendix B: Things Governments Do", "Bardach & Patashnik (2024), pp. 159–169 · Required"),
            item("ppd554", "2026-10-01", "reading", "Hints for Crafting Alternative Policies", "Peter J. May (1981), pp. 227–244 · Required"),
            item("ppd554", "2026-10-01", "reading", "Behavioral Assumptions of Policy Tools", "Anne Schneider & Helen Ingram (1990), pp. 510–529 · Required"),
            item("ppd554", "2026-10-01", "reading", "Correcting Market and Government Failures", "Weimer & Vining (2017), pp. 205–259 · Recommended"),
            item("ppd554", "2026-10-01", "reading", "Identifying Alternatives", "Patton, Sawicki & Clark (2012), pp. 215–237 · Recommended"),
            item("ppd554", "2026-10-15", "task", "Lab #3: Policy Alternatives", "Due before class"),
            item("ppd554", "2026-10-15", "reading", "Step 4: Select the Criteria", "Bardach & Patashnik (2024), pp. 33–50 · Required"),
            item("ppd554", "2026-10-15", "reading", "Equity", "Deborah Stone (2012) · Required"),
            item("ppd554", "2026-10-15", "reading", "Equality of What?", "Amartya Sen (1979) · Recommended"),
            item("ppd554", "2026-10-15", "reading", "Intersectionality and Public Policy", "Olena Hankivsky & Renee Cormier (2011), pp. 217–229 · Recommended"),
            item("ppd554", "2026-10-15", "reading", "Operationalizing Lasswell’s Call for Clarification of Value Goals", "Peter Linquiti (2024), pp. 193–219 · Recommended"),
            item("ppd554", "2026-10-15", "reading", "Evaluating Equity in Social Policy", "August Österle (2002), pp. 46–59 · Recommended"),
            item("ppd554", "2026-10-15", "reading", "Establishing Evaluation Criteria", "Patton, Sawicki & Clark (2012), pp. 176–206 · Recommended"),
            item("ppd554", "2026-10-22", "task", "Issue Diagnosis Group Presentation", "In class · 10%", "major"),
            item("ppd554", "2026-10-22", "reading", "Political Feasibility and Policy Analysis", "Arnold Meltsner (1972), pp. 859–867 · Required"),
            item("ppd554", "2026-10-22", "reading", "Policy Adoption", "Weimer & Vining (2017), ch. 11, pp. 259–279 · Required"),
            item("ppd554", "2026-10-22", "reading", "Democracy as Problem Solving — Introduction", "Xavier de Souza Briggs (2008), pp. 3–25 · Recommended"),
            item("ppd554", "2026-10-22", "reading", "Varieties of Participation in Complex Governance", "Archon Fung (2006), pp. 66–75 · Recommended"),
            item("ppd554", "2026-10-22", "reading", "Ten Things that Political Scientists Know That You Don’t", "Hans Noel (2010), pp. 1–19 · Recommended"),
            item("ppd554", "2026-10-22", "reading", "Policy Feedback in a Racialized Polity", "Jamila Michener (2019), pp. 1–23 · Recommended"),
            item("ppd554", "2026-10-22", "reading", "A Theory of Groups and Organizations", "Mancur Olson (1965), pp. 5–52 · Recommended"),
            item("ppd554", "2026-10-29", "reading", "Step 5: Project the Outcomes", "Bardach & Patashnik (2024), pp. 50–72 · Required"),
            item("ppd554", "2026-10-29", "reading", "An Introduction to Modeling", "Lee Friedman (2002), pp. 19–25 · Required"),
            item("ppd554", "2026-10-29", "reading", "Aiding Choices with the Criterion-Alternative Matrix", "Duncan MacRae & Dale Whittington (1997), pp. 193–228 · Required"),
            item("ppd554", "2026-10-29", "reading", "Forecasting Expected Policy Outcomes", "William Dunn (2017), pp. 118–147 · Recommended"),
            item("ppd554", "2026-10-29", "reading", "Evaluating Alternative Policies", "Patton, Sawicki & Clark (2012), pp. 243–313 · Recommended"),
            item("ppd554", "2026-11-05", "task", "Lab #4: CAM / Projecting Outcomes", "Due before class"),
            item("ppd554", "2026-11-05", "reading", "Step 6: Confront the Tradeoffs", "Bardach & Patashnik (2024), pp. 72–78 · Required"),
            item("ppd554", "2026-11-05", "reading", "Step 7: Stop, Focus, Narrow, Deepen, Decide!", "Bardach & Patashnik (2024), pp. 79–83 · Required"),
            item("ppd554", "2026-11-05", "reading", "The Science of Muddling Through", "Charles Lindblom (1959), pp. 79–88 · Required"),
            item("ppd554", "2026-11-05", "reading", "Confronting Tradeoffs", "Juliet Musso · Required"),
            item("ppd554", "2026-11-05", "reading", "Displaying Alternatives and Distinguishing among Them", "Patton, Sawicki & Clark (2012), pp. 315–337 · Recommended"),
            item("ppd554", "2026-11-12", "task", "Discussion Board #3", "Due in Brightspace"),
            item("ppd554", "2026-11-12", "task", "Policy Analysis Sentence Outline", "Due before class · 5%"),
            item("ppd554", "2026-11-12", "reading", "Why Policy Analysis and Ethics Are Incompatible", "Douglas Amy (1984), pp. 573–591 · Required"),
            item("ppd554", "2026-11-12", "reading", "Toward Professional Ethics", "Weimer & Vining (2017), pp. 42–56 · Required"),
            item("ppd554", "2026-11-12", "reading", "Thinking, Fast and Slow — excerpts", "Daniel Kahneman (2011) · Required"),
            item("ppd554", "2026-11-12", "reading", "The Nature of Implicit Prejudice", "Curtis Hardin & Mahzarin Banaji (2013), pp. 13–31 · Recommended"),
            item("ppd554", "2026-11-12", "reading", "Participatory Policy-Making Toolkit", "Antonnet Johnson & Kate Hamaji (2021) · Recommended"),
            item("ppd554", "2026-11-12", "reading", "Thin Simplifications and Practical Knowledge: Mētis", "James Scott (1998), pp. 309–341 · Recommended"),
            item("ppd554", "2026-11-12", "reading", "Economic Reasoning and the Ethics of Policy", "Thomas Schelling (1984), pp. 1–26 · Recommended"),
            item("ppd554", "2026-11-19", "reading", "Step 8: Tell Your Story", "Bardach & Patashnik (2024), pp. 84–93 · Required"),
            item("ppd554", "2026-11-19", "reading", "Landing on Your Feet: Organizing Your Policy Analysis", "Weimer & Vining (2017), pp. 340–376 · Required"),
            item("ppd554", "2026-11-19", "reading", "Pulling It All Together", "Andrew Pennock (2023), ch. 7, pp. 109–122 · Required"),
            item("ppd554", "2026-11-19", "reading", "Revising and Organizing", "Wayne Booth et al. (2024), ch. 11 · Required"),
            item("ppd554", "2026-11-19", "reading", "Revising Style: Telling Your Story Clearly", "Wayne Booth et al. (2024), ch. 15 · Required"),
            item("ppd554", "2026-11-19", "reading", "Visually Communicating: Creating and Writing About Tables", "Andrew Pennock (2023), pp. 75–92 · Recommended"),
            item("ppd554", "2026-12-03", "task", "Final Group Presentation", "In class · 10%", "major"),
            item("ppd554", "2026-12-10", "task", "Final Communications Briefer", "Final exam day · 5%"),
            item("ppd554", "2026-12-10", "task", "Final Policy Analysis Paper", "Final exam day · 25%", "major"),
        ],
    },
    {
        "id": "ppd558",
        "code": "PPD 558",
        "title": "Multivariate Statistical Analysis",
        "color": "#347a72",
        "instructor": "REDACTED",
        "meeting": "REDACTED",
        "location": "REDACTED",
        "office_hours": "REDACTED",
        "assistant": "REDACTED",
        "tools": ["Stata/BE 17+", "Laptop", "Brightspace", "VMware Horizon (CloudApps option)"],
        "grading": [
            {"label": "Problem sets", "percent": 15},
            {"label": "In-class activities and participation", "percent": 15},
            {"label": "Analysis project", "percent": 25},
            {"label": "Midterm exam", "percent": 20},
            {"label": "Final exam", "percent": 25},
        ],
        "textbooks": [],
        "timeline": [
            item("ppd558", "2026-08-25", "reading", "Using Econometrics — ch. 17", "A.H. Studenmund, 6th ed. · Optional"),
            item("ppd558", "2026-08-25", "reading", "Introductory Econometrics — chs. 1, 2.1–2.6; Math Refresher A–C", "Jeffrey Wooldridge · Optional; excludes A.5"),
            item("ppd558", "2026-09-01", "reading", "Using Econometrics — chs. 1–3.2, 5", "A.H. Studenmund · Optional"),
            item("ppd558", "2026-09-01", "reading", "Introductory Econometrics — chs. 3.1–3.2, 4.2–4.6", "Jeffrey Wooldridge · Optional"),
            item("ppd558", "2026-09-08", "task", "Problem Set 1", "Due by start of class"),
            item("ppd558", "2026-09-08", "reading", "Using Econometrics — chs. 4, 9, 10", "A.H. Studenmund · Optional"),
            item("ppd558", "2026-09-08", "reading", "Introductory Econometrics — chs. 3.3–4.1, 4.7, 8, 12.1–12.3", "Jeffrey Wooldridge · Optional"),
            item("ppd558", "2026-09-15", "task", "Problem Set 2", "Due by start of class"),
            item("ppd558", "2026-09-15", "reading", "Using Econometrics — chs. 3.3, 6–7", "A.H. Studenmund · Optional; topic spans weeks 4–5"),
            item("ppd558", "2026-09-15", "reading", "Introductory Econometrics — chs. 2.7, 6, 7.1–7.4, 9.1–9.2", "Jeffrey Wooldridge · Optional; topic spans weeks 4–5"),
            item("ppd558", "2026-09-22", "task", "Analysis Project: Proposal", "Due by start of class"),
            item("ppd558", "2026-09-29", "task", "Problem Set 3", "Due by start of class"),
            item("ppd558", "2026-09-29", "reading", "Using Econometrics — chs. 8, 11", "A.H. Studenmund · Optional"),
            item("ppd558", "2026-09-29", "reading", "Introductory Econometrics — chs. 3.4a, 9.5", "Jeffrey Wooldridge · Optional"),
            item("ppd558", "2026-10-06", "task", "In-Class Analysis Exercise", "Graded in-class activity"),
            item("ppd558", "2026-10-06", "reading", "Using Econometrics — ch. 13", "A.H. Studenmund · Optional; categorical models"),
            item("ppd558", "2026-10-06", "reading", "Introductory Econometrics — chs. 7.5, 7.7, 17", "Jeffrey Wooldridge · Optional; categorical models"),
            item("ppd558", "2026-10-13", "task", "Midterm Exam", "In class · 20%", "major"),
            item("ppd558", "2026-10-20", "task", "Analysis Project: Data and Methods", "Due by start of class"),
            item("ppd558", "2026-10-27", "task", "Problem Set 4", "Due by start of class"),
            item("ppd558", "2026-10-27", "reading", "Using Econometrics — chs. 16.1, 14", "A.H. Studenmund · Optional"),
            item("ppd558", "2026-10-27", "reading", "Introductory Econometrics — chs. 2.7a, 9.4, 15, 16.1–16.3", "Jeffrey Wooldridge · Optional"),
            item("ppd558", "2026-11-10", "task", "Analysis Project: Preliminary Results", "Due by start of class"),
            item("ppd558", "2026-11-10", "reading", "Using Econometrics — chs. 16.2–16.3", "A.H. Studenmund · Optional"),
            item("ppd558", "2026-11-10", "reading", "Introductory Econometrics — chs. 13–14", "Jeffrey Wooldridge · Optional"),
            item("ppd558", "2026-11-17", "task", "In-Class Analysis Exercise", "Graded in-class activity"),
            item("ppd558", "2026-11-24", "task", "Problem Set 5", "Asynchronous week · due by class start time"),
            item("ppd558", "2026-12-01", "task", "In-Class Analysis Exercise", "Graded in-class activity"),
            item("ppd558", "2026-12-01", "task", "Analysis Project: Final Paper", "Due by start of class · project is 25%", "major"),
            item("ppd558", "2026-12-10", "task", "Final Exam", "2:00–4:00 PM · 25%", "major"),
        ],
    },
    {
        "id": "dsci549",
        "code": "DSCI 549",
        "title": "Introduction to Computational Thinking and Data Science",
        "color": "#7367b8",
        "instructor": "REDACTED",
        "meeting": "REDACTED",
        "location": "REDACTED",
        "office_hours": "After class on request",
        "assistant": "REDACTED",
        "tools": ["KNIME", "Piazza", "Brightspace", "Web-based/free analysis tools"],
        "grading": [
            {"label": "Five homework assignments", "percent": 20},
            {"label": "Midterm exam", "percent": 40},
            {"label": "Final exam", "percent": 40},
        ],
        "textbooks": [],
        "timeline": [
            item("dsci549", "2026-09-09", "task", "HW1 assigned: Analyzing Data", "Due date not specified in syllabus"),
            item("dsci549", "2026-09-23", "task", "HW2 assigned: Machine Learning", "Due date not specified in syllabus"),
            item("dsci549", "2026-10-07", "task", "Midterm Exam", "In class · 40%", "major"),
            item("dsci549", "2026-10-21", "task", "HW3 assigned: NLP", "Due date not specified in syllabus"),
            item("dsci549", "2026-10-28", "task", "HW4 assigned: Data Visualization and Representation", "Due date not specified in syllabus"),
            item("dsci549", "2026-11-04", "task", "HW5 assigned: Bias in Data", "Due date not specified in syllabus"),
            item("dsci549", "2026-12-09", "task", "Final Exam (likely date)", "Syllabus says “Likely Wednesday, December 9, 2026” · 40%", "major"),
        ],
    },
    {
        "id": "gsba548",
        "code": "GSBA 548",
        "title": "Corporate Finance",
        "color": "#bd7a24",
        "instructor": "REDACTED",
        "meeting": "REDACTED",
        "location": "REDACTED",
        "office_hours": "REDACTED",
        "assistant": "Not listed",
        "tools": ["Non-internet-enabled calculator", "Brightspace", "Computer + reliable internet"],
        "grading": [
            {"label": "Problem sets and quizzes", "percent": 60},
            {"label": "Final exam", "percent": 40},
        ],
        "textbooks": [],
        "timeline": [
            item("gsba548", "2026-08-24", "reading", "Principles of Corporate Finance — ch. 1", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-08-26", "reading", "Principles of Corporate Finance — ch. 2", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-09-02", "reading", "Principles of Corporate Finance — ch. 3", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-09-09", "reading", "Principles of Corporate Finance — ch. 4", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-09-11", "task", "Problem Set 1", "Due Friday"),
            item("gsba548", "2026-09-16", "reading", "Principles of Corporate Finance — ch. 5", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-09-16", "task", "Quiz 1", "In class"),
            item("gsba548", "2026-09-23", "reading", "Principles of Corporate Finance — ch. 6", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-09-25", "task", "Problem Set 2", "Due Friday"),
            item("gsba548", "2026-09-30", "reading", "Principles of Corporate Finance — ch. 7", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-09-30", "task", "Quiz 2", "In class"),
            item("gsba548", "2026-10-07", "reading", "Principles of Corporate Finance — chs. 8.1–8.2", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-10-16", "task", "Problem Set 3", "Due Friday"),
            item("gsba548", "2026-10-19", "reading", "Principles of Corporate Finance — chs. 8.1–8.3", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-10-21", "task", "Quiz 3", "In class"),
            item("gsba548", "2026-10-28", "reading", "Principles of Corporate Finance — ch. 9", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-10-30", "task", "Problem Set 4", "Due Friday"),
            item("gsba548", "2026-11-02", "reading", "Principles of Corporate Finance — chs. 11–12", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-11-04", "task", "Quiz 4", "In class"),
            item("gsba548", "2026-11-09", "reading", "Principles of Corporate Finance — chs. 13–14", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-11-13", "task", "Problem Set 5", "Due Friday"),
            item("gsba548", "2026-11-18", "reading", "Principles of Corporate Finance — ch. 15", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-11-18", "task", "Quiz 5", "In class"),
            item("gsba548", "2026-11-23", "reading", "Principles of Corporate Finance — ch. 16", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-11-30", "reading", "Principles of Corporate Finance — ch. 17", "Brealey, Myers, Allen & Edmans · Optional"),
            item("gsba548", "2026-12-04", "task", "Problem Set 6", "Due Friday"),
            item("gsba548", "2026-12-11", "task", "Final Exam", "11:00 AM–1:00 PM · cumulative · 40%", "major"),
        ],
    },
    {
        "id": "ppd503",
        "code": "PPD 503",
        "title": "Economics for Public Policy",
        "color": "#3f6f9c",
        "instructor": "REDACTED",
        "meeting": "REDACTED",
        "location": "REDACTED",
        "office_hours": "REDACTED",
        "assistant": "REDACTED",
        "tools": ["Standalone calculator", "Brightspace", "Word or PDF", "Adobe Scan (recommended)", "Zoom"],
        "grading": [
            {"label": "Problem sets", "percent": 25},
            {"label": "Case studies", "percent": 10},
            {"label": "Midterm exam", "percent": 30},
            {"label": "Final exam", "percent": 35},
        ],
        "textbooks": [
            {"title": "Microeconomics", "authors": "Robert Pindyck & Daniel Rubinfeld", "note": "7th, 8th, or 9th ed. · Required"},
        ],
        "timeline": [
            item("ppd503", "2026-08-26", "reading", "Microeconomics — chs. 1–2", "Pindyck & Rubinfeld · Required"),
            item("ppd503", "2026-08-26", "reading", "The Economist as Plumber", "Esther Duflo (2017) · Schedule reading"),
            item("ppd503", "2026-08-26", "reading", "Economists vs. Economics", "Dani Rodrik (2015) · Schedule reading"),
            item("ppd503", "2026-08-26", "reading", "Nearly $9 a Dozen: Why Egg Prices Are Skyrocketing", "Karen Garcia, LA Times (2025) · Schedule reading"),
            item("ppd503", "2026-08-26", "reading", "Rents Likely to Balloon in Wake of L.A. Wildfires", "Liam Dillon, LA Times (2025) · Schedule reading"),
            item("ppd503", "2026-09-02", "task", "Problem Set 1", "Due at beginning of class"),
            item("ppd503", "2026-09-02", "reading", "Microeconomics — chs. 3–4", "Pindyck & Rubinfeld · ch. 4 appendix optional"),
            item("ppd503", "2026-09-02", "reading", "The Great Trailblazer: Economists Mourn Gary Becker", "The Economist (2014) · Schedule reading"),
            item("ppd503", "2026-09-02", "reading", "Nice Work if You Can Get Out", "The Economist (2014) · Schedule reading"),
            item("ppd503", "2026-09-09", "task", "Problem Set 2", "Due at beginning of class"),
            item("ppd503", "2026-09-09", "reading", "Microeconomics — chs. 6–8", "Pindyck & Rubinfeld · §§7.6–7.7 and ch. 7 appendix optional"),
            item("ppd503", "2026-09-16", "task", "Problem Set 3", "Due at beginning of class"),
            item("ppd503", "2026-09-16", "reading", "Microeconomics — chs. 9, 16", "Pindyck & Rubinfeld · Required"),
            item("ppd503", "2026-09-16", "reading", "How Food Banks Use Markets to Feed the Poor", "Canice Prendergast (2017) · Schedule reading"),
            item("ppd503", "2026-09-16", "reading", "Saving Capitalism from Econ 101", "Simon Johnson (2018) · Schedule reading"),
            item("ppd503", "2026-09-16", "reading", "Harris’ Plan to Stop Price Gouging Could Create More Problems", "Elisabeth Buchwald, CNN · Schedule reading"),
            item("ppd503", "2026-09-16", "reading", "The Fight over Fifteen", "The Economist (2021) · Schedule reading"),
            item("ppd503", "2026-09-23", "task", "Case Study 1", "Due at beginning of class"),
            item("ppd503", "2026-09-23", "reading", "Impacts of Neighborhoods on Intergenerational Mobility: Executive Summary", "Raj Chetty & Nathaniel Hendren (2015) · Schedule reading"),
            item("ppd503", "2026-09-23", "reading", "Mapping the Childhood Roots of Social Mobility: Executive Summary", "Chetty, Friedman, Hendren, Jones & Porter (2018) · Schedule reading"),
            item("ppd503", "2026-09-30", "task", "Problem Set 4", "Due at beginning of class"),
            item("ppd503", "2026-09-30", "reading", "How the Census Bureau Measures Poverty", "U.S. Census Bureau (2022) · Required article"),
            item("ppd503", "2026-09-30", "reading", "Policy Analysis — ch. 7", "Weimer & Vining · Schedule reading"),
            item("ppd503", "2026-09-30", "reading", "The Development and History of the U.S. Poverty Thresholds", "Gordon M. Fisher (1997) · Schedule reading"),
            item("ppd503", "2026-09-30", "reading", "Child Poverty in the US Was Stagnant — and Then Something Changed", "Shaefer, Cooney & Stevenson, Vox (2022) · Schedule reading"),
            item("ppd503", "2026-09-30", "reading", "Consumption and Income Inequality in the U.S. since the 1960s", "Meyer & Sullivan (2023), pp. 247–284 · Schedule reading"),
            item("ppd503", "2026-10-07", "task", "Midterm Exam", "Regular class time · 30%", "major"),
            item("ppd503", "2026-10-14", "reading", "Microeconomics — ch. 10", "Pindyck & Rubinfeld · Required"),
            item("ppd503", "2026-10-14", "reading", "Policy Analysis — chs. 4; 5, pp. 98–104", "Weimer & Vining · Schedule reading"),
            item("ppd503", "2026-10-21", "task", "Problem Set 5", "Due at beginning of class"),
            item("ppd503", "2026-10-21", "reading", "Microeconomics — chs. 11.1–11.2, 12", "Pindyck & Rubinfeld · Required"),
            item("ppd503", "2026-10-21", "reading", "Monopoly’s New Era", "Joseph E. Stiglitz (2016) · Schedule reading"),
            item("ppd503", "2026-10-21", "reading", "No More Mylan Monopolies", "Geoffrey F. Joyce & Neeraj Sood (2016) · Schedule reading"),
            item("ppd503", "2026-10-21", "reading", "Why Economics Must Go Digital", "Diane Coyle (2019) · Schedule reading"),
            item("ppd503", "2026-10-21", "reading", "No, Rent Control Doesn’t Always Reduce the Supply of Housing", "Gary Painter, LA Times (2018) · Schedule reading"),
            item("ppd503", "2026-10-21", "reading", "Labor Market Monopsony: Trends, Consequences, and Policy Responses", "Council of Economic Advisers (2016) · Schedule reading"),
            item("ppd503", "2026-10-28", "task", "Case Study 2", "Due at beginning of class"),
            item("ppd503", "2026-10-28", "reading", "Microeconomics — ch. 18", "Pindyck & Rubinfeld · §18.3 optional"),
            item("ppd503", "2026-10-28", "reading", "Policy Analysis — ch. 5, pp. 74–98", "Weimer & Vining · Schedule reading"),
            item("ppd503", "2026-10-28", "reading", "Why Governments Should Spend More Money on Public Goods", "Tim Worstall, Forbes (2013) · Schedule reading"),
            item("ppd503", "2026-10-28", "reading", "To Fight Pandemics, Reward Research", "Tyler Cowen, New York Times (2013) · Schedule reading"),
            item("ppd503", "2026-10-28", "reading", "Commons Sense", "The Economist (2008) · Schedule reading"),
            item("ppd503", "2026-10-28", "reading", "Elinor Ostrom", "The Economist (2012) · Schedule reading"),
            item("ppd503", "2026-11-04", "task", "Problem Set 6", "Due at beginning of class"),
            item("ppd503", "2026-11-04", "reading", "Externalities: Pigouvian Taxes", "The Economist (2017) · Schedule reading"),
            item("ppd503", "2026-11-04", "reading", "Waist Banned: Does a Tax on Junk Food Make Sense?", "The Economist (2009) · Schedule reading"),
            item("ppd503", "2026-11-18", "task", "Case Study 3", "Due at beginning of class"),
            item("ppd503", "2026-11-18", "reading", "Microeconomics — ch. 17", "Pindyck & Rubinfeld · §§17.5–17.6 optional"),
            item("ppd503", "2026-11-18", "reading", "Policy Analysis — ch. 5, pp. 104–113; ch. 6, pp. 119–127", "Weimer & Vining · Schedule reading"),
            item("ppd503", "2026-11-18", "reading", "Information Asymmetry: Secrets and Agents", "The Economist (2016) · Schedule reading"),
            item("ppd503", "2026-11-18", "reading", "Paying Teachers More", "The Economist (2000) · Schedule reading"),
            item("ppd503", "2026-11-18", "reading", "Intelligent Design", "The Economist (2007) · Schedule reading"),
            item("ppd503", "2026-12-02", "task", "Problem Set 7", "Due at beginning of class"),
            item("ppd503", "2026-12-02", "reading", "The Folk Economics of Housing", "Elmendorf, Nall & Oklobdjiza (2025), pp. 45–66 · Required article"),
            item("ppd503", "2026-12-02", "reading", "Policy Analysis — chs. 8–10", "Weimer & Vining · Schedule reading"),
            item("ppd503", "2026-12-02", "reading", "Richard Thaler Wins the Nobel Prize for Economic Sciences", "The Economist (2017) · Schedule reading"),
            item("ppd503", "2026-12-02", "reading", "Pensions: Nudge Nudge", "The Economist (2012) · Schedule reading"),
            item("ppd503", "2026-12-02", "reading", "Ezra Klein Interviews Jenny Schuetz", "The Ezra Klein Show transcript (2022) · Schedule reading"),
            item("ppd503", "2026-12-09", "task", "Final Exam", "7:00–9:00 PM · 35%", "major"),
        ],
    },
]


# -----------------------------------------------------------------------------
# Section 3: HTML, CSS, and JavaScript application template
# -----------------------------------------------------------------------------
PAGE_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>__PAGE_TITLE__</title>

  <!-- Section A: Distinctive editorial visual system -->
  <style>
    :root {
      --ink: #17211d;
      --muted: #66706a;
      --paper: #f3efe6;
      --card: #fffdf7;
      --line: #d9d2c4;
      --accent: #e0603e;
      --accent-soft: #f8d9ca;
      --forest: #254b3f;
      --shadow: 0 18px 42px rgba(48, 40, 29, 0.10);
      --radius: 22px;
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at 6% 4%, rgba(224, 96, 62, .14), transparent 24rem),
        linear-gradient(90deg, rgba(37, 75, 63, .035) 1px, transparent 1px),
        var(--paper);
      background-size: auto, 32px 32px, auto;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }

    button, input { font: inherit; }
    button { color: inherit; }
    button:focus-visible, input:focus-visible {
      outline: 3px solid rgba(224, 96, 62, .35);
      outline-offset: 3px;
    }

    .shell { width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 24px 0 72px; }
    .eyebrow {
      margin: 0 0 8px;
      color: var(--accent);
      font-size: .74rem;
      font-weight: 800;
      letter-spacing: .15em;
      text-transform: uppercase;
    }

    /* Section B: Semester masthead and elapsed-time meter */
    .masthead {
      position: relative;
      overflow: hidden;
      min-height: 280px;
      padding: clamp(26px, 5vw, 58px);
      border-radius: 30px;
      color: #fffaf1;
      background: var(--forest);
      box-shadow: var(--shadow);
    }
    .masthead::after {
      content: "";
      position: absolute;
      width: 290px;
      height: 290px;
      right: -70px;
      top: -85px;
      border: 42px solid rgba(255,255,255,.07);
      border-radius: 50%;
    }
    .masthead-grid { position: relative; z-index: 1; display: grid; grid-template-columns: 1.45fr .8fr; gap: 48px; align-items: end; }
    h1 {
      max-width: 760px;
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(2.7rem, 7vw, 5.8rem);
      font-weight: 500;
      letter-spacing: -.055em;
      line-height: .94;
    }
    .subtitle { max-width: 600px; margin: 20px 0 0; color: rgba(255,250,241,.72); font-size: 1rem; }
    .week-card { padding: 20px; border: 1px solid rgba(255,255,255,.18); border-radius: 18px; background: rgba(255,255,255,.08); backdrop-filter: blur(12px); }
    .week-label { display: flex; justify-content: space-between; gap: 12px; font-size: .82rem; color: rgba(255,250,241,.76); }
    .week-value { display: block; margin: 8px 0 15px; font-family: Georgia, serif; font-size: 2rem; }
    .meter { height: 9px; overflow: hidden; border-radius: 999px; background: rgba(255,255,255,.14); }
    .meter > span { display: block; width: 0; height: 100%; border-radius: inherit; background: #f1a07f; transition: width .7s ease; }

    /* Section C: Navigation controls */
    .control-bar {
      position: sticky;
      z-index: 20;
      top: 12px;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      margin: 28px 0;
      padding: 12px;
      border: 1px solid rgba(217,210,196,.86);
      border-radius: 18px;
      background: rgba(255,253,247,.9);
      box-shadow: 0 8px 28px rgba(48,40,29,.08);
      backdrop-filter: blur(16px);
    }
    .filters { display: flex; flex-wrap: wrap; gap: 8px; }
    .filter-button {
      padding: 9px 13px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: transparent;
      cursor: pointer;
      font-size: .84rem;
      font-weight: 700;
      transition: .18s ease;
    }
    .filter-button:hover { transform: translateY(-1px); border-color: #b9ad9b; }
    .filter-button.active { color: #fff; border-color: var(--forest); background: var(--forest); }
    .jump-button { border-style: dashed; }
    .toggle { display: flex; align-items: center; gap: 9px; white-space: nowrap; padding: 0 5px; font-size: .86rem; font-weight: 700; cursor: pointer; }
    .toggle input { width: 17px; height: 17px; accent-color: var(--accent); }

    /* Section D: Course information cards */
    .section-heading { display: flex; justify-content: space-between; align-items: end; gap: 16px; margin: 42px 0 16px; }
    h2 { margin: 0; font-family: Georgia, serif; font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 500; letter-spacing: -.035em; }
    .section-note { max-width: 460px; margin: 0; color: var(--muted); font-size: .9rem; text-align: right; }
    .course-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 16px; }
    .course-card {
      grid-column: span 6;
      overflow: hidden;
      border: 1px solid var(--line);
      border-top: 7px solid var(--course-color, var(--accent));
      border-radius: var(--radius);
      background: var(--card);
      box-shadow: 0 8px 25px rgba(48,40,29,.06);
    }
    .course-card__head { display: flex; justify-content: space-between; gap: 18px; padding: 22px 22px 14px; }
    .course-code { margin: 0 0 3px; color: var(--course-color, var(--accent)); font-size: .76rem; font-weight: 850; letter-spacing: .12em; text-transform: uppercase; }
    h3 { margin: 0; font-family: Georgia, serif; font-size: 1.45rem; font-weight: 500; line-height: 1.15; }
    .progress-badge { flex: 0 0 auto; min-width: 72px; padding: 9px 10px; border-radius: 13px; text-align: center; background: #f0ece2; font-size: .75rem; color: var(--muted); }
    .progress-badge strong { display: block; color: var(--ink); font-size: 1rem; }
    .course-facts { display: grid; grid-template-columns: 1fr 1fr; gap: 0; margin: 0; border-top: 1px solid var(--line); }
    .fact { min-height: 86px; padding: 14px 22px; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); }
    .fact:nth-child(even) { border-right: 0; }
    .fact dt { margin-bottom: 4px; color: var(--muted); font-size: .67rem; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; }
    .fact dd { margin: 0; font-size: .88rem; }
    .tool-list { display: flex; flex-wrap: wrap; gap: 6px; padding: 16px 22px 20px; }
    .tool-chip { padding: 5px 9px; border-radius: 7px; background: color-mix(in srgb, var(--course-color, var(--accent)) 12%, white); font-size: .74rem; font-weight: 750; }

    /* Section E: Textbook callout and grading panels */
    .reference-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .panel { padding: 24px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--card); box-shadow: 0 8px 25px rgba(48,40,29,.05); }
    .book-list, .grading-list { display: grid; gap: 12px; margin-top: 17px; }
    .book { padding-left: 14px; border-left: 4px solid var(--accent); }
    .book strong, .grade-row strong { display: block; }
    .book small { color: var(--muted); }
    .grade-course + .grade-course { margin-top: 22px; padding-top: 20px; border-top: 1px solid var(--line); }
    .grade-course-title { display: flex; align-items: center; gap: 8px; margin-bottom: 11px; font-size: .88rem; font-weight: 850; }
    .dot { width: 9px; height: 9px; border-radius: 50%; background: var(--course-color, var(--accent)); }
    .grade-row { display: grid; grid-template-columns: 1fr 52px; gap: 12px; align-items: center; margin: 9px 0; font-size: .82rem; }
    .grade-track { grid-column: 1 / -1; height: 5px; margin-top: -7px; overflow: hidden; border-radius: 9px; background: #ebe5d9; }
    .grade-track span { display: block; height: 100%; border-radius: inherit; background: var(--course-color, var(--accent)); }

    /* Section F: Unified chronological timeline */
    .timeline { border-top: 1px solid var(--line); }
    .date-group { display: grid; grid-template-columns: 150px 1fr; border-bottom: 1px solid var(--line); }
    .date-group.next-up { background: linear-gradient(90deg, rgba(224,96,62,.09), transparent 46%); }
    .date-group.next-up .date-column time::after { content: "Next up"; display: block; width: fit-content; margin-top: 7px; padding: 3px 6px; border-radius: 5px; color: #9d341c; background: var(--accent-soft); font-family: Inter, sans-serif; font-size: .58rem; font-weight: 850; letter-spacing: .06em; text-transform: uppercase; }
    .date-column { padding: 25px 20px 25px 0; }
    .date-column time { position: sticky; top: 96px; font-family: Georgia, serif; font-size: 1.05rem; }
    .date-column small { display: block; margin-top: 3px; color: var(--muted); font-size: .72rem; }
    .date-items { border-left: 1px solid var(--line); }
    .timeline-item {
      --course-color: var(--accent);
      display: grid;
      grid-template-columns: 36px minmax(0, 1fr) auto;
      gap: 13px;
      align-items: start;
      padding: 20px;
      border-bottom: 1px dashed var(--line);
      transition: opacity .2s ease, background .2s ease;
    }
    .timeline-item:last-child { border-bottom: 0; }
    .timeline-item:hover { background: rgba(255,255,255,.48); }
    .timeline-item.done { opacity: .48; }
    .timeline-item.done .item-title { text-decoration: line-through; }
    .check-wrap { position: relative; display: grid; place-items: center; width: 30px; height: 30px; margin-top: 2px; }
    .check-wrap input { position: absolute; width: 100%; height: 100%; margin: 0; opacity: 0; cursor: pointer; }
    .custom-check { display: grid; place-items: center; width: 23px; height: 23px; border: 2px solid #a99f90; border-radius: 7px; background: var(--card); pointer-events: none; }
    .check-wrap input:checked + .custom-check { color: white; border-color: var(--course-color); background: var(--course-color); }
    .check-wrap input:checked + .custom-check::after { content: "✓"; font-size: .83rem; font-weight: 900; }
    .item-title { margin: 0; font-size: .97rem; font-weight: 780; }
    .item-detail { margin: 4px 0 0; color: var(--muted); font-size: .8rem; }
    .tags { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 6px; max-width: 230px; }
    .tag { padding: 5px 8px; border-radius: 6px; background: #e9e4da; font-size: .66rem; font-weight: 850; letter-spacing: .045em; text-transform: uppercase; }
    .tag.course { color: #fff; background: var(--course-color); }
    .tag.major { color: #9d341c; background: var(--accent-soft); }

    /* Section G: Empty and status states */
    .empty-state { padding: 44px 28px; border: 1px dashed #bfb4a3; border-radius: var(--radius); text-align: center; background: rgba(255,253,247,.55); }
    .empty-state .mark { display: inline-grid; place-items: center; width: 52px; height: 52px; margin-bottom: 10px; border-radius: 50%; color: #fff; background: var(--forest); font-family: Georgia, serif; font-size: 1.5rem; }
    .empty-state h3 { margin-bottom: 8px; }
    .empty-state p { max-width: 580px; margin: 0 auto; color: var(--muted); }
    .status { position: fixed; right: 18px; bottom: 18px; z-index: 30; padding: 9px 13px; border: 1px solid var(--line); border-radius: 999px; background: var(--card); box-shadow: var(--shadow); color: var(--muted); font-size: .72rem; opacity: 0; transform: translateY(8px); transition: .2s ease; pointer-events: none; }
    .status.show { opacity: 1; transform: translateY(0); }

    /* Section H: Responsive and reduced-motion behavior */
    @media (max-width: 820px) {
      .masthead-grid, .reference-grid { grid-template-columns: 1fr; }
      .course-card { grid-column: span 12; }
      .control-bar, .section-heading { align-items: stretch; flex-direction: column; }
      .section-note { text-align: left; }
      .date-group { grid-template-columns: 92px 1fr; }
      .timeline-item { grid-template-columns: 32px 1fr; }
      .tags { grid-column: 2; justify-content: flex-start; max-width: none; }
    }
    @media (max-width: 540px) {
      .shell { width: min(100% - 20px, 1180px); padding-top: 10px; }
      .masthead { padding: 28px 22px; border-radius: 22px; }
      .control-bar { top: 6px; }
      .date-group { display: block; }
      .date-column { padding: 20px 0 9px; }
      .date-column time { position: static; }
      .date-items { border-left: 0; }
      .course-facts { grid-template-columns: 1fr; }
      .fact { border-right: 0; }
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
    }
  </style>
</head>
<body>
  <!-- Section I: Application mount point -->
  <main class="shell" id="app" aria-live="polite"></main>
  <div class="status" id="saveStatus" role="status">Saved</div>

  <!-- Section J: Syllabus-derived data embedded by Python -->
  <script type="application/json" id="dashboard-data">__DASHBOARD_DATA__</script>

  <!-- Section K: Dashboard behavior and persistence -->
  <script>
    (() => {
      "use strict";

      // Section K1: Read the embedded, Python-generated course data.
      const DATA = JSON.parse(document.getElementById("dashboard-data").textContent);
      const app = document.getElementById("app");
      const saveStatus = document.getElementById("saveStatus");
      const courseById = new Map(DATA.courses.map(course => [course.id, course]));
      const allItems = DATA.courses.flatMap(course =>
        course.timeline.map(item => ({...item, courseId: course.id}))
      ).sort((a, b) => a.date.localeCompare(b.date) || a.title.localeCompare(b.title));

      // Section K2: Use the host artifact API when available. A downloaded file
      // cannot receive that host API, so IndexedDB is the standards-based fallback.
      // localStorage is deliberately never used.
      const STORAGE_KEY = "semester-dashboard-completion-v1";
      const ArtifactStore = {
        host: window.artifactStorage || window.storage || null,
        async get(key) {
          if (this.host) {
            const result = this.host.getItem
              ? await this.host.getItem(key)
              : await this.host.get(key);
            return result && typeof result === "object" && "value" in result ? result.value : result;
          }
          return this.idb("readonly", store => store.get(key));
        },
        async set(key, value) {
          if (this.host) {
            return this.host.setItem
              ? await this.host.setItem(key, value)
              : await this.host.set(key, value);
          }
          return this.idb("readwrite", store => store.put(value, key));
        },
        async idb(mode, operation) {
          const db = await new Promise((resolve, reject) => {
            const request = indexedDB.open("semester-dashboard", 1);
            request.onupgradeneeded = () => request.result.createObjectStore("state");
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
          });
          return new Promise((resolve, reject) => {
            const tx = db.transaction("state", mode);
            const request = operation(tx.objectStore("state"));
            request.onsuccess = () => resolve(request.result ?? null);
            request.onerror = () => reject(request.error);
            tx.oncomplete = () => db.close();
          });
        }
      };

      // Section K3: UI state, formatting helpers, and safe HTML escaping.
      const state = { completed: new Set(), filter: "all", hideCompleted: false };
      const escapeHTML = value => String(value ?? "")
        .replaceAll("&", "&amp;").replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
      // Parse YYYY-MM-DD defensively: anything else (null, "[REDACTED]", a
      // number) yields null instead of an Invalid Date that would throw in Intl.
      const parseISO = (iso, time = "12:00:00") => {
        if (typeof iso !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(iso)) return null;
        const date = new Date(`${iso}T${time}`);
        return Number.isNaN(date.getTime()) ? null : date;
      };
      const formatDate = iso => {
        const date = parseISO(iso);
        return date ? new Intl.DateTimeFormat(undefined, {
          weekday: "short", month: "short", day: "numeric"
        }).format(date) : String(iso ?? "Undated");
      };
      const formatLongDate = iso => {
        const date = parseISO(iso);
        return date ? new Intl.DateTimeFormat(undefined, {
          month: "long", day: "numeric", year: "numeric"
        }).format(date) : "—";
      };
      const courseColor = course => course.color || "#e0603e";
      const itemCount = course => course.timeline.length;
      const completedCount = course => course.timeline.filter(item => state.completed.has(item.id)).length;
      const localISODate = date => [date.getFullYear(), String(date.getMonth() + 1).padStart(2, "0"), String(date.getDate()).padStart(2, "0")].join("-");

      // Section K4: Calculate calendar progress without hard-coding today's date.
      function semesterProgress() {
        const start = parseISO(DATA.semester.start_date, "00:00:00");
        const end = parseISO(DATA.semester.end_date, "23:59:59");
        if (!start || !end || end <= start) {
          return { label: "Dates not set", detail: "Add semester dates", percent: 0 };
        }
        const now = new Date();
        const elapsedDays = Math.max(0, Math.min((now - start) / 86400000, (end - start) / 86400000));
        const totalDays = Math.max(1, (end - start) / 86400000);
        const weeksElapsed = Math.min(Math.ceil(totalDays / 7), Math.max(0, Math.floor(elapsedDays / 7) + 1));
        const totalWeeks = Math.ceil(totalDays / 7);
        return {
          label: now < start ? "Starts soon" : now > end ? "Semester complete" : `Week ${weeksElapsed} of ${totalWeeks}`,
          detail: `${formatLongDate(DATA.semester.start_date)} — ${formatLongDate(DATA.semester.end_date)}`,
          percent: Math.round((elapsedDays / totalDays) * 100)
        };
      }

      // Section K5: Render the masthead and filter controls.
      function renderHeader() {
        const progress = semesterProgress();
        const courseButtons = DATA.courses.map(course => `
          <button class="filter-button" data-filter="${escapeHTML(course.id)}"
            aria-pressed="${state.filter === course.id}">${escapeHTML(course.code)}</button>
        `).join("");
        return `
          <header class="masthead">
            <div class="masthead-grid">
              <div>
                <p class="eyebrow">Academic field guide</p>
                <h1>${escapeHTML(DATA.semester.name)}</h1>
                <p class="subtitle">${DATA.courses.length} courses · ${allItems.filter(item => item.type === "reading").length} readings · ${allItems.filter(item => item.type === "task").length} tasks. One calm, chronological view.</p>
              </div>
              <div class="week-card" aria-label="Semester progress">
                <div class="week-label"><span>Weeks elapsed</span><span>${progress.percent}%</span></div>
                <strong class="week-value">${escapeHTML(progress.label)}</strong>
                <div class="meter" aria-hidden="true"><span style="width:${progress.percent}%"></span></div>
                <div class="week-label" style="margin-top:10px"><span>${escapeHTML(progress.detail)}</span></div>
              </div>
            </div>
          </header>
          <nav class="control-bar" aria-label="Timeline filters">
            <div class="filters">
              <button class="filter-button" data-filter="all" aria-pressed="${state.filter === "all"}">All courses</button>
              ${courseButtons}
              <button class="filter-button" data-filter="major" aria-pressed="${state.filter === "major"}">Exams + major work</button>
              <button class="filter-button jump-button" id="jumpToday" type="button">Jump to next ↓</button>
            </div>
            <label class="toggle"><input id="hideCompleted" type="checkbox" ${state.hideCompleted ? "checked" : ""}> Hide completed</label>
          </nav>`;
      }

      // Section K6: Render compact course reference cards.
      function renderCourseCards() {
        if (!DATA.courses.length) return renderEmpty("Course details are waiting for the syllabus files.");
        return `<div class="course-grid">${DATA.courses.map(course => {
          const done = completedCount(course);
          const total = itemCount(course);
          const assistant = course.assistant || "Not listed";
          const tools = (course.tools || []).length ? course.tools : ["None listed"];
          return `<article class="course-card" style="--course-color:${courseColor(course)}">
            <div class="course-card__head">
              <div><p class="course-code">${escapeHTML(course.code)}</p><h3>${escapeHTML(course.title)}</h3></div>
              <div class="progress-badge"><strong>${done}/${total}</strong> complete</div>
            </div>
            <dl class="course-facts">
              <div class="fact"><dt>Instructor</dt><dd>${escapeHTML(course.instructor || "Not listed")}</dd></div>
              <div class="fact"><dt>Meeting</dt><dd>${escapeHTML(course.meeting || "Not listed")}</dd></div>
              <div class="fact"><dt>Location</dt><dd>${escapeHTML(course.location || "Not listed")}</dd></div>
              <div class="fact"><dt>Office hours</dt><dd>${escapeHTML(course.office_hours || "Not listed")}</dd></div>
              <div class="fact" style="grid-column:1/-1"><dt>Course assistant</dt><dd>${escapeHTML(assistant)}</dd></div>
            </dl>
            <div class="tool-list" aria-label="Required tools">${tools.map(tool => `<span class="tool-chip">${escapeHTML(tool)}</span>`).join("")}</div>
          </article>`;
        }).join("")}</div>`;
      }

      // Section K7: Render textbooks and grading breakdowns.
      function renderReferencePanels() {
        const books = DATA.courses.flatMap(course => (course.textbooks || []).map(book => ({...book, course})));
        const bookHTML = books.length ? books.map(({title, authors, note, course}) => `
          <div class="book"><strong>${escapeHTML(title)}</strong><small>${escapeHTML(authors || "")}${authors && note ? " · " : ""}${escapeHTML(note || "")} · ${escapeHTML(course.code)}</small></div>
        `).join("") : `<p class="section-note" style="text-align:left">No required textbooks are available yet.</p>`;
        const gradeHTML = DATA.courses.length ? DATA.courses.map(course => `
          <div class="grade-course" style="--course-color:${courseColor(course)}">
            <div class="grade-course-title"><span class="dot"></span>${escapeHTML(course.code)}</div>
            ${(course.grading || []).map(part => `<div class="grade-row"><span>${escapeHTML(part.label)}</span><strong>${escapeHTML(part.percent)}%</strong><div class="grade-track"><span style="width:${Math.min(100, Number(part.percent) || 0)}%"></span></div></div>`).join("") || `<small>No grading breakdown listed.</small>`}
          </div>
        `).join("") : `<p class="section-note" style="text-align:left">No grading data is available yet.</p>`;
        return `<div class="reference-grid">
          <section class="panel"><p class="eyebrow">Required reading</p><h3>Textbook shelf</h3><div class="book-list">${bookHTML}</div></section>
          <section class="panel"><p class="eyebrow">How grades add up</p><h3>Grading breakdown</h3><div class="grading-list">${gradeHTML}</div></section>
        </div>`;
      }

      // Section K8: Filter and render the cross-course chronological timeline.
      function visibleItems() {
        return allItems.filter(item => {
          const matches = state.filter === "all" || item.courseId === state.filter ||
            (state.filter === "major" && item.type === "task" && item.importance === "major");
          return matches && !(state.hideCompleted && state.completed.has(item.id));
        });
      }

      function renderTimeline() {
        const items = visibleItems();
        if (!allItems.length) return renderEmpty("The combined timeline will appear after the weekly schedules are extracted.");
        if (!items.length) return renderEmpty("Nothing matches these filters. Try showing completed work or all courses.");
        const today = localISODate(new Date());
        const nextDate = items.find(item => parseISO(item.date) && item.date >= today)?.date || items.at(-1).date;
        const groups = Map.groupBy ? Map.groupBy(items, item => item.date) : items.reduce((map, item) => {
          if (!map.has(item.date)) map.set(item.date, []);
          map.get(item.date).push(item);
          return map;
        }, new Map());
        return `<div class="timeline">${[...groups].map(([date, dateItems]) => `
          <section class="date-group ${date === nextDate ? "next-up" : ""}" data-date-group="${escapeHTML(date)}">
            <div class="date-column"><time datetime="${escapeHTML(date)}">${escapeHTML(formatDate(date))}</time><small>${dateItems.length} item${dateItems.length === 1 ? "" : "s"}</small></div>
            <div class="date-items">${dateItems.map(item => {
              const course = courseById.get(item.courseId);
              const done = state.completed.has(item.id);
              return `<article class="timeline-item ${done ? "done" : ""}" style="--course-color:${courseColor(course)}">
                <label class="check-wrap" aria-label="Mark ${escapeHTML(item.title)} complete">
                  <input type="checkbox" data-item-id="${escapeHTML(item.id)}" ${done ? "checked" : ""}>
                  <span class="custom-check"></span>
                </label>
                <div><p class="item-title">${escapeHTML(item.title)}</p>${item.detail ? `<p class="item-detail">${escapeHTML(item.detail)}</p>` : ""}</div>
                <div class="tags"><span class="tag course">${escapeHTML(course.code)}</span><span class="tag">${item.type === "reading" ? "Reading" : "Task"}</span>${item.importance === "major" ? `<span class="tag major">Major</span>` : ""}</div>
              </article>`;
            }).join("")}</div>
          </section>`).join("")}</div>`;
      }

      // Section K9: Shared empty-state component and full-page render.
      function renderEmpty(message) {
        return `<div class="empty-state"><span class="mark">∴</span><h3>Ready for source material</h3><p>${escapeHTML(message)}</p></div>`;
      }

      function render() {
        app.innerHTML = `${renderHeader()}
          <section><div class="section-heading"><div><p class="eyebrow">At a glance</p><h2>Course atlas</h2></div><p class="section-note">People, places, office hours, and software—without reopening a PDF.</p></div>${renderCourseCards()}</section>
          <section><div class="section-heading"><div><p class="eyebrow">Reference desk</p><h2>Books + grading</h2></div></div>${renderReferencePanels()}</section>
          <section><div class="section-heading"><div><p class="eyebrow">One semester, one sequence</p><h2>Master timeline</h2></div><p class="section-note">Readings and graded work are interleaved by date. Major work receives an extra marker.</p></div>${renderTimeline()}</section>`;
        bindEvents();
      }

      // Section K10: Event handlers and automatically persisted completion state.
      function bindEvents() {
        document.querySelectorAll("[data-filter]").forEach(button => button.addEventListener("click", () => {
          state.filter = button.dataset.filter;
          render();
        }));
        document.getElementById("hideCompleted").addEventListener("change", event => {
          state.hideCompleted = event.target.checked;
          render();
        });
        document.getElementById("jumpToday").addEventListener("click", () => {
          const next = document.querySelector(".date-group.next-up");
          if (next) next.scrollIntoView({behavior: "smooth", block: "start"});
        });
        document.querySelectorAll("[data-item-id]").forEach(box => box.addEventListener("change", async () => {
          box.checked ? state.completed.add(box.dataset.itemId) : state.completed.delete(box.dataset.itemId);
          render();
          await saveState();
        }));
      }

      async function saveState() {
        try {
          await ArtifactStore.set(STORAGE_KEY, JSON.stringify([...state.completed]));
          saveStatus.textContent = ArtifactStore.host ? "Saved to artifact" : "Saved on this browser";
        } catch (error) {
          console.error("Could not save dashboard state", error);
          saveStatus.textContent = "Could not save";
        }
        saveStatus.classList.add("show");
        setTimeout(() => saveStatus.classList.remove("show"), 1400);
      }

      // Section K11: Restore completion state before the first paint.
      (async function initialize() {
        try {
          const saved = await ArtifactStore.get(STORAGE_KEY);
          if (saved) state.completed = new Set(JSON.parse(saved));
        } catch (error) {
          console.warn("No saved dashboard state could be restored", error);
        }
        render();
      })();
    })();
  </script>
</body>
</html>
'''


# -----------------------------------------------------------------------------
# Section 4: Data validation before generating the artifact
# -----------------------------------------------------------------------------
def validate_data() -> None:
    """Reject duplicate IDs and invalid grading totals before writing HTML."""
    course_ids = [course["id"] for course in COURSES]
    if len(course_ids) != len(set(course_ids)):
        raise ValueError("Every course must have a unique id.")

    item_ids: list[str] = []
    for course in COURSES:
        item_ids.extend(item["id"] for item in course.get("timeline", []))
        grading = course.get("grading", [])
        if grading:
            total = sum(float(item["percent"]) for item in grading)
            if abs(total - 100) > 0.01:
                raise ValueError(f"{course['code']} grading adds to {total:g}%, not 100%.")
    if len(item_ids) != len(set(item_ids)):
        raise ValueError("Every timeline item must have a globally unique id.")


# -----------------------------------------------------------------------------
# Section 5: Generate the portable HTML file
# -----------------------------------------------------------------------------
def build(output_path: Path) -> Path:
    """Validate the data and write one self-contained HTML dashboard."""
    validate_data()
    semester = {
        **SEMESTER,
        "start_date": to_iso(SEMESTER.get("start_date")),
        "end_date": to_iso(SEMESTER.get("end_date")),
    }
    payload = json.dumps(
        {"semester": semester, "courses": COURSES}, ensure_ascii=False, default=str
    )
    # Prevent embedded syllabus text from accidentally closing the JSON script tag.
    payload = payload.replace("</", "<\\/")
    page = PAGE_TEMPLATE.replace("__PAGE_TITLE__", str(SEMESTER["name"]))
    page = page.replace("__DASHBOARD_DATA__", payload)
    output_path.write_text(page, encoding="utf-8")
    return output_path


# -----------------------------------------------------------------------------
# Section 6: Command-line entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    destination = Path(__file__).with_name("semester_dashboard.html")
    print(build(destination).resolve())
