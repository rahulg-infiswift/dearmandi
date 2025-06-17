# mixins/isolating.py
# Copyright (C) 2024 - 2028 the PythonAccounting authors and contributors
# <see AUTHORS file>
#
# This module is part of PythonAccounting and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""
Provides functionality to scope accounting objects to a single Entity.

"""
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy import ForeignKey


# pylint: disable=too-few-public-methods
class IsolatingMixin:
    """
    This class enables isolating by User for accounting objects.

    Attributes:
        user_id (int): The id of the User to which the model belongs.
    """

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", use_alter=True))

    @declared_attr
    def user(self) -> Mapped["User"]:
        """Returns the User of the instance."""
        return relationship("User", foreign_keys=[self.user_id])
