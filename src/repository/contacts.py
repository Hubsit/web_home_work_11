from datetime import date, timedelta

from sqlalchemy import extract, and_
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(contact_email: str, db: Session):
    contact = db.query(Contact).filter_by(email=contact_email).first()
    return contact


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contact_by_first_name(contact_first_name: str, db: Session):
    contacts = db.query(Contact).filter_by(first_name=contact_first_name).all()
    return contacts


async def get_contact_by_last_name(contact_last_name: str, db: Session):
    contacts = db.query(Contact).filter_by(last_name=contact_last_name).all()
    return contacts


async def get_birthday(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).filter(and_(extract('day', Contact.birthday) >= today.day,
                                             extract('day', Contact.birthday) <= next_week.day,
                                             extract('month', Contact.birthday) == today.month)).all()
    return contacts
