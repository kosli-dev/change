
def in_dry_run(env):
    global_off = env.get('MERKELY_API_TOKEN', 'FALSE') == 'DRY_RUN'
    local_off = env.get('MERKELY_DRY_RUN', 'FALSE') == "TRUE"
    return global_off or local_off
