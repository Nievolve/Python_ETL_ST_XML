import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os

def create_plc_xml(st_file_path, output_xml_path):
    # 1. Läs innehållet från .st filen
    try:
        with open(st_file_path, 'r', encoding='utf-8') as f:
            st_content = f.read()
    except FileNotFoundError:
        print(f"Fel: Filen {st_file_path} hittades inte.")
        return

    # 2. Skapa XML-strukturen
    fb_name = os.path.splitext(os.path.basename(st_file_path))[0]
    
    root = ET.Element("FunctionBlock", name=fb_name)
    
    # Parametrar (Output)
    parameters = ET.SubElement(root, "Parameters")
    output_vars = ET.SubElement(parameters, "OutputVars")
    out_var = ET.SubElement(output_vars, "Variable", name="Output", orderWithinParamSet="1")
    out_type = ET.SubElement(out_var, "Type")
    ET.SubElement(out_type, "TypeName").text = "BOOL"

    # Variabler (Exempel på privata variabler)
    vars_node = ET.SubElement(root, "Vars", accessSpecifier="private")
    
    # Här kan man bygga ut logik för att parsa VAR_INPUT/VAR i .st filen dynamiskt
    # Just nu lägger vi till S1 som ett exempel
    var_s1 = ET.SubElement(vars_node, "Variable", name="S1")
    s1_type = ET.SubElement(var_s1, "Type")
    ET.SubElement(s1_type, "TypeName").text = "BOOL"
    s1_init = ET.SubElement(var_s1, "InitialValue")
    ET.SubElement(s1_init, "SimpleValue", value="TRUE")

    # MainBody med CDATA
    main_body = ET.SubElement(root, "MainBody")
    body_content = ET.SubElement(main_body, "BodyContent")
    body_content.set("xsi:type", "ST")
    
    st_node = ET.SubElement(body_content, "ST")
    # Vi använder en platshållare för CDATA då ElementTree inte hanterar det nativt vid skapande
    st_node.text = st_content

    # 3. Formatera XML (Prettify) och hantera CDATA manuellt
    xml_str = ET.tostring(root, encoding='utf-8')
    reparsed = minidom.parseString(xml_str)
    pretty_xml = reparsed.toprettyxml(indent="    ")

    # För att få exakt CDATA-struktur i filen:
    # (En enkel strängersättning för att kapsla in koden korrekt)
    final_xml = pretty_xml.replace(st_content, f"<![CDATA[\n{st_content}\n]]>")

    # 4. Spara till fil
    with open(output_xml_path, "w", encoding='utf-8') as f:
        f.write(final_xml)
    
    print(f"Klart! XML har skapats: {output_xml_path}")

# Kör programmet
if __name__ == "__main__":
    # Ändra dessa namn så de matchar dina filer
    input_file = "logic.st"
    output_file = "ST_FB.xml"
    
    # Skapa en testfil om den inte finns
    #if not os.path.exists(input_file):
    #    with open(input_file, "w") as f:
    #        f.write("// PLC logik\nS1TON(IN := S1, PT := T#1S);\nIF S1TON.Q THEN\n    S1 := FALSE;\nEND_IF;")

    create_plc_xml(input_file, output_file)
