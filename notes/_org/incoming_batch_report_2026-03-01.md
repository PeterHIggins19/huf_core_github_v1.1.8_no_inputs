# Incoming batch report — 2026-03-01

These files were ingested into the HUF document pipeline.

## What was done
- Copied originals into `notes/current_documents/inbox/2026-03/` (unchanged).
- Created staged, HUF-coded copies in `notes/current_documents/staged/<DOC_ID>/`.
- Inserted the two-line HUF header into **Markdown/Python/JSX** and inserted a header block into **DOCX** staged copies.

## Routing map (recommended promotion targets)
| File | DOC_ID | Type | Recommended destination |
|---|---|---|---|
| `appendix_d1_inserts_v3.docx` | `HUF.DRAFT.CASE.NOTE.APPENDIX_D1_INSERTS_V3` | `docx` | cases/<case>/docs/exhibits/ (when promoting) |
| `Book1.xlsx` | `HUF.DRAFT.CASE.DATA.BOOK1` | `xlsx` | cases/<case>/data/ (if publishable) else notes/_private/ |
| `CLAUDE_INSTRUCTIONS.md` | `HUF.DRAFT.ORG.NOTE.CLAUDE_INSTRUCTIONS` | `markdown` | notes/current_documents/staged/ |
| `HUF_Advanced_Mathematics_Handbook_v0.2.0_DRAFT.docx` | `HUF.DRAFT.BOOK.MANUSCRIPT.HUF_ADVANCED_MATHEMATICS_HANDBOOK_V0_2_0_DRAFT` | `docx` | docs/books/advanced_mathematics/index.md (Markdown) + keep DOCX in notes/current_documents/ |
| `HUF_Advanced_Mathematics_Handbook_v0.2.0_DRAFT.md` | `HUF.DRAFT.BOOK.MANUSCRIPT.HUF_ADVANCED_MATHEMATICS_HANDBOOK_V0_2_0_DRAFT` | `markdown` | docs/books/advanced_mathematics/index.md (Markdown) + keep DOCX in notes/current_documents/ |
| `HUF_Appendix_D_Case_Study_D1_Exhibit_A_v2.docx` | `HUF.DRAFT.CASE.EXHIBIT.HUF_APPENDIX_D_CASE_STUDY_D1_EXHIBIT_A_V2` | `docx` | cases/<case>/docs/exhibits/ (when promoting) |
| `HUF_Complete_Reference_Feb2026.docx` | `HUF.DRAFT.BOOK.MANUSCRIPT.HUF_COMPLETE_REFERENCE_FEB2026` | `docx` | notes/current_documents/ (source) then convert to docs/huf_reference.md when ready |
| `HUF_Governance_Explainer_v1.0_Mar2026.docx` | `HUF.DRAFT.ORG.NOTE.HUF_GOVERNANCE_EXPLAINER_V1_0_MAR2026` | `docx` | notes/_org/ (if it is governance policy) or docs/documentation/ (if public) |
| `HUF_Governance_Package_v1.0_Mar2026.zip` | `HUF.DRAFT.ORG.PACKAGE.HUF_GOVERNANCE_PACKAGE_V1_0_MAR2026` | `zip` | notes/_private/ or notes/current_documents/inbox/ |
| `huf_governance_state_observer.docx` | `HUF.DRAFT.BOOK.MANUSCRIPT.HUF_GOVERNANCE_STATE_OBSERVER` | `docx` | docs/books/formal_core/ (after consolidation) or keep as source |
| `HUF_Handbook_v1.2.0.docx` | `HUF.LEGACY.BOOK.MANUSCRIPT.HUF_HANDBOOK_V1_2_0` | `docx` | notes/current_documents/ (source) then convert to docs/handbook.md when ready |
| `huf_mathematical_foundations.docx` | `HUF.DRAFT.BOOK.MANUSCRIPT.HUF_MATHEMATICAL_FOUNDATIONS` | `docx` | docs/books/formal_core/ (after consolidation) or keep as source |
| `HUF_Mathematics_v0.1.0_DRAFT.docx` | `HUF.DRAFT.BOOK.MANUSCRIPT.HUF_MATHEMATICS_V0_1_0_DRAFT` | `docx` | notes/current_documents/ (source) then select canonical for docs/books/ |
| `huf_math_foundations_v2_1.docx` | `HUF.DRAFT.BOOK.MANUSCRIPT.HUF_MATH_FOUNDATIONS_V2_1` | `docx` | docs/books/formal_core/ (after consolidation) or keep as source |
| `HUF_Operator_Decision_Log_v1_1.docx` | `HUF.LEGACY.ORG.TRACE.HUF_OPERATOR_DECISION_LOG_V1_1` | `docx` | notes/_org/ (optional) or keep as trace under notes/current_documents/ |
| `HUF_Operator_Decision_Log_v1_2.docx` | `HUF.RELEASE.ORG.TRACE.HUF_OPERATOR_DECISION_LOG_V1_2` | `docx` | notes/_org/ (optional) or keep as trace under notes/current_documents/ |
| `HUF_Project_Analysis_March2026.docx` | `HUF.DRAFT.ORG.NOTE.HUF_PROJECT_ANALYSIS_MARCH2026` | `docx` | notes/current_documents/ then decide if becomes docs/research/ |
| `HUF_Ramsar_Croatia_Package_Feb2026.docx` | `HUF.DRAFT.PARTNER.PACKAGE.HUF_RAMSAR_CROATIA_PACKAGE_FEB2026` | `docx` | cases/ramsar_case/docs/package/ |
| `HUF_Vol3_CaseStudyD2_ExhibitB_framework.docx` | `HUF.DRAFT.CASE.EXHIBIT.HUF_VOL3_CASESTUDYD2_EXHIBITB_FRAMEWORK` | `docx` | cases/<case>/docs/exhibits/ (when promoting) |
| `HUF_Vol3_CaseStudyD2_ExhibitB_v1.docx` | `HUF.DRAFT.CASE.EXHIBIT.HUF_VOL3_CASESTUDYD2_EXHIBITB_V1` | `docx` | cases/<case>/docs/exhibits/ (when promoting) |
| `ramsar_contact_letter_v15.docx` | `HUF.DRAFT.PARTNER.LETTER.RAMSAR_CONTACT_LETTER_V15` | `docx` | cases/ramsar_case/docs/letters/ |
| `ramsar_contact_primer_v12.docx` | `HUF.DRAFT.PARTNER.PRIMER.RAMSAR_CONTACT_PRIMER_V12` | `docx` | cases/ramsar_case/docs/primer/ (and wiki link later) |
| `ramsar_huf_demo_v2.py` | `HUF.DRAFT.PARTNER.NOTE.RAMSAR_HUF_DEMO_V2` | `python` | cases/ramsar_case/ |
| `wiki_fourth_monitoring_category_expanded.md` | `HUF.DRAFT.WIKI.NOTE.WIKI_FOURTH_MONITORING_CATEGORY_EXPANDED` | `markdown` | notes/wiki_pages/ (or docs/research/ if you want it public) |
| `wiki_huf_taxonomy_complete.md` | `HUF.DRAFT.WIKI.NOTE.WIKI_HUF_TAXONOMY_COMPLETE` | `markdown` | notes/wiki_pages/ (or docs/research/ if you want it public) |
| `wiki_manufacturing_electronics_assembly.md` | `HUF.DRAFT.WIKI.NOTE.WIKI_MANUFACTURING_ELECTRONICS_ASSEMBLY` | `markdown` | notes/wiki_pages/ (or docs/research/ if you want it public) |
| `wiki_operator_entry_points.md` | `HUF.DRAFT.WIKI.NOTE.WIKI_OPERATOR_ENTRY_POINTS` | `markdown` | notes/wiki_pages/ (or docs/research/ if you want it public) |
| `huf code/huf_diagnostic.jsx` | `HUF.DRAFT.SOFTWARE.CODE.HUF_DIAGNOSTIC` | `jsx` | notes/code_snippets/ or a future ui/ package |
| `huf code/huf_todo.jsx` | `HUF.DRAFT.SOFTWARE.CODE.HUF_TODO` | `jsx` | notes/code_snippets/ or a future ui/ package |