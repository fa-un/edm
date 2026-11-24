# G003 source-statement registry — Practice analyses 1–2 and 3–6

Read-only fresh full pass through EOF on both HTML files. Registry unit is one explicit paragraph, labeled table row, or diagram arrow asserting a reusable ontology-relevant relation. Standalone definitions, generic UI steps, and specific synthetic instance values are excluded unless they teach a reusable relation. Distinct independent predicates in a paragraph are split; repeated source statements are counted again. Headings without HTML IDs are located by exact heading text, not invented anchors.

Legend: **D** direct source assertion; **C** case/context-specific; **I** inferred; **H** explicitly hypothetical. Source status for relation rows: **course-only** means the claim is stated in the derivative course page and is not independently established by the local citation. Modality/audience use plan, record, event; student. No relations below were independently sourced, inferred, or labeled hypothetical.

## `Практикумы №1–2 — разбор.html` — 19 rows

| # | Heading + exact row/paragraph/arrow locator | Faithful relation claim | D/C/I/H | Relation type | Source status | Modality / audience |
|---:|---|---|---|---|---|---|
| 1 | Opening paragraph, “Чтобы планировать выпуск…” | Production planning needs enabled production functions, a working calendar, and reference data for products/materials. | D | planning–prerequisites | course-only | plan / student |
| 2 | Same paragraph, “во втором создаём записи…” | The created product/material records are later selected in specifications and orders. | D | record–specification/order | course-only | plan / student |
| 3 | “Практикум № 1. Настройки производства” → “Задаваемые настройки”; row **Обособленное обеспечение при заказе в производство** | Material need is associated with the intended production output. | D | material need–production purpose | course-only | plan / student |
| 4 | Same table; row **Обособленное обеспечение при заказе в кладовую** | Stock is associated with its intended recipient. | D | stock–recipient | course-only | plan / student |
| 5 | Same table; row **Контроль выполнения операций (ОТК)** | Operation control can check a result and return the operation for rework. | D | operation–control/rework | course-only | event / student |
| 6 | Same table; row **Учёт трудозатрат в разрезе Физических лиц** | Labor effort is associated with individual performers. | D | labor effort–person | course-only | record / student |
| 7 | Same table; row **Учёт постатейных расходов по ОВЗ** | Cost information is analyzed by its cost-incurrence object/location. | D | cost–cost object | course-only | record / student |
| 8 | Same table; row **Производственный календарь** | Calendar dates determine working/non-working days and available time. | D | calendar–availability | course-only | plan / student |
| 9 | “Практикум № 2. Номенклатура и характеристики” → “Общие характеристики”; paragraph “Затем создаются шесть…” | Shared characteristics belong to item types and are available for selection on their items during accounting. | D | item type–characteristic–item | course-only | record / student |
| 10 | “Понятия раздела”; row **Производственная роль** | The resource specification, not the item name alone, clarifies its production role. | D | item–production role/specification | course-only | plan / student |
| 11 | “Свойства и допустимые значения”; row **Вид материала** | Property values are created for one item type and may be selected as shared characteristics for another. | D | property/value–item type | course-only | plan / student |
| 12 | Same table; row **Шпон** | The veneer property takes an existing nomenclature item as its value. | D | property–nomenclature value | course-only | plan / student |
| 13 | Same table; row **Использование защитного покрытия** | A Boolean property indicates whether protective coating is required. | D | property–Boolean value | course-only | record / student |
| 14 | Same heading; paragraph “Для «Шпона» значениями…” | Veneer values are references to nomenclature items; Boolean “Да/Нет” are primitive values, not separate records. | D | property value–record/primitive | course-only | record / student |
| 15 | “Как связаны записи”; paragraph “У дополнительного значения «Дуб»…” | A common characteristic stores a selected property value and is selected together with the nomenclature item. | D | characteristic–property value/item | course-only | record / student |
| 16 | Same heading; diagram arrow `реквизит-ссылка «Вид» → «Материалы с характеристиками»` | The “Доска” nomenclature record references the “Материалы с характеристиками” type. | D | nomenclature–item type | course-only | plan/record / student |
| 17 | Same diagram; arrow `свойство «Вид материала» → значения «Дуб», «Орех», «Сосна»` | The material-kind property links to its permitted values. | D | property–permitted value | course-only | plan/reference / student |
| 18 | “Организация и склад”; paragraph “В следующих заданиях…” | Materials and output are accounted for in the context of an organization and warehouse. | D | accounting–organization/warehouse | course-only | record / student |
| 19 | “Проверяемый результат”; final paragraph | Items are linked to item types; characteristics are available through those types and the resulting directories support specifications/orders. | D | item–type–characteristic–downstream use | course-only | plan/record / student |

## `Практикум №3–6 — разбор.html` — 23 rows

| # | Heading + exact row/paragraph/arrow locator | Faithful relation claim | D/C/I/H | Relation type | Source status | Modality / audience |
|---:|---|---|---|---|---|---|
| 1 | “Зачем создаются эти объекты”; paragraph “Чтобы планировать производство…” | Production planning needs departments where work occurs, capacity groups, workplaces, and their working time. | D | planning–organization/resources/time | course-only | plan / student |
| 2 | Same paragraph; “Настройки подразделения определяют…” | Department settings determine the depth/detail of work accounting. | D | department setting–accounting mode | course-only | plan / student |
| 3 | Same paragraph; “ВРЦ и РЦ позволяют…” | Work-center types and work centers distribute work by available capacity and help identify overload. | D | work–capacity/overload | course-only | plan / student |
| 4 | Same heading; paragraph “Практикумы № 3–6 последовательно…” | The model is prepared in sequence: department → work-center type → work center → availability. | D | object lifecycle/sequence | course-only | plan / student |
| 5 | `#practice-3` “Практикум № 3. Производственные подразделения”; opening paragraph | Three departments are subordinate to the existing production department; their modes are settings, not separate objects. | D | department–parent/settings | course-only | plan / student |
| 6 | Same section; paragraph “Разница между тремя записями…” | Order-based mode tracks an entire stage; operation-based mode tracks operations and their materials/output. | D | planning mode–tracking scope | course-only | plan / record / student |
| 7 | Same paragraph; clause “при регистрации операций работу распределяют…” | Operation registration distributes work across production areas and shift assignments. | D | operation registration–area/shift assignment | course-only | plan / event / student |
| 8 | `#practice-4` “Практикум № 4. Виды рабочих центров”; opening paragraph | Work-center types are assigned for departments and configured for capacity accounting and limits. | D | work-center type–department/capacity | course-only | plan / student |
| 9 | Same section; detailed-scheme paragraph “ВРЦ — отдельные записи, связанные с этим подразделением” under order-based department | Work-center-type records are associated with the order-based department. | D | work-center type–department | course-only | plan / record / student |
| 10 | Same section; corresponding paragraph under operation-based department | A work-center-type record is associated with the operation-based department. | D | work-center type–department | course-only | plan / record / student |
| 11 | Same section; corresponding paragraph under operation-registration department | A work-center-type record is associated with the operation-registration department. | D | work-center type–department | course-only | plan / record / student |
| 12 | `#practice-5` “Практикум № 5. Рабочие центры”; opening paragraph | For each work center, a type and time coefficient are selected; area and rates are set if required by the exercise. | D | work center–type/coefficient/area/rates | course-only | plan / record / student |
| 13 | Same section; detailed scheme, relation paragraph immediately before **Место столяра (позаказно) 1** | A work-center record has a reference field to its work-center type. | D | work center–type | course-only | plan/record / student |
| 14 | Same section; relation paragraph before **Место столяра (позаказно) 2** | A work-center record has a reference field to its work-center type. | D | work center–type | course-only | plan/record / student |
| 15 | Same section; relation paragraph before **Место столяра (пооперационно) 1** | A work-center record has a reference field to its work-center type. | D | work center–type | course-only | plan/record / student |
| 16 | Same section; relation paragraph before **Место столяра (пооперационно) 2** | A work-center record has a reference field to its work-center type. | D | work center–type | course-only | plan/record / student |
| 17 | Same section; relation paragraph before **Место столяра (регистрация операций) 1** | A work-center record has a reference field to its work-center type. | D | work center–type | course-only | plan/record / student |
| 18 | Same section; relation paragraph before **Место столяра (регистрация операций) 2** | A work-center record has a reference field to its work-center type. | D | work center–type | course-only | plan/record / student |
| 19 | Same section; table “Производственные участки — создаваемые записи”; row **Участок 1** | The named production area is selected on its corresponding work center. | C | production area–work center | course-only | plan/record / student |
| 20 | Same table; row **Участок 2** | The named production area is selected on its corresponding work center. | C | production area–work center | course-only | plan/record / student |
| 21 | `#practice-6` “Практикум № 6. Доступность рабочих центров”; opening paragraph | Availability is entered for a department and period; work-center-type availability may derive from group parameters while an individual center can have its own schedule. | D | availability–department/period/type/center | course-only | plan / student |
| 22 | Same section; paragraph “График рабочего центра — расписание…” | A center schedule maps availability to dates/intervals; without an individual schedule, the work-center-type or department schedule applies. | D | center–schedule inheritance | course-only | plan / student |
| 23 | “Результат практикумов № 3–6”; paragraph “В итоге система может сопоставить…” | The system compares planned work demand with available department/work-center capacity. | D | planned demand–available capacity | course-only | plan / student |

## Named method/model/metric/practice candidates

Four-way status: **1** verified against primary source; **2** secondary source only; **3** primary source unavailable; **4** mention does not define a verifiable method. FIFO status is deliberately narrow.

| File | Exact locator | Candidate | Status | Rationale / citation and access/version |
|---|---|---|---|---|
| `Практикумы №1–2 — разбор.html` | `#practice-2` “Практикум № 2. Номенклатура и характеристики” → “Понятия раздела”; row **ФИФО** | FIFO inventory cost formula | **1 — verified against primary source** | IFRS Foundation, *IAS 2 Inventories*, 2021 Issued IFRS Standards (Part A), ¶¶25–27, official PDF: [IAS 2 (2021)](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2021/issued/part-a/ias-2-inventories.pdf). Verified only as a cost formula for interchangeable inventories; this does **not** validate physical picking order or the course/1C configuration. |
| `Практикумы №1–2 — разбор.html` | `#practice-1` “Практикум № 1. Настройки производства” → “Понятия раздела”; row **Обособленное обеспечение** | Isolated material supply rule/practice | **2 — secondary source only** | The course page defines a named rule linking material need to order/recipient. It links the local educational manual `assets/mes.html`, “Управление производством и ремонтами в ERP”; no version/date or product-primary citation is stated on this page. |
| `Практикум №3–6 — разбор.html` | `#practice-3` → “Понятия раздела”; row **Позаказный режим** | Order-based planning mode | **2 — secondary source only** | Defined as planning whole stages by order without mandatory operation detail. Page cites local manual `assets/mes.html`, §§1.2.1–1.2.3; version/date and product-primary citation are not stated. |
| Same | Same table; row **Пооперационный режим** | Operation-based planning mode | **2 — secondary source only** | Defined as planning/accounting for individual operations inside a stage; local manual is the cited secondary source, without a stated version/date. |
| Same | Same table; row **Регистрация операций** | Operation-registration mode | **2 — secondary source only** | Defined as fixing operations by production areas and shift assignments; local manual is the cited secondary source, without a stated version/date. |
| Same | Same table; row **Коэффициент трудового участия (КТУ)** | Labor participation coefficient | **4 — mention does not define a verifiable method** | The page says it accounts for an employee’s contribution in output accounting, but provides no calculation method or verifiable source/version. |
| `Практикум №3–6 — разбор.html` | `#practice-4` → “Понятия раздела”; row **Пропускная способность** | Work-center capacity measure | **4 — mention does not define a verifiable method** | Defined broadly as volume of work per planning interval; no calculation method or versioned primary source is given. |
| Same | Same table; row **Резерв доступности** | Availability reserve measure | **4 — mention does not define a verifiable method** | Defined as a share of available time held free, but no verifiable calculation/application method is given. |
| `Практикум №3–6 — разбор.html` | `#practice-5` → “Понятия раздела”; row **Коэффициент времени работы** | Work-time coefficient | **4 — mention does not define a verifiable method** | Described as an adjustment to normative duration for a center, but no formula or primary source/version is supplied. |

**Candidate reconciliation:** Practice 1–2: 2 candidates; Practice 3–6: 7; **total 9 candidate rows**. FIFO is not counted as a candidate for validating production picking sequence/configuration.

## Motivated exclusions

- Practice 1–2: functional option, material analog, specification assignment, production set, technological operation, OTK, production calendar, cost object, nomenclature types/properties, characteristic templates, and accounting policy are respectively product features, data structures, organizational concepts, or configuration objects—not named methods taught as methods. Generic create/configure/check instructions are excluded.
- Practice 3–6: work-center schedule is a scheduling object/rule description, not a named method. Generic availability entries, planning horizons, sample capacities, dates, rates, and specific work-center assignments are configuration or synthetic values. “Normative” and resource specification are modeling/data constructs, not named methods in these files.
- The unresolved type for work center #3 is not asserted as a relation. Generic nested UI instructions and checks are excluded. The practice pages do not establish independent-primary support for their 1C-specific configuration claims.

## Reconciliation and scope

| File | Enumerated relation rows |
|---|---:|
| `Практикумы №1–2 — разбор.html` | 19 |
| `Практикум №3–6 — разбор.html` | 23 |
| **Total** | **42** |

These totals match the numbered rows in this artifact. This is only the two assigned practice-analysis pages, not the entire first-half HTML source set. No source HTML was edited.
