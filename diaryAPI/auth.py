from fastapi import Depends, HTTPException, status
from typing import Annotated

def get_current_user_id() -> int:
    return 100 

AuthenticatedUser = Annotated[int, Depends(get_current_user_id)]