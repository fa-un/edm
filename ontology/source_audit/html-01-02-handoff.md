# G003 exact source-statement handoff — HTML sources 1–2

Fresh full read through EOF of `lecture1_student_guide.html` and `seminar1_analyst_case.html`. Inclusion boundary: one relation unit per explicit paragraph, labeled table row, or diagram arrow asserting a reusable ontology-relevant relation; split only clearly independent predicates. Exclude generic UI/task steps, standalone definitions, and specific synthetic instance values unless they teach a reusable relation. Rows repeated in separate source statements are counted again. For a heading without HTML `id`, the locator below uses its exact text and does not invent an anchor.

**Status key:** D = direct source assertion; C = contextual/case-specific; I = inferred; H = explicitly hypothetical. Relation source status is **course-only** for these source statements (no independent primary/product citation attached to the statement). Modalities use plan, record, event; audience is student. No included relation is inferred or explicitly hypothetical.

## `lecture1_student_guide.html` — 23 relation rows

| # | Exact heading + paragraph/row locator | Faithful claim paraphrase | D/C/I/H | Relation type | Source status | Modality / audience |
|---:|---|---|---|---|---|---|
| 1 | “Зачем нужна аналитика изменений”; paragraph beginning “Предприятие меняет процессы…” | Enterprise changes processes, data, and information systems to address business goals. | D | enterprise–change–goal | course-only | plan / student |
| 2 | Same paragraph, clause “Аналитик помогает…” | Analyst investigates the initial problem and checks whether a proposed change yields the intended result. | D | analyst–problem/change–outcome | course-only | plan / student |
| 3 | `#architecture-view` “Деятельность, данные, приложения и технологии”; paragraph “Архитектура предприятия…” | Enterprise architecture describes connections among activity, data, applications, and technology. | D | architecture–viewpoint | course-only | plan / student |
| 4 | Same heading; table row **Данные (Data)** | Example links a request with its initiator, budget, and status. | D | data–association | course-only | plan / student |
| 5 | Same heading; table row **Приложения (Applications)** | Example transfers an approved request to the purchasing system. | D | application–data handoff | course-only | plan / student |
| 6 | “Как событие предприятия становится данными для решения”; paragraph “Когда поставщик привозит материал…” | A material-delivery event is recorded in the information system as transaction data. | D | event–record | course-only | event / record / student |
| 7 | Same paragraph, clause “Такая запись относится…” | The transaction record may describe date, supplier, material, and quantity. | D | record–attributes | course-only | record / student |
| 8 | Same heading; paragraph “OLTP-система…” | An OLTP system helps register everyday operations. | D | system–operation | course-only | event / record / student |
| 9 | Same paragraph, “Она сохраняет записи…” | The OLTP system saves operation records. | D | system–record | course-only | record / student |
| 10 | Same paragraph, “Если события не зафиксированы…” | Missing or erroneous records make subsequent analysis incomplete or incorrect. | D | record quality–analysis | course-only | record / student |
| 11 | Same paragraph, “Когда записи накапливаются…” | Accumulated records can be compared to examine delivery frequency and delays. | D | record–analysis | course-only | record / student |
| 12 | Same heading; paragraph beginning “Профилирование данных…” | BI tools help investigate data and produce reports; DSS uses information in choosing actions. | D | tool–analysis/decision | course-only | plan / student |
| 13 | Same paragraph, “Аналитический отчёт не заменяет…” | An analytical report does not replace event recording; inaccurate source records undermine conclusions. | D | record–report/conclusion | course-only | record / student |
| 14 | Same heading; paragraph beginning “Для этого нужны согласованные данные…” | Inconsistent representations of a supplier or material impede comparison and may make reports incomplete. | D | entity representation–comparison/report | course-only | record / student |
| 15 | Same paragraph, “Общие сведения о ключевых объектах…” | Shared key-object data and common allowed-value sets help link data across processes. | D | master/reference data–process data | course-only | record / student |
| 16 | `#analyst-work` → “От исследования к проверке результата”; table row **Подготовка** | Preparation produces common understanding of the task and how to measure it. | D | phase–output | course-only | plan / student |
| 17 | Same table; row **Исследование** | Research produces an agreed AS-IS model and problem list. | D | phase–output | course-only | plan / student |
| 18 | Same table; row **Проектирование** | Design produces a TO-BE model and testable requirements. | D | phase–output | course-only | plan / student |
| 19 | Same table; row **Реализация** | Implementation support and checking produce a configured solution aligned to requirements. | D | phase–output | course-only | plan / student |
| 20 | Same table; row **Эксплуатация** | Feedback and effect analysis produce confirmation of impact or grounds for another change. | D | phase–output | course-only | record / student |
| 21 | “Найти ограничение, а не улучшать любой участок”; paragraph “Узкое место…” | A bottleneck is an operation or resource that limits the process’s overall result. | D | resource/step–process outcome | course-only | plan / student |
| 22 | Same heading; paragraph “Поэтому узкое место сначала считают гипотезой…” | A suspected bottleneck is checked against loading, queues, step duration, and final output. | D | evidence–hypothesis test | course-only | plan / student |
| 23 | Same paragraph, “После изменения сравнивают…” | After a change, actual results are compared with the baseline and agreed goal. | D | result–measure | course-only | record / student |

**Explicit zeros:** C = 0, I = 0, H = 0. Independent-primary, product, missing, and access-gated relation statuses = 0.

## `seminar1_analyst_case.html` — 0 relation rows

No source statement met the inclusion boundary as a reusable ontology-relevant relation. The case values and scenario are specific to the synthetic case; the “Понятия семинара” table consists of standalone definitions; task instructions and checks prescribe student work rather than assert reusable domain relations.

**Explicit zeros:** relation rows = 0; D = 0, C = 0, I = 0, H = 0; independent-primary, product, course-only relation rows, missing, and access-gated statuses = 0.

## Named model/method/standard/metric/practice candidates

Four-way status: **1** verified against primary source; **2** secondary source only; **3** primary source unavailable; **4** mention does not define a verifiable method. Here categories 3 and 4 are deliberately distinct: a named practice with no supplied primary citation is category 3; model labels that define a state but not a modeling method are category 4.

| File | Exact heading + locator | Candidate | Four-way status | One-sentence rationale and source/version/access status |
|---|---|---|---|---|
| `lecture1_student_guide.html` | “Как событие предприятия становится данными для решения”; paragraph beginning **«Профилирование данных — проверка…»** | Профилирование данных | **3 — primary source unavailable** | The page describes a data-checking practice but supplies no citation, source/version, or accessible primary reference. |
| `lecture1_student_guide.html` | `#analyst-work` → “Понятия работы аналитика”; table row **AS-IS** | AS-IS model | **4 — mention does not define a verifiable method** | It describes the current-state model but gives no method for constructing or verifying it and cites no source/version. |
| `lecture1_student_guide.html` | `#analyst-work` → “Понятия работы аналитика”; table row **TO-BE** | TO-BE model | **4 — mention does not define a verifiable method** | It describes the target-state model but gives no method for constructing or verifying it and cites no source/version. |
| `seminar1_analyst_case.html` | “Понятия семинара”; table row **AS-IS — «как есть»** | AS-IS model | **4 — mention does not define a verifiable method** | Repeats the model concept and describes its scope, not a verifiable modeling method; no source/version is cited. |
| `seminar1_analyst_case.html` | “Понятия семинара”; table row **TO-BE — «как должно быть»** | TO-BE model | **4 — mention does not define a verifiable method** | Repeats the model concept and describes its scope, not a verifiable modeling method; no source/version is cited. |

**Candidate reconciliation:** lecture guide = 3 rows; seminar case = 2 rows; total = **5 candidate rows**. AS-IS and TO-BE are counted again where they recur in the second file.

### Motivated exclusions

- “Методологии внедрения,” “подходы SAP,” and “материалы 1С” in the homework section are generic source pointers; no distinct methodology name or version is supplied.
- OLTP, BI, DSS, ERP, CRM, and MES are system/tool categories in these passages, not methods taught as methods.
- Enterprise architecture, Gap/разрыв, business rule, bottleneck, and project/system lifecycle are concepts or generic process descriptions, not distinct named methods.
- “Показатель эффекта” is a generic metric category; no particular named metric is specified. Generic analyst actions (research, observation, comparison, review) are not named practices.

## Reconciliation

| File | Relation rows | Candidate rows |
|---|---:|---:|
| `lecture1_student_guide.html` | 23 | 3 |
| `seminar1_analyst_case.html` | 0 | 2 |
| **Total** | **23** | **5** |

Counts match the numbered relation and candidate tables above. These are only the two assigned sources; no course HTML was edited.
