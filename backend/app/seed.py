"""Create tables, a demo group, a SUPER_ADMIN user and a few sample assets.

Usage (from gis/backend):  python -m app.seed
"""
import os

from geoalchemy2.shape import from_shape
from shapely.geometry import LineString, Point

from app import models
from app.core.security import hash_password
from app.db import Base, SessionLocal, engine


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        group = db.query(models.Group).filter_by(name="Kishanganj_TEST").first()
        if not group:
            group = models.Group(name="Kishanganj_TEST")
            db.add(group)
            db.flush()

        if not db.query(models.User).filter_by(username="admin").first():
            db.add(models.User(
                username="admin",
                password_hash=hash_password(os.getenv("SEED_ADMIN_PASSWORD", "ChangeMe@123")),
                role="SUPER_ADMIN",
            ))

        if not db.query(models.Asset).filter_by(group_id=group.id).first():
            olt = models.Asset(group_id=group.id, asset_type="OLT", name="OLT-Indore",
                               location=from_shape(Point(75.8577, 22.7196), srid=4326))
            odf = models.Asset(group_id=group.id, asset_type="ODF", name="ODF-Ambedkar-Nagar",
                               location=from_shape(Point(75.7870, 22.5560), srid=4326))
            fat = models.Asset(group_id=group.id, asset_type="FAT", name="FAT-Simrol",
                               location=from_shape(Point(75.9150, 22.5290), srid=4326))
            db.add_all([olt, odf, fat])
            db.flush()
            cable = models.FiberCable(
                group_id=group.id, name="CBL-ODF-FAT-01", core_count=12,
                start_asset_id=odf.id, end_asset_id=fat.id,
                route=from_shape(LineString([(75.7870, 22.5560), (75.8400, 22.5500), (75.9150, 22.5290)]),
                                 srid=4326),
            )
            db.add(cable)
            db.flush()
            db.add_all(models.FiberCore(cable_id=cable.id, core_number=i) for i in range(1, 13))
        db.commit()
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
