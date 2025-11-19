from . import  logger

def strtobool(s: str) -> bool:
    true_set = {'true', '1', 'yes', 'y', 't'}
    false_set = {'false', '0', 'no', 'n', 'f'}
    s_lower = s.strip().lower()
    if s_lower in true_set:
        return True
    elif s_lower in false_set:
        return False
    else:
        logger.error(f"Invalid boolean string: {s}")
