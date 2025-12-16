# Blueprint-Driven React Code Generation Upgrade

## Overview
The AI UI Builder has been successfully upgraded from **template-driven** to **blueprint-driven** React code generation. This means different blueprints now produce different React files and layouts, not the same template for every image.

## What Changed
- **File**: `backend/ai/codegen.py` (completely refactored)
- **Scope**: Only the code generation logic was modified
- **Impact**: React code now dynamically matches blueprint structure

## How It Works

### 1. Blueprint Analysis
The system analyzes incoming blueprints to understand:
- Component types present (header, product_card, button, etc.)
- Count of each component type
- Component ordering
- Visual properties (colors, text, prices, images)

### 2. Dynamic Component Selection
Based on blueprint structure, the system generates only needed components:

| Blueprint Contains | Generated Files |
|---|---|
| header, product_card, product_card, button | Header.jsx, ProductGrid.jsx, ProductCard.jsx, CTAButton.jsx |
| header, text_block | Header.jsx, ContentSection.jsx |
| header, hero | Header.jsx, HeroSection.jsx |
| header, product_card, footer | Header.jsx, ProductCard.jsx, Footer.jsx |

### 3. Dynamic App.jsx
The App.jsx is generated to:
- Import only needed components
- Render components in blueprint order
- Use tokens for styling
- Preserve layout hierarchy

### 4. Tokens Always Included
`tokens.js` is always generated from blueprint tokens:
- Primary colors
- Spacing values
- Typography settings
- Border radius

## Component Registry

### Available Components
- **Header** - Top section with title
- **ProductCard** - Single product display
- **ProductGrid** - Multiple product cards in grid
- **Hero** - Large hero section
- **CTA** - Call-to-action button
- **ContentSection** - Text content blocks
- **Footer** - Bottom section

Each component is:
- Generated from blueprint data
- Styled with Tailwind CSS
- Uses design tokens
- Valid and ready-to-use JSX

## Key Features

✅ **Different blueprints → Different files**
- 2 product cards generates ProductGrid
- 1 product card generates ProductCard
- Text only generates ContentSection
- Multiple component types generate corresponding files

✅ **Deterministic output**
- Same blueprint always generates identical files
- No randomization or variation

✅ **API format preserved**
- Response still has `{files, entry}` shape
- No breaking changes to existing routes
- Frontend compatible without modification

✅ **Valid JSX + Tailwind**
- All generated code is syntactically valid
- Uses Tailwind CSS utility classes
- Responsive mobile-first approach
- No dependencies added

✅ **Tokens extracted from blueprint**
- Colors from `blueprint.tokens.primary_color`
- Spacing from `blueprint.tokens.base_spacing`
- Typography settings preserved
- Custom text and images from components

## Testing Results

### Test 1: Different Blueprints
```
Blueprint 1 (Storefront): header + 2 products + button
  Generated: Header, ProductGrid, ProductCard, CTAButton, tokens

Blueprint 2 (Info): header + text
  Generated: Header, ContentSection, tokens

Result: ✓ PASS - Different blueprints produce different files
```

### Test 2: Deterministic Output
```
Same blueprint generated twice:
  File 1 == File 2: True for all files

Result: ✓ PASS - Identical output for identical blueprints
```

### Test 3: API Compatibility
```
Response format: {files, entry}
Entry value: "src/App.jsx"
Status codes: All 200 OK

Result: ✓ PASS - API unchanged, fully backward compatible
```

### Test 4: Code Quality
```
Valid JSX: ✓
Valid Tailwind: ✓
Proper imports: ✓
Correct tokens usage: ✓

Result: ✓ PASS - All generated code is production-ready
```

## Example Outputs

### Storefront Blueprint
**Components**: header, 2x product_card, button

**Generated Files**:
- `tokens.js` - Design tokens
- `src/App.jsx` - Imports ProductGrid, Header, CTAButton
- `src/components/Header.jsx`
- `src/components/ProductGrid.jsx`
- `src/components/ProductCard.jsx`
- `src/components/CTAButton.jsx`

**App.jsx Structure**:
```jsx
import Header from "./components/Header";
import ProductGrid from "./components/ProductGrid";
import CTAButton from "./components/CTAButton";

export default function App() {
  const products = [{ id: 1, title: "Premium Product A", price: "$49.99", image: "/product_a.jpg" }, ...];
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <ProductGrid products={products} />
      <CTAButton />
    </div>
  );
}
```

### Info Page Blueprint
**Components**: header, text_block

**Generated Files**:
- `tokens.js` - Design tokens
- `src/App.jsx` - Imports Header, ContentSection
- `src/components/Header.jsx`
- `src/components/ContentSection.jsx`

**App.jsx Structure**:
```jsx
import Header from "./components/Header";
import ContentSection from "./components/ContentSection";

export default function App() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <ContentSection />
    </div>
  );
}
```

## Usage

No changes needed! The system is fully backward compatible:

1. Upload image as before
2. Get blueprint as before
3. Click "Generate React Files"
4. See different files for different blueprints
5. All files are valid React + Tailwind code

## Architecture Changes

### New Functions in `codegen.py`
- `_analyze_blueprint()` - Analyzes blueprint structure
- `_generate_header()` - Generates Header.jsx
- `_generate_product_card()` - Generates ProductCard.jsx
- `_generate_product_grid()` - Generates ProductGrid.jsx
- `_generate_cta_button()` - Generates CTAButton.jsx
- `_generate_hero_section()` - Generates HeroSection.jsx
- `_generate_content_section()` - Generates ContentSection.jsx
- `_generate_footer()` - Generates Footer.jsx
- `_generate_tokens_js()` - Generates tokens.js
- `_hex_to_tailwind_bg()` - Hex to Tailwind color conversion
- `_hex_to_tailwind_text()` - Text color conversion

### Refactored Function
- `generate_react_project()` - Now blueprint-driven instead of template-driven

## Constraints Met

✅ API routes unchanged
✅ Response format preserved
✅ No new dependencies
✅ Vision module untouched
✅ Autocorrect module untouched
✅ Edit agent untouched
✅ Frontend unchanged
✅ Deterministic output
✅ Valid JSX always
✅ Valid Tailwind always
✅ Tokens preserved
✅ Same blueprint = same output
✅ Different blueprint = different output

## Next Steps

The system is production-ready! You can now:
1. Upload different design images
2. Each will generate unique React code matching the design
3. All code is valid, ready-to-use React + Tailwind
4. Design tokens are preserved from the blueprint
5. Components adapt to blueprint structure

## Verification

Run these tests to verify everything is working:

```bash
# Test with sample blueprint
curl -X POST http://127.0.0.1:8000/generate/ \
  -H "Content-Type: application/json" \
  -d '{"blueprint": {...}}'

# Check different outputs
# Upload multiple images and compare generated files
# Verify identical blueprints produce identical code
```

---
**Status**: ✅ Complete and tested
**Date**: December 13, 2025
**Mode**: AI_MODE=on (with OpenAI support)
