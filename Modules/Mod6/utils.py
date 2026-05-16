def safe_int(value):

    try:
        return int(value)

    except:
        return None