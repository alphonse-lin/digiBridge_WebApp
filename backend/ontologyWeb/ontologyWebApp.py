from flask import Flask, render_template, request, jsonify
from owlready2 import *
import json
import os
app = Flask(__name__)
data_out_dir=os.path.join(os.path.dirname(__file__), 'data')
owl_file=os.path.join(os.path.dirname(__file__), 'data', 'v3-BMO.owl')
json_file_path=os.path.join(os.path.dirname(__file__), 'result.json')

def init_model():
    # downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    # json_file_path = os.path.join(downloads_folder, 'result.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    depth_of_corrosion = data['Severe corrosion percentage']
    if depth_of_corrosion > 30:
        depth_of_corrosion = 8
    else:  # inserted
        if depth_of_corrosion > 5:
            depth_of_corrosion = 3
        else:  # inserted
            depth_of_corrosion = 0.5
    percentage_of_surface = data['Total corrosion percentage']
    onto = get_ontology(owl_file)
    onto.load()
    with onto:
        rule = Imp()
        rule.set_as_rule('Corrosion(?C)^visibleDefect(?C,false) -> severityRating(?C,\"A\")^extentRating(?C,1)')
        rule = Imp()
        rule.set_as_rule('Corrosion(?C) ^ maxDepth(?C, ?Cd) ^ lessThan(?Cd, 1) ^ throughSection(?C, false) -> severityRating(?C, \"B\")')
        rule = Imp()
        rule.set_as_rule('Corrosion(?C)^maxDepth(?C,?Cd)^greaterThanOrEqual(?Cd,1)^lessThanOrEqual(?Cd,5)^throughSection(?C,false)-> severityRating(?C,\"C\")')
        rule = Imp()
        rule.set_as_rule('Corrosion(?C)^maxDepth(?C,?Cd)^greaterThan(?Cd,5)^lessThanOrEqual(?Cd,10)^throughSection(?C,false) -> severityRating(?C,\"D\")')
        rule = Imp()
        rule.set_as_rule('Corrosion(?C)^maxDepth(?C,?Cd)^greaterThan(?Cd,10)^throughSection(?C,false) -> severityRating(?C,\"E\")')
        rule = Imp()
        rule.set_as_rule('Corrosion(?C)^throughSection(?C,true) -> severityRating(?C,\"F\")')
        rule = Imp()
        rule.set_as_rule('Corrosion(?C)^hasTears(?C,true) -> severityRating(?C,\"G\")^extentRating(?C,6)')
        rule = Imp()
        rule.set_as_rule('Hazard(?C)^percentage(?C,?Ca)^equal(?Ca,0) -> extentRating(?C,1)')
        rule = Imp()
        rule.set_as_rule('Hazard(?C)^percentage(?C,?Ca)^greaterThan(?Ca,0)^lessThan(?Ca,5) -> extentRating(?C,3)')
        rule = Imp()
        rule.set_as_rule('Hazard(?C)^percentage(?C,?Ca)^greaterThanOrEqual(?Ca,5)^lessThanOrEqual(?Ca,10)-> extentRating(?C,4)')
        rule = Imp()
        rule.set_as_rule('Hazard(?C)^percentage(?C,?Ca)^greaterThan(?Ca,10)^lessThanOrEqual(?Ca,50) -> extentRating(?C,5)')
        rule = Imp()
        rule.set_as_rule('Hazard(?C)^percentage(?C,?Ca)^greaterThan(?Ca,50) -> extentRating(?C,6)')
        rule = Imp()
        rule.set_as_rule('Corrosion(?E)^severityRating(?E,?Es)^equal(?Es,\"A\") -> maintenanceDecision(?E,\"DailyMaintenance: There are no visible corrosion defects to the element.\")')
        rule = Imp()
        rule.set_as_rule('Hazard(?E)^severityRating(?E,?Es)^equal(?Es,\"F\") -> maintenanceDecision(?E,\"RepairMaintenance: There are severe corrosion defects and normal functions have been affected.\")')
        rule = Imp()
        rule.set_as_rule('Hazard(?E)^severityRating(?E,?Es)^equal(?Es,\"G\") -> maintenanceDecision(?E,\"EmergencyMaintenance: Severity G requires immediate notification to Network Rail, otherwise defects shall be noted down and submitted to Network Rail for regional assessment.\")')
        rule = Imp()
        rule.set_as_rule('Hazard(?E)^severityRating(?E, ?Es) ^equal(?Es, \"B\") -> maintenanceDecision(?E, \"PreventiveMaintenance: There are minor corrosion defects but no influence on functions.\")')
        rule = Imp()
        rule.set_as_rule('Hazard(?E)^severityRating(?E, ?Es) ^ equal(?Es, \"C\")  ->maintenanceDecision(?E, \"PreventiveMaintenance: There are medium corrosion defects but can keep normal functions.\")')
        rule = Imp()
        rule.set_as_rule('Hazard(?E)^ severityRating(?E, ?Es)  ^ equal(?Es, \"D\") -> maintenanceDecision(?E, \"PreventiveMaintenance: There are medium corrosion defects but can keep normal functions.\")')
        rule = Imp()
        rule.set_as_rule('Hazard(?E)^ severityRating(?E, ?Es)^ equal(?Es, \"E\")  -> maintenanceDecision(?E, \"PreventiveMaintenance: There are medium corrosion defects but can keep normal functions.\")')
    return onto

def process_corrosionAuto(depth_of_corrosion,percentage_of_surface):
    onto = init_model()
    # get_ontology(owl_file)
    onto.load()
    new_corrosion = onto.Corrosion()
    new_corrosion.throughSection.append(False)
    new_corrosion.maxDepth.append(depth_of_corrosion)
    new_corrosion.percentage.append(percentage_of_surface)
    with onto:
        sync_reasoner_pellet(infer_property_values=True,
                             infer_data_property_values=True)

    result00 = {
        'name': new_corrosion.name,
        'maxDepth': new_corrosion.maxDepth,
        'percentage': new_corrosion.percentage,
        'severityRating': new_corrosion.severityRating,
        'extentRating': new_corrosion.extentRating,
        'maintenanceDecision': new_corrosion.maintenanceDecision
    }

    response_data = {
        'result00': result00,
        'message': [
            f'Based on the Network Rail Standard-Condition Marking of Bridges (NR/L3/CIV/006/2C), for {result00["name"]}({result00["maxDepth"]} mm and {result00["percentage"]}%), its severity rating is {result00["severityRating"]}, and its extent rating is {result00["extentRating"]}.',
            f'The maintenance solution of {result00["name"]} is {result00["maintenanceDecision"]}.'
        ]
    }

    file_path = 'Corrosion file Result.json'
    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
    onto.destroy()
    return response_data

def upload(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        corrosion_depth = data.get('Severe corrosion percentage', 0)
        if corrosion_depth > 30:
            corrosion_depth = 8
        elif corrosion_depth > 5:
            corrosion_depth = 3
        else:
            corrosion_depth = 0.5
        corrosion_percentage = data.get('Total corrosion percentage', 0)
        owl_file = r'ontologyWeb\data\v3-BMO.owl'
        onto = init_model()
        onto.load()
        new_corrosion = onto.Corrosion()
        new_corrosion.throughSection.append(False)
        new_corrosion.maxDepth.append(corrosion_depth)
        new_corrosion.percentage.append(corrosion_percentage)
        with onto:
            sync_reasoner_pellet(infer_property_values=True,
                                 infer_data_property_values=True)

        result0 = {
            'name': new_corrosion.name,
            'maxDepth': new_corrosion.maxDepth,
            'percentage': new_corrosion.percentage,
            'severityRating': new_corrosion.severityRating,
            'extentRating': new_corrosion.extentRating,
            'maintenanceDecision': new_corrosion.maintenanceDecision
        }

        response_data = {
            'result0': result0,
            'message': [
                f'Based on the Network Rail Standard-Condition Marking of Bridges (NR/L3/CIV/006/2C), for {result0["name"]}({result0["maxDepth"]} mm and {result0["percentage"]}%), its severity rating is {result0["severityRating"]}, and its extent rating is {result0["extentRating"]}.',
                f'The maintenance solution of {result0["name"]} is {result0["maintenanceDecision"]}.'
            ]
        }

        output_file_path = os.path.join(data_out_dir, 'Corrosion file Result.json')    
        with open(output_file_path, 'w') as json_file:
            json.dump(response_data, json_file, indent=4)
        onto.destroy()
        return response_data
    else:
        onto.destroy()
        return {'error': 'File not found'}, 400

def process_corrosion(corrosion_depth, corrosion_percentage):
    onto = init_model()
    onto.load()
    new_corrosion = onto.Corrosion()
    new_corrosion.throughSection.append(False)
    new_corrosion.maxDepth.append(corrosion_depth)
    new_corrosion.percentage.append(corrosion_percentage)
    with onto:
        sync_reasoner_pellet(infer_property_values=True,
                             infer_data_property_values=True)

    result1 = {
        'name': new_corrosion.name,
        'maxDepth': new_corrosion.maxDepth,
        'percentage': new_corrosion.percentage,
        'severityRating': new_corrosion.severityRating,
        'extentRating': new_corrosion.extentRating,
        'maintenanceDecision': new_corrosion.maintenanceDecision
    }

    response_data = {
        'result1': result1,
        'message': [
            f'Based on the Network Rail Standard-Condition Marking of Bridges (NR/L3/CIV/006/2C), for {result1["name"]}({result1["maxDepth"]} mm and {result1["percentage"]}%), its severity rating is {result1["severityRating"]}, and its extent rating is {result1["extentRating"]}.',
            f'The maintenance solution of {result1["name"]} is {result1["maintenanceDecision"]}.'
        ]
    }

    file_path = os.path.join(data_out_dir, 'Corrosion Result.json') 
    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
    onto.destroy()
    return response_data

def process_coating_defect(selected_option, coatingDefect_percentage):
    # owl_file = 'C:\\Users\\Administrator\\Desktop\\ontologyWebPage\\v3-BMO.owl'
    # onto = get_ontology()
    onto = init_model()
    onto.load()
    new_coatingDefect = onto.CoatingDefect()
    if selected_option == '1':
        new_coatingDefect.visibleDefect.append(False)
        new_coatingDefect.percentage.append(0)
        # new_coatingDefect.percentage.append(coatingDefect_percentage)
    elif selected_option == '2':
        new_coatingDefect.abrasion.append(True)
        new_coatingDefect.percentage.append(coatingDefect_percentage)
    elif selected_option == '3':
        new_coatingDefect.flaking.append(True)
        new_coatingDefect.percentage.append(coatingDefect_percentage)
    elif selected_option == '4':
        new_coatingDefect.showingCorrosionSpots.append(True)
        new_coatingDefect.percentage.append(coatingDefect_percentage)
    else:  # inserted
        new_coatingDefect.completeLossCoating.append(True)
        new_coatingDefect.percentage.append(100)
    with onto:
        rule = Imp()
        rule.set_as_rule(
            'CoatingDefect(?C)^visibleDefect(?C,false) -> severityRating(?C,\"A\")^extentRating(?C,1)')
        rule = Imp()
        rule.set_as_rule(
            'CoatingDefect(?C)^abrasion(?C,true) -> severityRating(?C,\"I\")')
        rule = Imp()
        rule.set_as_rule(
            'CoatingDefect(?C)^flaking(?C,true) -> severityRating(?C,\"J\")')
        rule = Imp()
        rule.set_as_rule(
            'CoatingDefect(?C)^showingCorrosionSpots(?C,true) -> severityRating(?C,\"K\")')
        rule = Imp()
        rule.set_as_rule(
            'CoatingDefect(?C)^completeLossCoating(?C,true) -> severityRating(?C,\"L\")')
        rule = Imp()
        rule.set_as_rule(
            'CoatingDefect(?E)^severityRating(?E,?Es)^equal(?Es,\"A\") -> hasProtectiveCoatingSystem(?E,\"None\") ^ maintenanceDecision(?E,\"All coating intact, no visible defects.\") ')
        rule = Imp()
        rule.set_as_rule('Hazard(?E)^ severityRating(?E, ?Es) ^ equal(?Es, \"I\") -> maintenanceDecision(?E, \"There are no corrosion defects to underlying metal, surface abrasion.\") ^ hasProtectiveCoatingSystem(?E, \"ProtectiveSystemForExistingStructuresUsingEpoxy: Paint the topcoat. Select from the following and use a minimum dft of 50 microns: Anti-graffiti paint-polyurethane coloured finish, Acrylic urethane Topcoat, Polysiloxane Topcoat.\")')
        rule = Imp()
        rule.set_as_rule('Hazard(?E) ^severityRating(?E, ?Es) ^ equal(?Es, \"J\") -> maintenanceDecision(?E, \"There are no corrosion defects to underlying metal,flaking or blistering of top coat.\")^ hasProtectiveCoatingSystem(?E, \"ProtectiveSystemForExistingStructuresUsingEpoxy: Paint the intermediate coat and topcoat. 1. Epoxy Intermediate coat with a minimum dft of 125 microns. 2. Select from the following and use a minimum dft of 50 microns: Anti-graffiti paint-polyurethane coloured finish, Acrylic urethane Topcoat, Polysiloxane Topcoat.\")')
        rule = Imp()
        rule.set_as_rule('Hazard(?E) ^ severityRating(?E, ?Es) ^ equal(?Es, \"K\") -> maintenanceDecision(?E, \"There are corrosion defects to underlying metal.\") ^ hasProtectiveCoatingSystem(?E, \"ProtectiveSystemForExistingStructuresUsingEpoxy: 1. Existing iron or steel blast-cleaned to a surface standard Sa2½ and a surface profile mean peak to valley height of 70 to 100 microns. 2. Select Primer from the following - with a minimum dft of 50 microns: Blast Primer for damp surfaces, Epoxy blast Primer, Zinc rich epoxy blast Primer.Select Primer from the following: High solids epoxy Primer with a minimum dft of 100 microns, Epoxy Intermediate coat with a minimum dft of 125 microns. 3. Epoxy Intermediate coat with a minimum dft of 125 microns. 4. Select from the following and use a minimum dft of 50 microns: Anti-graffiti paint-polyurethane coloured finish, Acrylic urethane Topcoat, Polysiloxane Topcoat.\")')
        rule = Imp()
        rule.set_as_rule('Hazard(?E) ^severityRating(?E, ?Es) ^ equal(?Es, \"L\") ->maintenanceDecision(?E, \"Complete loss of coating to parent metal.\")^ hasProtectiveCoatingSystem(?E, \"ProtectiveSystemForExistingStructuresUsingEpoxy: 1. Existing iron or steel blast-cleaned to a surface standard Sa2½ and a surface profile mean peak to valley height of 70 to 100 microns. 2. Select Primer from the following - with a minimum dft of 50 microns: Blast Primer for damp surfaces, Epoxy blast Primer, Zinc rich epoxy blast Primer.Select Primer from the following: High solids epoxy Primer with a minimum dft of 100 microns, Epoxy Intermediate coat with a minimum dft of 125 microns. 3. Epoxy Intermediate coat with a minimum dft of 125 microns. 4. Select from the following and use a minimum dft of 50 microns: Anti-graffiti paint-polyurethane coloured finish, Acrylic urethane Topcoat, Polysiloxane Topcoat.\")')
    with onto:
        sync_reasoner_pellet(infer_property_values=True,
                             infer_data_property_values=True)
    result2 = []
    for coatingDefect in onto.CoatingDefect.instances():
        defect_data = {
            'name': coatingDefect.name,
            'percentage': coatingDefect.percentage[0],
            'severityRating': coatingDefect.severityRating[0] if coatingDefect.severityRating else None,
            'extentRating': coatingDefect.extentRating[0] if coatingDefect.extentRating else None,
            'maintenanceDecision': coatingDefect.maintenanceDecision[0] if coatingDefect.maintenanceDecision else None,
            'protectiveCoatingSystem': coatingDefect.hasProtectiveCoatingSystem[0] if coatingDefect.hasProtectiveCoatingSystem else None
        }
        result2.append(defect_data)

    response_data = {
        'result2': result2,
        'message': [
            f'Based on the Network Rail Standard-Condition Marking of Bridges (NR/L3/CIV/006/2C), for {defect["name"]}({defect["percentage"]}%), its severity rating is {defect["severityRating"]}, and its extent rating is {defect["extentRating"]}. {defect["maintenanceDecision"]}, and based on Specification for the Use of Protective Coating Systems (NR/L3/CIV/040), its protective coating system is {defect["protectiveCoatingSystem"]}.'
            for defect in result2
        ]
    }

    file_path = os.path.join(data_out_dir, 'Coating Defect Result.json')
    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)

    onto.destroy()
    return response_data

def process_crackOnMasonry(crack_Type,crackWidth,crackLengthPercentage):
    # owl_file = 'C:\\Users\\Administrator\\Desktop\\ontologyWebPage\\v3-BMO.owl'
    onto = init_model()
    onto.load()
    crack_types = {
        '1': 'Longitudinal',
        '2': 'Diagonal',
        '3': 'Transverse',
        '4': 'Ring',
        '5': 'Vertical',
        '6': 'Horizontal'
    }

    crack_type_value = crack_types.get(crack_Type, 'Horizontal')
    new_crack = onto.CrackOnMasonry()
    new_crack.crackType.append(crack_type_value)
    new_crack.maxWidth.append(crackWidth)
    new_crack.lengthpercentage.append(crackLengthPercentage)
    with onto:
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^visibleDefect(?C,false) -> severityRating(?C,\"A\")^extentRating(?C,1)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^lengthpercentage(?C,?Ca)^lessThan(?Ca, 20) -> extentRating(?C,7)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^lengthpercentage(?C,?Ca)^greaterThanOrEqual(?Ca,20)^lessThanOrEqual(?Ca,50) -> extentRating(?C,8)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^lengthpercentage(?C,?Ca)^greaterThan(?Ca,50)^lessThanOrEqual(?Ca,100)-> extentRating(?C,9)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^lengthpercentage(?C,?Ca)^greaterThan(?Ca,100)^lessThanOrEqual(?Ca,200) -> extentRating(?C,10)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^lengthpercentage(?C,?Ca)^greaterThan(?Ca,200) -> extentRating(?C,11)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Longitudinal\")^maxWidth(?C, ?y)^lessThan(?y, 1)-> severityRating(?C, \"G\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Diagonal\")^maxWidth(?C, ?y)^lessThan(?y, 1)-> severityRating(?C, \"G\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Transverse\")^maxWidth(?C, ?y)^lessThan(?y, 1)-> severityRating(?C, \"I\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Longitudinal\")^maxWidth(?C, ?y)^greaterThanOrEqual(?y, 1) ^ lessThanOrEqual(?y, 5)-> severityRating(?C, \"J\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Diagonal\")^maxWidth(?C, ?y)^greaterThanOrEqual(?y, 1) ^ lessThanOrEqual(?y, 5)-> severityRating(?C, \"J\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Longitudinal\")^maxWidth(?C, ?y)^greaterThan(?y, 5) ^ lessThanOrEqual(?y, 10)-> severityRating(?C, \"K\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Diagonal\")^maxWidth(?C, ?y)^greaterThan(?y, 5) ^ lessThanOrEqual(?y, 10)-> severityRating(?C, \"K\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Longitudinal\")^maxWidth(?C, ?y)^greaterThan(?y, 10) -> severityRating(?C, \"L\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Diagonal\")^maxWidth(?C, ?y)^greaterThan(?y, 10) -> severityRating(?C, \"L\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Transverse\")^maxWidth(?C, ?y)^greaterThanOrEqual(?y, 1)-> severityRating(?C, \"P\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Ring\")^maxWidth(?C, ?y)^lessThan(?y, 1)-> severityRating(?C, \"H\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Ring\")^maxWidth(?C, ?y)^greaterThanOrEqual(?y, 1) ^ lessThanOrEqual(?y, 5)-> severityRating(?C, \"M\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Ring\")^maxWidth(?C, ?y)^greaterThan(?y, 5) ^ lessThanOrEqual(?y, 10)-> severityRating(?C, \"N\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Ring\")^maxWidth(?C, ?y)^greaterThan(?y, 10) -> severityRating(?C, \"O\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Vertical\")^maxWidth(?C, ?y)^lessThan(?y, 1)-> severityRating(?C, \"G\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Diagonal\")^maxWidth(?C, ?y)^lessThan(?y, 1)-> severityRating(?C, \"G\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Horizontal\")^maxWidth(?C, ?y)^lessThan(?y, 1)-> severityRating(?C, \"I\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Vertical\")^maxWidth(?C, ?y)^greaterThanOrEqual(?y, 1) ^ lessThanOrEqual(?y, 5)-> severityRating(?C, \"J\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Diagonal\")^maxWidth(?C, ?y)^greaterThanOrEqual(?y, 1) ^ lessThanOrEqual(?y, 5)-> severityRating(?C, \"J\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Vertical\")^maxWidth(?C, ?y)^greaterThan(?y, 5) ^ lessThanOrEqual(?y, 10)-> severityRating(?C, \"K\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Diagonal\")^maxWidth(?C, ?y)^greaterThan(?y, 5) ^ lessThanOrEqual(?y, 10)-> severityRating(?C, \"K\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Vertical\")^maxWidth(?C, ?y)^greaterThan(?y, 10) -> severityRating(?C, \"L\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Diagonal\")^maxWidth(?C, ?y)^greaterThan(?y, 10) -> severityRating(?C, \"L\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Horizontal\")^maxWidth(?C, ?y)^greaterThanOrEqual(?y, 1) ^ lessThanOrEqual(?y, 5)-> severityRating(?C, \"M\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Horizontal\")^maxWidth(?C, ?y)^greaterThan(?y, 5) ^ lessThanOrEqual(?y, 10)-> severityRating(?C, \"N\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnMasonry(?C)^crackType(?C,?Ca) ^equal(?Ca,\"Horizontal\")^maxWidth(?C, ?y)^greaterThan(?y, 10) -> severityRating(?C, \"O\")')
    with onto:
        sync_reasoner_pellet(infer_property_values=True,
                             infer_data_property_values=True)
    result3 = []
    for crack in onto.CrackOnMasonry.instances():
        crack_data = {
            'name': crack.name,
            'crackType': crack.crackType[0],
            'maxWidth': crack.maxWidth[0],
            'lengthpercentage': crack.lengthpercentage[0],
            'severityRating': crack.severityRating[0] if crack.severityRating else None,
            'extentRating': crack.extentRating[0] if crack.extentRating else None
        }
        result3.append(crack_data)

    response_data = {
        'result3': result3,
        'message': [
            f'Based on the Network Rail Standard-Condition Marking of Bridges (NR/L3/CIV/006/2C), for {crack.name} ({crack.crackType[0]} crack, {crack.maxWidth[0]} mm wide and {crack.lengthpercentage[0]}% long), its severity rating is {crack.severityRating[0] if crack.severityRating else "Not determined"}, and its extent rating is {crack.extentRating[0] if crack.extentRating else "Not determined"}.'
            for crack in onto.CrackOnMasonry.instances()
        ]
    }

    file_path = os.path.join(data_out_dir, 'Crack On Masonry Result.json')
    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
    onto.destroy()
    return response_data

def process_crackOnReinforcedConcrete(selected_option, crackWidth, crackLengthPercentage):
    # owl_file = 'C:\\Users\\Administrator\\Desktop\\ontologyWebPage\\v3-BMO.owl'
    onto = init_model()
    onto.load()
    new_crack = onto.CrackOnReinforcedConcrete()
    if selected_option == '1':
        new_crack.showingCorrosionSpots.append(True)
        new_crack.lengthpercentage.append(crackLengthPercentage)
    else:  # inserted
        new_crack.showingCorrosionSpots.append(False)
        new_crack.maxWidth.append(crackWidth)
        new_crack.lengthpercentage.append(crackLengthPercentage)
    with onto:
        rule = Imp()
        rule.set_as_rule(
            'CrackOnReinforcedConcrete(?C)^visibleDefect(?C,false) -> severityRating(?C,\"A\")^extentRating(?C,1)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnReinforcedConcrete(?C)^lengthpercentage(?C,?Ca)^lessThan(?Ca, 20) -> extentRating(?C,2)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnReinforcedConcrete(?C)^lengthpercentage(?C,?Ca)^greaterThanOrEqual(?Ca,20)^lessThanOrEqual(?Ca,50) -> extentRating(?C,3)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnReinforcedConcrete(?C)^lengthpercentage(?C,?Ca)^greaterThan(?Ca,50)^lessThanOrEqual(?Ca,100)-> extentRating(?C,4)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnReinforcedConcrete(?C)^lengthpercentage(?C,?Ca)^greaterThan(?Ca,100)^lessThanOrEqual(?Ca,200) -> extentRating(?C,5)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnReinforcedConcrete(?C)^lengthpercentage(?C,?Ca)^greaterThan(?Ca,200) -> extentRating(?C,6)')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnReinforcedConcrete(?C)^showingCorrosionSpots(?C,false)^maxWidth(?C, ?y)^lessThan(?y, 1)-> severityRating(?C, \"B\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnReinforcedConcrete(?C)^showingCorrosionSpots(?C,false)^maxWidth(?C, ?y)^greaterThanOrEqual(?y, 1)-> severityRating(?C, \"C\")')
        rule = Imp()
        rule.set_as_rule(
            'CrackOnReinforcedConcrete(?C)^showingCorrosionSpots(?C,true) -> severityRating(?C,\"D\")')
    with onto:
        sync_reasoner_pellet(infer_property_values=True,
                             infer_data_property_values=True)
    result4 = []
    for crack in onto.CrackOnReinforcedConcrete.instances():
        crack_data = {
            'name': crack.name,
            'maxWidth': crack.maxWidth,
            'lengthpercentage': crack.lengthpercentage,
            'severityRating': crack.severityRating,
            'extentRating': crack.extentRating
        }
        result4.append(crack_data)

    response_data = {
        'result4': result4,
        'message': [
            f'Based on the Network Rail Standard-Condition Marking of Bridges (NR/L3/CIV/006/2C), for {crack.name}({crack.maxWidth} mm and {crack.lengthpercentage}%), its severity rating is {crack.severityRating}, and its extent rating is {crack.extentRating}.'
            for crack in onto.CrackOnReinforcedConcrete.instances()
        ]
    }

    file_path = 'Crack On Masonry Result.json'
    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
    onto.destroy()
    return response_data


if __name__ == "__main__":
    data_out_dir=r'backend\ontologyWeb\data'
    owl_file=r'backend\ontologyWeb\data\v3-BMO.owl'
    json_file_path=r'backend\ontologyWeb\result.json'
    
    file_path=r'backend\ontologyWeb\data\v3-BMO.owl'
    debug_json_path=r'backend\ontologyWeb\result.json'
    # json=process_corrosionAuto(8.0,68.1)
    # json=upload(debug_json_path)
    # json=process_corrosion(20.0,50.0)
    # json=process_coating_defect('2',20.0)
    # json=process_crackOnMasonry('Diagonal crack',1.0,20.0)
    json=process_crackOnReinforcedConcrete('2',1.0,20.0)
    print(json)