# RU AEC Skills

48 скиллов для помощи ИИ-агенту в архитектурно-строительном и инженерном проектировании в Российской Федерации: нормативная основа, исходные данные, расчётные процессы, BIM/CAD-координация, проверка и выпуск документации.

Это текстовые рабочие инструкции, а не расчётная программа, библиотека семейств или плагин управления Revit. Для работы с моделью агенту отдельно нужны доступ к приложению и подходящие инструменты. Наличие скилла не предоставляет этот доступ.

## Важно: возможны ошибки

**Скиллы и ответы ИИ могут содержать ошибки, пропуски и устаревшие сведения. Соответствие нормам, полнота расчётов и безопасность решений не гарантируются.**

- Проверяйте исходные данные, единицы, формулы, применимость методики и результаты. Для значимых решений нужна проверка компетентным специалистом.
- Редакцию нормы, изменения, дату действия и основание применения конкретного пункта устанавливают для каждого проекта. Пометка «действует» не означает обязательность всего документа.
- Предварительные оценки не являются окончательным подбором или документацией для строительства. Скиллы не заменяют ответственных проектировщиков, согласования и экспертизу.
- Перед изменением рабочих моделей и документов сохраняйте восстановимую копию. Проверяйте фактический результат, а не только сообщение агента об успехе.
- Набор не охватывает все разделы и типы объектов; например, полного комплекта расчётов несущих конструкций здесь нет.

## Установка

Пошаговые варианты для **Codex, Claude Code, Claude Desktop, Gemini CLI, Qwen Code, Qwen Desktop, Antigravity, Cherry Studio, AnythingLLM и других клиентов** — в [INSTALL.md](INSTALL.md). Для агентов с нативными скиллами используются папки скиллов; для чат-клиентов предусмотрен отдельный способ подключения выбранных инструкций. Модель и приложение — не одно и то же: выбор Gemini или Qwen в чате сам по себе не включает механизм скиллов.

### Через Codex

Если доступен встроенный `skill-installer`, отправьте ему:

```text
$skill-installer Установи все 48 скиллов из репозитория
https://github.com/proovcme/ru-aec-skills
Каждая папка верхнего уровня с SKILL.md — отдельный скилл.
Сохрани их рядом, вместе с references и agents.
При совпадении с уже установленными папками сначала покажи конфликт;
не перезаписывай мои изменения.
```

Не устанавливайте корень репозитория как один скилл. Установщик вашей версии Codex определяет пользовательский каталог установки. После установки проверьте доступность скиллов; если изменения не появились, перезапустите Codex.

### Вручную, для одного проекта

1. Скачайте репозиторий через **Code → Download ZIP** и распакуйте либо выполните в отдельной рабочей папке:

   ```sh
   git clone https://github.com/proovcme/ru-aec-skills.git
   ```

2. В своём проекте создайте `.agents/skills` и скопируйте туда **все 48 папок с `SKILL.md`**, включая их содержимое. Не копируйте `.git`. Перед заменой существующих одноимённых папок сохраните их отдельно и сравните изменения.
3. Итоговый путь должен иметь вид `.agents/skills/hvac-define-design-basis/SKILL.md`, а не `.agents/skills/ru-aec-skills/hvac-define-design-basis/SKILL.md`.
4. Откройте проект в Codex и проверьте, что нужный скилл доступен. Не держите разные версии одного скилла одновременно в проектном и пользовательском каталогах.

Проектное размещение и способы вызова описаны в [официальной документации по скиллам](https://learn.chatgpt.com/docs/build-skills). Для другого ИИ-агента используйте поддерживаемый им каталог и механизм загрузки; совместимость не предполагается автоматически.

### Зависимости и обновление

В скиллах есть относительные ссылки на общие процедуры соседних папок. Полная установка сохраняет эти зависимости. При выборочной установке перенесите также все транзитивные зависимости по локальным ссылкам; не ограничивайтесь одним `SKILL.md`.

Для обновления получите новую версию в отдельную папку, сравните её с установленной и сохраните собственные правки. Обновляйте связанные скиллы согласованно; `git pull` в скачанном репозитории сам по себе не обновляет ранее скопированные папки. Для воспроизводимой работы фиксируйте SHA коммита используемой версии.

## Как пользоваться

Выберите конкретную задачу, приложите относящиеся к ней исходные данные и укажите границы действий: объяснить, проверить или изменить. Не просите загружать весь комплект для каждой задачи.

Примеры явного вызова в Codex:

```text
$aec-review-design-usability Проверь планировку: двери, проходы,
рабочие места и обслуживание. Модель пока не изменяй.

$hvac-calculate-duct-networks Проверь заданную ветвь по приложенной
таблице. Покажи единицы и потери давления; неизвестное не выдумывай.

$aec-develop-rf-design-documentation Проверь состав выдачи РД
и согласованность планов, спецификаций и модели.

$operate-autocad-via-bimwright Оформи лист в нативном DWG через MCP.
До изменений проверь target, активный файл и доступность нужных tools.
```

Общий маршрут содержит [правила поиска нормативов и проверки их статуса](aec-govern-rf-capital-project/references/normative-workflow.md). Состав стадий, СПДС и ТИМ раскрываются через [подготовку проектной документации](aec-develop-rf-design-documentation/SKILL.md). Эти процедуры подключаются по задаче, а не требуют полного аудита для отдельной арифметической проверки.

## Реестр скиллов

Описания ниже обозначают назначение инструкций, а не гарантию автономного выполнения. Точная область применения указана в соответствующем `SKILL.md`.

### Проектный процесс, АР и строительство — 9

| Скилл | Назначение |
| --- | --- |
| [aec-govern-rf-capital-project](aec-govern-rf-capital-project/SKILL.md) | Жизненный цикл, контрольные этапы, ответственность и нормативный маршрут. |
| [aec-define-rf-compliance-path](aec-define-rf-compliance-path/SKILL.md) | Классификация объекта и применимость обязательных процедур. |
| [aec-collect-rf-initial-permits](aec-collect-rf-initial-permits/SKILL.md) | Исходно-разрешительная документация, ограничения и технические условия. |
| [aec-manage-rf-engineering-surveys](aec-manage-rf-engineering-surveys/SKILL.md) | Задание, достаточность и приёмка инженерных изысканий. |
| [aec-develop-rf-design-documentation](aec-develop-rf-design-documentation/SKILL.md) | Состав ПД и РД, ПП №87, СПДС, ТИМ, координация и ревизии. |
| [aec-pass-rf-expertise-and-permits](aec-pass-rf-expertise-and-permits/SKILL.md) | Экспертиза, замечания и разрешение на строительство. |
| [aec-control-rf-construction](aec-control-rf-construction/SKILL.md) | Контроль строительства, несоответствия и изменения на площадке. |
| [aec-manage-rf-executive-records](aec-manage-rf-executive-records/SKILL.md) | Исполнительные схемы, акты, журналы и подтверждающие записи. |
| [aec-review-design-usability](aec-review-design-usability/SKILL.md) | Эргономика, двери, маршруты, обслуживание и реализуемость планировки. |

### Оформление и AutoCAD — 2

| Скилл | Назначение |
| --- | --- |
| [apply-eskd-spds-to-drawings](apply-eskd-spds-to-drawings/SKILL.md) | Выбор ЕСКД/СПДС, актуальная нормативная база, формы, УГО и CAD-нормоконтроль. |
| [operate-autocad-via-bimwright](operate-autocad-via-bimwright/SKILL.md) | Безопасное создание и проверка нативных DWG через `bimwright/dwg-mcp`, включая блоки и листы. |

### Отопление, вентиляция и кондиционирование — 14

| Скилл | Назначение |
| --- | --- |
| [hvac-define-design-basis](hvac-define-design-basis/SKILL.md) | Исходные данные, границы и нормативная основа ОВ. |
| [hvac-select-system-strategy](hvac-select-system-strategy/SKILL.md) | Сравнение концепций отопления, вентиляции и кондиционирования. |
| [hvac-calculate-heating-loads](hvac-calculate-heating-loads/SKILL.md) | Теплопотери и расчётные нагрузки отопления. |
| [hvac-design-hydronic-heating](hvac-design-hydronic-heating/SKILL.md) | Водяное отопление, приборы, гидравлические контуры и регулирование. |
| [hvac-calculate-room-airflows](hvac-calculate-room-airflows/SKILL.md) | Воздухообмен помещений и воздушный баланс. |
| [hvac-design-general-ventilation](hvac-design-general-ventilation/SKILL.md) | Общеобменные системы, воздухораспределение и трассировка. |
| [hvac-design-industrial-ventilation](hvac-design-industrial-ventilation/SKILL.md) | Местные отсосы и вентиляция производств и складов. |
| [hvac-design-parking-ventilation](hvac-design-parking-ventilation/SKILL.md) | Общеобменная вентиляция закрытых автостоянок. |
| [hvac-calculate-duct-networks](hvac-calculate-duct-networks/SKILL.md) | Сечения, скорости, аэродинамика и балансировка воздуховодов. |
| [hvac-select-ventilation-equipment](hvac-select-ventilation-equipment/SKILL.md) | Проверка подбора установок, вентиляторов, секций, шумоглушителей и завес. |
| [hvac-design-smoke-exhaust](hvac-design-smoke-exhaust/SKILL.md) | Сценарии вытяжной противодымной вентиляции и компенсация. |
| [hvac-design-pressurization](hvac-design-pressurization/SKILL.md) | Противодымный подпор, утечки, давления и открывание дверей. |
| [hvac-coordinate-bim](hvac-coordinate-bim/SKILL.md) | BIM-координация ОВ, узлы, проходки и зоны обслуживания. |
| [hvac-issue-rf-documentation](hvac-issue-rf-documentation/SKILL.md) | Планы, схемы, расчёты, спецификации и выпуск ОВ. |

### Водоснабжение и канализация — 10

| Скилл | Назначение |
| --- | --- |
| [plumbing-define-design-basis](plumbing-define-design-basis/SKILL.md) | Исходные данные и границы систем ВК. |
| [plumbing-calculate-demand-and-balance](plumbing-calculate-demand-and-balance/SKILL.md) | Расходы воды, стоков и водный баланс. |
| [plumbing-design-water-supply](plumbing-design-water-supply/SKILL.md) | Холодное и технологическое водоснабжение, зонирование и давление. |
| [plumbing-design-hot-water-circulation](plumbing-design-hot-water-circulation/SKILL.md) | ГВС, циркуляция, температурный режим и тепловой баланс. |
| [plumbing-design-drainage](plumbing-design-drainage/SKILL.md) | Канализация, конденсат, уклоны, вентиляция сети и насосный отвод. |
| [plumbing-design-rainwater-drainage](plumbing-design-rainwater-drainage/SKILL.md) | Внутренние водостоки, воронки и аварийный перелив. |
| [plumbing-design-fire-water](plumbing-design-fire-water/SKILL.md) | Внутренний пожарный водопровод, обеспеченность и гидравлическая основа. |
| [plumbing-size-and-select-equipment](plumbing-size-and-select-equipment/SKILL.md) | Гидравлические размеры, насосы, баки, счётчики и арматура. |
| [plumbing-coordinate-bim](plumbing-coordinate-bim/SKILL.md) | BIM-координация ВК, отметки, проходки и задания смежникам. |
| [plumbing-issue-design-deliverables](plumbing-issue-design-deliverables/SKILL.md) | Согласованный выпуск расчётов, планов, схем и ведомостей ВК. |

### Электроснабжение и освещение — 5

| Скилл | Назначение |
| --- | --- |
| [electrical-define-design-basis](electrical-define-design-basis/SKILL.md) | Основа ЭОМ, ТУ, надёжность и резервирование. |
| [electrical-calculate-loads-and-circuits](electrical-calculate-loads-and-circuits/SKILL.md) | Нагрузки, токи, выбор кабелей и проверка защиты. |
| [electrical-design-lighting](electrical-design-lighting/SKILL.md) | Рабочее и аварийное освещение, фотометрия и управление. |
| [electrical-design-earthing-and-lightning](electrical-design-earthing-and-lightning/SKILL.md) | Заземление, уравнивание потенциалов, молниезащита и УЗИП. |
| [electrical-coordinate-bim](electrical-coordinate-bim/SKILL.md) | Щиты, цепи, кабельные трассы и координация ЭОМ. |

### Пожарная безопасность и совместный выпуск — 5

| Скилл | Назначение |
| --- | --- |
| [fire-define-design-basis](fire-define-design-basis/SKILL.md) | Пожарная концепция и необходимость систем защиты. |
| [fire-check-egress-and-compartmentation](fire-check-egress-and-compartmentation/SKILL.md) | Эвакуация, отсеки, преграды и проходки. |
| [fire-design-detection-and-automation](fire-design-detection-and-automation/SKILL.md) | СПС, СОУЭ и взаимодействие противопожарных систем. |
| [fire-design-suppression](fire-design-suppression/SKILL.md) | Автоматическое пожаротушение, расчётные случаи и координация. |
| [fire-electrical-issue-documentation](fire-electrical-issue-documentation/SKILL.md) | Комплектование и проверка выдачи ПБ и ЭОМ. |

### Семейства Revit — 1

| Скилл | Назначение |
| --- | --- |
| [revit-create-and-check-families](revit-create-and-check-families/SKILL.md) | Геометрия, параметры, графика и соединители семейств; проверка поведения. |

### Сметная подготовка — 2

| Скилл | Назначение |
| --- | --- |
| [prepare-work-quantity-statement](prepare-work-quantity-statement/SKILL.md) | Проверяемая ВОР по PDF, спецификациям и BIM: формулы, источники, правила измерения и контроль полноты. |
| [prepare-local-cost-estimate](prepare-local-cost-estimate/SKILL.md) | ЛСР по ВОР: нормы, ресурсы, коэффициенты, цены, форма РИМ и контроль покрытия. |

## Улучшение и дополнение

Как поручать **своему агенту** исправление ошибок, дополнение методик и создание новых скиллов — в [IMPROVING.md](IMPROVING.md). Внутри — готовые запросы, проверка результата и сохранение изменений для разных клиентов. Для личной доработки GitHub не обязателен.

Если хотите предложить улучшение общему репозиторию, порядок участия описан отдельно в [CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензия

[CC0-1.0](LICENSE): оригинальные материалы можно использовать, изменять и распространять, в том числе коммерчески, без требования указания авторства, в пределах предоставленных прав. Лицензия не распространяется на сторонние документы по ссылкам и товарные знаки. Материалы предоставляются без гарантий в пределах применимого права.
