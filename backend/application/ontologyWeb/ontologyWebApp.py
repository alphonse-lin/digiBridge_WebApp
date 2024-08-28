from flask import Flask, render_template, request, jsonify
from owlready2 import *
import json
import os
app = Flask(__name__)


def process_corrosionAuto(owl_file):
    onto = get_ontology(owl_file)
    onto.load()
    depth_of_corrosion = float(request.form['corrosionAuto_depth'])
    percentage_of_surface = float(request.form['corrosionAuto_percentage'])
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

    return jsonify(response_data)


def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        with open(uploaded_file.filename, 'r') as file:
            data = json.load(file)
        corrosion_depth = data.get('Severe corrosion percentage', 0)
        if corrosion_depth > 30:
            corrosion_depth = 8
        elif corrosion_depth > 5:
            corrosion_depth = 3
        else:
            corrosion_depth = 0.5
        corrosion_percentage = data.get('Total corrosion percentage', 0)
        owl_file = 'C:\\Users\\Administrator\\Desktop\\ontologyWebPage\\v3-BMO.owl'
        onto = get_ontology(owl_file)
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

        # 如果仍需要保存到文件
        file_path = 'Corrosion file Result.json'
        with open(file_path, 'w') as json_file:
            json.dump(response_data, json_file, indent=4)

        return jsonify(response_data)
    else:
        return jsonify({'error': 'No file uploaded'}), 400


def process_corrosion(owl_file):
    onto = get_ontology(owl_file)
    onto.load()
    new_corrosion = onto.Corrosion()
    new_corrosion.throughSection.append(False)
    corrosion_depth = float(request.form['corrosion_depth'])
    corrosion_percentage = float(request.form['corrosion_percentage'])
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

    file_path = 'Corrosion Result.json'
    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)

    return jsonify(response_data)


def process_coating_defect(owl_file):
    # owl_file = 'C:\\Users\\Administrator\\Desktop\\ontologyWebPage\\v3-BMO.owl'
    onto = get_ontology(owl_file)
    onto.load()
    new_coatingDefect = onto.CoatingDefect()
    selected_option = request.form['selected_option']
    if selected_option == '1':
        new_coatingDefect.visibleDefect.append(False)
        new_coatingDefect.percentage.append(0)
    elif selected_option == '2':
        new_coatingDefect.abrasion.append(True)
        coatingDefect_percentage = float(
            request.form['coatingDefect_percentage'])
        new_coatingDefect.percentage.append(coatingDefect_percentage)
    elif selected_option == '3':
        new_coatingDefect.flaking.append(True)
        coatingDefect_percentage = float(
            request.form['coatingDefect_percentage'])
        new_coatingDefect.percentage.append(coatingDefect_percentage)
    elif selected_option == '4':
        new_coatingDefect.showingCorrosionSpots.append(True)
        coatingDefect_percentage = float(
            request.form['coatingDefect_percentage'])
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

    file_path = 'Coating Defect Result.json'
    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)

    return jsonify(response_data)


def process_crackOnMasonry(owl_file):
    # owl_file = 'C:\\Users\\Administrator\\Desktop\\ontologyWebPage\\v3-BMO.owl'
    onto = get_ontology(owl_file)
    onto.load()
    crack_Type = request.form['crack_Type']
    if crack_Type == 'Longitudinal crack':
        new_crack = onto.CrackOnMasonry()
        new_crack.crackType.append('Longitudinal')
        crackWidth = float(request.form['crackWidth'])
        new_crack.maxWidth.append(crackWidth)
        crackLengthPercentage = float(request.form['crackLengthPercentage'])
        new_crack.lengthpercentage.append(crackLengthPercentage)
    else:  # inserted
        if crack_Type == 'Diagonal crack':
            new_crack = onto.CrackOnMasonry()
            new_crack.crackType.append('Diagonal')
            crackWidth = float(request.form['crackWidth'])
            new_crack.maxWidth.append(crackWidth)
            crackLengthPercentage = float(
                request.form['crackLengthPercentage'])
            new_crack.lengthpercentage.append(crackLengthPercentage)
        else:  # inserted
            if crack_Type == 'Transverse crack':
                new_crack = onto.CrackOnMasonry()
                new_crack.crackType.append('Transverse')
                crackWidth = float(request.form['crackWidth'])
                new_crack.maxWidth.append(crackWidth)
                crackLengthPercentage = float(
                    request.form['crackLengthPercentage'])
                new_crack.lengthpercentage.append(crackLengthPercentage)
            else:  # inserted
                if crack_Type == 'Ring crack':
                    new_crack = onto.CrackOnMasonry()
                    new_crack.crackType.append('Ring')
                    crackWidth = float(request.form['crackWidth'])
                    new_crack.maxWidth.append(crackWidth)
                    crackLengthPercentage = float(
                        request.form['crackLengthPercentage'])
                    new_crack.lengthpercentage.append(crackLengthPercentage)
                else:  # inserted
                    if crack_Type == 'Vertical crack':
                        new_crack = onto.CrackOnMasonry()
                        new_crack.crackType.append('Vertical')
                        crackWidth = float(request.form['crackWidth'])
                        new_crack.maxWidth.append(crackWidth)
                        crackLengthPercentage = float(
                            request.form['crackLengthPercentage'])
                        new_crack.lengthpercentage.append(
                            crackLengthPercentage)
                    else:  # inserted
                        if crack_Type == 'Diagonal crack':
                            new_crack = onto.CrackOnMasonry()
                            new_crack.crackType.append('Diagonal')
                            crackWidth = float(request.form['crackWidth'])
                            new_crack.maxWidth.append(crackWidth)
                            crackLengthPercentage = float(
                                request.form['crackLengthPercentage'])
                            new_crack.lengthpercentage.append(
                                crackLengthPercentage)
                        else:  # inserted
                            new_crack = onto.CrackOnMasonry()
                            new_crack.crackType.append('Horizontal')
                            crackWidth = float(request.form['crackWidth'])
                            new_crack.maxWidth.append(crackWidth)
                            crackLengthPercentage = float(
                                request.form['crackLengthPercentage'])
                            new_crack.lengthpercentage.append(
                                crackLengthPercentage)
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

    file_path = 'Crack On Masonry Result.json'
    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)

    return jsonify(response_data)


def process_crackOnReinforcedConcrete(owl_file):
    # owl_file = 'C:\\Users\\Administrator\\Desktop\\ontologyWebPage\\v3-BMO.owl'
    onto = get_ontology(owl_file)
    onto.load()
    new_crack = onto.CrackOnReinforcedConcrete()
    selected_option = request.form['selected_option']
    if selected_option == '1':
        new_crack.showingCorrosionSpots.append(True)
        crackLengthPercentage = float(request.form['crackLengthPercentage'])
        new_crack.lengthpercentage.append(crackLengthPercentage)
    else:  # inserted
        new_crack.showingCorrosionSpots.append(False)
        crackWidth = float(request.form['crackWidth'])
        new_crack.maxWidth.append(crackWidth)
        crackLengthPercentage = float(request.form['crackLengthPercentage'])
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

    return jsonify(response_data)
