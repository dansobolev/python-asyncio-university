class UserNotFoundException(Exception):
    pass


class UserIsBannedException(Exception):
    pass


class UserAlreadyExistingException(Exception):
    pass


class UserWithSuchLoginAlreadyExistedException(Exception):
    pass


class PasswordResetLinkNotFound(Exception):
    pass


class PasswordResetLinkExpired(Exception):
    pass


class UploadedFileTooLargeException(Exception):
    pass


class DiscussionNotFound(Exception):
    pass


class UploadNotFound(Exception):
    pass
