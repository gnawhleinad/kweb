from __future__ import annotations

from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):  # type: ignore[valid-type, misc]
    class Config:
        env_prefix = "kweb_"
        env_nested_delimiter = "_"

    fileslocation: Path
    meta_splitter: str = ":"
    editable: bool = False
    add_missing_layers: bool = True
    max_rdb_limit: int = 100
    """Maximum rdb errors the client can request."""

    @field_validator("fileslocation")
    @classmethod
    def resolvefileslocation(cls, v: Path | str) -> Path:
        return Path(v).expanduser().resolve()
