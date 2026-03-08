# Literature Review: How does the model count in French?

## Review Scope

### Research Question
How do language models represent and process counting, number words, and arithmetic in French, and what benchmarks/methods best expose these mechanisms?

### Inclusion Criteria
- Papers on LM numeracy, arithmetic reasoning, tokenization of number-like strings, and multilingual math reasoning.
- Papers with actionable datasets, baselines, or code.
- Preference for work with French or multilingual evaluation including French.

### Exclusion Criteria
- Unrelated general LLM papers without numeric component.
- Non-accessible papers without sufficient abstract/method information.

### Time Frame
2019-2025 (plus seminal references as needed).

### Sources
- Paper-finder script (service returned no relevant hits for this niche query)
- ACL Anthology
- arXiv
- Semantic/targeted manual search

## Search Log

| Date | Query | Source | Results | Notes |
|---|---|---|---:|---|
| 2026-03-08 | "How does the model count in French" | paper-finder | 0 | No direct hits |
| 2026-03-08 | numeracy / multilingual arithmetic queries | arXiv + manual | 8 core papers | Curated for direct relevance |

## Screening Results

| Paper | Title Screen | Abstract Screen | Full Text | Notes |
|---|---|---|---|---|
| Wallace et al. 2019 | Include | Include | Include (deep read chunks) | Foundational numeracy probing |
| Geva et al. 2020 | Include | Include | Include (deep read chunks) | Skill injection via synthetic data |
| Shi et al. 2022 | Include | Include | Include (deep read chunks) | MGSM benchmark with French |
| Labrak et al. 2024 | Include | Include | Include (deep read chunks) | French tokenization behavior |
| Chen et al. 2023 | Include | Include | Quick full text | Multilingual math training |
| Jin et al. 2021 | Include | Include | Quick full text | Numeral-aware GPT |
| Yu & Ananiadou 2024 | Include | Include | Quick full text | Arithmetic heads/neurons |
| Chang et al. 2024 | Include | Include | Quick full text | Algebraic structure hypothesis |

## Key Papers

### 1) Do NLP Models Know Numbers? Probing Numeracy in Embeddings (Wallace et al., 2019)
- **Source**: EMNLP 2019
- **Key Contribution**: Demonstrates that standard embeddings encode limited numerical magnitude; character-level methods often better.
- **Methodology**: Probing tasks (list max, decoding, addition) + analysis on DROP-style numerical QA.
- **Datasets Used**: DROP + synthetic probing datasets.
- **Baselines**: GloVe/word2vec/ELMo/BERT and char-based embeddings.
- **Results**: Strong in-range decoding, weak extrapolation to larger numbers.
- **Code Available**: Yes (paper-associated code links in publication ecosystem).
- **Relevance**: Suggests French counting performance may depend on tokenization granularity and representation choice.

### 2) Injecting Numerical Reasoning Skills into Language Models (Geva et al., 2020)
- **Source**: ACL 2020
- **Key Contribution**: Numerical reasoning can be injected with synthetic numeric pretraining; improves DROP substantially.
- **Methodology**: Multi-stage pretraining on synthetic numeric and textual data, then fine-tuning.
- **Datasets Used**: DROP, MAWPS, SQuAD.
- **Baselines**: Prior specialized numerical-reasoning architectures and vanilla LM baselines.
- **Results**: Large F1 gains on DROP; better transfer to math word problems.
- **Code Available**: Partial/associated resources.
- **Relevance**: Direct recipe for targeted French counting skill augmentation.

### 3) NumGPT (Jin et al., 2021)
- **Source**: AAAI 2022 / arXiv
- **Key Contribution**: Numeral-aware embedding + loss for generative pretraining.
- **Methodology**: Prototype-based mantissa representation and exponent embedding.
- **Datasets Used**: Multiple numeracy tasks (comparison, estimation, MWP-style tasks).
- **Baselines**: GPT and numeral-embedding variants.
- **Results**: Better numeracy across tasks than generic GPT baselines.
- **Code Available**: Paper resources available.
- **Relevance**: Candidate architecture for robust number-word and magnitude handling.

### 4) Language Models Are Multilingual Chain-of-Thought Reasoners (Shi et al., 2022)
- **Source**: arXiv
- **Key Contribution**: Introduces MGSM by translating GSM8K into 10 languages, including French.
- **Methodology**: CoT prompting across languages; compares in-language reasoning vs English intermediate steps.
- **Datasets Used**: MGSM.
- **Baselines**: Standard prompting vs CoT; GPT-3/PaLM scale analysis.
- **Results**: Multilingual reasoning emerges with scale; strong performance even in low-resource languages.
- **Code Available**: Yes (google-research/url-nlp).
- **Relevance**: Central benchmark for French counting/reasoning evaluation.

### 5) Breaking Language Barriers in Multilingual Mathematical Reasoning (Chen et al., 2023/2024)
- **Source**: arXiv
- **Key Contribution**: Builds multilingual math instruction datasets and trains MathOctopus models.
- **Methodology**: Parallel/cross training strategies with multilingual instruction data.
- **Datasets Used**: MGSM8KInstruct, MSVAMP.
- **Baselines**: Open-source LLMs and ChatGPT few-shot comparisons.
- **Results**: Strong multilingual gains; reports French improvements.
- **Code Available**: Yes (MathOctopus repo).
- **Relevance**: Practical baseline for multilingual/french math transfer.

### 6) How Important Is Tokenization in French Medical MLMs? (Labrak et al., 2024)
- **Source**: arXiv
- **Key Contribution**: Examines tokenization granularity and morpheme-aware segmentation in French domain LMs.
- **Methodology**: Compare BPE/SentencePiece and morphology-enriched segmentation across tasks.
- **Datasets Used**: French biomedical corpora/tasks.
- **Baselines**: Standard tokenizer setups.
- **Results**: Tokenization design meaningfully impacts downstream behavior.
- **Code Available**: Not primary focus.
- **Relevance**: Supports the hypothesis that French number-word segmentation likely affects counting behavior.

### 7) Interpreting Arithmetic Mechanism in LLMs (Yu & Ananiadou, 2024)
- **Source**: EMNLP 2024 / arXiv
- **Key Contribution**: Identifies arithmetic-specialized heads/neurons via Comparative Neuron Analysis.
- **Methodology**: Head/neuron attribution and intervention.
- **Datasets Used**: Arithmetic task setups.
- **Baselines**: Internal-ablation comparisons.
- **Results**: Arithmetic ability localized in limited components.
- **Code Available**: Yes.
- **Relevance**: Direct path to map where French counting operations are represented.

### 8) Unraveling Arithmetic in LLMs: Role of Algebraic Structures (Chang et al., 2024/2025)
- **Source**: ICLR workshop / arXiv
- **Key Contribution**: Proposes algebraic structure learning (commutativity/identity) as mechanism for arithmetic generalization.
- **Methodology**: Empirical + theoretical analysis with custom arithmetic data.
- **Datasets Used**: Custom arithmetic datasets + benchmark references.
- **Baselines**: Standard LLM arithmetic settings.
- **Results**: Structural priors can improve arithmetic behavior.
- **Code Available**: Not central.
- **Relevance**: Suggests structure-preserving probes for French counting variants (e.g., "quatre-vingt" composition).

## Common Methodologies
- Probing and diagnostic tasks for numeracy representations.
- Synthetic-data skill injection for arithmetic competence.
- Multilingual benchmark evaluation with CoT prompting.
- Mechanistic interpretability (head/neuron-level).

## Standard Baselines
- Prompting baselines: direct answer vs CoT.
- Model baselines: generic pretrained LMs vs numeracy-adapted models.
- Multilingual baselines: English-only fine-tune vs multilingual instruction tuning.

## Evaluation Metrics
- Accuracy / exact match for math word problems.
- F1 (for reading-comprehension numerical spans in DROP-like tasks).
- Per-language accuracy (critical for French-vs-other language comparison).

## Datasets in the Literature
- **MGSM**: multilingual test benchmark; includes French.
- **GSM8K**: core English grade-school math benchmark.
- **SVAMP/MSVAMP**: robustness and transfer for word-problem reasoning.
- **DROP/MAWPS**: classical numerical reasoning datasets.

## Gaps and Opportunities
- Few papers directly target French-specific number-word compositionality (e.g., 70/80/90 forms).
- Limited mechanistic work specifically on multilingual number-word tokenization effects.
- Need controlled French counting probes (digit-to-word, word-to-digit, compositional decomposition).

## Recommendations for Our Experiment
- **Recommended datasets**: MGSM (French), GSM8K, SVAMP; optionally synthetic French counting dataset.
- **Recommended baselines**: direct prompting, CoT prompting (French and English intermediate), multilingual instruction-tuned models.
- **Recommended metrics**: exact-match accuracy, per-language breakdown, error taxonomy by number pattern (e.g., 70/80/90).
- **Methodological considerations**:
  - Evaluate tokenization explicitly (subword splits of French number words).
  - Add controlled probes for compositional French numerals.
  - Use neuron/head attribution on arithmetic/counted tokens for interpretability.
