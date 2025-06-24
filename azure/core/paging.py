"""Paging support for Azure SDK"""
import time
from typing import Iterator, List, Any, Optional, TypeVar, Generic

T = TypeVar('T')


class ItemPaged(Generic[T], Iterator[T]):
    """Paged iteration of items"""
    
    def __init__(self, items: List[T], page_size: int = 100):
        self.items = items
        self.page_size = page_size
        self.current_index = 0
        
    def __iter__(self) -> Iterator[T]:
        return self
    
    def __next__(self) -> T:
        if self.current_index >= len(self.items):
            raise StopIteration
        
        item = self.items[self.current_index]
        self.current_index += 1
        
        # Simulate slight network delay
        time.sleep(0.001)
        
        return item
    
    def by_page(self, continuation_token: Optional[str] = None):
        """Get results by page"""
        start_index = 0
        if continuation_token:
            start_index = int(continuation_token)
            
        for i in range(start_index, len(self.items), self.page_size):
            yield self.items[i:i + self.page_size]
