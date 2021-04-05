
DRY_RUN = {"MERKELY_DRY_RUN": "TRUE"}


def dry_run(ev):
    return {**DRY_RUN, **ev}
