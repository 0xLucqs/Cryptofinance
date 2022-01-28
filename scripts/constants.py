from dataclasses import dataclass


@dataclass
class Constants:
    """Some bitcoin constants"""
    BLOCK_TIME: int = 600
    BLOCK_REWARD: float = 6.25
