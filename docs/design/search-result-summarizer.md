# Search Result Summarizer Design

## 1. Overview
This document describes the design for the Search Result Summarizer, which aims to improve the readability of `astr_kb_search` results by transforming raw text chunks into concise, point-form summaries.

## 2. System Architecture
The summarizer acts as a post-processing layer for the memory retrieval system.

**Data Flow**:
`astr_kb_search` $\rightarrow$ `Raw Search Results` $\rightarrow$ `Search Result Summarizer` $\rightarrow$ `Summarized Results` $\rightarrow$ `End User/Lily`

## 3. Component Design

### 3.1 SearchSummarizer
The core component responsible for orchestrating the summarization process.
- **Input**: A list of raw text chunks retrieved from the knowledge base.
- **Process**: 
    1. Iterate through search results.
    2. For each result, construct a prompt using the `SummarizationPromptTemplate`.
    3. Call the LLM to generate the summary.
    4. Format the output into a unified, readable structure.
- **Output**: A list of summaries, each containing 3-5 key points.

### 3.2 SummarizationPromptTemplate
A specialized prompt designed to ensure consistency and quality.
- **Requirements**:
    - Force output into 3-5 points.
    - Emphasize core discussion themes and key conclusions.
    - Strictly prohibit fabrication (hallucination).
    - Define the output format (e.g., Markdown bullet points).

## 4. Interface Definition

### 4.1 internal API
The summarizer will provide a method similar to:
`summarize_results(results: List[SearchResult]) -> List[SummarizedResult]`

### 4.2 Integration with `astr_kb_search`
Depending on the implementation, the summarization can be:
- **Integrated**: Inside the `astr_kb_search` function before returning.
- **Wrapper**: As a separate service that wraps the search call.

## 5. Data Model

### 5.1 SearchResult (Input)
- `content`: The raw text chunk.
- `score`: Relevance score.
- `metadata`: Source information.

### 5.2 SummarizedResult (Output)
- `summary`: A string containing the 3-5 bullet points.
- `original_content`: Reference to the original text (for verification).
- `score`: The original relevance score.

## 6. Algorithm Description

1. **Filtering**: Only summarize results that meet a certain relevance threshold to avoid wasting tokens on noise.
2. **Batching**: If multiple chunks are highly similar, they may be grouped and summarized together to reduce redundancy.
3. **Prompt Execution**: 
    - System Prompt: "You are a memory assistant. Your task is to summarize search results into concise points."
    - User Prompt: "Summarize the following text into 3-5 key points. Focus on themes and conclusions. \n\nText: [RAW_CONTENT]"
4. **Post-processing**: Clean up LLM artifacts (e.g., "Here is the summary:") to ensure a clean bulleted list.

## 7. Technical Selection

- **LLM**: Existing cloud LLM integrated into astrbot.
- **Performance**: To minimize latency, summaries will be generated in parallel if the LLM provider supports batching or concurrent requests.
- **Compatibility**: The system will maintain a toggle to return raw text if the summary fails or is explicitly requested.

## 8. Acceptance Criteria Alignment
- [ ] Results are displayed as points rather than raw chunks.
- [ ] Each summary contains 3-5 key points.
- [ ] Core themes and conclusions are captured.
- [ ] Response time increase is kept to a minimum.
- [ ] No degradation in search accuracy.
