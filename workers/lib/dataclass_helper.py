import dataclasses


def get_dict(interface):
    """
        can make user login class to dictionary
        :return SomeInteface created by dataclasses -> dict:
    """
    return dataclasses.asdict(interface)
