# Here we will implement the unit of work pattern for the auth module (if needed).
from abc import ABC, abstractmethod

class AbstractUnitOfWork(ABC):
    """
    Abstract base class for unit of work.
    This class should be inherited by concrete implementations.
    """

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:  # solo si hubo excepción
            self.rollback()
        
    @abstractmethod
    def commit(self):
        """
        Commit the transaction.
        This method should be implemented by concrete classes.
        """
        raise NotImplementedError("Commit method must be implemented by subclass.")

    @abstractmethod
    def rollback(self):
        """
        Rollback the transaction.
        This method should be implemented by concrete classes.
        """
        raise NotImplementedError("Rollback method must be implemented by subclass.")

    @abstractmethod
    def collect_events(self):
        """
        Collect events from the repositories.
        """
        raise NotImplementedError("Collect events method must be implemented by subclass.")