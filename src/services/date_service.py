from datetime import date, timedelta


class DateService:
    """
    Calcula el período completo del mes anterior.
    """

    def get_previous_month_period(self) -> tuple[date, date]:
        today = date.today()

        first_day_current_month = today.replace(day=1)

        last_day_previous_month = first_day_current_month - timedelta(days=1)

        first_day_previous_month = last_day_previous_month.replace(day=1)

        return (
            first_day_previous_month,
            last_day_previous_month,
        )
