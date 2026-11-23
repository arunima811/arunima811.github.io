---
title: AI-assisted thinking, not AI thinking
date: 2026-11-22
tab: notwork
summary: How I'm learning system design and prompt engineering with AI next to me, without letting it do the thinking I'm trying to learn.
tags: [ai, learning, system design, prompt engineering]
---

I'm learning system design and prompt engineering right now, with AI open next to me. It will happily hand me a finished architecture or a polished prompt. That's the trap. The research keeps finding the same pattern: when AI does the part of the work that builds skill, the work looks better, the learning gets worse, and people can't feel the difference.

So before I hand anything over, I ask one question: **do I want this done, or do I want to get better at it?** If I want it done, I delegate. If I want to get better at it, I keep the thinking and use AI to push on it.

## Output isn't understanding

About 1,000 high-school students in Turkey practiced math with no AI, with a plain ChatGPT-like assistant (GPT Base), or with a tutor version their teachers set up to give hints, never answers (GPT Tutor). Then everyone sat the same exam without AI ([Bastani et al.](https://www.pnas.org/doi/10.1073/pnas.2422633122)).

Each bar is a score as a share of the no-AI class's score (no AI is 100%).

![Scores as a share of the no-AI class's score. In practice with AI, GPT Base reached 148% and GPT Tutor 227%. On the exam without AI, GPT Base fell to 83% and GPT Tutor stayed at about 100%.](/posts/ai-assisted-thinking/practice-vs-exam.svg)

<details><summary>Data table</summary><table><thead><tr><th>Classroom</th><th>Practice with AI, vs the no-AI class</th><th>Exam without AI, vs the no-AI class</th></tr></thead><tbody><tr><td>No AI</td><td>baseline (100%)</td><td>baseline (100%)</td></tr><tr><td>GPT Base (plain)</td><td>+48% (148%)</td><td>−17% (83%), statistically significant</td></tr><tr><td>GPT Tutor (hints only)</td><td>+127% (227%)</td><td>no significant difference (estimate close to zero), shown as 100%</td></tr></tbody></table></details>

Plain GPT lifted practice scores, then those students scored 17% lower on the exam than the class without AI, and they didn't think they had learned less. The tutor version lifted practice even more and held level on the exam. Same model, different guardrails: in the first session, 67% of plain-GPT students' first message on a problem just pasted the question or asked for the answer; with the tutor, 37% did.

Anthropic found a similar learning cost in its own small trial; it makes the product, so weigh that. Developers learning an unfamiliar Python library scored 50% on a quiz with AI and 67% without, and the biggest gap was on debugging ([Shen & Tamkin, preprint](https://arxiv.org/abs/2601.20245)).

## How you ask matters

The researchers also sorted how people used the assistant. Anthropic's write-up gives only score bands for the six patterns, so those bars stop at the band edge.

![Quiz scores: 67% without AI and 50% with AI. Within the AI group, people who asked only conceptual questions, asked for code with explanations, or generated code and then asked about it scored 65% or more. People who fully delegated, relied on AI more and more, or let AI debug scored under 40%. The six pattern bars stop at the edge of their score band, not at an exact score.](/posts/ai-assisted-thinking/quiz-by-pattern.svg)

<details><summary>Data table</summary><table><thead><tr><th>Group or pattern</th><th>People</th><th>Quiz score</th></tr></thead><tbody><tr><td>No AI</td><td>whole group</td><td>67% average</td></tr><tr><td>With AI</td><td>whole group</td><td>50% average</td></tr><tr><td>Conceptual questions only</td><td>7</td><td>65% or more (and the second-fastest pattern)</td></tr><tr><td>Code together with explanations</td><td>3</td><td>65% or more</td></tr><tr><td>Generate code, then ask to understand it</td><td>2</td><td>65% or more</td></tr><tr><td>Full delegation</td><td>4</td><td>under 40%</td></tr><tr><td>Progressive reliance</td><td>4</td><td>under 40%</td></tr><tr><td>Iterative AI debugging</td><td>4</td><td>under 40%</td></tr></tbody></table></details>

Handing the work over went with scores under 40%. Asking questions to understand went with 65% or more, and asking only conceptual questions was the second-fastest pattern too. The groups are tiny and it's a correlation, but the team's [conclusion](https://www.anthropic.com/research/AI-assistance-coding-skills) is worth keeping: "Cognitive effort—and even getting painfully stuck—is likely important for fostering mastery."

My takeaway: use AI as a tutor and a critic, not an answer machine. In practice that means asking why before asking what, and asking for a hint before the answer.

## You can't feel it

In early 2025, experienced open-source developers felt about 20% faster with AI and were measured 19% slower ([METR](https://arxiv.org/abs/2507.09089)). METR's [2026 update](https://metr.org/blog/2026-02-24-uplift-update/) says developers were probably faster by early 2026, but it can't measure by how much. And when a supposed AI gave radiologists the wrong category, many followed it: accuracy was about 80% when the AI was right, but 19.8% for the least experienced and 45.5% for the most when it was wrong ([Dratsch et al.](https://doi.org/10.1148/radiol.222176)).

Smooth, finished-looking output feels like understanding. So I test myself instead of trusting the feeling.

## How I'm learning system design

This is my approach, not a study; most steps lean on the evidence.

- **I sketch first.** Requirements, rough numbers, the main components and the likely bottleneck go down before I open a chat. People remember what they produce better than what they read (the generation effect, across [86 studies](https://doi.org/10.3758/BF03193441)), and Ethan Mollick's order is ["think first, write first, meet first."](https://www.oneusefulthing.org/p/against-brain-damage)
- **Then I ask AI to attack it.** What fails first, what breaks at ten times the load, which trade-offs I missed. Karpathy finds that coding agents [don't push back or surface trade-offs](https://x.com/karpathy/status/2015883857489522876), so I ask for it directly, the way Anthropic suggests: [tell the model to push back when your assumptions are wrong](https://academy.claude.com/tutorials/the-ai-fluency-index).
- **I ask it to quiz me, then grade my explanation.** Recalling beats re-reading, and re-reading inflates confidence ([Roediger & Karpicke](https://doi.org/10.1111/j.1467-9280.2006.01693.x)).
- **I don't keep a component I can't defend.** If I can't say why it's there, it goes.

My three rules:

1. I think or sketch first, then prompt.
2. I own the design and the why; AI owns the typing.
3. I don't ship what I can't explain.

## Prompt engineering is design too

A prompt is a spec, so I write it like one: what a good answer looks like, plus a few test cases, before I ask. Then I check the output against them.

Karpathy argues that what AI can take over depends on whether the result can be checked: ["the new most predictive feature to look at is verifiability"](https://x.com/karpathy/status/1990116666194456651). Simon Willison is blunter: ["the one thing you absolutely cannot outsource to the machine is testing"](https://simonwillison.net/2025/Mar/11/using-llms-for-code/).

Where I can't write a check, I review by hand, using Birgitta Böckeler's [test for how hard to review](https://www.martinfowler.com/articles/exploring-gen-ai/to-vibe-or-not-vibe.html): how likely is the AI to be wrong, how bad would that be, and how easily would I notice? My line: **I read everything that decides whether a number is right; I skim boilerplate that has tests.**

## Try this tomorrow

- Before your next AI session, decide: do I want this done, or do I want to get better at it?
- On anything you're learning, ask for a hint before the answer.
- Ask the AI to quiz you, and answer without looking.
- Before your next prompt, write down what a good answer looks like and three test cases.
- Time one task with and without AI, and compare it with how fast it felt.

*How this was made: AI agents found and checked the sources, proposed the outline, drafted the text and made the charts. The idea, the rules I chose and the final edit are mine.*

<details><summary>Sources</summary>

- **Learning:** [Bastani et al. 2025, *PNAS*](https://www.pnas.org/doi/10.1073/pnas.2422633122); [Shen & Tamkin 2026, preprint](https://arxiv.org/abs/2601.20245) and [Anthropic's write-up](https://www.anthropic.com/research/AI-assistance-coding-skills); [Bertsch et al. 2007](https://doi.org/10.3758/BF03193441); [Roediger & Karpicke 2006](https://doi.org/10.1111/j.1467-9280.2006.01693.x).
- **Judging yourself:** [METR 2025, preprint](https://arxiv.org/abs/2507.09089) and [2026 update](https://metr.org/blog/2026-02-24-uplift-update/); [Dratsch et al. 2023](https://doi.org/10.1148/radiol.222176).
- **Practitioners and labs:** Andrej Karpathy on [agents](https://x.com/karpathy/status/2015883857489522876) (Jan 2026) and [verifiability](https://x.com/karpathy/status/1990116666194456651) (Nov 2025); Anthropic's [AI Fluency Index](https://academy.claude.com/tutorials/the-ai-fluency-index); [Ethan Mollick](https://www.oneusefulthing.org/p/against-brain-damage); [Birgitta Böckeler](https://www.martinfowler.com/articles/exploring-gen-ai/to-vibe-or-not-vibe.html); [Simon Willison](https://simonwillison.net/2025/Mar/11/using-llms-for-code/).

</details>
