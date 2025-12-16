# Code Generation Fix - Restaurant Menu Example

## Problem
The code generation was incomplete. It only generated:
- 2 hardcoded CTAButton components
- Missing all text components (header, section, menu items)
- Buttons didn't accept text props (hardcoded "order now!")

## Root Causes
1. **No text component generator** - Blueprint extracted text types but codegen had no handler
2. **No text rendering logic** - Second pass didn't render text components to App.jsx
3. **CTAButton not accepting props** - Buttons had hardcoded text, couldn't render different labels

## Solution Implemented

### 1. Added Text Component Generator
```python
def _generate_text_element(component: dict, tokens: dict) -> str:
    """Generate Text.jsx component for plain text content with flexible styling."""
    # Extracts: font_size, font_weight, text_color, text_alignment
    # Handles both 'header' and 'content' roles appropriately
    # Returns flexible component accepting props
```

### 2. Added Text Type Handling in First Pass
```python
elif comp_type == "text":
    if "Text" not in generated_components:
        files["src/components/Text.jsx"] = _generate_text_element(comp_data, tokens)
        imports.append('import Text from "./components/Text";')
        generated_components.add("Text")
```

### 3. Added Text Rendering in Second Pass
```python
elif comp_type == "text":
    text_content = comp_info["data"].get("text", "Text")
    visual = comp_info["data"].get("visual", {})
    # Extract font_size, font_weight, text_color, text_alignment
    # Render: <Text text="..." fontSize="..." fontWeight="..." ... />
```

### 4. Fixed CTAButton to Accept Text Props
```python
def _generate_cta_button(component: dict, tokens: dict) -> str:
    """Generate CTA button component."""
    # Changed from: <button>order now!</button>
    # To: export default function CTAButton({ text = "..." }) { ... {text} ... }
```

### 5. Updated Button Rendering to Pass Text
```python
elif comp_type == "button" and comp_info["data"].get("role") == "cta":
    button_text = comp_info["data"].get("text", "Click Me")
    component_renders.append(f'<CTAButton text="{button_text}" />')
```

## Results

### Before
```jsx
// Only 2 components, same button twice
<div className="min-h-screen bg-white">
  <CTAButton />
  <CTAButton />
</div>
```

### After
```jsx
// All 6 components with proper text
<div className="min-h-screen bg-white">
  <Text text="PANCHAKATTU DOSA" fontSize="24px" fontWeight="bold" textColor="#1F2937" align="center" />
  <Text text="Our Specials:" fontSize="16px" fontWeight="medium" textColor="#1F2937" align="left" />
  <Text text="1. Podi idly : 100 ruppees" fontSize="16px" fontWeight="normal" textColor="#1F2937" align="left" />
  <Text text="2. Kaaram Dosa: 150ruppees" fontSize="16px" fontWeight="normal" textColor="#1F2937" align="left" />
  <CTAButton text="order now!" />
  <CTAButton text="our branches" />
</div>
```

## Generated Components

### Text.jsx (NEW)
```jsx
export default function Text({ 
  text = "Text", 
  fontSize = "16px", 
  fontWeight = "normal", 
  textColor = "#1F2937", 
  align = "left" 
}) {
  return (
    <div style={{
      fontSize, 
      fontWeight, 
      color: textColor, 
      textAlign: align, 
      padding: "8px 16px"
    }}>
      {text}
    </div>
  );
}
```

### CTAButton.jsx (FIXED)
- Now accepts `text` prop
- Dynamic button labels
- Blue background with white text
- Hover effects and transitions

## Testing
✅ Generated 4 files (was 2)
✅ All 6 blueprint components rendered
✅ Text content extracted from Gemini analysis
✅ Proper styling applied based on roles
✅ No hardcoded values

## Impact
- Complex layouts now supported (menu with multiple text + buttons)
- Dynamic content generation from Gemini analysis
- Flexible text styling based on component roles
- Scalable to more complex designs
