from time import sleep


def retry(exception_cond, retries, cooldown):
    def decorator(func):
        def inner(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not exception_cond(e):
                        raise
                    sleep(cooldown)

        return inner

    return decorator
