import json

from fastapi import APIRouter, Depends, HTTPException, Query
from geoalchemy2.shape import to_shape
from shapely.geometry import LineString, Point, mapping
from geoalchemy2.shape import from_shape
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import get_current_user, require_role
from app.db import get_db

router = APIRouter(prefix="/api", tags=["gis"])

WRITERS = ("SUPER_ADMIN", "ADMIN", "EDITOR", "FIELD")


def _scope(user: models.User, group_id: int) -> int:
    if user.group_id and user.group_id != group_id:
        raise HTTPException(403, "No access to this group")
    return group_id


@router.get("/map/features", response_model=schemas.GeoJSONCollection)
def map_features(
    group_id: int,
    asset_type: str | None = Query(None),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """All points + cable lines of a group as GeoJSON, for the Leaflet map."""
    _scope(user, group_id)
    features = []

    aq = db.query(models.Asset).filter(models.Asset.group_id == group_id, models.Asset.location.isnot(None))
    if asset_type:
        aq = aq.filter(models.Asset.asset_type == asset_type)
    for a in aq.all():
        pt = to_shape(a.location)
        features.append({
            "type": "Feature",
            "geometry": mapping(pt),
            "properties": {"id": a.id, "kind": "asset", "asset_type": a.asset_type,
                           "name": a.name, "status": a.status},
        })

    for c in db.query(models.FiberCable).filter(models.FiberCable.group_id == group_id).all():
        features.append({
            "type": "Feature",
            "geometry": mapping(to_shape(c.route)),
            "properties": {"id": c.id, "kind": "cable", "name": c.name, "core_count": c.core_count},
        })
    return {"type": "FeatureCollection", "features": features}


@router.get("/assets", response_model=list[schemas.AssetOut])
def list_assets(
    group_id: int,
    asset_type: str | None = None,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _scope(user, group_id)
    q = db.query(models.Asset).filter(models.Asset.group_id == group_id)
    if asset_type:
        q = q.filter(models.Asset.asset_type == asset_type)
    out = []
    for a in q.order_by(models.Asset.name).all():
        pt = to_shape(a.location) if a.location is not None else None
        out.append(schemas.AssetOut(id=a.id, group_id=a.group_id, asset_type=a.asset_type, name=a.name,
                                    status=a.status, lat=pt.y if pt else 0, lng=pt.x if pt else 0))
    return out


@router.post("/assets", response_model=schemas.AssetOut, status_code=201)
def create_asset(body: schemas.AssetIn, user: models.User = Depends(require_role(*WRITERS)),
                 db: Session = Depends(get_db)):
    _scope(user, body.group_id)
    a = models.Asset(
        group_id=body.group_id, site_id=body.site_id, parent_id=body.parent_id,
        asset_type=body.asset_type.upper(), name=body.name, status=body.status,
        attributes=body.attributes, location=from_shape(Point(body.lng, body.lat), srid=4326),
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return schemas.AssetOut(id=a.id, group_id=a.group_id, asset_type=a.asset_type, name=a.name,
                            status=a.status, lat=body.lat, lng=body.lng)


@router.delete("/assets/{asset_id}", status_code=204)
def delete_asset(asset_id: int, user: models.User = Depends(require_role("SUPER_ADMIN", "ADMIN")),
                 db: Session = Depends(get_db)):
    a = db.get(models.Asset, asset_id)
    if not a:
        raise HTTPException(404, "Not found")
    _scope(user, a.group_id)
    db.delete(a)
    db.commit()


@router.post("/cables", status_code=201)
def create_cable(body: schemas.CableIn, user: models.User = Depends(require_role(*WRITERS)),
                 db: Session = Depends(get_db)):
    _scope(user, body.group_id)
    if len(body.coordinates) < 2:
        raise HTTPException(422, "A cable needs at least two coordinates")
    cable = models.FiberCable(
        group_id=body.group_id, name=body.name, core_count=body.core_count,
        start_asset_id=body.start_asset_id, end_asset_id=body.end_asset_id,
        route=from_shape(LineString(body.coordinates), srid=4326),
    )
    db.add(cable)
    db.flush()
    db.add_all(models.FiberCore(cable_id=cable.id, core_number=i) for i in range(1, body.core_count + 1))
    db.commit()
    return {"id": cable.id}


@router.get("/search")
def search(q: str, group_id: int, user: models.User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    """Header search: assets, cables, customers."""
    _scope(user, group_id)
    like = f"%{q}%"
    assets = db.query(models.Asset).filter(models.Asset.group_id == group_id,
                                           models.Asset.name.ilike(like)).limit(20).all()
    cables = db.query(models.FiberCable).filter(models.FiberCable.group_id == group_id,
                                                models.FiberCable.name.ilike(like)).limit(10).all()
    custs = db.query(models.Customer).filter(
        models.Customer.group_id == group_id,
        or_(models.Customer.name.ilike(like), models.Customer.code.ilike(like))).limit(10).all()
    return {
        "assets": [{"id": a.id, "name": a.name, "type": a.asset_type} for a in assets],
        "cables": [{"id": c.id, "name": c.name} for c in cables],
        "customers": [{"id": c.id, "name": c.name, "code": c.code} for c in custs],
    }


@router.get("/stats")
def stats(group_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    _scope(user, group_id)
    total = db.query(models.Asset).filter(models.Asset.group_id == group_id).count()
    return {"assets": total}
