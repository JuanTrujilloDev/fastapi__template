"""

Override sqladmin._queries.Query class methods to add custom logic to allow sqlmodel
creation


This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from typing import Any

import anyio
from fastapi import Request
from sqladmin._queries import Query


class SQLModelQueryHelper(Query):
    """Query helper class to override Query class methods"""

    def _insert_sync(self, data: dict[str, Any], request: Request) -> Any:
        obj = self.model_view.model(**data)

        with self.model_view.session_maker(expire_on_commit=False) as session:
            anyio.from_thread.run(
                self.model_view.on_model_change, data, obj, True, request
            )
            obj = self._set_attributes_sync(session, obj, data)
            session.add(obj)
            session.commit()
            anyio.from_thread.run(
                self.model_view.after_model_change, data, obj, True, request
            )
            return obj

    async def _insert_async(self, data: dict[str, Any], request: Request) -> Any:
        obj = self.model_view.model(**data)

        async with self.model_view.session_maker(expire_on_commit=False) as session:
            await self.model_view.on_model_change(data, obj, True, request)
            obj = await self._set_attributes_async(session, obj, data)
            session.add(obj)
            await session.commit()
            await self.model_view.after_model_change(data, obj, True, request)
            return obj
