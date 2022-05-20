import csv,datetime,json,pytz
import xml.etree.ElementTree as ET

# Problem 1 - to update the DEPART and RETURN dates in the XML file
def update_xml_data(dep, ret):
    xml_tree = ET.parse('test_payload1.xml')
    xml_roots = xml_tree.getroot()
    # update DEPART value with current date + user value for DEPART
    for item_depart in xml_roots.iter('DEPART'):
        item_depart.text = (datetime.datetime.now() + datetime.timedelta(days=dep)).strftime('%Y%m%d')
    # update RETURN value with current date + user value for RETURN
    for item_return in xml_roots.iter('RETURN'):
        item_return.text = (datetime.datetime.now() + datetime.timedelta(days=ret)).strftime('%Y%m%d')
    # write the modified XML to a new file
    xml_tree.write('updated_test_payload1.xml')
    
# Problem 2 - to delete an element (nested/non nested) from JSON file
def delete_json_data(element_to_delete):
    objects = json.load(open("test_payload.json"))
    # if the element_to_delete is at root level, then delete the item direcly
    if element_to_delete in objects.keys():
        del objects[element_to_delete]
    # Else If element_to_delete is not at the rool level, that is - inside inParams or outParams
    else:
        for key in objects.keys():
            # Check if element_to_delete is inside intParams (Dict) or outParams (List)
            if isinstance(objects[key], dict):
                # delete element_to_delete if it is present inside inParams
                if element_to_delete in objects[key].keys():
                    del objects[key][element_to_delete]
                    break
            elif isinstance(objects[key], list):
                # delete element_to_delete if it is present inside outParams
                if element_to_delete in objects[key]:
                    objects[key].remove(element_to_delete)
                    break

    open("updated_test_payload.json", "w").write(json.dumps(objects, indent=2))

# Problem 3 - to parse CSV file and prints the non-successful responses
def get_failed_responses_csv():
    with open('Jmeter_log1.jtl') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        #headers = next(csv_data)
        # filter non-successful messages, convert the timestamp to UTC and then to PST and print details to CONSOLE
        for row in csv_data:
            if row[3] != '200':
                 datetime_utc = datetime.datetime.utcfromtimestamp(int(row[0])/1000)
                 datetime_pst = datetime_utc.replace(tzinfo=pytz.timezone('UTC')).astimezone(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S %Z')
                 print(f'Respone code: {row[3]} | Response message: {row[4]} \t | Failure message: {row[8]} | PST Time: {datetime_pst} | label: {row[2]} ')

update_xml_data(10,20)      # Problem 1
delete_json_data('appdate') # Problem 2
get_failed_responses_csv()  # Problem 3


