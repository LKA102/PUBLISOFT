from modules.ranking.domain.entities.base_entity import BaseEntity
from typing import List, Optional
import enum
from uuid import UUID
from datetime import datetime, timezone

class MonthTypeEnum(str, enum.Enum):
    JANUARY = "Jan"
    FEBRUARY = "Feb"
    MARCH = "Mar"
    APRIL = "Apr"
    MAY = "May"
    JUNE = "Jun"
    JULY = "Jul"
    AUGUST = "Aug"
    SEPTEMBER = "Sep"
    OCTOBER = "Oct"
    NOVEMBER = "Nov"
    DECEMBER = "Dec"


class Ranking(BaseEntity):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__period: str = kwargs.get('period')
        self.__score: float = kwargs.get('score')
        self.__student_id: UUID = kwargs.get('student_id')
        self.__year: str = kwargs.get('year')
        self.__month: MonthTypeEnum = kwargs.get('month')
        self.events: set = set()
        
    def __eq__(self, other):
        if not isinstance(other, Ranking):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
    # region GETTERS AND SETTERS
    
    @property
    def period(self) -> str:
        return self.__period
    
    @period.setter
    def period(self, value: str):
        if not value:
            raise ValueError("El periodo no puede estar vacío")
        self.__period = value
        
    @property
    def score(self) -> float:
        return self.__score
    
    @score.setter
    def score(self, value: float):
        if value < 0:
            raise ValueError("El puntaje no puede ser negativo")
        self.__score = value
        
    @property
    def student_id(self) -> UUID:
        return self.__student_id
    
    @student_id.setter
    def student_id(self, value: UUID):
        if not isinstance(value, UUID):
            raise ValueError("El ID del estudiante debe ser un UUID válido")
        self.__student_id = value
        
    @property
    def year(self) -> str:
        return self.__year
    
    @year.setter
    def year(self, value: str):
        if not value or len(value) != 4 or not value.isdigit():
            raise ValueError("El año debe ser un string de 4 dígitos")
        self.__year = value
        
    @property
    def month(self) -> MonthTypeEnum:
        return self.__month
    
    @month.setter
    def month(self, value: MonthTypeEnum):
        if not isinstance(value, MonthTypeEnum):
            raise ValueError("El mes debe ser un valor de MonthTypeEnum")
        self.__month = value
        
    # endregion
    
    @classmethod
    def create(cls, period: str, score: float, student_id: UUID, year: str, month: MonthTypeEnum) -> 'Ranking':
        
        created_at = datetime.now(timezone.utc)
        
        if not period or not score or not student_id or not year or not month:
            raise ValueError("Todos los campos son obligatorios para crear un Ranking")
        
        if not isinstance(month, MonthTypeEnum):
            raise ValueError(f"El mes debe ser un valor de MonthTypeEnum, recibido: {month}")
        
        ranking = cls(
            period=period,
            score=score,
            student_id=student_id,
            year=year,
            month=month,
            created_at=created_at
        )
        return ranking