from sqlalchemy.orm import Session

from data.database import Base


class CONTROLLER:
    def __init__(self, db_session: Session, db_entity: Base):
        self.db_session = db_session
        self.db_entity = db_entity

    def get(self, base_id: int):
        return self.db_session.query(self.db_entity).get(base_id)

    def get_all(self):
        return self.db_session.query(self.db_entity).all()

    def create(self, schema_base):
        db_base = self.db_entity(**schema_base.dict())
        self.db_session.add(db_base)
        self.db_session.commit()
        self.db_session.refresh(db_base)

        return db_base

    def update(self, base_id: int, schema_base):
        self.db_session.query(self.db_entity).filter(
            self.db_entity.id == base_id
        ).update(schema_base.dict(), synchronize_session="evaluate")
        self.db_session.commit()

        return self.get(base_id)

    def delete(self, base_id: int):
        db_base = self.get(base_id)

        if not db_base:
            raise ValueError

        self.db_session.query(self.db_entity).filter(self.db_entity == db_base).delete(
            synchronize_session="evaluate"
        )
        self.db_session.commit()

        return
