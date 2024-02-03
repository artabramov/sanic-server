"""Entity Manager."""

from sqlalchemy import asc, desc, text
from sqlalchemy.sql import func, exists
from decimal import Decimal

_ORDER_BY, _ORDER = "order_by", "order"
_ASC, _DESC = "asc", "desc"
_OFFSET, _LIMIT = "offset", "limit"
_SQLALCHEMY_RESERVED = [_OFFSET, _LIMIT, _ORDER_BY, _ORDER]
_SQLALCHEMY_OPERATORS = {
    "in": "in_",
    "eq": "__eq__",
    "not": "__ne__",
    "gte": "__ge__",
    "lte": "__le__",
    "gt": "__gt__",
    "lt": "__lt__",
    "like": "like",
    "ilike": "ilike",
}


class EntityManager:
    """Entity Manager provides methods for working with SQLAlchemy objects in Postgres database."""

    def __init__(self, session, log) -> None:
        """Init Entity Manager."""
        self.session = session
        self.log = log

    async def insert(self, obj: object, commit: bool = False) -> None:
        """Insert SQLAlchemy object into Postgres database."""
        self.session.add(obj)
        await self.session.flush()

        self.log.debug("Insert SQLAlchemy object into Postgres database, cls=%s, obj=%s, commit=%s" % (
            str(obj.__class__.__name__), str(obj.__dict__), commit))

        if commit:
            await self.commit()

    async def select(self, cls: object, obj_id: int) -> object:
        """Select SQLAlchemy object from Postgres database."""
        obj = self.session.query(cls).filter(cls.id == obj_id).first()

        self.log.debug("Select SQLAlchemy object from Postgres database, cls=%s, obj_id=%s, obj=%s" % (
            str(cls.__name__), obj_id, str(obj.__dict__) if obj else None))

        return obj

    async def select_by(self, cls: object, **kwargs) -> object:
        """Select SQLAlchemy object from Postgres database."""
        objs = await self.select_all(cls, **kwargs)
        return objs[0] if objs else None

    async def update(self, obj: object, commit: bool = False) -> None:
        """Update SQLAlchemy object in Postgres database."""
        self.session.merge(obj)
        self.session.flush()

        self.log.debug("Update SQLAlchemy object in Postgres database, cls=%s, obj=%s." % (
            str(obj.__class__.__name__), str(obj.__dict__)))

        if commit:
            await self.commit()

    async def delete(self, obj: object, commit: bool = False) -> None:
        """Delete SQLAlchemy object from Postgres database."""
        self.session.delete(obj)

        self.log.debug("Delete SQLAlchemy object from Postgres database, cls=%s, obj=%s." % (
            str(obj.__class__.__name__), str(obj.__dict__)))

        if commit:
            await self.commit()

    async def select_all(self, cls: object, **kwargs) -> list:
        """Select a bunch of SQLAlchemy objects from Postgres database."""
        objs = self.session.query(cls) \
            .filter(*self._where(cls, **kwargs)) \
            .order_by(self._order_by(cls, **kwargs)) \
            .offset(self._offset(**kwargs)) \
            .limit(self._limit(**kwargs)) \
            .all()

        self.log.debug("Select a bunch of SQLAlchemy objects from Postgres database, cls=%s, kwargs=%s, objs=%s" % (
            str(cls.__name__), str(kwargs), str([obj.__dict__ for obj in objs])))

        return objs

    async def count_all(self, cls: object, **kwargs) -> int:
        """Count SQLAlchemy objects in Postgres database."""
        query = self.session.query(func.count(getattr(cls, "id"))).filter(*self._where(cls, **kwargs))
        res = query.one()[0]

        self.log.debug("Count SQLAlchemy objects in Postgres database, cls=%s, kwargs=%s, count=%s." % (
            str(cls.__name__), str(kwargs), res))

        return res

    async def sum_all(self, cls: object, column_name: str, **kwargs) -> Decimal:
        """Sum SQLAlchemy objects column in Postgres database."""
        query = self.session.query(func.sum(getattr(cls, column_name))).filter(*self._where(cls, **kwargs))
        res = query.one()[0]

        self.log.debug("Sum SQLAlchemy objects column in Postgres database, cls=%s, column_name=%s, kwargs=%s, sum=%s." % (
            str(cls.__name__), column_name, str(kwargs), res))

        return res

    async def exists(self, cls: object, **kwargs) -> bool:
        """Check if SQLAlchemy object exists in Postgres database."""
        res = self.session.query(exists().where(*self._where(cls, **kwargs))).scalar()

        self.log.debug("Check if SQLAlchemy object exists in Postgres database, cls=%s, kwargs=%s, res=%s." % (
            str(cls.__name__), str(kwargs), res))

        return res

    async def subquery(self, cls, foreign_key, **kwargs):
        """Make a subquery expression for another class by a foreign key."""
        return self.session.query(getattr(cls, foreign_key)).filter(*self._where(cls, **kwargs))

    async def exec(self, sql: str, commit: bool = False) -> object:
        """Execute a raw query."""
        res = self.db.engine.execute(text(sql))
        self.log.debug("Execute a raw query, sql=%s." % sql)

        if commit:
            await self.commit()

        return res

    async def commit(self) -> None:
        """Commit transaction."""
        await self.session.commit()
        self.log.debug("Commit transaction.")

    async def rollback(self) -> None:
        """Rollback transaction."""
        await self.session.rollback()
        self.log.debug("Rollback transaction.")

    def _where(self, cls, **kwargs):
        """Make "WHERE" statement.

        How to implement dynamic API filtering using query parameters:
        https://www.mindee.com/blog/flask-sqlalchemy
        """
        where = []
        for key in {x: kwargs[x] for x in kwargs if x not in _SQLALCHEMY_RESERVED}:
            column_name, operator = key.split("__")

            if hasattr(cls, column_name):
                column = getattr(cls, column_name)

                value = kwargs[key]
                if isinstance(value, str):
                    if operator == "in":
                        value = [x.strip() for x in value.split(",")]
                    else:
                        value = value

                operation = getattr(column, _SQLALCHEMY_OPERATORS[operator])(value)
                where.append(operation)
        return where

    def _order_by(self, cls, **kwargs):
        """Make "ORDER BY" statement."""
        order_by = getattr(cls, kwargs.get(_ORDER_BY, "id"))
        return asc(order_by) if kwargs.get(_ORDER, _ASC) == _ASC else desc(order_by)

    def _offset(self, **kwargs):
        """Make "OFFSET" statement."""
        return kwargs.get(_OFFSET, 0)

    def _limit(self, **kwargs):
        """Make "LIMIT" statement."""
        return kwargs.get(_LIMIT, 1)
