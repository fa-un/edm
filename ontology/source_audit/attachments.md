# G003 attachment audit: PDF and seminar decks

Audit record date: 2026-11-23. This is an evidence-candidate register for the three local attachments listed in `ontology/source_corpus_manifest.json`, not a verification of product performance, classroom configuration, student actions, or enterprise practice.

## Coverage and extraction boundary

| Attachment | Coverage and format-specific checks | Audience / evidence boundary |
|---|---|---|
| `assets/downloads/erp_concept_v8.pdf` | 100/100 pages text-extracted and reviewed for named methods/models/standards/metrics/practices and explicit relation claims. Low-text pages 16, 21, 66, 68, 76, 82, 85, 86, 95, 98 were rendered and visually inspected; they are title/divider or illustrative pages and add no methodology/relationship omitted from extraction. | 1C vendor product-concept brochure, © 2020 (p.100). Capability and implementation statistics are vendor claims, not evidence of this course's configuration or outcomes. |
| `assets/downloads/Семинар 1_Драфт 14-10-23.pptx` | 41/41 slides XML text/order and 30 notes parts extracted; rendered to PDF; image-bearing slides 2, 4, 9–17, 19–32, 34–41 visually reviewed in the 41-slide contact sheet; OCR output from the rendered contact sheet was consulted. | Teaching/instructional draft for seminar 1, focused on repair planning. Screenshots are demo-base instructions, not proof that the operations were performed. Login and password are masked in slide text (`****`); this report does not reproduce any credentials, user IDs, or individual instance values. |
| `assets/downloads/Семинар 2_Драфт 21-10-23.pptx` | 35/35 slides XML text/order and notes parts extracted; rendered to PDF; image-bearing slides 2, 4–6, 11–15, 17–25, 27–35 visually reviewed in the 35-slide contact sheet; OCR output from the rendered contact sheet was consulted. | Teaching/instructional draft for seminar 2. It shows planned-cost, order/phase, shift and output-report workflows. A displayed status/posted demo document is not independently verified physical work. Identifiers and demo values are not copied here. |

The decks were reviewed slide-by-slide, including screenshots; text extraction alone was not treated as sufficient. OCR supplements visual review and does not itself validate source meaning. No unseen sources, private materials, or credential-bearing documents were sought. Date strings in filenames are source identifiers and are not treated here as evidence of actual seminar delivery.

## Counting rules

- Named candidate: one distinct explicitly named model, method, standard, metric or practice asserted as such. Generic actions and vendor features/modes are excluded unless the source explicitly frames them as a method/model/practice.
- Relation inventory row: one source statement at one paragraph, labelled table row, or diagram arrow at a precise page/slide locator. A row may bundle multiple targets/predicates; these current rows are not a final atomic-edge schema. Future ontology migration may split them. Do not infer relations from isolated example values or IDs.
- `D` = directly stated by the attachment; `C` = conditional; `I` = inference; `H` = hypothesis. `D` records what the source states, not independent truth. `type` below is an ontology-relevant relation category (e.g. classification, assignment, planned-vs-actual), not a new claim about source authority.
- Source status is distinguished as vendor assertion, instructional model, manual/product citation, or unverified/cited-with-access-limit. Values and workflow steps remain classified as plan, configuration, record, report, or event separately.
- The numbered relation inventory preserves all 216 reviewed candidate statements for traceability and is classified into reusable-relation eligible, separate product-observation, and excluded groups below. These are row counts, not fully atomized S–P–O edge counts.

## Named method/model/standard/metric/practice candidates

### `erp_concept_v8.pdf` (2020 vendor brochure)

| ID | Exact locator | Candidate | Status / source / modality / boundary |
|---|---|---|---|
| PDF-M01 | p.17, `1С:Предприятие – рядом с вами`, bullet on implementation and support quality | ISO 9001 standard | D; vendor claim; edition not specified; not a claim that the course or a named customer is certified. Current ISO source is ISO 9001:2026, which supersedes withdrawn 2015; the brochure predates this edition. The public ISO summary supports QMS context at a high level, not clause-level interpretation/certification. |
| PDF-M02 | p.20, `Экономический эффект`, indicator list | Manufacturing cost of output (reported change −9%) | D; vendor-reported metric label/value from 185 implementations; period, denominator, definitions, sample selection and causal design are not supplied. |
| PDF-M03 | same locator | Material-stock volume (−21%) | D; vendor-reported; same limitations. |
| PDF-M04 | same locator | Production volume (+32%) | D; vendor-reported; same limitations. |
| PDF-M05 | same locator | Manufacturing labor productivity (+27%) | D; vendor-reported; same limitations. |
| PDF-M06 | same locator | Equipment downtime duration (−22%) | D; vendor-reported; same limitations. |
| PDF-M07 | same locator | Production defect rate/volume (−21%) | D; vendor-reported; same limitations; precise numerator/denominator not stated. |
| PDF-M08 | same locator | Warehouse-stock turnover (+23%) | D; vendor-reported; same limitations. |
| PDF-M09 | same locator | Order-fulfillment time (−23%) | D; vendor-reported; same limitations; exact start/end events not defined. |
| PDF-M10 | same locator | Operating and administrative expense (−16%) | D; vendor-reported; same limitations. |
| PDF-M11 | same locator | Profit (+13%) | D; vendor-reported; accounting basis and period not specified. |
| PDF-M12 | p.23, `Мониторинг и анализ показателей деятельности предприятия`, hierarchy of goals/target indicators | Hierarchical goal/target-indicator model | D; vendor functionality/model claim; no general management method or course use established. |
| PDF-M13 | p.23, same section, `День – Неделя – Месяц` | Day/week/month monitoring cadence | D; named product practice/principle; no evidence it is universal or configured in a classroom base. |
| PDF-M14 | p.27, `Управление производством`, `Барабан – Буфер – Веревка` | Drum–Buffer–Rope (DBR) | D; named method in vendor capability list; source does not explain the method or establish implementation. |
| PDF-M15 | p.41 title/diagram; also p.14 corporate overview | International Financial Reporting Standards / МСФО reporting framework | D; product/reporting context only; brochure does not establish accounting policy, compliance, or a particular consolidation procedure. |
| PDF-M16 | p.64, `Управление складом и запасами`, ABC/XYZ analysis | ABC inventory classification | D; product capability to store analysis results; no formula or thresholds in brochure. ASCM Supply Chain Dictionary 20th ed. (2026), p.7 supports ABC classification by annual dollar volume or other criteria; its sample percentages are typical, not mandatory. The current portal identifies the edition, but detailed dictionary content is member-gated. |
| PDF-M17 | same locator | XYZ inventory classification | D; product capability to store analysis results; no method definition/formula/cutoffs in brochure. The 2026 ASCM Dictionary details are member-gated and do not substantiate a universal XYZ formula here; 1C ERP 2.6 ITS TOC lists an ABC/XYZ chapter, but its detailed body is access-gated. Do not infer a formula or classroom configuration. |
| PDF-M18 | p.80, `Примеры ориентировочного расчета бюджета проекта внедрения 1С:ERP` | Simplified project-budget estimate: workstation count × labor per workstation × hourly rate | D; explicitly called a very simplified estimate; examples are illustrative and the same page warns not to use them as project-specific quotes. Vendor heuristic, not independently validated estimator. |

**Explicitly not counted as methods:** p.27 interval planning, bottleneck planning, MES/APS operational planning, three-level production planning; p.29 scenario modelling and multi-criteria schedule optimization; p.44 budgeting scenarios; p.64 inventory analysis and demand forecast are product features/capabilities here, not explained/taught as independent general methods. They remain candidate product/relation claims below where they state relations.

### `Семинар 1_Драфт 14-10-23.pptx`

| ID | Exact slide/locator | Candidate | Status / source / modality / boundary |
|---|---|---|---|
| S1-M01 | slide 4, `1. Система оценивания`, 0–3-point completion rubric | Seminar completion score | D; explicit assessment metric for the exercise; not an outcome or method-quality measure. |
| S1-M02 | slide 5, additional task | Runtime-based TR–KR–TR repair-cycle plan | D; named teaching practice; conditional student exercise, not a universal maintenance standard. The `365×24=8760` runtime-hours assumption is a teaching assumption. |
| S1-M03 | slide 6, `3. Схема процессы планирования ТОиР`, strategy question | Preventive maintenance by runtime | D; named instructional strategy option; no independent standard cited. |
| S1-M04 | same locator | Preventive maintenance by calendar periodicity | D; named instructional strategy option; no independent standard cited. |
| S1-M05 | same locator | Condition-based maintenance | D; named instructional strategy option; no independent standard cited. |
| S1-M06 | same locator | Run-to-failure strategy | D; named instructional strategy option; no independent standard cited. |
| S1-M07 | slide 6, program sequence `долгосрочная → предварительная годовая → годовая → квартал (месяц)` | Maintenance-program refinement practice | D; course process model; program is a plan, not work execution. |
| S1-M08 | slide 7, `4. План упражнений`; slides 33–40 | Repair-planning exercise sequence (objects/classes/nomenclature/specifications → maintenance plan/orders → production order/report) | D; student practice, spread across instructions. Steps are planned/demonstrated in 1C, not evidence they were completed by a named student. |
| S1-M09 | slide 26, `Определение операций в ресурсной спецификации`, explicit `ВАЖНО!` | Copy-based resource-specification setup | D; course-specific practice/instruction (copy a base specification, do not create from scratch); product/browser caveat, not general manufacturing method. |

### `Семинар 2_Драфт 21-10-23.pptx`

| ID | Exact slide/locator | Candidate | Status / source / modality / boundary |
|---|---|---|---|
| S2-M01 | slide 4, `1. Система оценивания`, completion/partial-report rubric | Seminar completion score | D; explicit exercise assessment metric; not an observed learning outcome. |
| S2-M02 | slides 9–15, `Создание плановой калькуляции для ТР и КР` | Planned repair-cost calculation exercise | D; student practice in the demo product; planned estimate, not actual cost/event. |
| S2-M03 | slides 16–25, `Создание производственных заказов и этапов из заказа ТОиР` | Repair-to-production-order/phase exercise | D; product workflow practice; planned documents/statuses are not proof of repair. |
| S2-M04 | slides 26–34, `Распределение и подтверждение операций` | Shift/brigade assignment and employee-output reporting exercise | D; product workflow practice; report is a record/report, not by itself proof of physical work. |

## Numbered relation source-statement inventory

For each row: status is the attachment's own assertion; source status is `vendor brochure` (PDF), `instructional course draft`, or `diagram/screenshot in course draft`. External/primary sources are noted only where verified. A cited product description is not proof of classroom configuration. D is direct as a source statement; it is not validation of real-world performance.

### PDF: `erp_concept_v8.pdf`

| ID | Exact page/locator | Candidate source statement (paraphrased; may bundle predicates) | Status / type / source status / modality boundary |
|---|---|---|---|
| PDF-R01 | p.17, `1С:Предприятие – рядом с вами`, ISO bullet | 1C implementation/support quality — is described as conducted under — ISO 9001 | D; quality-standard attribution; vendor marketing claim; edition/access not specified. |
| PDF-R02 | p.20, `Экономический эффект`, introductory sentence | The brochure's outcomes — are reported from — 185 ERP implementation projects | D; evidence provenance; vendor summary, underlying project studies not provided. |
| PDF-R03 | p.20, indicator `Снижение себестоимости...` | ERP implementations — are associated in the brochure with — 9% lower output cost | D; metric association, not causal estimate; vendor-reported, denominator/period absent. |
| PDF-R04 | same page, indicator `Снижение объемов материальных запасов` | ERP implementations — are associated with — 21% lower material-stock volume | D; metric association, not causal estimate; vendor-reported. |
| PDF-R05 | same page, indicator `Увеличение объема выпускаемой продукции` | ERP implementations — are associated with — 32% higher production volume | D; metric association, not causal estimate; vendor-reported. |
| PDF-R06 | same page, indicator `Рост производительности труда в производстве` | ERP implementations — are associated with — 27% higher manufacturing productivity | D; metric association, not causal estimate; vendor-reported. |
| PDF-R07 | same page, indicator `Сокращение длительности простоев оборудования` | ERP implementations — are associated with — 22% less equipment downtime | D; metric association, not causal estimate; vendor-reported. |
| PDF-R08 | same page, indicator `Снижение производственного брака` | ERP implementations — are associated with — 21% lower production defects | D; metric association, not causal estimate; vendor-reported; exact denominator absent. |
| PDF-R09 | same page, indicator `Рост оборачиваемости складских запасов` | ERP implementations — are associated with — 23% higher warehouse-stock turnover | D; metric association, not causal estimate; vendor-reported. |
| PDF-R10 | same page, indicator `Сокращение сроков исполнения заказов` | ERP implementations — are associated with — 23% shorter order-fulfillment time | D; metric association, not causal estimate; event boundaries absent. |
| PDF-R11 | same page, indicator `Сокращение операционных и административных расходов` | ERP implementations — are associated with — 16% lower operating/administrative expenses | D; metric association, not causal estimate; vendor-reported. |
| PDF-R12 | same page, indicator `Рост прибыли` | ERP implementations — are associated with — 13% higher profit | D; metric association, not causal estimate; accounting basis/period absent. |
| PDF-R13 | p.23, `Мониторинг...`, bullet on hierarchy | The product — supports — a hierarchy of goals and target indicators | D; model/capability relation; vendor feature; no course configuration evidence. |
| PDF-R14 | p.23, `День – Неделя – Месяц` bullet | Product monitoring — can be organized at — day/week/month cadence | D; temporal configuration; vendor feature, not universal method. |
| PDF-R15 | p.23, indicator variants bullet | Indicator variants — can be compared with — other variants | D; comparison relation; vendor feature. |
| PDF-R16 | p.23, target-monitoring bullet | Target indicators — can be monitored with drill-down to — source data | D; data provenance/drill-down; vendor feature. |
| PDF-R17 | p.23, financial-results bullet | Financial results — can be analyzed by — activity direction | D; analysis dimension; vendor feature. |
| PDF-R18 | p.23, report-form bullet | Indicator analysis — can be presented as — graphical analytical reports | D; representation relation; vendor feature. |
| PDF-R19 | p.23, email bullet | Enterprise indicators — can be distributed to — users by email | D; dissemination relation; vendor feature. |
| PDF-R20 | p.23, mobile-access bullet | Indicator data — can be accessed on — mobile devices | D; access relation; vendor feature. |
| PDF-R21 | p.25, first manager capability | Managers — can assess — enterprise performance indicators | D; analysis capability; vendor description. |
| PDF-R22 | p.25, deviation bullet | Managers — can identify — plan deviations, negative trends, and growth opportunities | D; monitoring capability; no proof that a particular decision was taken. |
| PDF-R23 | p.25, drill-down bullet | Performance indicators — can be traced to — individual business operations | D; data lineage/drill-down; vendor feature. |
| PDF-R24 | p.25, actual financial result bullet | Actual enterprise activity — supplies data for — retrospective financial assessment | D; actual-vs-planned distinction; brochure-level description. |
| PDF-R25 | p.25, planned-data bullet | Planned data — supports assessment of — future decision effectiveness | D; forecast/planning modality; vendor description, not observed outcome. |
| PDF-R26 | p.27, product-structure bullet | Product design — can be visualized as — a product structure | D; structure/representation; vendor capability. |
| PDF-R27 | p.27, resource-specification bullet | Resource specifications — describe — production processes | D; specification/process; vendor capability. |
| PDF-R28 | p.27, universal-specification bullet | A universal specification — can apply to — a nomenclature type | D; applicability; vendor capability. |
| PDF-R29 | p.27, route-card bullet | Route cards — detail — resources required for production | D; resource specification; vendor capability. |
| PDF-R30 | p.27, serial-accounting bullet | Serial accounting — can track — materials, semi-finished goods, and products | D; traceability; vendor capability. |
| PDF-R31 | p.27, parameterized-supply bullet | Parameterized provision — supports demand for — nomenclature | D; demand/supply relation; vendor capability. |
| PDF-R32 | p.27, three-level planning bullet | Production planning — has — three planning levels | D; hierarchy; vendor capability. |
| PDF-R33 | p.27, demand-consolidation bullet | Production planning — consolidates demand for — products | D; aggregation; vendor capability. |
| PDF-R34 | p.27, chief/local dispatcher bullet | Production planning — uses — chief and local dispatch roles | D; responsibility/role; vendor capability. |
| PDF-R35 | p.27, discrete/process manufacturing bullet | Production management — can address — discrete and process manufacturing | D; scope/classification; vendor capability. |
| PDF-R36 | p.27, repair-production bullet | Repair production — is supported within — production management/planning processes | D; subsystem/process integration; vendor capability, not classroom deployment. |
| PDF-R37 | p.27, `Интервальное планирование` bullet | Production planning — can use — interval planning | D; planning feature; vendor capability, not independently explained method. |
| PDF-R38 | p.27, `Барабан – Буфер – Веревка` bullet | Production planning — lists — Drum–Buffer–Rope | D; named method/product claim. Primary method source not audited in this attachment report. |
| PDF-R39 | p.27, bottleneck bullet | Planning — can prioritize — production bottlenecks | D; constraint relation; vendor capability, not proof of a specific method implementation. |
| PDF-R40 | p.27, MES/APS bullet | Operational planning — can be conducted at — MES/APS level | D; planning architecture/capability; vendor description. |
| PDF-R41 | p.28, shift-task first bullet | Shift tasks — support — shift-based work in production subdivisions | D; work organization; vendor capability. |
| PDF-R42 | p.28, no-route-map bullet | Shift tasks — can create — production operations without route maps | D; document/process relation; vendor capability. |
| PDF-R43 | p.28, priority bullet | Production orders — can be assigned — priority (including VIP priority) | D; ordering/priority; vendor capability. |
| PDF-R44 | p.28, availability bullet | Equipment/material availability — can be assessed within — a time interval | D; temporal/resource constraint; vendor capability. |
| PDF-R45 | p.28, resource provision bullet | Production resource provision — can be subject to — expanded control | D; control relation; vendor capability. |
| PDF-R46 | p.28, transport/waiting bullet | Production planning — can account for — transport and material waiting time | D; duration/dependency; vendor capability. |
| PDF-R47 | p.28, forecast bullet | Planning — can forecast — production-process progress | D; forecast relation; planned, not actual progress. |
| PDF-R48 | p.28, dispatching bullet | Production — can be dispatched at — intershop and intrashop levels | D; hierarchy/dispatch; vendor capability. |
| PDF-R49 | p.28, replanning bullet | The plan — can be changed by — flexible replanning | D; plan state; vendor capability. |
| PDF-R50 | p.28, output bullet | Employee work output — can be accounted for in — production | D; accounting/record relation; vendor capability, record not identical to physical event. |
| PDF-R51 | p.29, Industry 4.0 bullet | MES-level production management — can integrate — Industry 4.0 technologies | D; integration; vendor capability claim. |
| PDF-R52 | p.29, scenario-modeling bullet | Shop-level planning — can use — scenario modeling | D; planning/simulation; vendor capability. |
| PDF-R53 | p.29, optimization bullet | Production scheduling — can be optimized by — multiple criteria | D; optimization; vendor capability, method not described. |
| PDF-R54 | p.29, technology-constraints bullet | Production planning — can account for — technology characteristics and constraints | D; constraint; vendor capability. |
| PDF-R55 | p.29, real-time-information bullet | Production management — can provide — current process information | D; observation/reporting; vendor capability. |
| PDF-R56 | p.30, standards-data accuracy bullet | Planning quality — is described as less dependent on — normative-data accuracy | D; vendor benefit claim; not an independently demonstrated causal relation. |
| PDF-R57 | p.30, discrete/process/repair bullet | Production management — covers — discrete, process, and repair production | D; scope; vendor capability. |
| PDF-R58 | p.30, responsibility bullet | Production management — divides responsibility across — planning/consolidation, enterprise dispatcher, and shop level | D; roles/hierarchy; vendor model. |
| PDF-R59 | p.30, operation/material precision bullet | Production accounting — can specify — operation composition and material use per launch batch | D; accounting granularity; vendor capability. |
| PDF-R60 | p.30, replanning bullet | The system — is intended to reduce — replanning need | D; vendor benefit claim; causal effect not independently verified. |
| PDF-R61 | p.30, semaphore bullet | Stage dispatching — uses — a semaphore notification mechanism | D; status/notification; vendor capability. |
| PDF-R62 | p.30, forecast bullet | Production managers — can forecast — adverse plan/timing developments | D; forecast; planned, not observed event. |
| PDF-R63 | p.32, object-accounting bullet | The subsystem — records — repair objects | D; record/object relation; vendor capability. |
| PDF-R64 | p.32, classification bullet | Repair objects — can be classified by — shared composition/passport characteristics | D; classification; product feature. |
| PDF-R65 | p.32, same bullet | Repair objects — can be classified by — runtime indicators | D; classification; product feature. |
| PDF-R66 | p.32, same bullet | Repair objects — can be classified by — repair types | D; classification; product feature. |
| PDF-R67 | p.32, same bullet | Repair objects — can be classified by — operating modes | D; classification; product feature. |
| PDF-R68 | p.32, condition bullet | The subsystem — tracks — repair-object condition | D; monitoring; product feature. |
| PDF-R69 | p.32, affiliation/location bullet | The subsystem — tracks — repair-object affiliation and location | D; location/provenance; product feature. |
| PDF-R70 | p.32, hierarchy bullet | Repair objects — may contain — nested objects/nodes | D; containment; product feature. |
| PDF-R71 | p.32, defect-planning bullet | Defect diagnosis — informs — repair production and stock planning | D; evidence/dependency; product capability. |
| PDF-R72 | p.32, same bullet | Repair/stock planning — can consider — probability of different outcomes | D; uncertainty; product capability, probabilities not specified. |
| PDF-R73 | p.33, runtime/defects bullet | Operation of repair objects — yields entered records of — runtime | D; event/record; vendor workflow description, not a course event. |
| PDF-R74 | p.33, same bullet | Operation of repair objects — yields entered records of — detected defects | D; event/record; vendor workflow description. |
| PDF-R75 | p.33, defect-journal bullet | Defects — can be registered in — a journal | D; record relation; vendor capability. |
| PDF-R76 | p.33, same bullet | Registered defects — support — analysis | D; evidence/analysis; vendor capability. |
| PDF-R77 | p.33, same bullet | Defect analysis — supports organizing — planned repair measures | D; planning; not execution. |
| PDF-R78 | p.33, same bullet | Defect analysis — supports organizing — unplanned repair measures | D; planning; not execution. |
| PDF-R79 | p.34, schedule bullet | Registered defects — are inputs to — preventive repair schedule | D; planning dependency; vendor capability. |
| PDF-R80 | p.34, schedule bullet | Runtime — is an input to — preventive repair schedule | D; planning dependency; vendor capability. |
| PDF-R81 | p.34, schedule bullet | Repair rules — are inputs to — preventive repair schedule | D; planning dependency; rules not defined in brochure. |
| PDF-R82 | p.34, schedule bullet | External orders — are inputs to — preventive repair schedule | D; planning dependency; vendor capability. |
| PDF-R83 | p.34, integration bullet | Repair subsystem — integrates with — production subsystem | D; subsystem relation; vendor capability. |
| PDF-R84 | p.34, integration bullet | Repair subsystem — integrates with — regulated accounting subsystem | D; subsystem relation; vendor capability. |
| PDF-R85 | p.34, work-center bullet | Repair objects — may be linked to — production work centers | D; association; vendor capability. |
| PDF-R86 | p.34, availability bullet | Planned equipment repairs — affect — equipment availability for production planning | D; plan/resource-availability; vendor capability; plan is not completed maintenance. |
| PDF-R87 | p.36, first bullet | The cost subsystem — controls — material flows and resource consumption | D; control/flow; vendor capability. |
| PDF-R88 | p.36, same bullet | Resource consumption — supports — production activity | D; resource/activity; vendor capability. |
| PDF-R89 | p.36, same bullet | Resource consumption — supports — management activity | D; resource/activity; vendor capability. |
| PDF-R90 | p.36, same bullet | Resource consumption — supports — commercial activity | D; resource/activity; vendor capability. |
| PDF-R91 | p.36, operational-accounting bullet | Cost accounting/product costing — is based on — operational accounting data | D; data dependency; vendor description. |
| PDF-R92 | p.36, actual-cost dimensions bullet | Actual enterprise costs — can be recorded by — activity type | D; classification/dimension; vendor capability. |
| PDF-R93 | p.36, same bullet | Actual enterprise costs — can be measured in — natural and monetary units | D; measurement; vendor capability. |
| PDF-R94 | p.36, WIP bullet | Work-in-progress resources — can be accounted for by — operational quantity | D; inventory/state; vendor capability. |
| PDF-R95 | p.36, period-end WIP bullet | WIP balances — can be measured at — reporting-period end | D; temporal/state; vendor capability. |
| PDF-R96 | p.36, allocation bullet | Nomenclature costs — can be allocated by — rule | D; cost allocation; product capability. |
| PDF-R97 | p.36, same bullet | Nomenclature costs — can be allocated to — expense articles | D; cost allocation; product capability. |
| PDF-R98 | p.36, same bullet | Nomenclature costs — can be allocated by — outputs | D; cost allocation; product capability. |
| PDF-R99 | p.36, overhead-allocation bullet | Overhead expenses — may use — different allocation variants | D; cost allocation; variants not defined. |
| PDF-R100 | p.36, actual-cost bullet | Actual output cost — is calculated for — a reporting period | D; calculation/period; vendor capability. |
| PDF-R101 | p.36, cost-structure bullet | Output cost — can be decomposed into — source costs | D; decomposition; vendor capability. |
| PDF-R102 | p.36, GOZ bullet | Financial results — can be accounted for separately by — organizations performing GOZ work | D; entity/segregation; vendor capability. |
| PDF-R103 | p.37, actual-cost bullet | Calculated cost — can be traced to — source costs | D; provenance; vendor capability. |
| PDF-R104 | p.37, actual-cost bullet | Source-cost detail — supports — variance analysis | D; analysis/evidence; vendor capability. |
| PDF-R105 | p.37, planned-cost bullet | Planned output cost — can be calculated from — planned cost data | D; planned calculation; vendor capability, not actual expenditure. |
| PDF-R106 | p.37, same bullet | Planned-cost detail — can be broken down by — semi-finished goods | D; classification/decomposition; vendor capability. |
| PDF-R107 | p.37, same bullet | Planned-cost detail — can be broken down by — production stages | D; classification/decomposition; vendor capability. |
| PDF-R108 | p.37, preliminary estimate bullet | Output cost — can receive — a preliminary monetary estimate during the period | D; estimate/time; vendor capability, not final actual cost. |
| PDF-R109 | p.37, allocation bullet | Costs — can be distributed using — different methods | D; allocation; methods not defined in brochure. |
| PDF-R110 | p.37, results bullet | Financial results — can be analyzed by — enterprise activity direction | D; dimension/analysis; vendor capability. |
| PDF-R111 | p.41, title/diagram; p.14 corporate-overview item | Subsidiary legal entities — use — 1C:ERP operational reporting | D; architecture/source diagram; product brochure only. |
| PDF-R112 | p.41, diagram | Subsidiary reporting — is aggregated by — the management company using 1C:Holding | D; aggregation/system relation; product capability claim. |
| PDF-R113 | p.41, diagram; p.14 corporate overview | The holding-level reporting set — includes — IFRS financial reports | D; reporting-standard scope; the figure does not substantiate compliance or accounting rules. |
| PDF-R114 | p.41, diagram | The holding-level reporting set — includes — budgets | D; reporting/data relation; vendor diagram. |
| PDF-R115 | p.41, diagram | The holding-level reporting set — includes — KPI | D; reporting/data relation; vendor diagram. |
| PDF-R116 | p.41, diagram | The holding-level reporting set — includes — financial reports | D; reporting/data relation; vendor diagram. |
| PDF-R117 | p.64, warehouse feature list | Inventory analysis — can store results of — ABC classification | D; analysis/result persistence; product capability. ASCM dictionary supports ABC, not fixed thresholds. |
| PDF-R118 | p.64, same bullet | Inventory analysis — can store results of — XYZ classification | D; analysis/result persistence; product capability; formula unavailable in ASCM dictionary and 1C 2.6 detail is access-gated. |
| PDF-R119 | p.64, demand bullet | Inventory planning — can calculate — forecast demand | D; planning/forecast; product feature, not actual demand. |
| PDF-R120 | p.80, budget-estimate equation | Project cost estimate — is calculated from — workstation count × labor hours per workstation × hourly rate | D; calculation/dependency; simplified vendor heuristic; examples explicitly not project-specific estimates. |

### Seminar 1: `Семинар 1_Драфт 14-10-23.pptx`

| ID | Exact slide/locator | Candidate source statement (paraphrased; may bundle predicates) | Status / type / source status / modality boundary |
|---|---|---|---|
| S1-R01 | slide 4, `1. Система оценивания`, report criteria | Completion of assigned tasks — determines — a 0–3 point score | D; assessment; course rubric; not observed student performance. |
| S1-R02 | slide 5, additional assignment | One calendar year — is assumed to equal — 365×24 = 8,760 runtime hours | D; teaching assumption; course-only; not a sourced engineering constant for every asset. |
| S1-R03 | same slide | A repair cycle — may be planned as — TR → KR → TR | D; cycle/sequence; instructional exercise; planned, not executed. |
| S1-R04 | slide 6, `3. Схема процессы планирования ТОиР`, production-assets questions | The maintenance process — begins by defining — production assets/equipment | D; process; slide diagram; course model. |
| S1-R05 | same slide, question on asset division | Production assets — may be classified as — main/supporting/reserve equipment | D; classification; instructional prompt, organization-specific values unspecified. |
| S1-R06 | same slide, maintenance-strategy question | Asset maintenance strategy — may be selected by — runtime | D; strategy; course prompt, no independent standard cited. |
| S1-R07 | same locator | Asset maintenance strategy — may be selected by — calendar periodicity | D; strategy; course prompt, no independent standard cited. |
| S1-R08 | same locator | Asset maintenance strategy — may be selected by — condition | D; strategy; course prompt, no independent standard cited. |
| S1-R09 | same locator | Asset maintenance strategy — may be selected as — run-to-failure | D; strategy; course prompt, no independent standard cited. |
| S1-R10 | same slide, repair-technology questions | Repair technology — determines — service/maintenance standards for equipment | D; requirements relation; course prompt; exact norms left unspecified. |
| S1-R11 | same slide | Repair technology — determines — the sequence of repair work | D; process relation; course prompt. |
| S1-R12 | same slide | Repair technology — determines — required tools/materials and quantities | D; resource requirement; course prompt. |
| S1-R13 | same slide | Repair technology — determines — required personnel and qualification | D; resource requirement; course prompt. |
| S1-R14 | same slide | Repeat repair work — is planned at — a stated recurrence interval | D; temporal planning; course prompt; interval depends on asset, not supplied. |
| S1-R15 | same slide, condition monitoring questions | Current equipment condition — is assessed using — condition index/calculation | D; measurement; teaching prompt; formula/source not supplied. |
| S1-R16 | same slide | Equipment condition and need — inform identification of — assets requiring maintenance/repair | D; assessment/planning; course model. |
| S1-R17 | same slide | Runtime/operation indicators — are inputs to — equipment monitoring | D; measurement; course model. |
| S1-R18 | same slide | Sensor/technology-system readings — are inputs to — condition monitoring | D; measurement; course model. |
| S1-R19 | same slide | Monitoring and assessment — may lead to — corrective measures | D; decision/process; course model. |
| S1-R20 | same slide, program sequence | Long-term maintenance program — is refined into — preliminary annual program | D; planning hierarchy; course model. |
| S1-R21 | same slide | Preliminary annual program — is refined into — annual program | D; planning hierarchy; course model. |
| S1-R22 | same slide | Annual program — is updated into — quarterly/monthly program | D; planning hierarchy; course model. |
| S1-R23 | slide 7, `4. План упражнений` | Exercise creates — an object of operation — in 1C | D; object creation; planned student practice, not evidence a student did it. |
| S1-R24 | same slide | Exercise creates — object class and nomenclature — for maintenance resources | D; classification/reference; planned student practice. |
| S1-R25 | same slide | Resource specifications — describe — repair work | D; specification/work relation; planned student practice. |
| S1-R26 | slide 11, TR repair-type form | TR repair type — has — a one-year interval in the example | D; attribute/interval; demo configuration, not a general standard. |
| S1-R27 | same slide | TR repair type — is configured with — a three-day duration in the example | D; attribute/interval; demo configuration, not a general standard. |
| S1-R28 | same slide | TR repair type — generates orders on — a monthly schedule in the example | D; schedule; demo configuration only. |
| S1-R29 | slide 12, `Создание номенклатуры, соответствующей виду ремонта ТР` | TR repair type — is associated with — corresponding repair-work nomenclature | D; reference; demo setup instruction. |
| S1-R30 | slide 14, KR setup | KR repair type — is associated with — corresponding repair-work nomenclature | D; reference; demo setup instruction. |
| S1-R31 | slide 15, `Создание узла объекта эксплуатации` | Equipment decomposition — creates — object-operation nodes | D; part/whole; demo product workflow. |
| S1-R32 | slide 16, `Создание узлов` | A node — may have — its own repair cycle | D; part/whole/attribute; slide notes example leaves it empty, so no instance assignment is claimed. |
| S1-R33 | same slide | A created object node — is assigned — a specific object class | D; classification; demo workflow. |
| S1-R34 | slide 17, equipment type | Equipment — is assigned an equipment type from — an additional-attribute reference | D; attribute/reference; demo workflow. |
| S1-R35 | slide 18, `Структура предприятия и Ресурсные спецификации` | Repair dispatcher subdivision — is distinct from — repair execution subdivision | D; organizational distinction; instructional model. |
| S1-R36 | same slide | TR work/service — is linked to — a TR resource specification | D; specification/reference; planned setup. |
| S1-R37 | same slide | KR work/service — is linked to — a KR resource specification | D; specification/reference; planned setup. |
| S1-R38 | slide 20, dispatcher subdivision | Dispatcher subdivision — is marked as responsible for — production orders | D; responsibility/role; configuration instruction. |
| S1-R39 | slides 21–22, repair shop setup | Repair shop subdivision — is configured with — work-calendar/shift and availability settings | D; resource/calendar; screenshot/workflow, exact values not treated as universal. |
| S1-R40 | slide 23, VRC/RC creation | A work-center type (VRC) — groups/defines — work centers (RCs) | D; classification/hierarchy; demo configuration. |
| S1-R41 | slide 24, VRC/RC screenshot | Work center (RC) — is associated with — a work-center type (VRC) | D; assignment; demo screenshot; identifiers omitted. |
| S1-R42 | slide 26, resource specification copied | A copied resource specification — contains — a production process | D; composition; demo product workflow. |
| S1-R43 | slide 27 | The repair resource specification — references — nomenclature and dispatcher subdivision | D; reference; demo configuration. |
| S1-R44 | slide 28 | A production phase — is assigned to — subdivision and VRC | D; assignment; plan/configuration, not work event. |
| S1-R45 | slide 29 | A production operation — is assigned to — RC | D; assignment; plan/configuration. |
| S1-R46 | slide 30 | Resource specification — becomes available for use when — status is set to `Действует` | D; lifecycle/state; demo configuration. |
| S1-R47 | slide 31 | KR repair resource specification — is created by copying — a base KR specification | D; derivation/copy; demo workflow. |
| S1-R48 | slide 33, `Упражнение: Планирование работ ТОиР` | Maintenance planning — creates — maintenance work plan | D; plan creation; planned exercise. |
| S1-R49 | same slide | Maintenance planning — creates — repair orders | D; document creation; planned exercise, not actual repair. |
| S1-R50 | same slide | Repair orders — can lead to creation of — production orders | D; process/document; planned exercise; next seminar covers later steps. |
| S1-R51 | slide 34, repair planning (0/3) | Equipment object status — is set to — `В эксплуатации` before planning | D; state/precondition; demo instruction, not proof of a real asset. |
| S1-R52 | slide 36, repair planning (1/3) | Maintenance planning selection — is filtered by — previously created class | D; selection/classification; demo workflow. |
| S1-R53 | slide 37, repair planning (2/3) | Planning step — automatically populates — required fields from data | D; data-flow; demo product claim; not independently verified outside screenshot. |
| S1-R54 | slide 37 | A selected repair — opens — detailed repair-order information | D; interface navigation/data relation; demo workflow. |
| S1-R55 | slide 38, repair planning (3/3) | Repair order — requires — organization `ТОиР` in the example | D; document attribute; demo configuration only. |
| S1-R56 | slide 39, transfer to production | Repair order status `К выполнению` — enables creation of — production order | D; state/process; demo instruction. |
| S1-R57 | slide 40, control report | A repair object — can be filtered into — repair-progress report | D; report/object relation; report is not by itself proof of executed work. |

### Seminar 2: `Семинар 2_Драфт 21-10-23.pptx`

| ID | Exact slide/locator | Candidate source statement (paraphrased; may bundle predicates) | Status / type / source status / modality boundary |
|---|---|---|---|
| S2-R01 | slide 4, scoring rubric | Seminar task completion — determines — 0–3 point score | D; assessment; course rubric, not observed outcome. |
| S2-R02 | slide 4, report criteria | Repair-order report — contributes — one point per listed order (seminar 1 scoring rule) | D; scoring metric; rubric; not evidence of real repair. |
| S2-R03 | same slide | Planned-cost report — contributes — one point per listed calculation (seminar 2 scoring rule) | D; scoring metric; rubric; planned figure only. |
| S2-R04 | same slide | Employee-output report — contributes — an additional point when required totals are present | D; scoring metric; report completeness, not proof of event. |
| S2-R05 | slide 6, rubric note | Shop identifier — is expected to match — brigade identifier | D; validation condition; rubric example, actual IDs omitted. |
| S2-R06 | slide 8, TOиР scheme | Repair planning — precedes — repair execution | D; temporal/process; instructional process map. |
| S2-R07 | slide 8, program flow | Long-term program — is refined into — preliminary annual program | D; planning hierarchy; instructional model. |
| S2-R08 | same | Preliminary annual program — is refined into — annual program | D; planning hierarchy. |
| S2-R09 | same | Annual program — is updated into — quarter/month program | D; planning hierarchy. |
| S2-R10 | same, execution flow | Repair plan — informs — cost estimate | D; dependency; planned work. |
| S2-R11 | same | Work volume — is updated/approved in — repair order | D; document/state; planned work. |
| S2-R12 | same | Repair order — is subject to — operational operation-by-operation planning | D; workflow; planned work. |
| S2-R13 | same | Operational plan — produces — work assignments | D; process/document; planned work. |
| S2-R14 | same | Work execution — records use of — materials | D; record/event; expected process, not verified activity. |
| S2-R15 | same | Work execution — records — work performed | D; record/event; expected process, not verified activity. |
| S2-R16 | same | Completed repair order — is followed by — order closure | D; lifecycle; workflow, no actual work verified. |
| S2-R17 | slide 12, `Создание плановых калькуляций...` | Planned cost estimate — uses — planned material prices | D; calculation/input; planned value. |
| S2-R18 | same slide | Planned cost estimate — is built from — resource specification | D; calculation/dependency; planned value. |
| S2-R19 | slide 15, report filters | Planned-cost report — is filtered by — student's own calculation and organization `ТОиР` | D; report/filter; no student ID copied. |
| S2-R20 | slide 18, repair order selection | Production-order exercise — selects — repair orders | D; document/process; planned exercise. |
| S2-R21 | slide 19, creating production order | Selected repair order — enables creation of — production order | D; process/document; planned workflow. |
| S2-R22 | slide 20, production order fields | Production order — records — nomenclature, specification, and shop | D; document fields; planned workflow. |
| S2-R23 | same slide | Production order — is assigned status — `К производству` | D; state; status is not proof of execution. |
| S2-R24 | slide 22, phase formation | Production order — generates — production phases | D; derivation/containment; planned document. |
| S2-R25 | slide 23, phase dispatch | Dispatcher subdivision — is selected for — phase dispatch | D; assignment; planned workflow. |
| S2-R26 | slide 24, phase status | Phase — receives status — `Начат` in the exercise | D; state; training-base value, not proof of physical work. |
| S2-R27 | same slide | Phase — references — warehouse `ТОиР` in the exercise | D; document/resource association; demo configuration. |
| S2-R28 | same slide | Phase — is marked `Произведено` by — indicator setting | D; recorded status; not independent evidence that goods/work physically occurred. |
| S2-R29 | slide 25, phase material provision | Phase — requests shipment of — repair kit material | D; provision/document flow; training instruction. |
| S2-R30 | slide 25 | Material issue — supplies — production phase | D; resource/phase relation; commanded demo workflow, not verified event. |
| S2-R31 | slide 27, creating a brigade | Brigade — is associated with — a shop/subdivision | D; organization; demo workflow. |
| S2-R32 | slide 29, selecting shift and brigade | Shift assignment — selects — a current-date shift | D; temporal assignment; workflow instruction. |
| S2-R33 | same slide | Shift assignment — selects — brigade | D; assignment; planned work. |
| S2-R34 | slide 30, assigning operation | Production operation — is assigned to — selected brigade | D; assignment; planned work. |
| S2-R35 | slide 31, shift status | Shift task — is set to — `Сформировано` | D; workflow state; not proof of execution. |
| S2-R36 | slide 32, confirming execution | Exercise confirmation — records — operation completion | D; record/state; setting is not independent evidence of physical repair. |
| S2-R37 | same slide | Shift task — is set to — `Закрыто` | D; workflow state; not physical-event evidence. |
| S2-R38 | slide 33, work report | Employee-output report — summarizes — recorded completed-work output | D; report/record; not proof of repair without supporting event evidence. |
| S2-R39 | slide 34, control report example | Work-output report — groups output by — shop and brigade | D; report dimension; training example values omitted. |

## Critic disposition of the 216 numbered source-statement rows

The independent review classifies these existing rows as **source-statement rows**, not fully atomized edges. One row refers to one source paragraph, labelled table row, or arrow; a row can still bundle more than one target. Keep raw rows for traceability. Do not treat 148 as the final number of atomic S–P–O edges.

| Attachment | Reusable relation-eligible rows | Separate product observations | Excluded under relation rule | Enumerated rows |
|---|---:|---:|---:|---:|
| PDF | 76 | 29 | 15 | 120 |
| Seminar 1 | 43 | 1 | 13 | 57 |
| Seminar 2 | 29 | 0 | 10 | 39 |
| **Total** | **148** | **30** | **38** | **216** |

### Exact ID partitions

- **PDF — reusable relation-eligible (76):** `PDF-R23–R25`, `PDF-R27–R36`, `PDF-R39`, `PDF-R43–R44`, `PDF-R46–R50`, `PDF-R54`, `PDF-R57–R59`, `PDF-R63–R86`, `PDF-R88–R108`, `PDF-R110`, `PDF-R113–R116`, `PDF-R119`.
- **PDF — separate product observations (29):** `PDF-R13–R22`, `PDF-R26`, `PDF-R37–R38`, `PDF-R40–R42`, `PDF-R45`, `PDF-R51–R53`, `PDF-R55`, `PDF-R61–R62`, `PDF-R87`, `PDF-R109`, `PDF-R111–R112`, `PDF-R117–R118`. They describe product reporting/access, planning features, operational controls, or architecture; retain as vendor capabilities, not core ontology relations or course configuration evidence.
- **PDF — exclude (15):** `PDF-R01–R12`, `PDF-R56`, `PDF-R60`, `PDF-R120`. `R01` is a vendor attribution to a standard, not a domain relation. `R02–R12` are vendor-reported performance/effect figures. `R56` and `R60` are benefit/causal claims, not reusable relation assertions. `R120` is an expressly simplified vendor estimate, not a domain relation.
- **Seminar 1 — reusable relation-eligible (43):** `S1-R04–R22`, `S1-R25`, `S1-R29–R38`, `S1-R40–R46`, `S1-R48–R51`, `S1-R55–R56`.
- **Seminar 1 — separate product observation (1):** `S1-R53`, automatic field population. This is a demonstrated product capability, not a core domain relation.
- **Seminar 1 — exclude (13):** `S1-R01–R03`, `S1-R23–R24`, `S1-R26–R28`, `S1-R39`, `S1-R47`, `S1-R52`, `S1-R54`, `S1-R57`. These are a grading metric, calendar-hours teaching assumption/example repair cycle, exercise/UI setup, example-specific interval/duration/schedule, configuration/copy workflow, filtering, UI navigation, and report filtering.
- **Seminar 2 — reusable relation-eligible (29):** `S2-R06–R18`, `S2-R21–R24`, `S2-R26–R31`, `S2-R34–R39`.
- **Seminar 2 — exclude (10):** `S2-R01–R05`, `S2-R19–R20`, `S2-R25`, `S2-R32–R33`. These are grading/rubric assertions, report filtering, generic document selection, phase-dispatch UI selection, and shift/brigade selection steps.

**Interpretation boundary:** Eligible status means the attachment states a reusable relation; it does not establish the statement's truth, product behavior, or classroom execution. Status/report relations are schema/process assertions, not physical-event proof. For example, `S2-R23`, `S2-R26`, `S2-R28`, `S2-R35`, and `S2-R37` can describe document/phase/task state. `S2-R14–R15`, `S2-R36`, and `S2-R38–R39` can describe execution-to-record/report links if the ontology carries evidence provenance. Seminar slides show intended/demo workflow, not proof of real work. `S1-R54` is UI navigation and `S1-R57` is report filtering; both are excluded.

### Four-way verification status for named methods/concepts

The method/concept verification status is separate from `D` (what the attachment says). Status 1 verifies the named concept at the cited scope; it does not verify vendor application or course configuration. Status 4 means the mention does not define a verifiable method. `N/A` marks vendor metric/rubric rather than an external method.

| Candidate IDs | Four-way status | Basis and boundary |
|---|---|---|
| `PDF-M01` ISO 9001 | **1 — primary source, narrowly** | ISO's official record identifies current ISO 9001:2026, replacing withdrawn 2015. The 2020 brochure only says `ISO 9001`; no edition, certification scope, clause, or proof of 1C certification is established. The public ISO summary supports QMS context only. [ISO record](https://www.iso.org/standard/9001) |
| `PDF-M02–M11` outcome metrics | **N/A** | Vendor-reported metric labels/values, not methods. Keep as brochure-only statements; no underlying study, definitions, denominator, period, or causal design is supplied. |
| `PDF-M12–M13` hierarchy/cadence | **4 — no verifiable method defined** | Generic vendor goal/indicator model and monitoring cadence; neither gives a general method or verifies course use. |
| `PDF-M14` DBR | **1 — primary/owner source** | The free Goldratt Research Labs overview identifies DBR as an operations rule/method. This confirms the concept, not its 1C implementation. Detailed Goldratt S&T/library material may be paid/restricted and was not treated as reviewed. [Goldratt Research Labs: Introduction to TOC](https://www.goldrattresearchlabs.com/introduction-to-toc/) |
| `PDF-M15` IFRS/МCФО | **1 — primary source, existence only** | Verifies the reporting framework exists; not product compliance, accounting policy, or the depicted consolidation procedure. See [IFRS Foundation standards](https://www.ifrs.org/issued-standards/list-of-standards/). |
| `PDF-M16` ABC | **1 — primary source, narrow** | ASCM Supply Chain Dictionary, **20th ed. (2026), p.7**, supports ABC classification; the cited edition/locator is verified but detailed dictionary content is member-gated. It does not verify the brochure's algorithm or course setup. [ASCM Dictionary portal](https://learn.ascm.org/s/ascm-dictionary) · [20th-edition PDF](https://learn.ascm.org/sfc/servlet.shepherd/document/download/069R300000i9sW9IAI) |
| `PDF-M17` XYZ | **3 — exact primary details unavailable/gated** | The 1C ERP 2.6 TOC lists an ABC/XYZ topic, but detailed chapter content is auth-gated; no formula, cutoff, or classroom configuration is claimed. |
| `PDF-M18` simplified project estimate | **4 — mention does not define a verifiable method** | It is explicitly described as a very simplified estimate, with a warning that example values are not project-specific. |
| `S1-M01`, `S2-M01` scoring metrics | **N/A** | Local exercise rubrics, not external methods or outcome measures. |
| `S1-M02`, `S1-M07–M09`, `S2-M02–M04` | **4 — no verifiable external method defined** | Course exercises, workflows, or product setup instructions. They do not define general methods. |
| `S1-M03–M06` maintenance-strategy concepts | **1 — primary source, concept level** | NASA primary material supports time/cycle-based, condition-based, and run-to-failure maintenance concepts. It does not supply universal intervals, a complete taxonomy, or a local policy. [NASA maintenance reference](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_8831_002E_&page_name=all) |

**Related standards/method limits:** IAS 2 supports FIFO only as an inventory cost formula, not physical picking sequence, warehouse configuration, or a particular 1C algorithm. The IFRS standard PDF link redirected to subscription-only access in this pass; the supplied source review is limited to IAS 2 cost-formula support. The 1C ERP 2.6 TOC-only/gated limits remain; do not silently substitute version 2.5 or infer hidden details. ASCM Dictionary 20th ed. (2026) uses p.7 for ABC, p.116 for Min–max, and p.124 for OTIF; detailed dictionary pages are member-gated. The supplied ASCM OTIF definition is not identical to SCOR RL.1.1 Perfect Customer Order Fulfillment; dictionary detail is member-gated, so this distinction is reported from the cited researcher review rather than a direct download in this pass.

## Primary-source and version/access cross-checks

- **Coase (1937)**, *The Nature of the Firm*, original publisher text: <https://onlinelibrary.wiley.com/doi/full/10.1111/j.1468-0335.1937.tb00002.x>. Its firm/coordination argument does not establish that ERP necessarily reduces transaction costs. Coase appears in HTML, not these three attachment candidate rows.
- **Porter**, *Competitive Advantage* publisher record (<https://www.simonandschuster.com/books/Competitive-Advantage/Michael-E-Porter/9780684841465>) and HBS value-chain overview (<https://www.isc.hbs.edu/strategy/business-strategy/Pages/the-value-chain.aspx>): value-chain analysis concerns strategically relevant activities and links; it is not a 1C module taxonomy. Not located as a named method in the three attachments.
- **ASCM SCOR v14.0** (<https://scor.ascm.org/api/files/24?v=1701805144791>): the official source distinguishes six level-1 processes. **OTIF** in ASCM Supply Chain Dictionary 20th ed. (2026), p.124 is not identical to SCOR RL.1.1 Perfect Customer Order Fulfillment, which additionally covers documents and condition. Neither term is asserted in these attachment candidate rows; no extrapolation was made.
- **CIPS supplier-evaluation guidance** (<https://1prd-dxp.cips.org/intelligence-hub/managing-suppliers/supplier-evaluation>) is guidance, not a mandatory standard or course rubric. No attachment relation was credited to it.
- **ISO 9001:** official ISO record (<https://www.iso.org/standard/9001>) shows ISO 9001:2026 current as of the audit date and replacing withdrawn 2015. The 2020 brochure says only “ISO 9001” at p.17; it gives no edition, scope, certificate, or clause evidence. The public summary is insufficient for full normative interpretation.
- **ABC/XYZ and Min–max:** ASCM Supply Chain Dictionary 20th ed. (2026) gives ABC p.7, Min–max p.116, OTIF p.124 (edition/locators via researcher; direct PDF gated); the sample ABC percentages are typical, not fixed. The 1C ERP 2.6 ITS TOC for ABC/XYZ (<https://its.1c.ru/db/erp26doc/bookmark/ABCXYZClassification/ABCXYZClassification>) and Min–max (<https://its.1c.ru/db/erp26doc/bookmark/ExtendedProvision/ParametersOfMaintainingStock1>) is TOC-only/auth-gated; no detailed algorithm, thresholds, or classroom configuration is claimed. The 2020 PDF names ABC/XYZ but does not state a formula.

## Remaining limits

- The PDF is a dated vendor brochure. Marketing figures lack underlying studies, definitions and causal evidence; listed product capabilities are not proof of local deployment.
- The seminar decks contain screenshots from an instructional/demo workflow. They record intended setup and statuses; they do not confirm a student completed a task or that a physical repair occurred.
- Password/login fields appear masked in the deck text and no secrets or individual identifiers have been reproduced. Any screenshot OCR artifacts/ambiguous UI labels were not treated as facts unless corroborated by the slide text/visual itself.
- General maintenance strategies on slide 6 are teaching prompts. No external standard or local organizational policy is asserted.
- This register is limited to the 3 corpus attachments and the candidate method/relation grain above. It makes no claim about inaccessible personal-account files or other sources outside the declared corpus.
