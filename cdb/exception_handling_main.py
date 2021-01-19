from cdb.http_retry import HttpRetryExhausted


def exception_handling_main(callback):
    try:
        callback()
        return 0
    except HttpRetryExhausted:
        print("Retry limit exhausted.")
        print("Command failed.")
        return 1
