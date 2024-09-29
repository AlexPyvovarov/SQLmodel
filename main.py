from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Relationship
from sqlalchemy.orm import sessionmaker


class PosadaEmployee(SQLModel, table=True):
    posada_id: int | None = Field(primary_key=True, foreign_key="posada.id")
    employee_id: int | None = Field(primary_key=True, foreign_key="employee.id")


class Posada(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    employees: list["Employee"] = Relationship(back_populates="posada", link_model=PosadaEmployee)


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    salary: int
    # posada_id: Optional[int] = Field(default=None, foreign_key="posada.id")
    posada: list[Posada] = Relationship(back_populates="employees", link_model=PosadaEmployee)


engine = create_engine("sqlite:///my_db.sql", echo=True)
session_factory = sessionmaker(bind=engine)
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

with session_factory.begin() as session:
    commander = Posada(name="commander")
    employee1 = Employee(name="kora", salary=9000, )
    employee2 = Employee(name="dara", salary=2000, )
    commander.employees.extend((employee1, employee2))
    session.add(commander)