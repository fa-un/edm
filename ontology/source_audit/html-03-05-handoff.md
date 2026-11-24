# Durable source-audit handoff — HTML 03–05

Read-only source audit. Sources were reread completely through EOF from the repository checkout; no course source was edited. This artifact is a fresh reconstruction from the source files, not a copy of an earlier ephemeral message. It uses source-statement grain: one eligible paragraph, labeled table row, or diagram arrow/caption; split independent predicates only where separable. Generic definitions, synthetic instance values (unless teaching a rule), generic UI steps, and mere feature names are excluded. Locator wording below is repository-relative (file is identified by its section) and uses the exact visible heading, table-row label, or paragraph opening. `lecture2_student_guide.html` has explicit IDs for several headings (`#common-definitions`, `#production-data`, `#shelf-norm`, `#plan-and-fact`, `#planning-levels`, `#dispatching`, `#cost-deviations`, `#repair-model`); `ai_analyst_tools.html` and `seminar2_production_case.html` do not assign IDs to these headings, so their exact visible heading text is the locator rather than an invented fragment. All three pages are student-facing.

**Count reconciliation:** named candidates A=13, L=11, S=6 (total 30); relation rows A=26, L=78, S=25 (total 129). IDs are sequential per source and are the count basis. D=directly stated; C=conditional; I=interpretive; H=hypothesis/explicitly provisional. Source status on relation rows describes validation of the claim beyond the course page, not truth of the course-page occurrence. “Course only” means no independent primary validation was performed. Modality = instructional / illustrative / hypothetical / plan / target / observed-record as stated; audience=student unless otherwise noted.

## Named method/model/standard/metric/practice candidates

Status key: **V** verified against primary/owner source; **S** secondary source only; **U** primary source unavailable; **N** mention does not define a verifiable method. Each row is one candidate; no bundling.

|ID|Source locator|Named candidate|Status and source/version/access rationale|
|---|---|---|---|
|A-M01|`Задача аналитика`, paragraph beginning “В IT4IT выделяют…”|IT4IT value-stream concept|**V** — The Open Group owner material for IT4IT v3.0.1 confirms value streams as a generic concept. This does not validate the page’s exact four stream labels.|
|A-M02|same paragraph|Strategy to Portfolio|**U** — Named as an exact IT4IT stream label; full IT4IT v3.0.1 details are gated, so exact label/definition not independently checked against accessible primary text.|
|A-M03|same paragraph|Requirement to Deploy|**U** — Same gated IT4IT v3.0.1 source; exact label not independently verifiable from accessible owner text.|
|A-M04|same paragraph|Request to Fulfill|**U** — Same gated IT4IT v3.0.1 source; exact label not independently verifiable from accessible owner text.|
|A-M05|same paragraph|Detect to Correct|**U** — Same gated IT4IT v3.0.1 source; exact label not independently verifiable from accessible owner text.|
|A-M06|same paragraph|Plan—Build—Deliver—Run|**N** — Explicitly a simple course frame, expressly not official IT4IT equivalents; no independent named method asserted.|
|A-M07|`Почему одной записи саммари недостаточно`, paragraph beginning “Запись сохраняет…”|transcript/source-to-summary verification practice|**N** — Instructional practice, but page supplies no independently named/verifiable standard or procedure.|
|A-M08|`Как устроена автоматизация интерфейса`, first paragraph|RPA (robotic process automation)|**S** — Page cites vendor explanations and describes a vendor-implemented UI-automation example. Reread confirms RPA here is not a universal implementation guarantee; no proof of 1C deployment.|
|A-M09|`Как связать отчёт с таблицей через MCP`, first paragraph|MCP (Model Context Protocol) conformance|**V** — Primary protocol spec dated 2026-07-28 supports resources/list/read and tools/list/call. It does not prescribe the course’s particular workflow or guarantee write access.|
|A-M10|same paragraph|course read-match-write-reread workflow|**N** — Course-specific worked practice, not a workflow prescribed by MCP; protocol’s availability of tools is not a universal write permission.|
|A-M11|`Сценарий 2: проверка вывода об активности`, paragraph beginning “Онтологическая проверка выясняет…”|ontological checking|**N** — Descriptive course practice, not a separately specified verifiable method.|
|A-M12|same section, paragraph beginning “Навык greek-scholastic…”|Greek-scholastic skill|**N** — Named skill/tool, not a defined method in the page. Public FPF/skill resources do not validate course-specific execution.|
|A-M13|same paragraph|Logika|**N** — Named learning aid, not a method defined or independently applied by the page.|
|L-M01|`Общие понятия`, row `Ресурсная спецификация`|resource-specification model|**N** — Course/product instructional model; cited 1C manual is not independently inspected here.|
|L-M02|`Общие понятия`, row `Технологический процесс`|technological-process model|**N** — Defined by the course page; no independently verified method standard.|
|L-M03|`Норматив, план и факт`, table row `Нормативные данные`|normative-data model|**N** — Teaching distinction, not a separately named method.|
|L-M04|same table, row `Оперативные данные`|operational-data model|**N** — Teaching distinction, not a separately named method.|
|L-M05|same table, row `План-факт`|plan/fact comparison|**N** — General comparison practice, not a defined/validated named method in this source.|
|L-M06|`Три уровня планирования`, table rows|three-level production-planning model|**N** — Course model; 1C manual cited but not independently checked.|
|L-M07|`Как диспетчер проверяет выполнимость`, row `Производственная мощность`|capacity model|**N** — Conceptual teaching model, no independently verified named method.|
|L-M08|same section, row `Резерв доступности`|availability reserve|**N** — Setting/metric concept, not a method. Example percentage is not universal.|
|L-M09|same section, row `Коэффициент времени работы`|work-time coefficient|**N** — Product/course setting, not general method; example coefficient is not validated as universal.|
|L-M10|`Почему фактическая себестоимость отличается…`, table rows|cost variance analysis|**N** — Diagnostic teaching practice; page frames causes as candidates for checking, not a validated named method.|
|L-M11|`Как та же модель применяется к ремонтам`, paragraph beginning “При ремонте силами…”|production-to-repair analogy|**N** — Explicit analogy, not an independently verified repair method or identity claim.|
|S-M01|`Общие понятия`, rows `Норматив`, `План`, `Факт`, `Отклонение`|norm/plan/fact/deviation classification|**N** — Explicit course taxonomy; not a separately named standard/method.|
|S-M02|`2. Путь заказа`, table `Понятия производственного задания`|production-order lifecycle model|**N** — Course exercise model; the page cites practice materials but does not define an external method.|
|S-M03|`3. Разбор отклонения`, paragraph beginning “Рассмотрите перерасход…”|ordered hypothesis checking|**N** — Teaching exercise; no named diagnostic method or validated ordering rule.|
|S-M04|`4. Ремонты по аналогии`, paragraph beginning “Уточните, от какого события…”|repair-interval planning practice|**N** — Course exercise requiring a verified reference point; no independently named method.|
|S-M05|`Общие понятия`, row `Вид рабочего центра (ВРЦ)`|interchangeable-work-center grouping model|**N** — Course/product model; no manual independently inspected.|
|S-M06|`Общие понятия`, row `Резерв доступности`|availability-reserve metric|**N** — Definition/practice, not independently named or externally validated metric.|

## Relation registry: `ai_analyst_tools.html` (A01–A26)

All relation rows below are **course-page-supported**; exact external-source status appears only where noted. Source class in brackets; D/C/I/H as above; audience `student` throughout.

|ID|Exact locator (heading + paragraph opening / row / caption)|Reusable relation claim|D/C/I/H; class; status/modality|
|---|---|---|---|
|A01|`Задача аналитика`, opening paragraph `В первой лекции аналитик…`|Enterprise analysis converts a need into a testable requirement; AI draft remains subject to source checking.|D; evidence→requirement; course-only; instructional|
|A02|`Задача аналитика`, paragraph `В IT4IT выделяют…`|IT4IT value streams are presented as a frame for linking lifecycle work.|D; value-stream model; owner concept V, exact labels U; instructional|
|A03|same paragraph|Plan—Build—Deliver—Run is explicitly a course frame, not equivalent to IT4IT streams.|D; model distinction; course-only; instructional|
|A04|`Почему одной записи саммари недостаточно`, paragraph `Запись сохраняет…`|Recording preserves a primary source; transcript makes it searchable/citable; summary compresses and may omit qualifications.|D; provenance/representation; course-only; instructional|
|A05|same heading, paragraph `mymeet.ai — пример…`|The simulated exercise is not an output of the named service and does not test speech-recognition quality.|D; source/provenance; course-only; simulation|
|A06|`Практика: найдите нюанс…`, paragraph `Ролевая симуляция…`|The dialogue and summary are synthetic teaching artifacts, not a real interview.|D; provenance; course-only; simulation|
|A07|`Результат в analysis.md`, paragraph `Например, из известной проблемы…`|A known status problem can be turned into a conditional requirement with observable status/reason result.|D; problem→requirement/test; course-only; illustrative|
|A08|same section, paragraph `Это черновик…`|Reported duration is not a verified measurement; target duration is desired, not achieved.|D; evidence/modality distinction; course-only; illustrative/target|
|A09|`Как устроена автоматизация интерфейса`, figure caption `Цикл автоматизации…`|Automation cycle links task, screen observation, action, report generation, and result check.|D; process/state; course-only; illustrative|
|A10|same heading, paragraph `RPA — автоматизация…`|UI task execution proceeds through observed state→action→new state→verification; this vendor-style example does not prove a prerecorded robot or DB access.|D; process/state; secondary vendor example; illustrative|
|A11|same heading, paragraph `Детальный отчёт…`|Detailed and summary reports differ; filter/report identity and both dates must be checked before using a result.|D; report/filter dependency; course-only; warning|
|A12|`Как связать отчёт с таблицей через MCP`, figure caption `Агент вызывает…`|An MCP tool invocation may read or make a permitted table write and then check the result.|C; tool/data access; MCP primary confirms tool calls, not write guarantee; illustrative|
|A13|same heading, paragraph `MCP (Model Context Protocol)…`|Client invokes an exposed service tool, which accesses data under provided permissions and returns data.|D; protocol/tool relation; MCP spec 2026-07-28 validates resources/list/read and tools/list/call, access conditional|
|A14|same paragraph|Course read→match→permitted-write→reread is an instructional workflow, not mandated by MCP.|D; process/data; course-only; illustrative|
|A15|same paragraph|MCP does not determine grade meaning or verify source-data correctness.|D; scope/epistemic limit; primary protocol boundary; instructional|
|A16|same section, paragraph `В учебном примере преподаватель…`|A valid cell write is not evidence that a task was completed by a required date.|D; record/event distinction; course-only; synthetic example|
|A17|`Сценарий 2: проверка вывода об активности`, figure caption `Событие изменения…`|System change, work result, criterion check, and grade are separate stages.|D; event/result/evaluation; course-only; instructional|
|A18|same heading, paragraph `Онтологическая проверка выясняет…`|Ontology/logic checks can expose errors but do not replace fact-checking against source.|D; epistemic dependency; course-only; instructional|
|A19|same heading, paragraph `Рассмотрим утверждение…`|System-operation event is distinct from task result; criterion check links result to task; grade records evaluation.|D; event/result/assessment; course-only; simulated claim|
|A20|same paragraph|A later system event does not by itself establish completion by an earlier date or link event to assignment.|D; temporal/provenance; course-only; simulated claim|
|A21|same section, paragraph `Навык greek-scholastic…`|Concept/type clarification precedes checking premises and confidence; valid form alone does not establish true premises.|D; reasoning/evidence; course-only; instructional|
|A22|`Сценарий 3: от интервью…`, paragraph `Заказчик описал…`|Interview input describes intended application behavior while implementation remains unbuilt.|D; evidence/plan; course-only; hypothetical plan|
|A23|`Как уточнять неизвестное`, figure caption `Вопросы и ответы…`|Question-answer exchange clarifies requirements, then plan review may revise them.|D; elicitation/revision; course-only; instructional|
|A24|same heading, paragraph `Сократическое интервью…`|Answers refine the next question and yield roles/authority boundaries rather than code.|D; elicitation/requirements; course-only; illustrative|
|A25|`Как проверять план`, paragraph `Затем планировщик составляет…`|Planner/architect/critic review returns findings for plan revision; human checks them against interview; agreement is not proof.|D; review/provenance; course-only; workflow example|
|A26|`Данные и следующий уровень`, paragraph `Как применить дальше…`|Confirmed process steps are distinguished from assumptions; acceptance criteria are tied to observable results.|D; requirement/verification; course-only; instructional|

## Relation registry: `lecture2_student_guide.html` (L01–L78)

Rows are one relation assertion each. All are student-facing; values in examples are pedagogical examples, not universal ERP defaults. Course page is the immediate source; manual sections are cited but the inaccessible/local manual was not independently inspected.

|ID|Exact locator|Reusable relation claim|D/C/I/H; relation class; status/modality|
|---|---|---|---|
|L01|`Зачем ERP связывает эти данные`, opening paragraph|Shared reference data/documents connect planning, supply, execution, and cost accounting.|D; process/data linkage; course-only; instructional|
|L02|`Краткая схема производственной модели`, `pre` arrow/tree `Структура предприятия → Производственное подразделение`|Production subdivision is part of enterprise structure.|D; part-of; course-only; model|
|L03|same `pre`, `Рабочие центры → Вид рабочего центра`|Work-center type groups/organizes work centers.|D; grouping; course-only; model|
|L04|same `pre`, `Рабочие центры → Рабочий центр`|Work center is a production-model resource.|D; participation; course-only; model|
|L05|same `pre`, `Ресурсная спецификация`|Resource specification is a reusable normative model.|D; normative artifact; course-only; model|
|L06|same `pre`, `Заказ на производство`|Production order is a concrete production artifact.|D; plan artifact; course-only; model|
|L07|same `pre`, `График этапов и внутрицеховые задания`|Order stages are scheduled and dispatched through intershop/in-shop planning.|D; process/assignment; course-only; model|
|L08|same `pre`, `Документы учёта`|Accounting documents capture outcome/records.|D; record relation; course-only; model|
|L09|`Общие понятия`, row `ERP`|Shared data connects enterprise processes across departments.|D; data/process; course-only; example|
|L10|same table, row `Бизнес-процесс`|A process links work steps to an outcome.|D; process/result; course-only; example|
|L11|same table, row `Ресурс`|Work requires resources such as material, labor, equipment, or time.|D; requirement/dependency; course-only; definition/example|
|L12|same table, row `Материал`|Material is consumed or transformed during production.|D; transformation; course-only; definition|
|L13|same table, row `Продукция`|Process yields a product or completed work.|D; result; course-only; definition|
|L14|same table, row `Производство`|Production transforms materials/labor into product/work.|D; transformation; course-only; definition|
|L15|same table, row `Организация`|Organization is document/accounting entity; production shop is selected separately as subdivision.|D; organizational distinction; course-only; example|
|L16|same table, row `Подразделение`|Subdivision is a part of enterprise structure where work is organized.|D; part-of; course-only; definition|
|L17|`Данные для производства`, row `Документ`|Order specifies planned output; registered production result evidences actual manufacture.|D; plan/event distinction; course-only; instructional|
|L18|same table, row `Реквизит`|Document field can store a value or reference to another object.|D; attribute/reference; course-only; example|
|L19|same table, row `Таблица документа`|Document table rows enumerate homogeneous lines and are not separate documents.|D; containment/identity; course-only; definition|
|L20|same table, row `Характеристика номенклатуры`|Characteristic values distinguish a variant of an item.|D; identity/attribute; course-only; definition|
|L21|same table, row `Ресурсная спецификация`|Specification links result to stages/resources and supports planning and comparison with fact.|D; specification/dependency; course-only; model|
|L22|same table, row `Технологический процесс`|Reusable process template orders production operations.|D; sequence/template; course-only; definition|
|L23|same table, row `Полуфабрикат`|Intermediate product is used in making another product; it may be stocked or produced for an order.|D; input/result; course-only; alternatives|
|L24|same table, row `Рабочий центр (РЦ)`|Work center performs a production stage or operation.|D; execution assignment; course-only; definition|
|L25|same table, row `Вид рабочего центра (ВРЦ)`|Work-center type groups interchangeable centers under common planning rules.|D; grouping; course-only; definition|
|L26|same table, row `Этап производства`|Order stage holds planned and execution information and is scheduled.|D; document/schedule; course-only; definition|
|L27|same table, row `Производственная операция`|Production operation records a concrete execution of a technological operation.|D; norm/fact distinction; course-only; definition|
|L28|`Норма на примере полки`, `Ресурс — Нормативное количество` header row|Specification resource quantity is a per-unit norm.|D; norm/quantity; course-only; illustrative|
|L29|`Норма на примере полки`, paragraph `Для конкретного заказа…`|Order volume scales required quantity; post-execution comparison uses recorded consumption at same output quantity.|D; calculation/comparison; course-only; instructional|
|L30|`Норматив, план и факт`, row `Нормативные данные`|Specification states what/how to produce before work.|D; norm/process; course-only; model|
|L31|same table, row `Оперативные данные`|Order/stages show specific plan and production document captures outcome.|D; plan/fact; course-only; model|
|L32|same table, row `План`|Order stage specifies where and in what sequence to make product.|D; schedule/assignment; course-only; model|
|L33|same table, row `Факт`|Production receipt and consumption records evidence actual output/consumption.|D; record/fact; course-only; model|
|L34|same table, row `План-факт`|Comparison relates planned and actual times, volumes, and costs.|D; comparison; course-only; model|
|L35|`Три уровня планирования`, row `Предприятие — План продаж`|Sales plan estimates period sales volume and demand.|D; demand/planning; course-only; model|
|L36|same table, row `Предприятие — План производства`|Production plan sets product types/quantities for period to meet demand.|D; plan/demand; course-only; model|
|L37|same table, row `Межцеховой`|Intershop schedule places order stages by subdivision and time.|D; schedule/assignment; course-only; model|
|L38|same row|Chief dispatcher coordinates intershop schedule.|D; responsibility; course-only; model|
|L39|same table, row `Внутрицеховой`|In-shop task assigns work to concrete performers inside subdivision.|D; task/assignment; course-only; model|
|L40|same row|Local dispatcher distributes in-shop task.|D; responsibility; course-only; model|
|L41|`Три уровня планирования`, paragraph `Заказ на производство может…`|Order may originate from production plan or operational demand.|D; derivation; course-only; model|
|L42|same paragraph|Production program sets volume; schedule sets stage dates; tasks specify execution.|D; plan/schedule/execution distinction; course-only; instructional|
|L43|`Как диспетчер проверяет выполнимость`, row `Производственная мощность`|Resource capacity limits stages schedulable in an interval.|D; capacity/constraint; course-only; model|
|L44|same table, row `Доступность`|Work schedules/manual changes set available VRC/RC hours.|D; availability/constraint; course-only; example|
|L45|same table, row `Резерв доступности`|Reserved time is excluded from ordinary planning.|D; capacity/constraint; course-only; illustrative (5% not universal)|
|L46|same table, row `Коэффициент времени работы`|Work-center coefficient adjusts normative time; effect is checked in schedule.|D; calculation/dependency; course-only; illustrative|
|L47|same table, row `Обеспечение материалами`|Materials are supplied by stock, purchase, production, or transfer.|D; supply path; course-only; alternatives|
|L48|same table, row `Очередь заказов`|Order queue determines planned execution order using stated priority factors and release time.|D; sequence/priority; course-only; model|
|L49|same table, row `Приоритет`|Higher priority affects scheduling order when capacity is insufficient.|C; priority/constraint; course-only; conditional|
|L50|same table, row `Статус документа`|Document state changes responsibility/actions and may indicate preparation, release, or closure; output still requires registered result.|D; state/permission/evidence; course-only; model|
|L51|same table, row `Этапы не сформированы`|Missing stages prompt checking selected specification and order structure.|D; diagnostic/check; course-only; instructional|
|L52|same table, row `Материалов не хватает`|Shortage check compares available stock/expected receipts with stage demand.|D; diagnostic/dependency; course-only; instructional|
|L53|same table, row `Срок срывается`|Deadline risk prompts checking center availability, queue, and calculated dates.|D; diagnostic/dependency; course-only; instructional|
|L54|`Почему фактическая себестоимость отличается…`, row `Трудозатраты`|Normative labor time is compared with time registered during execution.|D; norm/fact comparison; course-only; model|
|L55|same table, row `Статья калькуляции`|Cost article classifies costs used in cost calculation.|D; classification; course-only; definition|
|L56|same table, row `Себестоимость`|Cost is monetary expression of production/work expenditures.|D; cost/result; course-only; definition|
|L57|same table, row `Плановая калькуляция`|Planned cost calculation monetizes specification resources.|D; calculation/input; course-only; model|
|L58|same table, row `Фактическая себестоимость`|Actual cost uses recorded consumption, labor, and output.|D; calculation/input; course-only; model|
|L59|same table, row `Перерасход материала`|Material-overuse hypothesis compares norm and actual consumption at equal output.|H; hypothesis/comparison; course-only; diagnostic|
|L60|same table, row `Больше трудозатрат`|Labor-overrun hypothesis compares normative time and registered labor.|H; hypothesis/comparison; course-only; diagnostic|
|L61|same table, row `Брак`|Scrap hypothesis compares resources, good output, and recorded losses.|H; hypothesis/comparison; course-only; diagnostic|
|L62|`Почему фактическая себестоимость отличается…`, paragraph `В этапе команда…`|Displayed norm beside current demand is not actual consumption; execution records evidence use.|D; UI data/fact distinction; course-only; instructional|
|L63|same heading, paragraph `Отклонение указывает…`|Variance motivates investigation but does not prove its cause.|D; evidence/hypothesis; course-only; instructional|
|L64|same paragraph|Investigation compares norm, plan, consumption, and output using stage/operation records.|D; comparison/evidence; course-only; instructional|
|L65|`Как та же модель применяется к ремонтам`, row `Техническое обслуживание (ТО)`|Maintenance supports equipment condition and prevents failure.|D; lifecycle/function; course-only; definition|
|L66|same table, row `Ремонт`|Repair restores operability after wear/failure.|D; lifecycle/function; course-only; definition|
|L67|same table, row `ТОиР`|Maintenance/repair subsystem moves rules and timing into work planning/execution.|D; process/model; course-only; definition|
|L68|same table, row `Объект эксплуатации`|Equipment object carries operating and repair information.|D; object/record; course-only; definition|
|L69|same table, row `Класс ОЭ`|Equipment class groups assets with common accounting/maintenance rules.|D; classification; course-only; definition|
|L70|same table, row `Ремонтный цикл`|Class card’s repair cycle orders repair types and intervals.|D; sequence/reference; course-only; definition|
|L71|same table, row `Вид ремонта`|Repair type normatively describes class service, duration, materials, and work.|D; specification; course-only; definition|
|L72|same table, row `Заказ на ремонт`|Repair order records decision, object, work, dates, and state.|D; planning/document; course-only; definition|
|L73|same table, row `Предмет работы`|Production concerns item/nomenclature; repair concerns equipment/operational object.|D; domain distinction; course-only; model|
|L74|same table, row `Норматив`|Repair type sets maintenance content; repair-work resource specification describes execution.|D; norm/specification; course-only; model|
|L75|same table, row `Конкретное поручение`|Repair order can link to production order for shop execution.|C; derivation/link; course-only; conditional|
|L76|same heading, `pre` arrow `Объект эксплуатации → класс → виды ремонта/ремонтный цикл`|Equipment object/class connect to repair types and cycle entries.|D; classification/reference; course-only; diagram/model|
|L77|same `pre`, `Планирование ремонтов → заказ на ремонт → заказ на производство`|Repair planning yields repair order and may yield production order.|D; derivation; course-only; diagram/model|
|L78|same section, paragraph `При ремонте силами…`|Production order uses repair-work specification; order creation is not completion evidence, which requires work/consumption records.|D; specification + plan/fact; course-only; conditional|

## Relation registry: `seminar2_production_case.html` (S01–S25)

|ID|Exact locator|Reusable relation claim|D/C/I/H; relation class; status/modality|
|---|---|---|---|
|S01|`Общие понятия`, row `Норматив`|Reusable rule/expected resource quantity applies to a typical job.|D; norm; course-only; definition|
|S02|same table, row `План`|Plan assigns concrete work, quantity, place, and time.|D; plan; course-only; definition|
|S03|same table, row `Факт`|Registered execution/consumption records actual work/output.|D; record/fact; course-only; definition|
|S04|same table, row `Отклонение`|Variance compares compatible expected and actual values at equal output/material/unit.|D; comparison; course-only; definition|
|S05|same table, row `Вид рабочего центра (ВРЦ)`|Work-center type groups interchangeable centers under common planning rules.|D; grouping; course-only; definition|
|S06|same table, row `Доступность`|Available work-center time constrains planning.|D; capacity/constraint; course-only; definition|
|S07|same table, row `Резерв доступности`|Some available time is reserved for unplanned work.|D; capacity/constraint; course-only; definition|
|S08|`1. Норма, план, факт или отклонение`, row `В спецификации полки…`|Specification resource amount is a normative per-unit value.|D; norm; course-only; synthetic example|
|S09|same section, row `Спецификация предусматривает…`|Specification labor time is a norm for a unit of product.|D; norm; course-only; synthetic example|
|S10|same section, row `У вида рабочего центра указан резерв…`|VRC reserve is a planning norm, not realized work.|D; norm/plan distinction; course-only; synthetic example|
|S11|same section, row `В заказе требуется изготовить…`|Order quantity is planned output, not actual output.|D; plan/fact distinction; course-only; synthetic example|
|S12|same section, row `Этап № 1 израсходовал…`|Recorded consumption is execution fact.|D; event/record; course-only; synthetic example|
|S13|same section, row `По этапу выпущено…`|Actual output is compared with planned output.|D; fact/plan; course-only; synthetic example|
|S14|same section, row `Фактическая себестоимость заказа…`|Actual-vs-planned cost difference is a variance requiring analysis.|D; comparison; course-only; synthetic example|
|S15|`2. Путь заказа`, row `Ресурсная спецификация`|Specification links product to materials, labor, and production stages.|D; specification/dependency; course-only; model|
|S16|same table, row `Заказ на производство`|Production order creates/organizes concrete output and production stages.|D; derivation/plan; course-only; model|
|S17|same table, row `Этап в спецификации`|Specification stage is normative process description.|D; norm; course-only; model|
|S18|same table, row `Этап производства`|Production stage is a concrete-order document with plan and execution data.|D; plan/fact; course-only; model|
|S19|same table, row `Технологическая операция`|Technological operation is normative action description.|D; norm; course-only; model|
|S20|same table, row `Производственная операция`|Production operation documents concrete execution of technological operation.|D; execution/record; course-only; model|
|S21|same table, row `Обеспечение`|Material provision determines source and due time for required materials.|D; supply/dependency; course-only; model|
|S22|same table, row `Выработка`|Registered performer output is used to account for labor.|D; record/accounting; course-only; model|
|S23|same section, step row `Создание заказа, формирование этапов и обеспечение материалами`|Order creation leads to stages and material provision before execution.|D; process/derivation; course-only; exercise model|
|S24|same section, step row `Регистрация расхода, выпуска и выработки`|Consumption, output, and labor registration record execution results.|D; event/record; course-only; exercise model|
|S25|`3. Разбор отклонения`, paragraph `Рассмотрите перерасход…`|Candidate causes (material, labor, scrap, norm error) require comparison evidence and remain hypotheses until checked.|H; hypothesis/evidence; course-only; exercise|

## Limits and motivated exclusions

- `ai_analyst_tools.html`: synthetic dialogue, mock reports, 1C activity totals, a demo grade, and project/app scenario are not real enterprise/student events. Excluded exact dates, counts, grade values, and UI navigation actions as instance data. Included only reusable source/evidence, permission, report-verification, event/result, and requirements relations. RPA is a vendor implementation example, not a universal technology guarantee. MCP’s 2026-07-28 primary spec validates protocol capabilities, not a course-specific read-match-write procedure or access rights.
- `lecture2_student_guide.html`: excluded standalone definitions and specific furniture/material quantities except rows expressly used to teach reusable norm/plan/fact relations. Specific coefficients, percentages, cost amounts, and names are illustrative. The page cites the 1C manual, but the manual was not independently read in this audit; claims remain course-only.
- `seminar2_production_case.html`: excluded synthetic IDs/values as facts; retained a few example rows only where the row explicitly teaches norm/plan/fact or variance relations. Repair interval example lacks last service/reference point, so the source does not establish that repair is due. The production-to-repair relation is analogy/conditional, not identity.
- No teacher-only content or inaccessible hidden behavior was audited. Relation totals count the listed source statements, not all conceivable atomic triples.
