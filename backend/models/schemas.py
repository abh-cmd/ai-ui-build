from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any


# Allowed component types based on design system
ALLOWED_COMPONENT_TYPES = {
    "header", "title", "subtitle", "description", "text", 
    "button", "cta", "image", "product_card", "container",
    "list", "card", "section", "hero", "footer", "divider"
}


class ComponentModel(BaseModel):
    """Represents a single UI component in the blueprint."""
    id: str
    type: str  # "header", "product_card", "button", etc.
    bbox: List[float]  # [x, y, width, height]
    text: Optional[str] = None
    role: Optional[str] = None  # "hero", "content", "cta", etc.
    confidence: float  # 0.0 to 1.0
    visual: Optional[Dict[str, Any]] = None  # Color, size, image info, etc.
    
    @field_validator('bbox')
    @classmethod
    def validate_bbox(cls, v):
        if not isinstance(v, list) or len(v) != 4:
            raise ValueError('bbox must be [x, y, width, height]')
        if not all(isinstance(n, (int, float)) for n in v):
            raise ValueError('bbox values must be numbers')
        return v
    
    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError('confidence must be between 0.0 and 1.0')
        return v


class TokensModel(BaseModel):
    """Design tokens for consistent styling."""
    base_spacing: int = 8
    primary_color: str = "#3B82F6"
    accent_color: str = "#F59E0B"
    font_scale: Optional[Dict[str, float]] = None
    border_radius: str = "8px"
    cta_height: Optional[int] = None


class BlueprintModel(BaseModel):
    """Complete blueprint structure for a screen."""
    screen_id: str
    screen_type: str  # "storefront", "product_detail", etc.
    orientation: str  # "portrait" or "landscape"
    tokens: TokensModel
    components: List[ComponentModel]
    meta: Optional[Dict[str, Any]] = None
    
    class Config:
        orm_mode = True
