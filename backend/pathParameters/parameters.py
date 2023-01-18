class ConditionParameter:
    condition: str | None


class EmailParameter:
    email: str


class FormParameter:
    form_id: str
    form_link: str
    file_type: str


class PrivateTableParameter:
    email: str
    stage_index: int
    table_path: str
    file_type: str


class GeneralTableParameter:
    file_path: str
    file_type: str


class StageParameter:
    index: int
    name: str
    forms: list[FormParameter]
    general: GeneralTableParameter
