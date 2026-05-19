from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel,Field,field_validator

class DebateStance(str,Enum):
    PRO="PRO"
    CON="CON"
    NEUTRAL="NEUTRAL"

class Evidence(BaseModel):
    source:str=Field(
        ...,
        min_length=3,
        description="Source or origin of the evidence"
    )
    content:str=Field(
        ...,
        min_length=10,
        description="Supporting evidence content"
    )
    credibility_score:float=Field(
        ...,
        ge=0,
        le=1,
        description="Reliability score of the evidence"
    )

class DebateArgument(BaseModel):
    agent_name:str=Field(
        ...,
        min_length=3,
        description="Name of the debating agent"
    )
    topic:str=Field(
        ...,
        min_length=5,
        description="Debate Topic"
    )
    stance:DebateStance

    argument:str=Field(
        ...,
        min_length=20,
        description="Main reasoning or claim"
    )
    confidence:float=Field(
        ...,
        ge=0,
        le=1,
        description="Confidence score of the arguement"
    )
    evidence:List[Evidence]=Field(
        default_factory=list,
        description="List of Supporting evidence"
    )
    round_number:int=Field(
        ...,
        ge=1,
        description="Debate round number"
    )
    timestamp:datetime=Field(
        default_factory=datetime.utcnow
    )

    @field_validator("argument")
    @classmethod
    def validate_argument(cls,value:str) ->str:
        if not value.strip():
            raise ValueError("Arguement cannot be empty")
        return value

class DebateVerdict(BaseModel):
    topic:str=Field(
        ...,
        min_length=5
    )
    winning_stance:DebateStance
    reasoning:str=Field(
        ...,
        min_length=20
    )
    confidence:float=Field(
        ...,
        ge=0,
        le=1
    )
    summary:str=Field(
        ...,
        min_length=15
    )
    timestamp:datetime=Field(
        default_factory=datetime.utcnow
    )