This page documents Pydantic's implementation of generic models and forward references, which are advanced typing features that enhance model reusability and enable self-referential data structures. These features are essential parts of Pydantic's type system, complementing the fundamental types covered in [Constrained Types](#3.1) and [Network Types](#3.2).

## Generic Models

Generic models in Pydantic allow you to create model templates that can be parameterized with different types, similar to how generic classes work in languages like Java or C#. This enables type-safe reuse of model structures across different data types.

### Basic Usage

To create a generic model, inherit from both `BaseModel` and `Generic[T]` (where `T` is a type variable):

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class Container(BaseModel, Generic[T]):
    value: T