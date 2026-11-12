# AGENTS.md authoring guidelines

Source review date: 2026-10-28. English first; full Russian translation follows.

[English](#en) · [Русский перевод](#ru)

<a id="en"></a>
## English

### Purpose and evidence

This is a reference for designing skills that create or improve `AGENTS.md` files. It is not an installed skill or an instruction file to load automatically. A future skill should inspect the target project, select relevant guidance, and produce a small set of project-specific instructions. Do not copy this entire reference into every project.

The recommendations below synthesize primary documentation and first-party examples. Examples are illustrative, not commands or architecture requirements suitable for every project. The likelihood-and-impact policy is an agreed user decision policy, not a consensus attributed to the cited authors. No practice here guarantees an improvement for every project or model; effectiveness must be checked against representative tasks.

### Ten authoring principles

#### 1. Include information that changes decisions

**Why:** A useful rule supplies consequential context the agent might otherwise miss. Start with the project's purpose, authoritative entry points, and non-obvious constraints rather than generic exhortations. [OpenAI: review rules][O-review].

**Example:** “The response field `status` is consumed by supported older clients; preserve its meaning when changing the response.”

**Check:** Identify a plausible task where removing the rule would lead to a materially worse decision. If none exists, omit it or move explanatory background to a reference.

#### 2. Separate standing instructions from task state

**Why:** Stable project expectations belong in persistent guidance. The current request, temporary workarounds, progress, and historical observations have different lifetimes. [Z.ai: best practice][Z-practice] and [memory mechanism][Z-memory].

**Example:** “Use the issue's acceptance criteria for the current task. Store temporary investigation findings in its work notes.”

**Check:** A fresh session must not mistake a completed task or an old incident for a standing requirement. Promote a lesson into a rule only after establishing its continuing relevance.

#### 3. Scope instructions and load details when needed

**Why:** Specialized guidance should accompany the work it governs. File discovery, inheritance, overrides, and imports are properties of the agent client, not of the model provider alone. Check the intended client's documentation. [OpenAI: instruction discovery][O-discovery].

**Example:** “For schema changes, read the migration guide before preparing the migration.”

**Check:** Exercise a relevant task and an unrelated task. Confirm the necessary guidance is available without making every task load it. Do not assume a Markdown link automatically imports its target.

#### 4. Write an actionable rule with a clear boundary

**Why:** A condition and required action reduce ambiguity; an explicit safe path or valid exception prevents excessive restriction. Prefer concrete obligations over “be careful” or “write clean code.” [OpenAI: review rules][O-review] and [Z.ai: memory mechanism][Z-memory].

**Example:** “When changing a public response, preserve fields used by supported clients. Add a compatible field for new behavior; an intentional break follows the approved migration procedure.”

**Check:** A reader should be able to distinguish a violation, a permitted exception, and an unrelated change. Add a reason when it explains a non-obvious boundary.

#### 5. Give each fact one authoritative home

**Why:** Duplicated requirements drift. Keep the short obligation in the instruction file and detailed procedure or rationale in its owning document. Local instructions should not repeat the root's rules. [DeepSeek: documentation standard][D-docs].

**Example:** “Before changing stored record formats, follow the compatibility procedure in the persistence guide.”

**Check:** Verify that the reference exists, states the promised procedure, and does not conflict with the short rule. Avoid copied code and fragile line-number references when a stable document section or symbol is sufficient.

#### 6. Make verification reproducible

**Why:** Check names alone do not explain what they prove. Record the actual command, working directory, prerequisites, and relevant scope. Match evidence to the changed behavior. [DeepSeek: repository instructions][D-root].

**Example:** “For changes to this component, run `<verified component check>` from `<verified working directory>`. Record external prerequisites and any skipped checks.” Replace placeholders with inspected project facts before use.

**Check:** Confirm commands exist and exercise the stated behavior. Keep build, static analysis, behavioral tests, and live-system checks distinct. Select checks proportionately while preserving mandatory project requirements.

#### 7. Define completion through observable results

**Why:** A concrete outcome gives the agent a stopping criterion. Verification should remain capable of rejecting an incorrect change. Karpathy's research workflow illustrates an explicit objective and protected evaluation; this is a transferable lesson, not a general development standard. [Karpathy: program.md][K-program].

**Example:** “For this bug, demonstrate the reported failure and verify the expected behavior after the fix. Report checks that could not run.”

**Check:** Distinguish observed results, conclusions from inspection, and unverified assumptions. Do not weaken acceptance criteria merely to obtain a passing result. Change a test when its expected behavior is demonstrably obsolete, explaining why.

#### 8. Let tools enforce mechanical requirements

**Why:** Formatting and deterministic checks are better enforced by the relevant tools than by lengthy prose. Reserve instructions for how to invoke those checks and for judgments they cannot express. [HumanLayer][H-guide].

**Example:** “Use the configured formatter and linter; report remaining diagnostics relevant to the change.”

**Check:** Confirm the tool configuration and execution path exist. A prose prohibition alone does not enforce filesystem access, protect a branch, or prevent an unsafe operation; configure such controls in the execution environment where needed. [Z.ai: best practice][Z-practice].

#### 9. State autonomy and change boundaries precisely

**Why:** Instructions should allow authorized work to finish while identifying consequential actions that need a separate decision. Avoid requiring approval for each routine step or prescribing a large workflow for a trivial edit. Revisit boundaries when the client or model changes. [OpenAI: revisiting instructions][O-rethink].

**Example:** “Run relevant isolated checks and fix failures caused by the requested change. Publishing requires explicit authorization.” Use this only where those checks are actually isolated and that publication policy applies.

**Check:** The agent should complete permitted work and stop at the stated boundary. Prefer the smallest change that satisfies the request; do not infer permission for unrelated cleanup or speculative architecture. [Karpathy: simplicity criterion][K-program].

#### 10. Test and maintain the instructions themselves

**Why:** Guidance has maintenance cost. Keep rules that prevent meaningful mistakes, update stale ones, and narrow or retire instructions that cause noise. The number of rules is not a measure of quality. [OpenAI: revisiting instructions][O-rethink].

**Example:** “When a repeated failure motivates a rule, record the representative scenario used to validate it.”

**Check:** Use the evaluation method below. Do not universalize a fixed line budget, mandatory test-first workflow for every edit, or particular architecture. Uncle Bob's TDD discussion itself distinguishes significant behavior from cases where direct tests add little. [Uncle Bob: The Pragmatics of TDD][B-tdd].

### Compact structure and wording

Use only sections the project needs. The following is an outline, not a ready-to-run instruction file:

```markdown
# Project instructions

## Purpose and orientation
<Purpose and authoritative entry points.>

## Constraints and scope
<Non-obvious obligations, permissions, and applicable exceptions.>

## Verification
<Verified commands, working directories, prerequisites, and scope.>

## Completion
<Observable results and required reporting of incomplete checks.>

## Task-specific references
<When to read each document and what it governs.>
```

| Weak wording | More useful wording |
| --- | --- |
| “Read all documentation before every edit.” | “Read the deployment guide when preparing a deployment.” |
| “Write good tests.” | “For changed behavior, select a check that would fail for the original defect.” |
| “Always follow Clean Architecture.” | “Preserve this project's documented dependency direction; consult its architecture guide before changing that direction.” |
| “Fix every possible race.” | “Establish a reachable interleaving, then assess likelihood and impact separately.” |

These are original illustrative formulations. HumanLayer supports keeping onboarding concise and directing the agent to relevant details; the examples do not imply that its preferred file length is a universal optimum. [HumanLayer][H-guide].

### Likelihood and impact

**Status:** Agreed user policy for deciding what to recommend about discovered cases, including races. Apply it to findings, not as permission to change code.

Assess two independent dimensions:

- **Likelihood:** How plausibly the case occurs under actual usage, supported configurations, concurrency, load, retries, and existing protections. Explain the conditions and evidence rather than inventing percentages. Frequent means recurring or expected in ordinary supported operation; rare requires a reasoned explanation of the unusual conditions. Missing information means unknown.
- **Impact:** Consequences for data, security, essential operations, and users, including scale, duration, and reversibility. Explain which project obligation makes a consequence critical. A race is not automatically critical; a limited, reversible defect is not automatically harmless if it occurs often.

| Impact | Likelihood | Recommendation |
| --- | --- | --- |
| Critical, with a credible reachable scenario | Any credible likelihood, including low | Recommend a fix; low likelihood does not justify deferral. |
| Noncritical | High; recurring in supported operation | Recommend a fix. |
| Noncritical, with limited consequences | Low, supported by evidence | Document the case and explicitly inform the user. |
| Insufficient evidence to assess reachability, impact, or likelihood | Unknown or not established | State what is unknown and propose a targeted check; do not silently classify it as low risk. |

If a credible critical consequence is established, unknown frequency does not cancel the fix recommendation. If a case cannot be justified as one of the assessed rows, expose the uncertainty instead of forcing it into the defer row. Do not multiply ordinal scores in a way that lets low likelihood hide a critical consequence.

For a suspected race, describe the actors, shared state, relevant operation order, and the protection that is missing or insufficient. A concrete interleaving supported by code and execution semantics can establish a defect without a recorded production incident. An artificial stress test or deterministic reproducer establishes reachability, not production frequency. Conversely, failure to reproduce and absence of reported incidents do not prove low likelihood. If a verified invariant prevents the interleaving, explain why the finding does not apply.

Choose the smallest sufficient correction for a case recommended for repair. Fix cost and possible regressions inform the implementation choice but do not erase critical impact. A recommendation does not authorize changes outside the agreed task. Documenting a deferred issue does not mean it is fixed or that the user has silently accepted its risk.

For a documented case, record:

- scenario and triggering conditions;
- supporting evidence and remaining uncertainty;
- likelihood assessment and justification;
- consequences and impact assessment;
- recommendation and reason for deferral;
- available mitigation, if known, and conditions for reconsideration.

Show deferred findings to the user with this rationale; do not bury them in a file without mentioning them.

**Examples:**

1. A rare retry race can charge the same payment twice, violating a critical billing invariant: recommend a fix despite low likelihood.
2. Overlapping refreshes frequently display outdated information, requiring a user retry but causing no permanent loss: recommend a fix because it recurs.
3. An unusual timing combination causes a brief visual flicker that self-corrects, without data loss or blocked work: document it, explain the limited impact, and reconsider if frequency or consequences change.
4. A possible interleaving depends on unverified assumptions about concurrent writers: report the hypothesis and check those assumptions before assigning frequency. If critical harm is credible, prioritize that verification.

### Evaluate usefulness and maintain the guide

For a proposed rule, try a real violation, a valid exception, and an unrelated task. The desired result is appropriate action in the first case and no unnecessary intervention in the others. This three-case pattern is explicitly recommended for review rules by OpenAI. [OpenAI: review rules][O-review].

For a set of instructions, compare representative tasks with and without the proposed change under comparable model, client, permissions, repository state, and tool conditions. Where practical, repeat trials. Evaluate completed behavior and actual actions, not merely the agent's ability to repeat the instructions.

Record outcome correctness, unrelated modifications, avoidable clarification or approval stops, verification actually performed, and time or other measurable cost. Watch for regressions in tasks the new rule should not affect. A single successful run, shorter file, or lower token count does not establish better results. State which observations support retention of the rule and which remain untested.

A future authoring skill should locate existing instructions and their owners, verify project commands and client loading behavior, select applicable rules, check for conflicts, and present the resulting changes for the workflow's normal review. Keep evaluation examples and detailed rationale in supporting references so the generated `AGENTS.md` remains focused.

### Source notes and limits

| Source | Evidence type and useful contribution | Limit |
| --- | --- | --- |
| [OpenAI discovery][O-discovery], [review rules][O-review], [revisiting instructions][O-rethink] | Official documentation and guidance on loading, scoped rules, evaluation, and instruction maintenance. | Codex mechanics and model-specific advice are not universal client behavior. |
| [HumanLayer][H-guide] | Author's direct guidance on `CLAUDE.md`, explicitly extended to `AGENTS.md`. | Length and instruction-count suggestions are heuristics, not universal thresholds. |
| [Z.ai best practice][Z-practice], [memory mechanism][Z-memory] | Official educational guidance on task context, persistent rules, and separation of memory roles. | Verify descriptions of other clients against those clients' own documentation. |
| [DeepSeek documentation standard][D-docs], [repository instructions][D-root] | First-party repository examples of document ownership and verification policy. | Local budgets, commands, and architecture are not requirements for other projects. |
| [Karpathy program.md][K-program] | Author's working experimental protocol with a goal, evaluation, scope, and simplicity criterion. | Not a general `AGENTS.md` standard; do not import its indefinite loop or Git operations. Third-party “Karpathy guidelines” are not automatically his own text. |
| [Uncle Bob: The Pragmatics of TDD][B-tdd] | Author's engineering argument for testing significant code with contextual exceptions. | Application to instruction authoring is this guide's synthesis, not an author-issued `AGENTS.md` recipe. |

---

<a id="ru"></a>
## Русский перевод

### Назначение и основания

Это справочник для разработки навыков, которые создают или улучшают файлы `AGENTS.md`. Он не является установленным навыком или файлом инструкций для автоматической загрузки. Будущий навык должен изучить целевой проект, выбрать применимые рекомендации и составить небольшой набор инструкций для этого проекта. Не следует целиком копировать справочник в каждый проект.

Рекомендации ниже обобщают первичную документацию и примеры самих авторов и команд. Примеры иллюстративные: это не команды или архитектурные требования, подходящие любому проекту. Политика оценки вероятности и последствий согласована с пользователем и не приписывается всем перечисленным авторам. Ни одна практика здесь не гарантирует улучшения для любого проекта или модели; эффективность необходимо проверять на репрезентативных задачах.

### Десять принципов составления инструкций

#### 1. Включать информацию, которая меняет решения

**Зачем:** Полезное правило сообщает значимый контекст, который агент иначе мог бы упустить. Начинать следует с назначения проекта, основных источников истины и неочевидных ограничений, а не с общих призывов. [OpenAI: правила ревью][O-review].

**Пример:** «Поле ответа `status` используется поддерживаемыми старыми клиентами; при изменении ответа сохраняй его смысл».

**Проверка:** Найти правдоподобную задачу, в которой отсутствие правила привело бы к существенно худшему решению. Если такой задачи нет, исключить правило или перенести поясняющий контекст в справочную документацию.

#### 2. Отделять постоянные инструкции от состояния задачи

**Зачем:** Устойчивые требования проекта относятся к постоянным инструкциям. Текущий запрос, временные обходы, прогресс и исторические наблюдения имеют другой срок актуальности. [Z.ai: практические рекомендации][Z-practice] и [организация памяти][Z-memory].

**Пример:** «Для текущей задачи используй её критерии приёмки. Временные результаты расследования сохраняй в рабочих заметках этой задачи».

**Проверка:** Новая сессия не должна принимать завершённую задачу или старый инцидент за постоянное требование. Превращать наблюдение в правило следует только после подтверждения его дальнейшей применимости.

#### 3. Ограничивать область действия и подключать подробности по необходимости

**Зачем:** Специализированные инструкции должны сопровождать ту работу, к которой относятся. Обнаружение файлов, наследование, переопределения и импорты определяются клиентом агента, а не только поставщиком модели. Нужно проверять документацию выбранного клиента. [OpenAI: загрузка инструкций][O-discovery].

**Пример:** «При изменении схемы данных прочитай руководство по миграциям до подготовки миграции».

**Проверка:** Выполнить относящуюся к правилу и постороннюю задачу. Убедиться, что нужные инструкции доступны, но их чтение не навязано каждой задаче. Не считать, что Markdown-ссылка автоматически импортирует целевой документ.

#### 4. Формулировать выполнимое правило с понятными границами

**Зачем:** Условие и требуемое действие уменьшают неоднозначность; явно описанный допустимый путь или исключение предотвращает чрезмерные ограничения. Предпочитать конкретные обязательства пожеланиям «будь осторожен» и «пиши чистый код». [OpenAI: правила ревью][O-review] и [Z.ai: организация памяти][Z-memory].

**Пример:** «При изменении публичного ответа сохраняй поля, используемые поддерживаемыми клиентами. Для нового поведения добавляй совместимое поле; намеренное несовместимое изменение проходит согласованную процедуру миграции».

**Проверка:** Читатель должен отличать нарушение, допустимое исключение и постороннее изменение. Добавлять причину, когда она объясняет неочевидное ограничение.

#### 5. Хранить каждый факт в одном основном источнике

**Зачем:** Дублируемые требования расходятся. Короткое обязательство должно оставаться в файле инструкций, а подробная процедура или обоснование — в документе, отвечающем за эту тему. Локальные инструкции не должны повторять правила корня. [DeepSeek: стандарт документации][D-docs].

**Пример:** «Перед изменением форматов сохраняемых записей выполни процедуру проверки совместимости из руководства по хранению данных».

**Проверка:** Убедиться, что ссылка существует, содержит обещанную процедуру и не противоречит короткому правилу. Не копировать код и не использовать хрупкие ссылки на номера строк, когда достаточно устойчивого раздела документа или символа.

#### 6. Делать проверки воспроизводимыми

**Зачем:** Одно название проверки не объясняет, что она доказывает. Указывать реальную команду, рабочий каталог, предусловия и соответствующий охват. Подбирать доказательства под изменённое поведение. [DeepSeek: инструкции репозитория][D-root].

**Пример:** «При изменениях этого компонента запускай `<проверенная команда для компонента>` из `<проверенный рабочий каталог>`. Укажи внешние предусловия и пропущенные проверки». Перед применением заменить условные обозначения подтверждёнными фактами проекта.

**Проверка:** Убедиться, что команды существуют и проверяют заявленное поведение. Различать сборку, статический анализ, поведенческие тесты и проверки работающей системы. Выбирать соразмерные проверки, сохраняя обязательные требования проекта.

#### 7. Определять завершение через наблюдаемый результат

**Зачем:** Конкретный результат задаёт критерий остановки. Проверка должна сохранять способность отклонить неверное изменение. Исследовательский процесс Карпати показывает явную цель и защищённую оценку результата; это переносимый принцип, а не общий стандарт разработки. [Karpathy: program.md][K-program].

**Пример:** «Для этого бага продемонстрируй описанный сбой и проверь ожидаемое поведение после исправления. Сообщи о проверках, которые не удалось выполнить».

**Проверка:** Различать наблюдаемые результаты, выводы по исходникам и непроверенные предположения. Не ослаблять критерии приёмки ради успешного результата. Менять тест, если доказано, что его ожидаемое поведение устарело, и объяснять причину.

#### 8. Обеспечивать механические требования инструментами

**Зачем:** Форматирование и детерминированные проверки лучше обеспечивать соответствующими инструментами, чем длинными текстовыми правилами. В инструкциях описывать запуск этих проверок и решения, которые они не способны выразить. [HumanLayer][H-guide].

**Пример:** «Используй настроенные форматтер и линтер; сообщи об оставшихся диагностических сообщениях, относящихся к изменению».

**Проверка:** Убедиться, что конфигурация и способ запуска инструмента существуют. Сам по себе текстовый запрет не ограничивает доступ к файловой системе, не защищает ветку и не предотвращает опасную операцию; при необходимости такие ограничения настраиваются в среде выполнения. [Z.ai: практические рекомендации][Z-practice].

#### 9. Точно задавать границы самостоятельности и изменений

**Зачем:** Инструкции должны позволять завершить разрешённую работу и обозначать значимые действия, требующие отдельного решения. Не требовать согласования каждого обычного шага и не навязывать большой процесс тривиальной правке. Пересматривать границы при смене клиента или модели. [OpenAI: пересмотр инструкций][O-rethink].

**Пример:** «Запускай относящиеся к задаче изолированные проверки и исправляй сбои, вызванные запрошенным изменением. Публикация требует явного разрешения». Использовать такую формулировку только при реальной изолированности проверок и соответствующей политике публикации.

**Проверка:** Агент должен завершать разрешённую работу и останавливаться на указанной границе. Предпочитать минимальное изменение, достаточное для выполнения запроса; не считать разрешёнными посторонний клинап и архитектуру про запас. [Karpathy: критерий простоты][K-program].

#### 10. Проверять и сопровождать сами инструкции

**Зачем:** Инструкции требуют сопровождения. Сохранять правила, предотвращающие значимые ошибки, обновлять устаревшие, сужать или исключать создающие шум. Количество правил не является показателем качества. [OpenAI: пересмотр инструкций][O-rethink].

**Пример:** «Если повторяющаяся ошибка стала причиной нового правила, зафиксируй репрезентативный сценарий, на котором проверена его полезность».

**Проверка:** Использовать описанный ниже способ оценки. Не превращать фиксированный лимит строк, обязательный test-first для каждой правки или конкретную архитектуру в универсальное требование. Сам Uncle Bob в обсуждении TDD различает значимое поведение и случаи, где прямые тесты дают мало пользы. [Uncle Bob: The Pragmatics of TDD][B-tdd].

### Компактная структура и формулировки

Включать только необходимые проекту разделы. Ниже структура, а не готовый к применению файл инструкций:

```markdown
# Инструкции проекта

## Назначение и ориентиры
<Назначение проекта и основные источники истины.>

## Ограничения и область действия
<Неочевидные обязательства, разрешения и применимые исключения.>

## Проверки
<Проверенные команды, рабочие каталоги, предусловия и охват.>

## Завершение
<Наблюдаемые результаты и сообщение о невыполненных проверках.>

## Документы для отдельных задач
<Когда читать каждый документ и что он регулирует.>
```

| Неудачная формулировка | Более полезная формулировка |
| --- | --- |
| «Читай всю документацию перед каждой правкой». | «Читай руководство по развёртыванию при подготовке развёртывания». |
| «Пиши хорошие тесты». | «Для изменённого поведения выбирай проверку, которая обнаружила бы исходный дефект». |
| «Всегда следуй Clean Architecture». | «Сохраняй документированное направление зависимостей проекта; перед его изменением обратись к архитектурному руководству». |
| «Исправляй каждую возможную гонку». | «Установи достижимое чередование операций, затем отдельно оцени вероятность и тяжесть последствий». |

Это собственные иллюстративные формулировки. HumanLayer рекомендует краткое введение в проект и ссылки на необходимые подробности; примеры не означают, что предпочитаемый автором размер файла является универсальным оптимумом. [HumanLayer][H-guide].

### Вероятность и тяжесть последствий

**Статус:** Согласованная с пользователем политика выбора рекомендаций по найденным случаям, включая гонки состояний. Применять её к замечаниям, не трактуя как разрешение менять код.

Оценивать две независимые характеристики:

- **Вероятность:** Насколько правдоподобно возникновение случая при реальном использовании, поддерживаемых настройках, параллельной работе, нагрузке, повторах и существующих защитах. Объяснять условия и доказательства, не выдумывать проценты. Частый случай повторяется или ожидается в обычной поддерживаемой эксплуатации; редкость требует обоснования необычных условий. Отсутствие информации означает неизвестность.
- **Тяжесть последствий:** Влияние на данные, безопасность, основные операции и пользователей с учётом масштаба, продолжительности и обратимости. Объяснять, какое обязательство проекта делает последствия критичными. Гонка не является критичной автоматически; ограниченный обратимый дефект не становится безвредным автоматически, если возникает часто.

| Последствия | Вероятность | Рекомендация |
| --- | --- | --- |
| Критичные, при обоснованном достижимом сценарии | Любая обоснованная, включая низкую | Рекомендовать исправление; низкая вероятность не оправдывает отсрочку. |
| Некритичные | Высокая; случай повторяется при поддерживаемой эксплуатации | Рекомендовать исправление. |
| Некритичные, с ограниченными последствиями | Низкая, подтверждённая аргументами | Документировать случай и явно сообщить пользователю. |
| Недостаточно доказательств для оценки достижимости, последствий или вероятности | Неизвестна или не установлена | Указать неизвестное и предложить прицельную проверку; не относить молча к низкому риску. |

Если обоснованы критичные последствия, неизвестная частота не отменяет рекомендацию исправить. Если случай нельзя обоснованно отнести к одной из оценённых строк, показать неопределённость, а не принудительно относить его к отсрочке. Не перемножать порядковые оценки так, чтобы низкая вероятность скрывала критичные последствия.

Для предполагаемой гонки описать участников, общее состояние, существенный порядок операций и отсутствующую либо недостаточную защиту. Конкретное чередование операций, подтверждённое кодом и семантикой выполнения, может установить дефект без зарегистрированного инцидента в рабочей системе. Искусственный нагрузочный тест или детерминированный воспроизводитель подтверждает достижимость, но не частоту в эксплуатации. И наоборот: неудача воспроизведения и отсутствие сообщений об инцидентах не доказывают низкую вероятность. Если проверенный инвариант исключает такое чередование, объяснить, почему замечание неприменимо.

Для случая, рекомендованного к исправлению, выбирать минимальное достаточное решение. Стоимость исправления и возможные регрессии влияют на способ реализации, но не отменяют критичности последствий. Рекомендация не разрешает изменения за пределами согласованной задачи. Документирование отложенной проблемы не означает, что она исправлена или пользователь молча принял её риск.

Для документируемого случая фиксировать:

- сценарий и условия возникновения;
- подтверждающие данные и оставшуюся неопределённость;
- оценку вероятности и обоснование;
- последствия и оценку их тяжести;
- рекомендацию и причину отсрочки;
- известный способ снижения риска, если он есть, и условия пересмотра решения.

Показывать отложенные замечания пользователю вместе с этим обоснованием; не прятать их в файле без упоминания.

**Примеры:**

1. Редкая гонка при повторе может провести один платёж дважды, нарушая критичный инвариант биллинга: рекомендовать исправление несмотря на низкую вероятность.
2. Пересекающиеся обновления часто показывают устаревшую информацию, требуя повтора от пользователя, но не приводя к постоянной потере данных: рекомендовать исправление из-за повторяемости.
3. Необычное сочетание таймингов вызывает краткое мерцание интерфейса, которое само устраняется без потери данных и блокировки работы: документировать, объяснить ограниченные последствия и пересмотреть решение при изменении частоты или последствий.
4. Возможное чередование операций зависит от непроверенных предположений о параллельных записях: сообщить о гипотезе и проверить эти предположения до назначения частоты. Если критичный ущерб правдоподобен, приоритизировать эту проверку.

### Проверка полезности и сопровождение справочника

Для предлагаемого правила проверить реальное нарушение, допустимое исключение и постороннюю задачу. Ожидаемый результат — нужное действие в первом случае и отсутствие лишнего вмешательства в остальных. OpenAI явно рекомендует такую тройку сценариев для правил ревью. [OpenAI: правила ревью][O-review].

Для набора инструкций сравнивать репрезентативные задачи с предлагаемым изменением и без него при сопоставимых модели, клиенте, разрешениях, состоянии репозитория и инструментах. Где практически возможно, повторять прогоны. Оценивать итоговое поведение и реальные действия, а не только способность агента пересказать инструкции.

Фиксировать правильность результата, посторонние изменения, лишние остановки для уточнений или согласований, фактически выполненные проверки, время или другие измеримые затраты. Отслеживать ухудшения в задачах, на которые новое правило не должно влиять. Один удачный запуск, более короткий файл или меньшее число токенов не доказывают улучшения. Указывать, какие наблюдения обосновывают сохранение правила, а что остаётся непроверенным.

Будущий навык составления инструкций должен находить существующие инструкции и ответственных за них, проверять команды проекта и загрузку файлов клиентом, выбирать применимые правила, искать противоречия и предоставлять изменения для предусмотренного рабочим процессом ревью. Примеры для оценки и подробные обоснования следует хранить во вспомогательных документах, чтобы создаваемый `AGENTS.md` оставался сосредоточенным на необходимом.

### Источники и границы выводов

| Источник | Тип подтверждения и полезный вклад | Ограничение |
| --- | --- | --- |
| [OpenAI: загрузка инструкций][O-discovery], [правила ревью][O-review], [пересмотр инструкций][O-rethink] | Официальные документы и рекомендации по загрузке, области действия правил, оценке и сопровождению инструкций. | Механика Codex и советы для конкретных моделей не определяют поведение всех клиентов. |
| [HumanLayer][H-guide] | Прямые рекомендации автора по `CLAUDE.md`, явно распространённые на `AGENTS.md`. | Предложения по длине и количеству инструкций являются эвристиками, а не универсальными порогами. |
| [Z.ai: практические рекомендации][Z-practice], [организация памяти][Z-memory] | Официальные обучающие материалы о контексте задачи, постоянных правилах и разделении назначения памяти. | Описания других клиентов нужно сверять с собственной документацией этих клиентов. |
| [DeepSeek: стандарт документации][D-docs], [инструкции репозитория][D-root] | Примеры собственного репозитория команды о распределении ответственности между документами и политике проверок. | Локальные бюджеты, команды и архитектура не являются требованиями к другим проектам. |
| [Karpathy: program.md][K-program] | Рабочий экспериментальный протокол автора с целью, оценкой, областью изменений и критерием простоты. | Это не общий стандарт `AGENTS.md`; не переносить его бесконечный цикл и Git-операции. Чужие «правила Карпати» не становятся его авторским текстом автоматически. |
| [Uncle Bob: The Pragmatics of TDD][B-tdd] | Авторское инженерное обоснование тестирования значимого кода с учётом контекстных исключений. | Применение к составлению инструкций — обобщение этого справочника, а не выпущенный автором рецепт `AGENTS.md`. |

[O-discovery]: https://learn.chatgpt.com/docs/agent-configuration/agents-md
[O-review]: https://developers.openai.com/blog/custom-code-review-rules-for-codex
[O-rethink]: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
[H-guide]: https://www.humanlayer.dev/blog/writing-a-good-claude-md
[Z-practice]: https://docs.z.ai/devpack/resources/best-practice
[Z-memory]: https://docs.z.ai/devpack/resources/memory-mechanism
[D-docs]: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/AGENTS.md
[D-root]: https://github.com/deepseek-ai/deepseek-harness/blob/master/AGENTS.md
[K-program]: https://github.com/karpathy/autoresearch/blob/master/program.md
[B-tdd]: https://blog.cleancoder.com/uncle-bob/2013/03/06/ThePragmaticsOfTDD.html
