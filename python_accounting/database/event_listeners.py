# database/event_listeners.py
# Copyright (C) 2024 - 2028 the PythonAccounting authors and contributors
# <see AUTHORS file>
#
# This module is part of PythonAccounting and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""
This mixin provides logic for handling events in sqlalchemy's orm lifecycle
that are relevant to accounting.

"""
from datetime import datetime

from sqlalchemy.orm.session import Session
from sqlalchemy import event, orm, and_, update

from python_accounting.models import User, Recyclable, Transaction, Account, Ledger
from python_accounting.mixins import IsolatingMixin
from python_accounting.exceptions import MissingUserError


def _filter_options(execute_state, option) -> bool:
    return (
        not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get(option, False)
        and not execute_state.session.info.get(option, False)
    )


# pylint: disable=too-few-public-methods
class EventListenersMixin:
    """
    Event Listeners class.
    """

    @event.listens_for(Session, "do_orm_execute")
    def _add_filtering_criteria(  # pylint: disable=no-self-argument
        execute_state,
    ) -> None:
        # Recycling filter
        if _filter_options(execute_state, "include_deleted"):
            execute_state.statement = execute_state.statement.options(
                orm.with_loader_criteria(
                    Recyclable,
                    lambda cls: and_(
                        cls.deleted_at == None,  # pylint: disable=singleton-comparison
                        cls.destroyed_at  # pylint: disable=singleton-comparison
                        == None,
                    ),
                    execute_state,
                    include_aliases=True,
                )
            )

        # User filter
        if (
            _filter_options(execute_state, "ignore_isolation")
            and execute_state.statement.column_descriptions[0]["type"] is not User
        ):
            session_user_id = execute_state.session.user.id
            execute_state.statement = execute_state.statement.options(
                orm.with_loader_criteria(
                    IsolatingMixin,
                    lambda cls: cls.user_id == session_user_id,
                    include_aliases=True,
                )
            )

    @event.listens_for(Session, "transient_to_pending")
    def _set_session_user(self, object_) -> None:
        if not hasattr(self, "user") or self.user is None:
            if isinstance(object_, User):
                self.user = object_
            elif object_.user_id is None:
                raise MissingUserError
            else:
                self.user = self.get(User, object_.user_id)

        if (
            self.user.reporting_period is None
            or self.user.reporting_period.calendar_year != datetime.today().year
        ):
            self._set_reporting_period()

    @event.listens_for(Session, "transient_to_pending")
    def _set_object_index(self, object_) -> None:
        if (isinstance(object_, (Account, Transaction))) and object_.id is None:
            object_.session_index = (
                len(
                    [
                        t
                        for t in self.new
                        if isinstance(t, Transaction)
                        and t.transaction_type == object_.transaction_type
                    ]
                )
                if isinstance(object_, Transaction)
                else len(
                    [
                        a
                        for a in self.new
                        if isinstance(a, Account)
                        and a.account_type == object_.account_type
                    ]
                )
            )

    @event.listens_for(Ledger, "after_insert")
    def _set_ledger_hash(  # pylint: disable=no-self-argument
        mapper, connection, target
    ):
        connection.execute(
            update(Ledger)
            .where(Ledger.id == target.id)
            .values(hash=target.get_hash(connection))
        )

    @event.listens_for(Session, "before_flush")
    def _validate_model(self, _, __) -> None:
        for model in list(self.new) + list(self.dirty):
            if hasattr(model, "validate"):
                model.validate(self)
