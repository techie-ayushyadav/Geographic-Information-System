from typing import Any, Optional

from pydantic import BaseModel


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str


class GroupOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class AssetIn(BaseModel):
    group_id: int
    site_id: Optional[int] = None
    parent_id: Optional[int] = None
    asset_type: str
    name: str
    status: str = "ACTIVE"
    attributes: Optional[str] = None
    lat: float
    lng: float


class AssetOut(BaseModel):
    id: int
    group_id: int
    asset_type: str
    name: str
    status: str
    lat: float
    lng: float


class CableIn(BaseModel):
    group_id: int
    name: str
    core_count: int
    start_asset_id: Optional[int] = None
    end_asset_id: Optional[int] = None
    coordinates: list[list[float]]  # [[lng, lat], ...]


class GeoJSONCollection(BaseModel):
    type: str = "FeatureCollection"
    features: list[dict[str, Any]]
