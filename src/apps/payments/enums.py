from enum import StrEnum


class PaymentStatus(StrEnum):
    PENDING = 'pending'
    SUCCEEDED = 'succeeded'
    CANCELED = 'canceled'
    WAITING_FOR_CAPTURE = 'waiting_for_capture'
