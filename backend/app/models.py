from geoalchemy2 import Geography
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db import Base


class Group(Base):
    """Top-level tenant / region (e.g. 'Kishanganj_TEST'), selectable in the header."""
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="VIEWER")  # SUPER_ADMIN, ADMIN, EDITOR, FIELD, VIEWER
    is_active = Column(Boolean, default=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)  # NULL = all groups


class Site(Base):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    site_type = Column(String(40))  # POP, HUB, NODE ...
    address = Column(Text)
    location = Column(Geography("POINT", srid=4326), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Asset(Base):
    """Generic point asset: OLT, ODF, Splitter, FAT, Splice Closure, Pole, Manhole, ONT, Network Device."""
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    parent_id = Column(Integer, ForeignKey("assets.id"), nullable=True)  # e.g. splitter -> FAT
    asset_type = Column(String(40), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    status = Column(String(30), default="ACTIVE")
    attributes = Column(Text)  # JSON string for type-specific fields
    location = Column(Geography("POINT", srid=4326))
    created_at = Column(DateTime, server_default=func.now())

    ports = relationship("Port", back_populates="asset", cascade="all, delete-orphan")


class Port(Base):
    """PON ports, ODF ports, splitter ports, FAT ports, device interfaces."""
    __tablename__ = "ports"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    port_kind = Column(String(30), nullable=False)  # PON, ODF, SPLITTER, FAT, INTERFACE
    number = Column(Integer, nullable=False)
    label = Column(String(80))
    status = Column(String(30), default="FREE")  # FREE, USED, RESERVED, FAULTY
    connected_core_id = Column(Integer, ForeignKey("fiber_cores.id"), nullable=True)

    asset = relationship("Asset", back_populates="ports")


class FiberCable(Base):
    __tablename__ = "fiber_cables"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    core_count = Column(Integer, nullable=False)
    start_asset_id = Column(Integer, ForeignKey("assets.id"))
    end_asset_id = Column(Integer, ForeignKey("assets.id"))
    length_m = Column(Integer)
    route = Column(Geography("LINESTRING", srid=4326), nullable=False)

    cores = relationship("FiberCore", back_populates="cable", cascade="all, delete-orphan")


class FiberCore(Base):
    __tablename__ = "fiber_cores"
    id = Column(Integer, primary_key=True)
    cable_id = Column(Integer, ForeignKey("fiber_cables.id"), nullable=False, index=True)
    core_number = Column(Integer, nullable=False)
    tube_color = Column(String(30))
    core_color = Column(String(30))
    status = Column(String(30), default="FREE")

    cable = relationship("FiberCable", back_populates="cores")


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    phone = Column(String(30))
    address = Column(Text)
    ont_asset_id = Column(Integer, ForeignKey("assets.id"))
    fat_port_id = Column(Integer, ForeignKey("ports.id"))
    location = Column(Geography("POINT", srid=4326))


class CustomerService(Base):
    __tablename__ = "customer_services"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    plan = Column(String(80))
    status = Column(String(30), default="ACTIVE")
    activated_at = Column(DateTime)


class Photo(Base):
    """Field data & photo capture, attached to any asset."""
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    file_path = Column(String(255), nullable=False)
    caption = Column(String(255))
    taken_by = Column(Integer, ForeignKey("users.id"))
    taken_at = Column(DateTime, server_default=func.now())
