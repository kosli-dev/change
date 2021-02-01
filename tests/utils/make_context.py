
def make_context(env):
    context = type('context', (), {})()
    context.env = env
    return context
