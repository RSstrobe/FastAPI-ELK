from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """Base abstract class for all getting repositories."""

    @abstractmethod
    async def get(self, *args, **kwargs):
        """Get data from database."""
        raise NotImplementedError

    @abstractmethod
    async def set(self, *args, **kwargs):
        """Function for execute set operations."""
        raise NotImplementedError
