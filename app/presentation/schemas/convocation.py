from pydantic import BaseModel


class RefineConvocationRequest(BaseModel):
    message: str
    critical_fragments: list[str]
    style: str | None = None


class RefineConvocationResponse(BaseModel):
    refined_message: str
    was_refined: bool
