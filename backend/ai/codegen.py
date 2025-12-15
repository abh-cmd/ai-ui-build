"""
Production-grade React code generator from design blueprints.
Handles all component types with proper visual property extraction and rendering.
"""
import json
import re


def _get_visual_property(visual: dict, *keys, default=None):
    """
    Safely extract visual property with multiple key name fallbacks.
    Handles variations like: text_align, textAlign, text_alignment
    """
    if not visual:
        return default
    for key in keys:
        if key in visual:
            return visual[key]
    return default


def _generate_text_element(component: dict, tokens: dict) -> str:
    """Generate flexible Text component with visual properties."""
    text = component.get("text", "Text")
    visual = component.get("visual", {})
    
    # Extract visual properties with fallbacks
    font_size = _get_visual_property(visual, "font_size", "font-size", default="16px")
    font_weight = _get_visual_property(visual, "font_weight", "fontWeight", default="normal")
    text_color = _get_visual_property(visual, "text_color", "color", default="#1F2937")
    text_align = _get_visual_property(visual, "text_align", "text_alignment", "textAlign", default="left")
    
    return f'''export default function Text({{ text = "{text}", fontSize = "{font_size}", fontWeight = "{font_weight}", textColor = "{text_color}", align = "{text_align}" }}) {{
  return (
    <div style={{{{fontSize, fontWeight, color: textColor, textAlign: align, padding: "8px 16px"}}}} >
      {{text}}
    </div>
  );
}}
'''


def _generate_image(component: dict, tokens: dict) -> str:
    """Generate Image component with styling."""
    visual = component.get("visual", {})
    border = _get_visual_property(visual, "border", default="none")
    bg_color = _get_visual_property(visual, "background_color", "backgroundColor", default="#EEEEEE")
    
    return f'''export default function Image({{ src = "/placeholder.jpg", alt = "Image" }}) {{
  return (
    <img 
      src={{src}} 
      alt={{alt}} 
      className="w-full h-auto object-cover" 
      style={{{{border: "{border}", backgroundColor: "{bg_color}"}}}} 
    />
  );
}}
'''


def _generate_header(component: dict, tokens: dict) -> str:
    """Generate Header component."""
    text = component.get("text", "Welcome")
    visual = component.get("visual", {})
    bg_color = _get_visual_property(visual, "bg_color", "background_color", "backgroundColor", 
                                    default=tokens.get("primary_color", "#FFFFFF"))
    text_color = _get_visual_property(visual, "text_color", "color", 
                                     default=tokens.get("accent_color", "#000000"))
    
    return f'''export default function Header() {{
  return (
    <header className="px-4 py-6" style={{{{backgroundColor: "{bg_color}", color: "{text_color}"}}}} >
      <h1 className="text-2xl font-bold">{text}</h1>
    </header>
  );
}}
'''


def _generate_divider(component: dict, tokens: dict) -> str:
    """Generate Divider component."""
    visual = component.get("visual", {})
    color = _get_visual_property(visual, "color", default=tokens.get("accent_color", "#000000"))
    thickness = _get_visual_property(visual, "thickness", default="1px")
    
    return f'''export default function Divider() {{
  return (
    <div style={{{{height: "{thickness}", backgroundColor: "{color}", margin: "16px 0"}}}} />
  );
}}
'''


def _generate_cta_button(component: dict, tokens: dict) -> str:
    """Generate CTA Button with correct colors."""
    text = component.get("text", "Click Me")
    visual = component.get("visual", {})
    bg_color = _get_visual_property(visual, "background_color", "backgroundColor", 
                                   default=tokens.get("primary_color", "#FFFFFF"))
    text_color = _get_visual_property(visual, "text_color", "color", 
                                     default=tokens.get("accent_color", "#000000"))
    
    return f'''export default function CTAButton({{ text = "{text}" }}) {{
  return (
    <button className="w-full py-3 font-semibold rounded-lg hover:opacity-90 transition" style={{{{backgroundColor: "{bg_color}", color: "{text_color}"}}}} >
      {{text}}
    </button>
  );
}}
'''


def _generate_label(component: dict, tokens: dict) -> str:
    """Generate Label component."""
    text = component.get("text", "Label")
    visual = component.get("visual", {})
    text_color = _get_visual_property(visual, "text_color", "color", default="#1F2937")
    
    return f'''export default function Label({{ text = "{text}" }}) {{
  return (
    <label className="block text-sm font-medium" style={{{{color: "{text_color}"}}}} >
      {{text}}
    </label>
  );
}}
'''


def _generate_text_input(component: dict, tokens: dict) -> str:
    """Generate TextInput component."""
    placeholder = component.get("text") or "Enter text"
    visual = component.get("visual", {})
    border_color = _get_visual_property(visual, "border_color", "borderColor", 
                                       default=tokens.get("primary_color", "#D1D5DB"))
    
    return f'''export default function TextInput({{ placeholder = "{placeholder}", type = "text" }}) {{
  return (
    <input
      type={{type}}
      placeholder={{placeholder}}
      className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2"
      style={{{{borderColor: "{border_color}", outline: "none"}}}}
    />
  );
}}
'''


def _generate_link(component: dict, tokens: dict) -> str:
    """Generate Link component."""
    text = component.get("text", "Link")
    visual = component.get("visual", {})
    link_color = _get_visual_property(visual, "text_color", "color", 
                                     default=tokens.get("primary_color", "#3B82F6"))
    
    return f'''export default function Link({{ text = "{text}", href = "#" }}) {{
  return (
    <a href={{href}} style={{{{color: "{link_color}", textDecoration: "none"}}}} >
      {{text}}
    </a>
  );
}}
'''


def _generate_hero_section(component: dict, tokens: dict) -> str:
    """Generate HeroSection component."""
    text = component.get("text", "Welcome")
    visual = component.get("visual", {})
    bg_color = _get_visual_property(visual, "bg_color", "background_color", "backgroundColor", 
                                   default=tokens.get("primary_color", "#3B82F6"))
    
    return f'''export default function HeroSection({{ text = "{text}", bgColor = "{bg_color}" }}) {{
  return (
    <section className="text-white px-4 py-12 text-center" style={{{{backgroundColor: bgColor}}}} >
      <h1 className="text-4xl font-bold">{{text}}</h1>
    </section>
  );
}}
'''


def _generate_tokens_js(blueprint: dict) -> str:
    """Generate tokens.js from blueprint tokens."""
    tokens = blueprint.get("tokens", {})
    
    base_spacing = tokens.get("base_spacing", 16)
    primary_color = tokens.get("primary_color", "#FFFFFF")
    accent_color = tokens.get("accent_color", "#000000")
    border_radius = tokens.get("border_radius", "0px")
    font_scale = tokens.get("font_scale", {"heading": 1.5, "body": 1.0})
    
    return f'''// Design tokens
export const tokens = {{
  baseSpacing: {base_spacing},
  primaryColor: "{primary_color}",
  accentColor: "{accent_color}",
  fontScale: {{
    heading: {font_scale.get("heading", 1.5)},
    body: {font_scale.get("body", 1.0)},
  }},
  borderRadius: "{border_radius}",
}};
'''


def generate_react_project(blueprint: dict) -> dict:
    """
    Generate complete React project from blueprint.
    Properly handles all component types and visual properties.
    """
    tokens = blueprint.get("tokens", {})
    files = {}
    imports = []
    component_renders = []
    generated_components = set()
    product_grid_data = []
    has_product_grid = False
    
    # Generate tokens
    files["tokens.js"] = _generate_tokens_js(blueprint)
    # Don't add to imports here - it will be added to the template directly
    
    # Analyze blueprint
    components = blueprint.get("components", [])
    component_count = {}
    for comp in components:
        comp_type = comp.get("type", "unknown")
        component_count[comp_type] = component_count.get(comp_type, 0) + 1
    
    # FIRST PASS: Generate all unique component files
    for comp in components:
        comp_type = comp.get("type", "unknown")
        
        if comp_type == "header":
            if "Header" not in generated_components:
                files["src/components/Header.jsx"] = _generate_header(comp, tokens)
                imports.append('import Header from "./components/Header";')
                generated_components.add("Header")
        
        elif comp_type == "text":
            if "Text" not in generated_components:
                files["src/components/Text.jsx"] = _generate_text_element(comp, tokens)
                imports.append('import Text from "./components/Text";')
                generated_components.add("Text")
        
        elif comp_type == "image":
            if "Image" not in generated_components:
                files["src/components/Image.jsx"] = _generate_image(comp, tokens)
                imports.append('import Image from "./components/Image";')
                generated_components.add("Image")
        
        elif comp_type == "divider":
            if "Divider" not in generated_components:
                files["src/components/Divider.jsx"] = _generate_divider(comp, tokens)
                imports.append('import Divider from "./components/Divider";')
                generated_components.add("Divider")
        
        elif comp_type == "button" and comp.get("role") == "cta":
            if "CTAButton" not in generated_components:
                files["src/components/CTAButton.jsx"] = _generate_cta_button(comp, tokens)
                imports.append('import CTAButton from "./components/CTAButton";')
                generated_components.add("CTAButton")
        
        elif comp_type == "product_card":
            if "ProductCard" not in generated_components:
                files["src/components/ProductCard.jsx"] = _product_card_component()
                generated_components.add("ProductCard")
            
            # Handle multiple product cards
            if component_count.get("product_card", 0) > 1 and "ProductGrid" not in generated_components:
                files["src/components/ProductGrid.jsx"] = _product_grid_component()
                imports.append('import ProductGrid from "./components/ProductGrid";')
                generated_components.add("ProductGrid")
                has_product_grid = True
                
                # Extract product data
                for i, pc in enumerate([c for c in components if c.get("type") == "product_card"]):
                    text_content = pc.get("text", "Product")
                    visual = pc.get("visual", {})
                    
                    # Parse text for title/price
                    title = text_content
                    price = None
                    
                    # Try newline split
                    if "\n" in text_content:
                        parts = text_content.split("\n", 1)
                        title = parts[0].strip()
                        price = parts[1].strip()
                    else:
                        # Try regex for price pattern
                        price_match = re.search(r'\$[\d.]+', text_content)
                        if price_match:
                            price = price_match.group()
                            title = text_content.replace(price, "").strip()
                    
                    if not price:
                        price = f"${(i+1)*10 + 9}.99"
                    if not title:
                        title = "Product"
                    
                    product_grid_data.append({
                        "id": i + 1,
                        "title": title.strip(),
                        "price": price.strip(),
                        "image": visual.get("image_url", "/placeholder.jpg")
                    })
        
        elif comp_type == "label":
            if "Label" not in generated_components:
                files["src/components/Label.jsx"] = _generate_label(comp, tokens)
                imports.append('import Label from "./components/Label";')
                generated_components.add("Label")
        
        elif comp_type == "text_input" or comp_type == "input":
            if "TextInput" not in generated_components:
                files["src/components/TextInput.jsx"] = _generate_text_input(comp, tokens)
                imports.append('import TextInput from "./components/TextInput";')
                generated_components.add("TextInput")
        
        elif comp_type == "link":
            if "Link" not in generated_components:
                files["src/components/Link.jsx"] = _generate_link(comp, tokens)
                imports.append('import Link from "./components/Link";')
                generated_components.add("Link")
        
        elif comp_type == "hero_section" or comp_type == "hero":
            if "HeroSection" not in generated_components:
                files["src/components/HeroSection.jsx"] = _generate_hero_section(comp, tokens)
                imports.append('import HeroSection from "./components/HeroSection";')
                generated_components.add("HeroSection")
    
    # SECOND PASS: Render components in blueprint order
    product_card_rendered = False
    for comp in components:
        comp_type = comp.get("type", "unknown")
        comp_role = comp.get("role", "content")
        
        if comp_type == "header":
            component_renders.append("<Header />")
        
        elif comp_type == "divider":
            component_renders.append("<Divider />")
        
        elif comp_type == "text":
            text_content = comp.get("text", "Text")
            visual = comp.get("visual", {})
            font_size = _get_visual_property(visual, "font_size", "font-size", default="16px")
            font_weight = _get_visual_property(visual, "font_weight", "fontWeight", default="normal")
            text_color = _get_visual_property(visual, "text_color", "color", default="#1F2937")
            text_align = _get_visual_property(visual, "text_align", "text_alignment", "textAlign", default="left")
            component_renders.append(f'<Text text="{text_content}" fontSize="{font_size}" fontWeight="{font_weight}" textColor="{text_color}" align="{text_align}" />')
        
        elif comp_type == "image":
            component_renders.append('<Image />')
        
        elif comp_type == "product_card":
            if not product_card_rendered and has_product_grid:
                component_renders.append("<ProductGrid products={products} />")
                product_card_rendered = True
        
        elif comp_type == "button" and comp_role == "cta":
            button_text = comp.get("text", "Click Me")
            component_renders.append(f'<CTAButton text="{button_text}" />')
        
        elif comp_type == "label":
            label_text = comp.get("text", "Label")
            component_renders.append(f'<Label text="{label_text}" />')
        
        elif comp_type == "text_input" or comp_type == "input":
            placeholder = comp.get("text") or "Enter text"
            component_renders.append(f'<TextInput placeholder="{placeholder}" />')
        
        elif comp_type == "link":
            link_text = comp.get("text", "Link")
            component_renders.append(f'<Link text="{link_text}" href="#" />')
        
        elif comp_type == "hero_section" or comp_type == "hero":
            hero_text = comp.get("text", "Welcome")
            component_renders.append(f'<HeroSection text="{hero_text}" />')
    
    # Generate App.jsx
    import_section = "\n".join(imports) if imports else "// No imports"
    render_items = "\n      ".join(component_renders) if component_renders else "<div>No components</div>"
    
    if has_product_grid:
        products_json = json.dumps(product_grid_data)
        app_jsx = f'''import {{ tokens }} from "./tokens";
{import_section}

export default function App() {{
  const products = {products_json};
  
  return (
    <div className="min-h-screen bg-white">
      {render_items}
    </div>
  );
}}
'''
    else:
        app_jsx = f'''import {{ tokens }} from "./tokens";
{import_section}

export default function App() {{
  return (
    <div className="min-h-screen bg-white">
      {render_items}
    </div>
  );
}}
'''
    
    files["src/App.jsx"] = app_jsx
    
    return {
        "files": files,
        "entry": "src/App.jsx"
    }


def _product_card_component() -> str:
    """Product card component."""
    return '''export default function ProductCard({ title, price, image }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <img
        src={image}
        alt={title}
        className="w-full aspect-square object-cover"
      />
      <div className="p-4">
        <h2 className="text-lg font-semibold text-gray-800">{title}</h2>
        <p className="text-xl font-bold text-amber-600 mt-2">{price}</p>
      </div>
    </div>
  );
}
'''


def _product_grid_component() -> str:
    """Product grid component."""
    return '''export default function ProductGrid({ products }) {
  return (
    <div className="grid grid-cols-2 gap-4 px-3 py-6">
      {products.map((product) => (
        <div key={product.id} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <img
            src={product.image}
            alt={product.title}
            className="w-full aspect-square object-cover"
          />
          <div className="p-4">
            <h2 className="text-lg font-semibold text-gray-800">{product.title}</h2>
            <p className="text-xl font-bold text-amber-600 mt-2">{product.price}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
'''
