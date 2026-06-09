# LinkedIn Post Template

> Long-form research storytelling. 300–800 words. One post, no threads needed.

---

## Structure

```
[Headline: Problem-focused, one sentence that hooks researchers]

[Paragraph 1 — The Problem]
[Why this matters. Human angle. Who is affected. 2-3 sentences.]

[Paragraph 2 — What We Built]
[The pipeline, tool, or method in plain language. 3-4 sentences.]
[Avoid jargon. A computational linguist should get it. An economist should too.]

[Paragraph 3 — What We Found]
[Results. Numbers. 2-3 sentences with a key figure if possible.]

[Paragraph 4 — Why It Matters / What's Next]
[Implications for the field. Call to collaboration. 2-3 sentences.]

[Call to Action]
We're actively seeking [linguists / NLP researchers / annotators] for [languages].
Full collaboration framework: [COLLABORATION.md link]
Full paper: [OSF/arXiv link]

#LILALab #[field] #[languages]
```

---

## Example

**Headline:** We built the first economic narrative index for Bangla — here's what we found.

**Paragraph 1:**
Bangla is the 7th most spoken language in the world, with 265 million speakers. Yet there are zero validated NLP tools for measuring economic narratives in Bangla news. This means policymakers in Bangladesh have no way to track how news coverage shapes inflation expectations, currency sentiment, or economic confidence — in the language most people actually read.

**Paragraph 2:**
We built the Bangla Exploration & Native-language Intelligence pipeline (LILA-BENI — the Bangla member of our XENI family). It collects raw Bangla news articles, classifies them as Economic or Not Economic using a TF-IDF classifier trained on 3,200 human-annotated + LLM-corrected labels, and outputs a daily narrative index. The full pipeline requires no GPU and costs about $0.02/article in LLM annotation — making it replicable for any low-resource language.

**Paragraph 3:**
When we validated the index against Bangladesh's macroeconomic indicators, we found a level correlation of r=-0.75 with CPI and r=-0.72 with the Taka-Dollar exchange rate (both p<0.001). This is the first evidence that Bangla-language economic news narratives track real economic outcomes — and that our pipeline can capture that signal.

**Paragraph 4:**
The pipeline is language-agnostic. We designed it for easy adaptation — swap the language, adjust the stopword list, and the same pipeline produces a narrative index for Assamese, Nepali, Sylheti, or any low-resource language with sufficient news text.

**Call to Action:**
We're actively seeking linguistic experts for Assamese, Nepali, and other South Asian languages to help build the next XENI pipelines. If you speak a language underserved by current NLP, we want to work with you.

Full collaboration framework → [COLLABORATION.md link]
Technical report → [OSF/arXiv link]
Code → [GitHub link]

#LILALab #NLP #LowResourceLanguages #Bangla #ComputationalSocialScience
