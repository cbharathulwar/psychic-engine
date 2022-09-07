from __future__ import annotations

from functools import cached_property
from typing import TypeVar

import torch

from gnn_tracking.utils.types import assert_int


def zero_divide(a: float, b: float) -> float:
    if b == 0:
        return 0
    return a / b


class BinaryClassificationStats:
    def __init__(
        self, output: torch.Tensor, y: torch.Tensor, thld: torch.Tensor | float
    ):
        """

        Args:
            output:
            y:
            thld:

        Returns:
            accuracy, TPR, TNR
        """
        assert_int(y)
        self._output = output
        self._y = y
        self._thld = thld

    @cached_property
    def TP(self) -> float:
        return torch.sum((self._y == 1) & (self._output > self._thld)).item()

    @cached_property
    def TN(self) -> float:
        return torch.sum((self._y == 0) & (self._output < self._thld)).item()

    @cached_property
    def FP(self) -> float:
        return torch.sum((self._y == 0) & (self._output > self._thld)).item()

    @cached_property
    def FN(self) -> float:
        return torch.sum((self._y == 1) & (self._output < self._thld)).item()

    @cached_property
    def acc(self) -> float:
        return zero_divide(self.TP + self.TN, self.TP + self.TN + self.FP + self.FN)

    @cached_property
    def TPR(self) -> float:
        return zero_divide(self.TP, self.TP + self.FN)

    @cached_property
    def TNR(self) -> float:
        return zero_divide(self.TN, self.TN + self.FP)


_P = TypeVar("_P")


def add_key_prefix(dct: dict[str, _P], prefix: str = "") -> dict[str, _P]:
    """Return a copy of the dictionary with the prefix added to all keys."""
    return {f"{prefix}{k}": v for k, v in dct.items()}
