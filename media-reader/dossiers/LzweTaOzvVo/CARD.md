# Video: LzweTaOzvVo

- **URL:** https://www.youtube.com/watch?v=LzweTaOzvVo
- **Kind:** youtube
- **Title:** Master ALL Jev Design Patterns (With Practical  Examples)
- **Channel:** The AI Automators (@TheAIAutomators)
- **Category:** AgentManagement
- **Uploaded:** 2026-09-25 · **Duration:** 14:20 (860 s) · **Views:** 703
- **Bead:** dr-o0h
- **First analyzed:** 2026-09-25
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

Verification key: **[sb]** = read by Claude on the YouTube storyboard mosaics (320×180 tiles, ~5 s apart; see Lessons for why not `frames`); **[zoom]** = clipped verbatim-speech zoom; **[arith]** = arithmetic check. Unmarked on-screen detail is Gemini-only and unread.

### What "Jev" is
- **Jev is TypeSafe AI's "decision model", version 1.13** — the same TypeSafe Jev that the `jev-loop` skill calls. Not a framework or a pattern language. 00:00 [zoom]: *"Jev isn't a chat model, it's a decision model. You give it some context and a question, and it returns an answer that your software can act on."* On-screen "Jev · decision model", "Jev 1.13" [sb]. The TypeSafe AI docs site appears at 06:58 ("Line-by-line search" how-to) [sb].
- **Pricing** 01:21 [zoom]: *"TypeSafe currently lists the price of Jev at 4.2 US cent per million input tokens, with no charge for output tokens."* Card "$0.042 · input tokens per 1M · output tokens free · checked 25 Sep 2026" [sb]. Worked example 01:35–01:47: 1,000 input tokens × 1,000,000 requests = $42 [arith ✓].
- **Vendor speed claim** 01:19: a pink TypeSafe slide "193.6x Faster, 444.6x Cheaper" [sb], footnoted (Gemini) "*Based On Workflows For System One Tasks (Proof)". The presenter does not repeat or source it; treat as vendor marketing.
- 01:04 [zoom]: *"with the incredible success of this model in only the space of a week, we are guaranteed to see a wave of new decision models, both proprietary and open source"* — Jev was about a week old at upload. He says the patterns are **not Jev-specific**.

### The decision types (what comes back)
Three types, 04:00–05:06 [zoom + sb]:
- **noul** (spelled so on screen [sb], and "Noul question" in TypeSafe's own docs [sb]): a yes/no question that returns the *probability of yes*. Example: "Does the customer in this email mention a deadline within the next two days?" returns 0.9, and code `if (deadline.noul > 0.8) ticket.flag("deadline")` [sb, code partly legible]. A value near 0.5 (0.52 shown [sb]) means the model is unsure.
- **choice**: you supply the answers and it picks one (bug / billing / account access / feature request / something else). Returns probabilities plus a confidence value.
- **score**: a position on an ordered scale you define (trivial / minor / major / blocker). It can fall between levels (2.58), and it also returns a confidence.

### The five use-case categories (TypeSafe's grouping, 02:00–03:51)
Automation (triage into queues, 02:04); real-time applications (Jev playing Doom, "150 ms per decision", a sketchpad "make something bigger", 02:20–02:58; he says *"you may have seen examples online"*, and it is **not demonstrated**); data processing at scale ("AI map-reduce": classify, then count with ordinary code; monthly zip-complaint bars 96/118/143/201 [sb], 262/331 and total 1,151 Gemini-only, sum consistent [arith]; 02:58–03:18); verification (does a citation support a claim; does a drafted reply promise something policy forbids; 03:19–03:37); harness engineering ("the software around an AI agent, like Claude Code or Codex", 03:42).

### The ten decision shapes (the job being done), 05:06–09:32 [zoom]
*"The type tells us what comes back. The shape, however, describes the job."* 1 classification (choice: bug; invoice / sales pitch / delivery update; 05:22); 2 detection (noul: "asks us to stop contacting?" 0.93, then `suppress(sender)`; 05:45); 3 scoring ("both a shape and a type": bug disruptiveness 2.58, help-article clarity 1.09, used to order engineering or editorial work; 06:11); 4 routing (order status → database lookup, product question → docs assistant; he used it in his previous video to route queries to a fast versus a strong model; 06:30); 5 search (match by meaning; TypeSafe's line-by-line search how-to scores 218 line ids of GitHub's ToS with one Choice question plus a Noul "does the document contain an answer" [sb]; *"that's not to say you can use a decision model as a search engine"*; 06:52); 6 retrieval (pick which returns-policy passages apply to this customer's region and purchase, "8 found → 2 supplied"; 07:26); 7 ranking (sort 10 backpacks against "laptop … rainy bike commute"; *"search finds the candidates, ranking orders them, and retrieval uses the results"*; 07:47); 8 verification (*"A quote can exist and still be used to make the wrong claim."*; 08:17); 9 feature extraction (language → numeric inputs for a non-generative ML model, e.g. buyer intent for a demand forecast; 08:44); 10 structured data extraction (code or Jev picks candidate values; "Pick the value, don't write it"; LLM extraction is "slow and expensive"; 09:03).

### The four design patterns, 09:32–12:18 (all speech [zoom]; title cards [sb])
1. **Speculative fan-out** (09:43). *"With a fan-out, we can ask those independent questions all together in a single request. And once the results come back, code uses the relevant answers."* Example: one ticket, four questions (category, disruption, deadline?, repro steps?), giving bug / 2.58 / 0.9 / 0.35 [sb]. If it is billing, the repro answer is ignored. It is "speculative" because *"the time it takes to ask one question versus 10 questions in a single request is virtually the same"*. Dependent questions still need a stage 2 ("which known bug?" [sb]).
2. **Confidence-gated routing** (10:36). *"Sometimes the best available answer is still too uncertain to act upon."* The example is "cancel it": subscription 54% / appointment 46%, confidence 0.08, so ask to clarify. "Cancel my gym membership" gives confidence 0.94 and goes to the handler [sb]. The threshold is 0.60 [sb]: `if (answer.confidence >= 0.60) handle(answer) else askToClarify(customer)`. *"You need to test the different thresholds then against your own use case."* Keep permission checks and confirmation rules: *"don't just trust what Jev … is going to tell you, you still need to properly secure and gate everything on your own side, using your own business logic."*
3. **Composite scoring** (11:23). *"Ask for each score separately, and then you combine them using weights that you control. And you could even have dynamic weights by sending in the situation into the model."* Example: four backpacks scored on intended use / preferences / budget. The fixed weights are ×0.50/×0.30/×0.20 and put Commuter 22L top at 0.72 [sb]. Jev-set weights for "end of the month, money's tight" are ×0.25/×0.15/×0.60 (Gemini [zoom]) and put Metro 18L top at 0.80 (Gemini). The storyboard caught a mid-animation state, ×0.42/×0.25/×0.32 with scores 0.65/0.73/0.59/0.43 [sb]. That state lies exactly on the straight-line tween between the two weight sets, which corroborates both endpoints. Arithmetic: Commuter's criterion scores 1.88/1.32/0.49 are on a 0–2 scale (poor / partial / good), and they reproduce 0.72, 0.48 and the mid-tween 0.65 [arith ✓]. The other rows do not all reconcile from Gemini's small-cell reads (Trail 0.42 vs computed 0.50; Metro 0.80 vs 0.68). Either Gemini misread them or the mock-up is not strictly computed. This is **unresolved and low-stakes**: the numbers are illustrative.
4. **Intent routing** (11:51). *"We're placing a decision at the entrance to several different handlers."* Reset my password → reset flow (a function); how do I configure SSO → documentation assistant; unresolved account dispute → support (a person) [sb]. *"It's the user's intent that determines where it actually goes, and then confidence is key."* "I can't log in" gives 48% / 45% / 7%, confidence 0.22 [sb], below the ready threshold of 0.5, so the system clarifies.
- **Bring it together** (12:18–13:34): a support system runs 01 intake → 02 fan-out (one request) → 03 gate ("clear enough to use?") → 04 handler (your code, P1) → 05 writer (a generative LLM drafts the reply "using the relevant evidence") [sb, stage labels via Gemini]. *"Each decision has a defined job and the application controls how the pieces fit together."* Where to start (13:13): *"pick a workflow you already understand, find a point where the software needs to interpret some fuzzy natural language, and then figure out what is the smallest useful question … what should happen when the answer is uncertain?"*

### Demonstrated vs described
**Nothing is run live.** Every pattern is a motion-graphics mock-up, and the numbers carry "illustrative" labels (00:07, 03:09, 03:29 …). The only real artefacts shown are TypeSafe's pricing and docs pages and the channel's own site. The claim that Jev runs inside their agentic RAG app is deferred to a separate video (14:09).

### Sales funnel
Subscribe/like ask at 06:02. The pitch runs 13:38–14:08 (*"These are the types of topics that we cover in our community, The AI Automators"*). It covers the "AI Builders Course" with modules Intro to Agentic Systems & AI Agents, Technical Foundations & Implementation (AI Coding), Agentic Retrieval and Harness Engineering [sb], and *"Link is in the description below"*. The end card, "Jev's decision engine in a real app — the agentic RAG build", is at 14:10 [sb]. No TypeSafe sponsorship is disclosed or evident. Whether any relationship exists is unknown.

### Analyst section — what transfers to Steve's enterprise (Claude Code zgents, beads, Gas City)
_This is Claude's assessment, not the video's._ The patterns are ordinary control-flow discipline around a probabilistic classifier. The video itself says they are model-agnostic. Jev's selling point is cost and latency at millions of calls, and that is not Steve's regime: his volume is dozens of decisions a day, run on Claude sessions. So take the patterns and leave the vendor.
- **Confidence-gated routing: transfers strongly.** It is already the enterprise's "Asking Steve" rule (act when decidable, ask one question when not, and silence means Deferred). The transferable refinement is to make the gate an explicit, tested threshold on a dispatch decision (`gc sling` / bead routing) rather than a judgment call, and to keep permission and confirmation checks outside the model. The caveat is that Claude or Gemini self-reported confidence is not a calibrated probability the way noul claims to be. Gemini's `uncertainties` field is the nearest analogue the enterprise has.
- **Intent routing: transfers.** It is the natural shape for an intake zgent or mail triage in front of `gc dispatch`: classify the request, send it to the owning rig or zgent, and clarify below the threshold. It matters once DReader has a query surface (dr-ok8).
- **Speculative fan-out: transfers where there are scripted LLM calls.** mread.py's wide pass already does it: one request, many questions, and code picks what it needs. The `jev-loop` skill's seven-question battery per tick is literally this pattern on Jev. It does not apply to interactive agent turns.
- **Composite scoring: partial.** It fits ranking `bd ready` work or grading cards (the corpus's Clarity/Alignment grades are an informal composite). Keep **weights you control**. Model-set dynamic weights hide the decision, which cuts against the audit-trail ethos.
- **Verification shape: already doctrine.** It matches `verify-quotes` and claim-vs-source checks. His line *"a quote can exist and still be used to make the wrong claim"* is worth keeping.
- **Does not transfer:** the real-time uses (150 ms games or UI), map-reduce over millions of records, and feature extraction for non-generative ML models. The enterprise has none of these workloads. The $/token case for adding a TypeSafe dependency does not arise at this volume.

### Credibility
It is a clear and well-structured explainer: Clarity A−. The taxonomy (types → shapes → patterns) is sound and honestly framed as model-agnostic. The weaknesses are that every example is an illustrative animation with no live run, and the vendor's 193.6×/444.6× claim is shown without scrutiny. The episode is a funnel into the community and course, and into the RAG-build video where any real evidence would be. Use it as a vocabulary and pattern reference, not as evidence that Jev performs.

**Uncertainties:** the presenter's name, "Daniel Walsh" (a Gemini read of the 03:25 lower third, not caught by any storyboard tile); Composite-scoring rows other than Commuter; stage labels in the 12:25 diagram; the footnote text on the 193.6× slide; the `client.systemOne(req)` code line at 00:07 (Gemini-only).

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-26 (dr-o0h).** The aim was to establish what Jev is, list every pattern and shape with definition, example and timestamp, separate demo from description, and assess what transfers to the enterprise. Runs: wide pass `20260926-065441` (78,662 prompt tokens); clipped zooms `065511` `065518` `065521` `065523` `065526` (mixed speech + on-screen); verbatim-speech-only zooms `065601` `065604` `065605` `065610`; composite-scoring numbers `070105`. `frames` failed with a YouTube 403, so on-screen claims were checked on storyboard mosaics M0, M1, M4, M5, M9, M13–M16 and M18. Verdict: Jev is TypeSafe's decision model (the one jev-loop uses). The video gives 3 types, 10 shapes and 4 patterns, all described with nothing run live, and ends in a course funnel. Closed.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- The AI Automators produces motion-graphics explainers with a picture-in-picture presenter. Section title cards ("01 / Design pattern / …") are large and read cleanly even on 320×180 storyboard tiles. Code snippets and table cells do not.
- Numbers on the mock-ups are self-labelled "illustrative". Arithmetic checks work on the headline row but not reliably on the others, so do not spend frames reconciling them.
- The channel runs a series on Jev plus an agentic RAG app build. The end card points to the RAG video ("I gave my RAG agent a decision engine (Jev)"), which is where any live evidence would be.
- 06:00–12:20 is the dense stretch (shapes → patterns). The mixed "speech + on-screen text" zoom paraphrased the speech there. A speech-only verbatim prompt fixed it.

## Run log
_(machine-appended by mread.py — do not edit above this line's entries)_
- 20260926-065441 [full] gemini-flash-latest (tok 78662/2318) — Q: First: what does the word 'Jev' (or whatever the word in the title is — spell it… — runs/20260926-065441/
- 20260926-065511 [00:00-03:00] gemini-flash-latest (tok 16667/4634) — Q: Transcribe the presenter's speech in this window VERBATIM with timestamps (every… — runs/20260926-065511/
- 20260926-065518 [12:15-14:20] gemini-flash-latest (tok 11660/2409) — Q: Transcribe the presenter's speech in this window VERBATIM with timestamps (every… — runs/20260926-065518/
- 20260926-065521 [03:00-06:00] gemini-flash-latest (tok 16667/4570) — Q: Transcribe the presenter's speech in this window VERBATIM with timestamps (every… — runs/20260926-065521/
- 20260926-065523 [06:00-09:45] gemini-flash-latest (tok 20762/4108) — Q: Transcribe the presenter's speech in this window VERBATIM with timestamps (every… — runs/20260926-065523/
- 20260926-065526 [09:40-12:20] gemini-flash-latest (tok 14846/4196) — Q: Transcribe the presenter's speech in this window VERBATIM with timestamps (every… — runs/20260926-065526/
- 20260926-065601 [05:55-07:30] gemini-flash-latest (tok 8938/1548) — Q: Speech transcription ONLY. Transcribe every word the presenter speaks in this wi… — runs/20260926-065601/
- 20260926-065604 [07:25-09:45] gemini-flash-latest (tok 13033/2090) — Q: Speech transcription ONLY. Transcribe every word the presenter speaks in this wi… — runs/20260926-065604/
- 20260926-065605 [09:40-11:00] gemini-flash-latest (tok 7573/1179) — Q: Speech transcription ONLY. Transcribe every word the presenter speaks in this wi… — runs/20260926-065605/
- 20260926-065610 [10:55-12:20] gemini-flash-latest (tok 8028/1165) — Q: Speech transcription ONLY. Transcribe every word the presenter speaks in this wi… — runs/20260926-065610/
- 20260926-070105 [11:24-11:54] gemini-flash-latest (tok 3073/1952) — Q: This is an animated composite-scoring table. Transcribe EVERY distinct state of … — runs/20260926-070105/
