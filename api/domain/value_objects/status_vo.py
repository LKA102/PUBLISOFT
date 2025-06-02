from enums.status_enum import StatusEnum


class StatusVO:
    def __init__(self, description_status: str):
        if not description_status or not description_status.strip():
            raise ValueError("Status description cannot be empty")

        description_status = description_status.strip()
        if description_status not in [status.name for status in StatusEnum]:
            raise ValueError(
                "Status description must be a valid status from StatusEnum"
            )

        self.description_status = description_status

    def __str__(self):
        return self.description_status
