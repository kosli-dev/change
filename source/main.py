from commands import External, main  # pragma: no cover
import sys  # pragma: no cover

if __name__ == '__main__':  # pragma: no cover
    external = External()
    exit_code = main(external)
    print(external.stdout.getvalue())
    sys.exit(exit_code)
