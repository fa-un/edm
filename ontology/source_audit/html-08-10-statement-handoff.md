# Exact source-statement handoff: canonical HTML files 8–10

Audit scope: read the three declared student-facing HTML sources through EOF. This handoff inventories reusable relation candidates and named candidate status; it does not verify actual student execution or the external truth of course assertions. Course sources remain unchanged.

## Counting rule and supersession

One relation-candidate unit is one explicit source statement at a precise locator: one paragraph, one labeled table row, or one diagram arrow. Split only clearly independent predicates within that source statement. A row must state a reusable relation between domain entities or states; standalone definitions, generic UI/navigation, grading rules, example-only IDs/values, and ungrounded interpretations are excluded. A candidate's D/C/I/H code describes what the course source asserts, not its independent truth. Citation status distinguishes course-only evidence from cited vendor/manual evidence. Planned documents, statuses, reports, and records are not treated as proof of a physical event.

**Reconciled counts for this statement-level pass:** file 8 = 8 relation candidates; file 9 = 9; file 10 = 7. This replaces the earlier provisional bundled totals **19/47/20**. Those earlier totals used a broader grouping and admitted non-eligible procedure/example content; do not treat the new counts as arithmetic reductions of the old ones. Named-candidate totals/statuses are separately listed below.

## 8. `Практикумы №7–8 — разбор.html` — 5 named candidates; 8 relations

### Named candidates and four-way source-verification status

Four-way status: 1 = verified against independent authoritative primary/owner source; 2 = secondary source only; 3 = exact method verifiable but primary unavailable/gated; 4 = mention does not define a distinct verifiable method. The course assignment verifies only that it teaches/describes the exercise, not general validity.

| Candidate | Status | Rationale / boundary |
|---|---|---|
| Direct-material specification | 4 | A resource-specification setup pattern in the exercise, not an independently verified general method. |
| Automatic material/characteristic selection | 4 | Product behavior/workflow illustrated by the 1C teaching example, not a general method. |
| Separately produced semi-finished goods | 4 | Product/process option illustrated in the exercise; no independent method authority asserted. |
| In-process semi-finished production | 4 | Product/process option illustrated in the exercise; no independent method authority asserted. |
| Conditional/formula material consumption | 4 | A configured specification rule in the exercise, not an independent general method. |

### Relation candidates

| ID | Exact locator | Concise claim | Evidence / class / source boundary / modality |
|---|---|---|---|
| 8-R01 | `Практикум № 7. Спецификации полки` → `Понятия ресурсной спецификации`, table row `Ресурсная спецификация` | A resource specification describes a typical output, process stages, and required resources. | D; specification-to-output/process/resource; course definition with 1C manual context cited; normative model, student-facing. |
| 8-R02 | `Практикум № 7` → `1. Прямые материалы`, table `Материалы и работы` (resource rows) | A specification includes material-resource lines for the output. | D; specification-to-material requirement; instructional example / product-manual context, not a production event. |
| 8-R03 | `Практикум № 7` → `2. Автовыбор материалов`, table row `Автовыбор характеристики` | Matching product-property values determine a material characteristic selection. | D; selection/dependency; course definition and product example; product behavior claim, not independently validated. |
| 8-R04 | `Практикум № 7` → `3. Полуфабрикаты производятся отдельно`, table row `Способ получения материала` | A semi-finished input may be supplied from stock rather than produced in the parent order. | D; alternative supply/state; course definition and product example; planned process, not an observed issue. |
| 8-R05 | `Практикум № 8` → `1. Спецификация основания полки`, paragraph/list row `Результат: Основание полки` | A resource specification identifies the intermediate output it produces. | D; specification-to-output; instructional/product-model evidence; planned normative relation. |
| 8-R06 | `Практикум № 8` → `2. Спецификация полки с производством полуфабрикатов в процессе`, list row beginning `В строках «Основание полки»...` | The parent-order specification can call for semi-finished goods to be produced by their own specifications. | D; specification/process dependency; course exercise and product-model claim; plan, not completed production. |
| 8-R07 | `#semi-finished-paths`, table row `Производить в процессе` | In-process semi-finished goods are produced for the same order and passed to a later stage, unlike independent stock supply. | D; process/state distinction; course synthesis; reusable course model, no actual event asserted. |
| 8-R08 | `Практикум № 7` → `2. Автовыбор материалов`, list row `В строке «Лак Текнос»` | Material consumption is conditional on the product's protective-coating property being set. | C; conditional dependency; course/product example; configuration rule, not an observed consumption event. |

### Motivated exclusions / limits

- Standalone glossary definitions are not counted as relation candidates unless the source explicitly connects entities (the specification definition is retained at 8-R01 because it explicitly connects output, stages, and resources).
- Concrete synthetic values (e.g. product names, characteristics, quantities, labor hours, buffers, order counts) are excluded as candidate relations. They remain examples, not generic thresholds or production facts.
- Copying specifications/orders, setting status `Действует`, passing an order to production, and checking completeness are procedural steps, not extra domain edges. The relevant specification/output or planned-document relations are retained above.
- Missing inputs and conflicting values called out in the page (including unspecified first-order details and conflicting semi-finished quantities) are not resolved by inference. No sample order/status is evidence of physical production.

## 9. `seminar1_toir_notes.html` — 7 named candidates; 9 relations

### Named candidates and four-way source-verification status

| Candidate | Status | Rationale / boundary |
|---|---|---|
| Four-part maintenance-process model | 4 | Course/process framing; not an independently established standard or method. |
| TR/KR repair-cycle sequence | 4 | Course exercise pattern; no independent authority establishes this cycle universally. |
| Interval/usage-based maintenance planning | 1, concept level only | NASA primary maintenance material supports time/cycle-based task concepts; it does not verify the course's example intervals or local policy. [NASA maintenance reference](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_8831_002E_&page_name=all) |
| Long-term → annual → quarter/month program refinement | 4 | Instructional planning hierarchy, not a separately verified general method. |
| Repair resource-specification practice | 4 | Course/product workflow, not an independently verified maintenance method. |
| Resource-center scheduling model | 4 | 1C/product/course model; no distinct general scheduling method is specified. |
| Grouped/individual repair-order planning | 4 | Product workflow option described in course material, not a general method standard. |

### Relation candidates

| ID | Exact locator | Concise claim | Evidence / class / source boundary / modality |
|---|---|---|---|
| 9-R01 | `#processes-service`, process diagram, row `1. Производственные активы` | The maintenance process identifies equipment assets, their role, and maintenance strategy as planning inputs. | D; asset-to-strategy/process; seminar-slide-derived course model; student-facing plan, not a completed maintenance event. |
| 9-R02 | `#section-1-2`, `Подробная схема`, arrow `«Класс»` | An equipment object references a class that carries shared equipment rules. | D; reference/classification; course diagram plus 1C manual citation; model relation. |
| 9-R03 | `#section-1-2`, `Подробная схема`, arrow `класса` / cycle table node | A class's repair-cycle table contains ordered repair-type rows and their intervals. | D; containment/order/time; course diagram and manual context; normative plan, not actual work. |
| 9-R04 | `#section-1-2`, `Подробная схема`, arrow `Строка ремонтного цикла → реквизит-ссылка «Вид ремонта»` | A repair-cycle row references a repair-type record. | D; reference; course diagram; example intervals and identifiers remain instance values. |
| 9-R05 | `#section-2-3`, opening paragraph beginning `Вид ремонта и ресурсная спецификация` | Repair type and resource specification are distinct records linked through the repair-work nomenclature. | D; identity/reference/specification; course explanation and 1C manual context; planned normative relation. |
| 9-R06 | `#section-2-2`, diagram `#scheme-structure`, hierarchy arrows | Dispatcher subdivision, repair shop, work-center type, and work center form an organizational/resource hierarchy. | D; part-of/organization hierarchy; course diagram and manual context; configuration model, not universal naming. |
| 9-R07 | `#section-2-3`, detailed specification diagram, stage/operation relation rows | A specification stage is assigned to an organizational/work-center grouping, while a concrete operation is assigned to a work center. | D; assignment/resource constraint; course diagram and manual context; plan/specification, not event. |
| 9-R08 | `#section-3-2`, diagram `#scheme-planning`, paragraph/arrow beginning `Выбранный заказ на ремонт → заказ на производство` | A repair plan yields repair-order documents; the order records planned work, distinct from execution fact. | D; plan/document versus event; course/presentation/manual context; planned state only. |
| 9-R09 | `#section-3-3`, row `Заказ на производство: Основание: заказ на ремонт` | A production order is derived from a selected repair order. | D; document derivation/reference; course/presentation/manual context; planned document, not proof of completed repair. |

### Motivated exclusions / limits

- Do not generalize the example's 1-year/3-day/15-day intervals, monthly generation, 999-day horizon, `xx.yy` identifiers, or demo organization names as standards or enterprise facts.
- UI steps such as opening planning, filtering by class, selecting a status, or generating an order are excluded as procedures; the reusable document/reference edges are listed above.
- The source explicitly permits grouping several repair orders; three target orders are not guaranteed by merely including TR and KR rows. The report is a check/output, not a cause or execution event.
- NASA supports only the broad time/cycle-based maintenance concept. It does not verify the TR/KR sequence or the course's local interval values.

## 10. `seminar2_toir_execution.html` — 4 named candidates; 7 relations

### Named candidates and four-way source-verification status

| Candidate | Status | Rationale / boundary |
|---|---|---|
| Planned repair-cost calculation | 4 | Seminar exercise; not a distinct externally verified cost method. |
| Repair-order to production-order/phase exercise | 4 | Product/document workflow demonstrated by course material, not a general method standard. |
| Shift/brigade operation assignment | 4 | Course exercise workflow; no independent method is named. |
| Employee-output reporting | 4 | Product/reporting exercise, not a verified measure of physical repair. |

### Relation candidates

| ID | Exact locator | Concise claim | Evidence / class / source boundary / modality |
|---|---|---|---|
| 10-R01 | `#terms`, table row `Плановая калькуляция` | Planned cost calculation uses resource inputs and planned prices. | D; calculation/input; course explanation with 1C manual reference; estimate/plan, not actual expense. |
| 10-R02 | `#terms`, table row `Заказ на производство` | Production order is created on the basis of a repair order and organizes the work. | D; document derivation/process; course explanation and seminar deck; planned document. |
| 10-R03 | `#terms`, table row `Этап производства` | Production phase is part of/organized under the production order. | D; containment; course explanation; planned document. |
| 10-R04 | `#terms`, table row `Сменное задание` | Shift task contains an operation linked to a phase and assigned to a brigade. | D; containment/assignment; course explanation and seminar deck; planned assignment. |
| 10-R05 | `#terms`, table row `Выработка сотрудников` | Employee-output report presents registered work output by shop and brigade. | D; report-to-record/dimension; course explanation and seminar deck; report is not evidence by itself of physical work. |
| 10-R06 | `#production`, paragraph beginning `Заказ на производство создаётся из заказа на ремонт` | Production order derives from the repair order; its phases derive from the selected resource specification. | D; document derivation/specification dependency; course explanation and seminar deck; planned workflow. |
| 10-R07 | `#dispatch`, paragraph beginning `При распределении работ выбирают операцию` | Operation linked to a production phase is assigned to a brigade through a shift task; operation completion and task closure are separate statuses. | D; assignment/state distinction; course explanation and seminar deck; workflow record, not independent proof of physical repair. |

### Motivated exclusions / limits

- Exclude assessment scores and discrepancies between 2023 and 2024 grading drafts; they are rubric facts, not domain relations or method validation.
- Exclude concrete `xx.yy` identifiers, example cost amounts, product names, the exact `Ремонтный комплект №1`, and sample dates/values.
- UI menu navigation and button actions are not additional relations. Statuses are retained only as document/operation state distinctions, not as proof of execution.
- Keep report↔record and state↔event boundaries: report output is based on registered information; the source warns that statuses/`Произведено` do not prove a physical repair.

## Overall source and audience boundary

All three files are student-facing course material. Seminar 1 is a note based on presentation/manual sources; seminar 2 cites a presentation and the seminar 1 note, while the manual is described as available in the personal account. The student exercise pages describe resource specifications and planned orders. They do not establish execution in a live enterprise, actual 1C configuration outside the described teaching example, or a universal maintenance/production standard. Source citations in the course material are not independent verification unless identified above.
