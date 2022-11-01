import csv
import sys
import os

# Converts a google contacts csv file to a collection of markdown files


if (len(sys.argv)!=3):
    print("\noutlookcontacts2obsidian.py - by Jonathan Beckett\n\npython outputcontacts2obsidian.py <source_file> <output_directory>\n\nExample : python outlookcontacts2obsidian.py contacts.csv c:\\my\\vault\\contacts\n\n")
    sys.exit(0)

source_file = sys.argv[1]
output_path = sys.argv[2]

with open(source_file,newline="") as csvfile:
    csvreader = csv.DictReader(csvfile,delimiter=",",quotechar="\"")
    for row in csvreader:

        name = row["First Name"] + " " + row["Last Name"]
        job_title = row["Job Title"]
        email_address = row["E-mail Address"]
        office_phone = row["Business Phone"]
        mobile_phone = row["Mobile Phone"]
        company = row["Company"]
        address = row["Business Street"] + "\n" + row["Business Postal Code"]

        address_lines = list(filter(None, address.replace("\r\n","\n").split("\n")))
        address_inline = ", ".join(address_lines)

        # if email begins with /o its got an active directory address
        # split it on the -
        if email_address:
            if email_address[0:2] == "/o":
                email_address = email_address.split("-")[1]

        print("Processing " + name)

        # output YAML front matter
        output_text = "---\n"
        output_text += "name: " + name + "\n"
        if job_title:
            output_text += "job_title: " + job_title + "\n"
        if company:
            output_text += "company: " + company + "\n"
        if email_address:
            output_text += "email_address: " + email_address + "\n"
        if office_phone:
            output_text += "office_phone: " + office_phone + "\n"
        if mobile_phone:
            output_text += "mobile_phone: " + mobile_phone + "\n"
        if address_inline:
            output_text += "address: " + address_inline + "\n"
        output_text += "---\n"
        
        # output human readable version
        output_text += "\n"

        output_text += "### Name\n"
        output_text += name + "\n\n"

        if job_title:
            output_text += "### Job Title\n"
            output_text += job_title + "\n\n"

        if company:
            output_text += "### Company\n"
            output_text += company + "\n\n"

        if email_address:
            output_text += "### Email Address\n"
            output_text += email_address + "\n\n"

        if office_phone:
            output_text += "### Office Phone\n"
            output_text += office_phone + "\n\n"

        if mobile_phone:
            output_text += "### Mobile Phone\n"
            output_text += mobile_phone + "\n\n"

        if address_inline:
            output_text += "### Address\n"
            output_text += address + "\n\n"
        
        output_text += "#contact\n"

        # write the file
        output_file_path = os.path.join(output_path,name + ".md")
        output_file = open(output_file_path, 'wb')
        output_file.write(bytes(output_text,'utf-8'))
        output_file.close()