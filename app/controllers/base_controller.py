from sqlalchemy.orm import Session

from data.database import Base


class CRUD():

    def __init__(self, db: Session, base: Base):
        self.db = db
        self.base = base

    def get(self, base_id: int):
        return self.db.query(self.base).get(base_id)

    def get_all(self):
        return self.db.query(self.base).all()

    def create(self, schema_base):
        db_base = self.base(**schema_base.dict())
        self.db.add(db_base)
        self.db.commit()
        self.db.refresh(db_base)

        return db_base

    def update(self, base_id: int, schema_base):
        self.db.query(self.base).filter(self.base.id == base_id).update(
            schema_base.dict(), synchronize_session='evaluate')
        self.db.commit()

        return self.get(base_id)

    def delete(self, base_id: int):
        db_base = self.get(base_id)

        if not db_base:
            raise ValueError

        self.db.query(self.base).filter(self.base == db_base).delete(
            synchronize_session='evaluate')
        self.db.commit()

        return
