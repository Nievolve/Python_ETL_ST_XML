import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import re
import os

def parse_st_content(content):
    """Extraherar namn, variabler och logik från ST-kod."""
    # Extrahera FB Namn
    fb_name_match = re.search(r"FUNCTION_BLOCK\s+(\w+)", content)
    fb_name = fb_name_match.group(1) if fb_name_match else "UnknownFB"

    # Extrahera logik (allt mellan sista END_VAR och END_FUNCTION_BLOCK)
    # Vi letar efter sista förekomsten av END_VAR
    parts = re.split(r"END_VAR", content)
    if len(parts) > 1:
        logic = parts[-1].replace("END_FUNCTION_BLOCK", "").strip()
    else:
        logic = content.strip()

    # Extrahera variabler (enkel parsing för demo)
    var_pattern = re.compile(r"(\w+)\s*:\s*(\w+)\s*(?:[:=]+\s*([^;]+))?;")
    variables = var_pattern.findall(content)
    
    return fb_name, variables, logic

def create_plc_xml(st_file_path, output_xml_path):
    with open(st_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    fb_name, vars_found, logic_code = parse_st_content(content)

    # XML Setup
    XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
    ET.register_namespace('xsi', XSI_NS)
    root = ET.Element("FunctionBlock", name=fb_name)
    
    # Skapa variabler i XML baserat på parsing
    vars_node = ET.SubElement(root, "Vars", accessSpecifier="private")
    for var_name, var_type, init_val in vars_found:
        v = ET.SubElement(vars_node, "Variable", name=var_name)
        t = ET.SubElement(v, "Type")
        ET.SubElement(t, "TypeName").text = var_type
        if init_val:
            iv = ET.SubElement(v, "InitialValue")
            ET.SubElement(iv, "SimpleValue", value=init_val.strip())

    # MainBody
    main_body = ET.SubElement(root, "MainBody")
    body_content = ET.SubElement(main_body, "BodyContent")
    body_content.set(f"{{{XSI_NS}}}type", "ST")
    st_node = ET.SubElement(body_content, "ST")
    
    placeholder = "___LOGIC_PLACEHOLDER___"
    st_node.text = placeholder

    # Prettify
    xml_str = ET.tostring(root, encoding='utf-8')
    reparsed = minidom.parseString(xml_str)
    pretty_xml = reparsed.toprettyxml(indent="    ")

    # Sätt in ren logik i CDATA
    final_xml = pretty_xml.replace(placeholder, f"<![CDATA[\n{logic_code}\n        ]]>")

    with open(output_xml_path, "w", encoding='utf-8') as f:
        f.write(final_xml)

    print(f"Konvertering klar: {fb_name} -> {output_xml_path}")

if __name__ == "__main__":
    create_plc_xml("logic.st", "ST_FB.xml")
