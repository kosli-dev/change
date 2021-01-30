import os

if __name__ == '__main__':
    from command_processor import execute
    context = {'env': os.environ}
    execute(context)
