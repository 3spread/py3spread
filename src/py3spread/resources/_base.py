from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import Client


class Resource:
    def __init__(self, client: "Client"):
        self._client = client

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._client.request(path, params)

    def _iter_cursor(self, path: str, params: dict[str, Any]) -> Iterator[dict[str, Any]]:
        # keyset paging: resend the same filters plus the returned cursor
        params = dict(params)
        while True:
            page = self._get(path, params)
            yield from page.get("data") or []
            cursor = page.get("next_cursor")
            if not cursor:
                return
            params["cursor"] = cursor

    def _iter_offset(self, path: str, params: dict[str, Any]) -> Iterator[dict[str, Any]]:
        params = dict(params)
        offset = int(params.pop("offset", None) or 0)
        while True:
            page = self._get(path, {**params, "offset": offset})
            rows = page.get("data") or []
            yield from rows
            if not rows or page.get("has_more") is False:
                return
            offset += len(rows)
            total = page.get("total")
            if total is not None and offset >= total:
                return

    def _entities(
        self,
        path: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        return self._get(
            path,
            dict(limit=limit, offset=offset, search=search, sort=sort, order=order),
        )
