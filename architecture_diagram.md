```mermaid
flowchart TD
A[User Uploads JD & Resume] --> B[Streamlit UI]
B --> C[JD Parser]
B --> D[PDF Parser]
C --> E[Skill Extractor]
D --> F[Resume Text]
E --> G[Scoring Engine]
F --> G
G --> H[Gemini API]
H --> I[Final Output Screen]
```