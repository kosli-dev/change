from cdb.http_retry import HttpRetryExhauted


def exception_handling_main(callback):
    try:
        callback()
        return 0
    except HttpRetryExhauted:
        print("Retry limit exhausted.")
        print("Command failed.")
        return 1
