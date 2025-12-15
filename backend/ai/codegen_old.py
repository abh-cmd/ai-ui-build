def _analyze_blueprint(blueprint: dict) -> dict:
    """Analyze blueprint structure to determine component types needed."""
    components = blueprint.get("components", [])
    analysis = {
        "component_types": {},
        "component_list": [],
        "component_count": {}
    }
    
    for i, comp in enumerate(components):
        comp_type = comp.get("type", "unknown")
        comp_role = comp.get("role", "content")
        comp_id = comp.get("id", f"comp_{i}")
        
        if comp_type not in analysis["component_types"]:
            analysis["component_types"][comp_type] = []
            analysis["component_count"][comp_type] = 0
        
        analysis["component_types"][comp_type].append(comp)
        analysis["component_count"][comp_type] += 1
        analysis["component_list"].append({
            "id": comp_id,
            "type": comp_type,
            "role": comp_role,
            "index": i,
            "data": comp
        })
    
    return analysis


def _generate_header(component: dict, tokens: dict) -> str:
    """Generate Header.jsx from header component."""
    text = component.get("text", "Welcome")
    visual = component.get("visual", {})
    bg_color = visual.get("bg_color", tokens.get("primary_color", "#3B82F6"))
    text_color = visual.get("text_color", tokens.get("accent_color", "#FFFFFF"))
    
    return f'''export default function Header() {{
  return (
    <header className="px-4 py-6" style={{{{backgroundColor: "{bg_color}", color: "{text_color}"}}}} >
      <h1 className="text-2xl font-bold">{text}</h1>
    </header>
  );
}}
'''


def _generate_product_card(component: dict, tokens: dict, include_data: bool = False) -> str:
    """Generate ProductCard.jsx component."""
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


def _generate_divider(component: dict, tokens: dict) -> str:
    """Generate Divider.jsx component."""
    visual = component.get("visual", {})
    color = visual.get("color", tokens.get("accent_color", "#000000"))
    thickness = visual.get("thickness", "1px")
    
    return f'''export default function Divider() {{
  return (
    <div style={{{{height: "{thickness}", backgroundColor: "{color}", margin: "16px 0"}}}} />
  );
}}
'''


def _generate_product_grid(components: list, tokens: dict) -> str:
    """Generate ProductGrid.jsx for multiple product cards in 2-column grid."""
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


def _generate_cta_button(component: dict, tokens: dict) -> str:
    """Generate CTA button component."""
    text = component.get("text", "Click Me")
    visual = component.get("visual", {})
    # Get button colors from visual properties
    bg_color = visual.get("background_color", tokens.get("primary_color", "#FFFFFF"))
    text_color = visual.get("text_color", tokens.get("accent_color", "#000000"))
    
    return f'''export default function CTAButton({{ text = "{text}" }}) {{
  return (
    <button className="w-full py-3 font-semibold rounded-lg hover:opacity-90 transition" style={{{{backgroundColor: "{bg_color}", color: "{text_color}"}}}} >
      {{text}}
    </button>
  );
}}
'''


def _generate_hero_section(component: dict, tokens: dict) -> str:
    """Generate HeroSection.jsx component."""
    text = component.get("text", "Welcome to Our Store")
    visual = component.get("visual", {})
    bg_color = visual.get("bg_color", tokens.get("primary_color", "#3B82F6"))
    
    return f'''export default function HeroSection({{ text = "{text}", bgColor = "{bg_color}" }}) {{
  return (
    <section className="text-white px-4 py-12 text-center" style={{{{backgroundColor: bgColor}}}} >
      <h1 className="text-4xl font-bold">{{text}}</h1>
    </section>
  );
}}
'''


def _generate_content_section(component: dict, tokens: dict) -> str:
    """Generate ContentSection.jsx component."""
    text = component.get("text", "Content goes here")
    
    return f'''export default function ContentSection({{ text = "{text}" }}) {{
  return (
    <section className="px-4 py-6">
      <p className="text-gray-700 leading-relaxed">{{text}}</p>
    </section>
  );
}}
'''


def _generate_footer(component: dict, tokens: dict) -> str:
    """Generate Footer.jsx component."""
    text = component.get("text", "Footer")
    visual = component.get("visual", {})
    bg_color = visual.get("bg_color", tokens.get("primary_color", "#3B82F6"))
    
    return f'''export default function Footer({{ text = "{text}", bgColor = "{bg_color}" }}) {{
  return (
    <footer className="px-4 py-6 text-center" style={{{{backgroundColor: bgColor, color: "white"}}}} >
      <p>{{text}}</p>
    </footer>
  );
}}
'''


def _generate_text_section(component: dict, tokens: dict) -> str:
    """Generate TextSection.jsx component."""
    text = component.get("text", "This is a text section")
    visual = component.get("visual", {})
    text_color = visual.get("text_color", "#1F2937")
    
    return f'''export default function TextSection() {{
  return (
    <section className="px-4 py-6">
      <p className="text-gray-800 leading-relaxed text-base">{text}</p>
    </section>
  );
}}
'''


def _generate_bullet_list(component: dict, tokens: dict) -> str:
    """Generate BulletList.jsx component."""
    text = component.get("text", "Item 1\nItem 2\nItem 3")
    items = [item.strip() for item in text.split("\n") if item.strip()]
    
    items_jsx = "".join([f'        <li className="text-gray-700">{item}</li>\n' for item in items])
    
    return f'''export default function BulletList() {{
  return (
    <section className="px-4 py-6">
      <ul className="space-y-3">
{items_jsx}      </ul>
    </section>
  );
}}
'''


def _generate_feature_card(component: dict, tokens: dict) -> str:
    """Generate FeatureCard.jsx component."""
    text = component.get("text", "Feature")
    visual = component.get("visual", {})
    bg_color = visual.get("bg_color", "#FEE2E2")
    text_color = visual.get("text_color", "#1F2937")
    
    bg_class = _hex_to_tailwind_bg(bg_color)
    
    return f'''export default function FeatureCard({{ title, description }}) {{
  return (
    <div className="{bg_class} rounded-lg px-6 py-8">
      <h3 className="text-lg font-semibold text-gray-800">{{title}}</h3>
      <p className="text-gray-700 mt-2">{{description}}</p>
    </div>
  );
}}
'''


def _generate_feature_cards_grid(components: list, tokens: dict) -> str:
    """Generate FeatureCardsGrid.jsx for multiple feature cards."""
    features = []
    for comp in components:
        if comp.get("type") == "feature_card":
            visual = comp.get("visual", {})
            features.append({
                "title": comp.get("text", "Feature"),
                "bg_color": visual.get("bg_color", "#FEE2E2"),
                "text_color": visual.get("text_color", "#1F2937")
            })
    
    features_jsx = "".join([
        f'    {{ title: "{feat["title"]}", description: "Description for {feat["title"]}", bgColor: "{feat["bg_color"]}", textColor: "{feat["text_color"]}" }},\n' 
        for feat in features[:3]
    ])
    
    return f'''export default function FeatureCardsGrid() {{
  const features = [
{features_jsx}  ];

  return (
    <section className="px-3 py-6 space-y-4">
      {{features.map((feature, idx) => (
        <div key={{idx}} className="rounded-lg px-6 py-8" style={{{{backgroundColor: feature.bgColor, color: feature.textColor}}}} >
          <h3 className="text-lg font-semibold">{{feature.title}}</h3>
          <p className="mt-2">{{feature.description}}</p>
        </div>
      ))}}
    </section>
  );
}}
'''


def _generate_text_element(component: dict, tokens: dict) -> str:
    """Generate Text.jsx component for plain text content with flexible styling."""
    text = component.get("text", "Text content")
    visual = component.get("visual", {})
    role = component.get("role", "content")
    
    # Extract styling from visual properties with appropriate defaults
    font_size = visual.get("font_size", "16px")
    font_weight = visual.get("font_weight", "normal")
    text_color = visual.get("text_color", "#1F2937")
    # Try both text_align and text_alignment field names
    text_align = visual.get("text_align") or visual.get("text_alignment", "left")
    
    # For header role, use center alignment and bold by default
    if role == "header":
        if font_weight == "normal":
            font_weight = "bold"
        if text_align == "left":
            text_align = "center"
    
    return f'''export default function Text({{ text = "{text}", fontSize = "{font_size}", fontWeight = "{font_weight}", textColor = "{text_color}", align = "{text_align}" }}) {{
  return (
    <div style={{{{fontSize, fontWeight, color: textColor, textAlign: align, padding: "8px 16px"}}}} >
      {{text}}
    </div>
  );
}}
'''


def _generate_image(component: dict, tokens: dict) -> str:
    """Generate Image.jsx component for displaying images."""
    visual = component.get("visual", {})
    border = visual.get("border", "none")
    bg_color = visual.get("background_color", "#EEEEEE")
    
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


def _generate_label(component: dict, tokens: dict) -> str:
    """Generate Label.jsx component for form labels."""
    text = component.get("text", "Label")
    visual = component.get("visual", {})
    # Use dark color for labels so they're readable
    text_color = visual.get("text_color", "#1F2937")
    
    return f'''export default function Label({{ text = "{text}" }}) {{
  return (
    <label className="block text-sm font-medium" style={{{{color: "{text_color}"}}}} >
      {{text}}
    </label>
  );
}}
'''


def _generate_text_input(component: dict, tokens: dict) -> str:
    """Generate TextInput.jsx component for form inputs."""
    placeholder = component.get("text") or "Enter text"
    visual = component.get("visual", {})
    border_color = visual.get("border_color", tokens.get("primary_color", "#D1D5DB"))
    
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
    """Generate Link.jsx component for clickable links."""
    text = component.get("text", "Link")
    visual = component.get("visual", {})
    link_color = visual.get("link_color", tokens.get("accent_color", "#0000FF"))
    
    return f'''export default function Link({{ text = "{text}", href = "#" }}) {{
  return (
    <a href={{href}} style={{{{color: "{link_color}", cursor: "pointer", textDecoration: "underline"}}}} >
      {{text}}
    </a>
  );
}}
'''


def _generate_menu_item(component: dict, tokens: dict) -> str:
    """Generate MenuItem.jsx component for menu items."""
    text = component.get("text", "Menu Item")
    visual = component.get("visual", {})
    text_color = visual.get("text_color", "#1F2937")
    font_size = visual.get("font_size", "16px")
    
    return f'''export default function MenuItem({{ text = "{text}" }}) {{
  return (
    <div style={{{{fontSize: "{font_size}", color: "{text_color}", padding: "8px 16px"}}}} >
      {{text}}
    </div>
  );
}}
'''


def _generate_price(component: dict, tokens: dict) -> str:
    """Generate Price.jsx component for menu prices."""
    text = component.get("text", "Price")
    visual = component.get("visual", {})
    text_color = visual.get("text_color", tokens.get("accent_color", "#0000FF"))
    font_size = visual.get("font_size", "14px")
    font_weight = visual.get("font_weight", "bold")
    
    return f'''export default function Price({{ text = "{text}" }}) {{
  return (
    <span style={{{{fontSize: "{font_size}", fontWeight: "{font_weight}", color: "{text_color}", padding: "8px 16px"}}}} >
      {{text}}
    </span>
  );
}}
'''


def _hex_to_tailwind_bg(hex_color: str) -> str:
    """Convert hex color to inline style with actual color."""
    if not hex_color:
        return 'style={{backgroundColor: "#3B82F6"}}'
    return f'style={{backgroundColor: "{hex_color}"}}'


def _hex_to_tailwind_text(hex_color: str) -> str:
    """Convert hex color to inline style with actual color."""
    if not hex_color:
        return 'style={{color: "#FFFFFF"}}'
    return f'style={{color: "{hex_color}"}}'


def _generate_tokens_js(blueprint: dict) -> str:
    """Generate tokens.js from blueprint tokens."""
    tokens = blueprint.get("tokens", {})
    base_spacing = tokens.get("base_spacing", 16)
    primary_color = tokens.get("primary_color", "#3B82F6")
    accent_color = tokens.get("accent_color", "#F59E0B")
    border_radius = tokens.get("border_radius", "8px")
    font_scale = tokens.get("font_scale", {})
    
    return f'''// Design tokens
export const tokens = {{
  baseSpacing: {base_spacing},
  primaryColor: "{primary_color}",
  accentColor: "{accent_color}",
  fontScale: {{
    heading: 1.5,
    body: 1.0,
  }},
  borderRadius: "{border_radius}",
}};
'''


def generate_react_project(improved_json: dict) -> dict:
    """
    Generate React + Tailwind code from improved blueprint JSON.
    Blueprint-driven generation: different blueprints produce different files.
    
    Args:
        improved_json: Improved blueprint from autocorrect
    
    Returns:
        dict: { "files": { path: content }, "entry": "src/App.jsx" }
    """
    
    # Analyze blueprint structure
    analysis = _analyze_blueprint(improved_json)
    tokens = improved_json.get("tokens", {})
    components = improved_json.get("components", [])
    
    # Initialize files dict - always include tokens
    files = {}
    files["tokens.js"] = _generate_tokens_js(improved_json)
    
    # Track generated components and their imports
    imports = []
    component_renders = []  # Will track components in blueprint order
    generated_components = set()
    product_grid_data = []  # Store products for grid rendering
    has_product_grid = False
    
    # First pass: generate all component files needed
    for comp_info in analysis["component_list"]:
        comp_type = comp_info["type"]
        comp_data = comp_info["data"]
        comp_id = comp_info["id"]
        
        if comp_type == "header" and "Header" not in generated_components:
            files["src/components/Header.jsx"] = _generate_header(comp_data, tokens)
            imports.append('import Header from "./components/Header";')
            generated_components.add("Header")
        
        elif comp_type == "product_card":
            if "ProductCard" not in generated_components:
                files["src/components/ProductCard.jsx"] = _generate_product_card(comp_data, tokens)
                generated_components.add("ProductCard")
            
            # Check if we have multiple product cards - need ProductGrid
            if analysis["component_count"].get("product_card", 0) > 1:
                if "ProductGrid" not in generated_components:
                    files["src/components/ProductGrid.jsx"] = _generate_product_grid(
                        analysis["component_types"].get("product_card", []), tokens
                    )
                    imports.append('import ProductGrid from "./components/ProductGrid";')
                    generated_components.add("ProductGrid")
                    has_product_grid = True
                    
                    # Collect product data - parse text to extract title and price
                    for i, pc in enumerate(analysis["component_types"].get("product_card", [])):
                        visual = pc.get("visual", {})
                        text_content = pc.get("text", "Product")
                        
                        # Parse text field - try multiple formats:
                        # 1. "Title\nPrice" (newline separated)
                        # 2. "Title Price" (space separated with price starting with $)
                        # 3. "Title" (just title, use fallback price)
                        
                        title = text_content
                        price = None
                        
                        # Try newline split first
                        if "\n" in text_content:
                            parts = text_content.split("\n", 1)
                            title = parts[0].strip()
                            price = parts[1].strip()
                        else:
                            # Try to find price pattern ($ followed by digits)
                            import re
                            price_match = re.search(r'\$[\d.]+', text_content)
                            if price_match:
                                price = price_match.group()
                                # Remove price from text to get title
                                title = text_content.replace(price, "").strip()
                        
                        # Fallback if no price found
                        if not price:
                            price = visual.get("price", f"${(i+1)*10 + 9}.99")
                        
                        # Ensure title is not empty
                        if not title or title == "$":
                            title = "Product"
                        
                        product_grid_data.append({
                            "id": i + 1,
                            "title": title.strip(),
                            "price": price.strip(),
                            "image": visual.get("image_url", "/placeholder.jpg")
                        })
        
        elif comp_type == "button" and comp_data.get("role") == "cta":
            if "CTAButton" not in generated_components:
                files["src/components/CTAButton.jsx"] = _generate_cta_button(comp_data, tokens)
                imports.append('import CTAButton from "./components/CTAButton";')
                generated_components.add("CTAButton")
        
        elif comp_type == "divider":
            if "Divider" not in generated_components:
                files["src/components/Divider.jsx"] = _generate_divider(comp_data, tokens)
                imports.append('import Divider from "./components/Divider";')
                generated_components.add("Divider")
        
        elif comp_type == "text":
            if "Text" not in generated_components:
                files["src/components/Text.jsx"] = _generate_text_element(comp_data, tokens)
                imports.append('import Text from "./components/Text";')
                generated_components.add("Text")
        
        elif comp_type == "image":
            if "Image" not in generated_components:
                files["src/components/Image.jsx"] = _generate_image(comp_data, tokens)
                imports.append('import Image from "./components/Image";')
                generated_components.add("Image")
        
        elif comp_type == "hero_section":
            if "HeroSection" not in generated_components:
                files["src/components/HeroSection.jsx"] = _generate_hero_section(comp_data, tokens)
                imports.append('import HeroSection from "./components/HeroSection";')
                generated_components.add("HeroSection")
        
        elif comp_type == "hero":
            if "HeroSection" not in generated_components:
                files["src/components/HeroSection.jsx"] = _generate_hero_section(comp_data, tokens)
                imports.append('import HeroSection from "./components/HeroSection";')
                generated_components.add("HeroSection")
        
        elif comp_type == "text_section":
            if "TextSection" not in generated_components:
                files["src/components/TextSection.jsx"] = _generate_text_section(comp_data, tokens)
                imports.append('import TextSection from "./components/TextSection";')
                generated_components.add("TextSection")
        
        elif comp_type == "text_block":
            if "ContentSection" not in generated_components:
                files["src/components/ContentSection.jsx"] = _generate_content_section(comp_data, tokens)
                imports.append('import ContentSection from "./components/ContentSection";')
                generated_components.add("ContentSection")
        
        elif comp_type == "bullet_list":
            if "BulletList" not in generated_components:
                files["src/components/BulletList.jsx"] = _generate_bullet_list(comp_data, tokens)
                imports.append('import BulletList from "./components/BulletList";')
                generated_components.add("BulletList")
        
        elif comp_type == "feature_card":
            if analysis["component_count"].get("feature_card", 0) > 1:
                if "FeatureCardsGrid" not in generated_components:
                    files["src/components/FeatureCardsGrid.jsx"] = _generate_feature_cards_grid(
                        analysis["component_types"].get("feature_card", []), tokens
                    )
                    imports.append('import FeatureCardsGrid from "./components/FeatureCardsGrid";')
                    generated_components.add("FeatureCardsGrid")
            else:
                if "FeatureCard" not in generated_components:
                    files["src/components/FeatureCard.jsx"] = _generate_feature_card(comp_data, tokens)
                    imports.append('import FeatureCard from "./components/FeatureCard";')
                    generated_components.add("FeatureCard")
        
        elif comp_type == "footer":
            if "Footer" not in generated_components:
                files["src/components/Footer.jsx"] = _generate_footer(comp_data, tokens)
                imports.append('import Footer from "./components/Footer";')
                generated_components.add("Footer")
        
        elif comp_type == "label":
            if "Label" not in generated_components:
                files["src/components/Label.jsx"] = _generate_label(comp_data, tokens)
                imports.append('import Label from "./components/Label";')
                generated_components.add("Label")
        
        elif comp_type == "text_input" or comp_type == "input":
            if "TextInput" not in generated_components:
                files["src/components/TextInput.jsx"] = _generate_text_input(comp_data, tokens)
                imports.append('import TextInput from "./components/TextInput";')
                generated_components.add("TextInput")
        
        elif comp_type == "link":
            if "Link" not in generated_components:
                files["src/components/Link.jsx"] = _generate_link(comp_data, tokens)
                imports.append('import Link from "./components/Link";')
                generated_components.add("Link")
        
        elif comp_type == "menu_item":
            if "MenuItem" not in generated_components:
                files["src/components/MenuItem.jsx"] = _generate_menu_item(comp_data, tokens)
                imports.append('import MenuItem from "./components/MenuItem";')
                generated_components.add("MenuItem")
        
        elif comp_type == "price":
            if "Price" not in generated_components:
                files["src/components/Price.jsx"] = _generate_price(comp_data, tokens)
                imports.append('import Price from "./components/Price";')
                generated_components.add("Price")
    
    # Second pass: build component renders in blueprint order
    product_card_count = 0
    feature_card_count = 0
    for comp_info in analysis["component_list"]:
        comp_type = comp_info["type"]
        
        if comp_type == "header":
            component_renders.append("<Header />")
        
        elif comp_type == "product_card":
            product_card_count += 1
            # Only render ProductGrid on first product card encounter
            if product_card_count == 1 and has_product_grid:
                component_renders.append("<ProductGrid products={products} />")
        
        elif comp_type == "hero_section":
            component_renders.append("<HeroSection />")
        
        elif comp_type == "hero":
            component_renders.append("<HeroSection />")
        
        elif comp_type == "text_section":
            component_renders.append("<TextSection />")
        
        elif comp_type == "text_block":
            component_renders.append("<ContentSection />")
        
        elif comp_type == "bullet_list":
            component_renders.append("<BulletList />")
        
        elif comp_type == "feature_card":
            feature_card_count += 1
            # Only render FeatureCardsGrid on first feature card encounter if multiple
            if feature_card_count == 1 and analysis["component_count"].get("feature_card", 0) > 1:
                component_renders.append("<FeatureCardsGrid />")
            elif feature_card_count == 1 and analysis["component_count"].get("feature_card", 0) == 1:
                component_renders.append("<FeatureCard title=\"Feature\" description=\"Description\" />")
        
        elif comp_type == "button" and comp_info["data"].get("role") == "cta":
            button_text = comp_info["data"].get("text", "Click Me")
            component_renders.append(f'<CTAButton text="{button_text}" />')
        
        elif comp_type == "divider":
            component_renders.append('<Divider />')
        
        elif comp_type == "text":
            text_content = comp_info["data"].get("text", "Text")
            visual = comp_info["data"].get("visual", {})
            font_size = visual.get("font_size", "16px")
            font_weight = visual.get("font_weight", "normal")
            text_color = visual.get("text_color", "#1F2937")
            # Try both text_align and text_alignment field names
            text_align = visual.get("text_align") or visual.get("text_alignment", "left")
            component_renders.append(f'<Text text="{text_content}" fontSize="{font_size}" fontWeight="{font_weight}" textColor="{text_color}" align="{text_align}" />')
        
        elif comp_type == "image":
            component_renders.append('<Image />')
        
        elif comp_type == "label":
            label_text = comp_info["data"].get("text", "Label")
            component_renders.append(f'<Label text="{label_text}" />')
        
        elif comp_type == "text_input" or comp_type == "input":
            placeholder = comp_info["data"].get("text") or "Enter text"
            component_renders.append(f'<TextInput placeholder="{placeholder}" />')
        
        elif comp_type == "link":
            link_text = comp_info["data"].get("text", "Link")
            component_renders.append(f'<Link text="{link_text}" href="#" />')
        
        elif comp_type == "menu_item":
            item_text = comp_info["data"].get("text", "Menu Item")
            component_renders.append(f'<MenuItem text="{item_text}" />')
        
        elif comp_type == "price":
            price_text = comp_info["data"].get("text", "Price")
            component_renders.append(f'<Price text="{price_text}" />')
        
        elif comp_type == "footer":
            component_renders.append("<Footer />")
    
    # Build App.jsx with all components in correct order
    import_section = "\n".join(imports) if imports else "// No components"
    
    # Build render section - include product data if using ProductGrid
    render_items = "\n      ".join(component_renders) if component_renders else "<div>No components</div>"
    
    if has_product_grid:
        # Use JSON for proper formatting
        import json
        products_str = json.dumps(product_grid_data)
        render_section = f"""
  const products = {products_str};
  
  return (
    <div className="min-h-screen bg-white">
      {render_items}
    </div>
  );"""
    else:
        render_section = f"""
  return (
    <div className="min-h-screen bg-white">
      {render_items}
    </div>
  );"""
    
    app_content = f'''import {{ tokens }} from "./tokens";
{import_section}

export default function App() {{{render_section}
}}
'''
    
    files["src/App.jsx"] = app_content
    
    return {
        "files": files,
        "entry": "src/App.jsx"
    }
