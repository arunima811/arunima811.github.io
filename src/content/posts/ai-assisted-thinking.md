---
title: AI-assisted thinking, not AI thinking
date: 2026-11-18
tab: notwork
summary: What the research says about using AI without switching your own brain off, and how I decide what to hand over and what to keep.
tags: [ai, thinking, learning]
---

[YOUR STORY: a moment you noticed you'd stopped thinking — a non-work one, 3–5 sentences]

Turns out I'm in good company. In January 2026, Andrej Karpathy, who gave vibe coding its name, wrote that in about a month he'd gone from writing 80% of his code by hand to letting agents write 80% of it. Then: ["I am slowly starting to atrophy my ability to write code manually."](https://x.com/karpathy/status/2015883857489522876)

A week later, the essay [*I miss thinking hard*](https://www.jernesto.com/articles/thinking_hard) drew [1,310 points on Hacker News](https://news.ycombinator.com/item?id=46881264). Its author felt AI coding was feeding the builder in him and starving the thinker. Anthropic's researchers, studying their own engineers, [describe a paradox of supervision](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic): using Claude well takes the very skills that fade when Claude does the work. Some of those engineers now work without AI on purpose, to stay sharp.

My idea is simple: let AI do the execution, and keep the thinking human. The research mostly agrees, with one refinement: *thinking* isn't one thing. For any task, ask: **do I want this done, or do I want to get better at it?**

## AI is great at doing, unevenly

This isn't an anti-AI post, so the good news first. On the right tasks the gains are big, and biggest for people with less experience.

- ChatGPT cut professionals' writing time by 40%, and the writing got better too ([Noy & Zhang](https://doi.org/10.1126/science.adh2586)).
- With an AI assistant, the least skilled customer-support agents resolved 34% more issues per hour ([Brynjolfsson, Li & Raymond](https://www.nber.org/papers/w31161)).
- BCG consultants using GPT-4 worked 25.1% faster on tasks within AI's reach ([Dell'Acqua et al.](https://doi.org/10.1287/orsc.2025.21838)).

Then the catch. On one task just outside what the authors call AI's jagged frontier, the uneven edge of what it does well, consultants with AI were 19 percentage points less likely to get it right. The frontier isn't marked; you find out which side you're on by checking. Across 106 studies, human-plus-AI beat humans alone but often did worse than the better of human or AI alone, especially on decisions ([Vaccaro, Almaatouq & Malone](https://doi.org/10.1038/s41562-024-02024-1)).

Karpathy's test for what AI will take over is [whether the result can be verified](https://x.com/karpathy/status/1990116666194456651). That's my working definition of *execution*: work whose result I can check.

## Output isn't learning

This is the study I wish everyone knew. About 1,000 high-school students in Turkey practiced math with no AI, a plain ChatGPT-like assistant (GPT Base), or a tutor version their teachers set up to give hints, never answers (GPT Tutor). Then everyone sat the same exam without AI ([Bastani et al.](https://www.pnas.org/doi/10.1073/pnas.2422633122)).

Each bar is a score as a share of the no-AI class's score (no AI is 100%).

![Scores as a share of the no-AI class's score. In practice with AI, GPT Base reached 148% and GPT Tutor 227%. On the exam without AI, GPT Base fell to 83% and GPT Tutor stayed at about 100%.](/posts/ai-assisted-thinking/practice-vs-exam.svg)

<details><summary>Data table</summary><table><thead><tr><th>Classroom</th><th>Practice with AI, vs the no-AI class</th><th>Exam without AI, vs the no-AI class</th></tr></thead><tbody><tr><td>No AI</td><td>baseline (100%)</td><td>baseline (100%)</td></tr><tr><td>GPT Base (plain)</td><td>+48% (148%)</td><td>−17% (83%), statistically significant</td></tr><tr><td>GPT Tutor (hints only)</td><td>+127% (227%)</td><td>no significant difference (estimate close to zero), shown as ≈100%</td></tr></tbody></table></details>

Plain GPT lifted practice scores, then those students scored 17% lower on the exam than the class without AI. The tutor lifted practice even more and held level on the exam. Same model, different guardrails. The part that stings, for me: the plain-GPT students didn't think they had learned less.

Other studies agree. Students who studied with ChatGPT remembered less on a surprise test 45 days later, 57.5% against 68.5% ([Barcaui](https://doi.org/10.1016/j.ssaho.2025.102287)). Teenagers learned a text better by taking notes than by using an AI chatbot on its own, yet most preferred the chatbot ([Kreijkes et al.](https://doi.org/10.1016/j.compedu.2025.105514)).

Output and learning are different things. Even the labs now ship [study](https://openai.com/index/chatgpt-study-mode/) and [learning](https://www.anthropic.com/news/introducing-claude-for-education) modes that ask you questions instead of handing over answers.

## How you ask matters more than whether

Anthropic ran its own small trial on this, so read it knowing they make the product. Mostly junior developers learned Trio, a Python library new to them, with or without an AI assistant, then took a quiz. The AI group averaged 50% and the no-AI group 67%, with the biggest gap on debugging ([Shen & Tamkin, preprint](https://arxiv.org/abs/2601.20245)). The researchers also sorted how people used the assistant. Anthropic's write-up gives only score bands for the six patterns, so those bars stop at the band edge.

![Quiz scores: 67% without AI and 50% with AI. Within the AI group, people who asked only conceptual questions, asked for code with explanations, or generated code and then asked about it scored 65% or more. People who fully delegated, relied on AI more and more, or let AI debug scored under 40%. The six pattern bars stop at the edge of their score band, not at an exact score.](/posts/ai-assisted-thinking/quiz-by-pattern.svg)

<details><summary>Data table</summary><table><thead><tr><th>Group or pattern</th><th>People</th><th>Quiz score</th></tr></thead><tbody><tr><td>No AI</td><td>whole group</td><td>67% average</td></tr><tr><td>With AI</td><td>whole group</td><td>50% average</td></tr><tr><td>Conceptual questions only</td><td>7</td><td>65% or more (and the second-fastest pattern)</td></tr><tr><td>Code together with explanations</td><td>3</td><td>65% or more</td></tr><tr><td>Generate code, then ask to understand it</td><td>2</td><td>65% or more</td></tr><tr><td>Full delegation</td><td>4</td><td>under 40%</td></tr><tr><td>Progressive reliance</td><td>4</td><td>under 40%</td></tr><tr><td>Iterative AI debugging</td><td>4</td><td>under 40%</td></tr></tbody></table></details>

Handing over the work went with low scores; asking questions to understand it went with high ones, and the concepts-only group was the second-fastest too. The groups are tiny and it's a correlation, but it fits the other studies here. As the team [put it](https://www.anthropic.com/research/AI-assistance-coding-skills): "Cognitive effort—and even getting painfully stuck—is likely important for fostering mastery."

Bigger studies agree. In a supervised trial, AI's boost lasted a week for students who used it as a tutor and faded for those who let it write for them ([Contractor & Reyes, preprint](https://arxiv.org/abs/2607.08849)). And among 244 of those consultants whose chat logs were studied, the 27% who handed the whole task to AI built neither domain skill nor AI skill, judging by their logs and interviews ([Randazzo et al.](https://www.hbs.edu/ris/Publication%20Files/26-036_e7d0e59a-904c-49f1-b610-56eb2bdfe6f9.pdf)).

## You can't feel it

If AI were quietly making us worse, wouldn't we notice? Mostly, no.

- In a small early-2025 study, experienced open-source developers felt 20% faster with AI and were measured 19% slower ([METR](https://arxiv.org/abs/2507.09089)). METR now says developers are probably faster, but it [can't measure by how much](https://metr.org/blog/2026-02-24-uplift-update/). What lasts is the gap between feeling and stopwatch.
- Using AI on logic-test questions, people overestimated their scores by 4 points, and those who knew more about AI were worse at judging their own score ([Fernandes et al.](https://doi.org/10.1016/j.chb.2025.108779)).
- People with an AI assistant wrote less secure code and felt surer it was secure ([Perry et al.](https://arxiv.org/abs/2211.03622)).
- Struggling beginners ended up with what researchers call an illusion of competence ([Prather et al.](https://arxiv.org/abs/2405.17739)).

Fluent output feels like understanding. So I'd rather measure than trust the feeling.

## What's good for the brain (my reasoning)

This section is my reasoning, not a finding about AI: well-tested learning science applied to AI, with each mechanism named so you can check me. None of it shows AI damages your brain; the MIT study behind the scariest headlines is a small preprint, not yet peer-reviewed, of 54 students writing essays ([Kosmyna et al.](https://arxiv.org/abs/2506.08872)).

1. **Make the first move yourself.** Sketch or guess before you prompt. *Mechanism:* the generation effect: you remember what you produce better than what you read, a small-to-medium boost averaged over 86 studies ([Bertsch et al.](https://doi.org/10.3758/BF03193441)). Going first also helps keep the AI from anchoring you; some studies find AI help makes people's ideas more alike ([Doshi & Hauser](https://doi.org/10.1126/sciadv.adn5290)), though not all.
2. **After AI explains something, close it and say it back.** *Mechanism:* the testing effect. Recalling beats re-reading, and re-reading inflates confidence ([Roediger & Karpicke](https://doi.org/10.1111/j.1467-9280.2006.01693.x)). An AI explanation is re-reading.
3. **Keep the struggle you can win.** Ask for hints, not answers. *Mechanism:* desirable difficulties: what slows practice down often helps learning, if you can get past it ([Bjork & Bjork](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf)).
4. **Offload what you're not trying to get better at.** *Mechanism:* cognitive offloading, letting a tool hold some of your thinking ([Risko & Gilbert](https://doi.org/10.1016/j.tics.2016.07.002)). It frees your head when the tool is reliable ([Storm & Stone](https://doi.org/10.1177/0956797614559285)), and AI is only partly reliable, so offload where you can check.
5. **The better the AI gets, the more you should practice the rare case.** *Mechanism:* automation bias. People follow automation when it's wrong, experts included, and training doesn't prevent it ([Parasuraman & Manzey](https://doi.org/10.1177/0018720810376055)). Bainbridge named a related irony in 1983: the most automated systems may need the best-trained humans ([Bainbridge](https://doi.org/10.1016/0005-1098(83)90046-8)).

Here's number 5 in real life: 27 radiologists read mammograms with suggestions from what was presented as an AI, wrong on 12 of the 40 images ([Dratsch et al.](https://doi.org/10.1148/radiol.222176)).

![Radiologists' accuracy. When the AI suggestion was right, all three experience levels scored about 80%. When it was wrong, inexperienced readers scored 19.8%, moderately experienced 24.8% and very experienced 45.5%.](/posts/ai-assisted-thinking/ai-wrong-by-experience.svg)

<details><summary>Data table</summary><table><thead><tr><th>Experience</th><th>Accuracy when the AI was right</th><th>Accuracy when the AI was wrong</th></tr></thead><tbody><tr><td>Inexperienced</td><td>79.7%</td><td>19.8%</td></tr><tr><td>Moderately experienced</td><td>81.3%</td><td>24.8%</td></tr><tr><td>Very experienced</td><td>82.3%</td><td>45.5%</td></tr></tbody></table></details>

When the AI was wrong, even the most experienced readers fell from about 80% to 45.5%. Experts fell less far than beginners, but they still fell.

Ted Chiang has the best image for using AI on work you're meant to grow from: it's ["like bringing a forklift into the weight room"](https://www.newyorker.com/culture/the-weekend-essay/why-ai-isnt-going-to-make-art).

## It depends on your job

What matters more than job title is how new you are to the work, and whether you want the output or the skill. Newcomers gain the most output ([less experienced developers gained more](https://doi.org/10.1287/mnsc.2025.00535)) and have the most learning to lose; experience protects only partly. A workshop Martin Fowler wrote up concluded that [mid-level developers face the hardest squeeze](https://www.martinfowler.com/fragments/2026-02-13.html).

Each row says what backs it: *studies*, *practitioners* (experience, not measurement) or *my read*. The senior, data/platform and manager rows are mostly my read.

| Role | Delegate | Keep | Optimize for | Main risk |
|---|---|---|---|---|
| **Student** *(studies)* | Explanations after your own attempt, practice questions, a hints-only tutor | The first attempt, the struggle, your own notes, the essay's argument | What you can do without AI next week, not this week's grade | Practice goes up, the unaided exam goes down, and you don't notice |
| **Junior engineer** *(studies, practitioners)* | Boilerplate (repetitive standard code) you can already read, explanations, concept questions | First-pass debugging, design choices, explaining every line | Skill, and a mental model of the system | Looking competent without being it |
| **Senior / staff engineer** *(practitioners, my read)* | Well-specified, testable work: restructuring code, migration mechanics, test scaffolding | Framing the problem, splitting it up, deciding how hard to review | Leverage without losing the ability to supervise | Review skills fade from disuse, and shortcuts become normal |
| **Data / platform engineer** *(my read, practitioners)* | Pipeline boilerplate, backfill mechanics, reconciliation queries and tests | What the data means, whether a number is right, judgment on an on-call night | Correctness that's hard to see, and readiness for the rare bad night | Silently wrong numbers, and nobody practiced for the incident that matters |
| **Manager / tech lead** *(my read, practitioners)* | Status summaries, first drafts, meeting notes, all read critically | The team's shared understanding, who learns what, your own hands-on time | Team understanding and review capacity, not output per head | [Cognitive debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/), code nobody can explain; juniors who don't grow because [seniors absorb their work](https://arxiv.org/abs/2607.17067) |
| **Writer** *(practitioners, studies)* | Reader feedback, edits, fact-checks, research lookups | The first draft, the argument, the voice | The thinking that writing does | Write-nots become think-nots, and your voice drifts toward everyone else's |

**Researchers** *(practitioners, my read)*: hand off boilerplate, reports and a first literature pass; keep the question, the new ideas and the primary sources. Karpathy hand-wrote his nanochat project because agents were [net unhelpful there](https://x.com/karpathy/status/1977758204139331904), possibly because it was far from what they'd been trained on.

**Designers** *(my read)*: sketch first, then let AI generate variants and edge cases; keep choosing and judging. Beware polish: when a Claude chat produced a finished artifact, [people questioned its reasoning less](https://academy.claude.com/tutorials/the-ai-fluency-index).

## Nothing is free: tradeoffs and my rules

- **AI first or me first?** An AI first draft kills the blank page but can anchor you toward what everyone else would write. Going first costs time and keeps the ideas mine. Ethan Mollick's order: ["think first, write first, meet first."](https://www.oneusefulthing.org/p/against-brain-damage)
- **All in, or a dial?** Vibe coding, accepting whatever the AI writes unread, is OK for what Karpathy scoped it to: [throwaway weekend projects](https://x.com/karpathy/status/1886192184808149383). For real work he argues for an [autonomy slider](https://www.youtube.com/watch?v=LCEmiRjPEtQ). Mine: low on new or high-stakes work, higher on boilerplate with good tests.
- **Review everything, or sample?** Birgitta Böckeler [sets review effort by risk](https://www.martinfowler.com/articles/exploring-gen-ai/to-vibe-or-not-vibe.html): how likely is the AI to be wrong, how bad would that be, and how easily would you notice? Simon Willison wrote in 2025 that ["the one thing you absolutely cannot outsource to the machine is testing"](https://simonwillison.net/2025/Mar/11/using-llms-for-code/); in 2026 he stopped reading every line of routine code and named the risk himself, [normalization of deviance](https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/): small shortcuts slowly becoming normal.
- **Always on, or time off?** The skills you need when AI is wrong are the ones that fade. Addy Osmani suggests [no-AI days](https://addyo.substack.com/p/avoiding-skill-atrophy-in-the-age); an essay on site reliability work suggests [keeping some incidents for human practice](https://newsletter.signoz.io/p/ai-isnt-replacing-sres-its-deskilling), like pilots' required manual flying time.

My own rules are short:

1. I think or sketch first, then prompt.
2. I own the design and the why; AI owns the typing.
3. I don't ship what I can't explain.

The third echoes Simon Willison's [golden rule](https://simonwillison.net/2025/Mar/19/vibe-coding/) for production code. And here's where I stop delegating: **I read everything that decides whether a number is right; I skim boilerplate that has tests.**

## Try this tomorrow

1. Sort tomorrow's tasks into two lists, *want it done* and *want to get better at it*, and delegate only from the first.
2. Switch on a study or learning mode for the next new thing you learn.
3. Before you accept an answer you can't easily check, write down how you'd notice if it were wrong.
4. Put one no-AI hour in your calendar this week, for a skill you'd need on the day the AI gets it wrong.
5. Time one task with AI and a similar one without, and compare that with how fast it felt.

## The part I keep

Paul Graham argues that writing is thinking, so as AI removes the pressure to learn to write, people will split into those who think and those who don't: ["there's a kind of thinking that can only be done by writing"](https://paulgraham.com/writes.html). Anthropic's [Reflect](https://www.anthropic.com/news/reflect-with-claude) dashboard asks people what they want to keep doing themselves, even if Claude could do it faster.

That's the question I'd leave you with. Here's one thing I keep: a poem I wrote without AI.

[YOUR POEM: 8–12 lines, written by you without AI]

*How this was made: AI agents found and checked the sources, proposed the outline, drafted the text and made the charts. The idea, the rules I chose, the story, the poem and the final edit are mine.*

<details><summary>Sources</summary>

- **Learning:** [Bastani et al. 2025, *PNAS*](https://www.pnas.org/doi/10.1073/pnas.2422633122); [Shen & Tamkin 2026, preprint](https://arxiv.org/abs/2601.20245) and [Anthropic's write-up](https://www.anthropic.com/research/AI-assistance-coding-skills); [Barcaui 2025](https://doi.org/10.1016/j.ssaho.2025.102287); [Kreijkes et al. 2026](https://doi.org/10.1016/j.compedu.2025.105514); [Contractor & Reyes 2026, preprint](https://arxiv.org/abs/2607.08849); [Kosmyna et al. 2025, preprint](https://arxiv.org/abs/2506.08872).
- **Work:** [Noy & Zhang 2023](https://doi.org/10.1126/science.adh2586); [Brynjolfsson, Li & Raymond, working paper](https://www.nber.org/papers/w31161) and [2025 journal version](https://doi.org/10.1093/qje/qjae044); [Dell'Acqua et al. 2026](https://doi.org/10.1287/orsc.2025.21838); [Randazzo et al. 2025, working paper](https://www.hbs.edu/ris/Publication%20Files/26-036_e7d0e59a-904c-49f1-b610-56eb2bdfe6f9.pdf); [Vaccaro, Almaatouq & Malone 2024](https://doi.org/10.1038/s41562-024-02024-1); [Cui et al. 2026](https://doi.org/10.1287/mnsc.2025.00535); [Doshi & Hauser 2024](https://doi.org/10.1126/sciadv.adn5290); [Yu & Moon 2026](https://arxiv.org/abs/2607.17067).
- **Judging yourself:** [METR 2025, preprint](https://arxiv.org/abs/2507.09089) and [2026 update](https://metr.org/blog/2026-02-24-uplift-update/); [Fernandes et al. 2026](https://doi.org/10.1016/j.chb.2025.108779); [Perry et al. 2023](https://arxiv.org/abs/2211.03622); [Prather et al. 2024](https://arxiv.org/abs/2405.17739).
- **Automation:** [Dratsch et al. 2023](https://doi.org/10.1148/radiol.222176); [Parasuraman & Manzey 2010](https://doi.org/10.1177/0018720810376055); [Bainbridge 1983](https://doi.org/10.1016/0005-1098(83)90046-8).
- **Learning science:** [Bertsch et al. 2007](https://doi.org/10.3758/BF03193441); [Roediger & Karpicke 2006](https://doi.org/10.1111/j.1467-9280.2006.01693.x); [Bjork & Bjork 2011](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf); [Risko & Gilbert 2016](https://doi.org/10.1016/j.tics.2016.07.002); [Storm & Stone 2015](https://doi.org/10.1177/0956797614559285).
- **Practitioners and labs:** Karpathy on [vibe coding](https://x.com/karpathy/status/1886192184808149383) (Feb 2025), [nanochat](https://x.com/karpathy/status/1977758204139331904) (Oct 2025), [verifiability](https://x.com/karpathy/status/1990116666194456651) (Nov 2025) and [atrophy](https://x.com/karpathy/status/2015883857489522876) (Jan 2026), plus his [Software 3.0 talk](https://www.youtube.com/watch?v=LCEmiRjPEtQ) (2025); Anthropic on [work at Anthropic](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic), the [AI Fluency Index](https://academy.claude.com/tutorials/the-ai-fluency-index), [Reflect](https://www.anthropic.com/news/reflect-with-claude) and [learning mode](https://www.anthropic.com/news/introducing-claude-for-education); OpenAI's [study mode](https://openai.com/index/chatgpt-study-mode/); Simon Willison on [how he codes with LLMs](https://simonwillison.net/2025/Mar/11/using-llms-for-code/) and [vibe coding](https://simonwillison.net/2025/Mar/19/vibe-coding/) (2025) and [agentic engineering](https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/) (2026); [Ethan Mollick](https://www.oneusefulthing.org/p/against-brain-damage); [Birgitta Böckeler](https://www.martinfowler.com/articles/exploring-gen-ai/to-vibe-or-not-vibe.html); [Martin Fowler](https://www.martinfowler.com/fragments/2026-02-13.html); [Margaret-Anne Storey](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/); [Addy Osmani](https://addyo.substack.com/p/avoiding-skill-atrophy-in-the-age); [Paul Graham](https://paulgraham.com/writes.html); [Ted Chiang](https://www.newyorker.com/culture/the-weekend-essay/why-ai-isnt-going-to-make-art); [*I miss thinking hard*](https://www.jernesto.com/articles/thinking_hard) and its [Hacker News thread](https://news.ycombinator.com/item?id=46881264); [an essay on SRE deskilling](https://newsletter.signoz.io/p/ai-isnt-replacing-sres-its-deskilling).

</details>
