from fastapi import HTTPException, status


class SubscriptionAlreadyExistsHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already has an active subscription',
        )


class SubscriptionNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Subscription not found',
        )
