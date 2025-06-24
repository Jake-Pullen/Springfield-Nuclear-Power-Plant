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
        # Simulate realistic paging delays
        if self.current_index % self.page_size == 0 and self.current_index > 0:
            time.sleep(0.1)  # Small delay between pages
        item = self.items[self.current_index]
        self.current_index += 1
        return item
    
    def by_page(self, continuation_token=None):
        """Return pages of items"""
        start_index = 0
        if continuation_token:
            start_index = int(continuation_token)
        while start_index < len(self.items):
            end_index = min(start_index + self.page_size, len(self.items))
            page_items = self.items[start_index:end_index]
            next_token = str(end_index) if end_index < len(self.items) else None
            yield page_items, next_token
            start_index = end_index
