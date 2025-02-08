import tkinter as tk
from tkinter import *
from tkinter import ttk
import datetime
from tkcalendar import DateEntry
from SaveDocx import pDocx
from AIResponses import AIResponse
import threading
import json

# Global variables
patients_data = []
providers_data = []

def popup_err(e):
    win = tk.Toplevel()
    win.wm_title("Error")

    l = tk.Label(win, text=e, wraplength=400, justify="center", padx=20, pady=20, bg='#ffdddd', font=('Arial', 12))
    l.pack(padx=20, pady=20)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.pack(pady=10)

def popup_gen(t):
    win = tk.Toplevel()
    win.wm_title(t)

    l = tk.Label(win, text=t, wraplength=400, justify="center", padx=20, pady=20, bg='#ddffdd', font=('Arial', 12))
    l.pack(padx=20, pady=20)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.pack(pady=10)

def load_company_name():
    try:
        with open('template.txt', 'r') as file:
            company_name = file.readline().strip()
            companyName.set(company_name)
    except Exception as e:
        popup_err(f"Failed to load company name: {e}")

def load_patient_data():
    global patients_data
    try:
        with open('patients.json', 'r') as file:
            patients_data = json.load(file)
            clientName_combo['values'] = [patient['name'] for patient in patients_data]
            update_client_list()
    except Exception as e:
        popup_err(f"Failed to load patient data: {e}")

def load_providers():
    global providers_data
    try:
        with open('providers.json', 'r') as file:
            providers_data = json.load(file)
            serviceProvidedBy_combo['values'] = [provider['name'] for provider in providers_data]
    except Exception as e:
        popup_err(f"Failed to load providers data: {e}")

def on_client_name_selected(event):
    selected_name = clientName.get()
    for patient in patients_data:
        if patient['name'] == selected_name:
            clientID.set(patient['id'])
            clientDOB.set(patient['dob'])
            serviceProvided.set(patient['service'])
            SupportPlan.set(patient['support_plan'])
            serviceProvidedBy.set(patient.get('provider', ''))
            break

def save_client_data():
    new_patient = {
        "name": clientName.get(),
        "id": clientID.get(),
        "dob": clientDOB.get(),
        "service": serviceProvided.get(),
        "support_plan": SupportPlan.get(),
        "provider": serviceProvidedBy.get()
    }

    # Check if the patient already exists and update their information
    for patient in patients_data:
        if patient['name'] == new_patient['name']:
            patient.update(new_patient)
            break
    else:
        # If the patient does not exist, append the new patient data
        patients_data.append(new_patient)

    try:
        with open('patients.json', 'w') as file:
            json.dump(patients_data, file, indent=4)
        popup_gen("Client saved successfully.")
        clientName_combo['values'] = [patient['name'] for patient in patients_data]
        update_client_list()
    except Exception as e:
        popup_err(f"Failed to save client data: {e}")

def delete_client_data():
    selected_name = clientName.get()
    global patients_data
    patients_data = [patient for patient in patients_data if patient['name'] != selected_name]

    try:
        with open('patients.json', 'w') as file:
            json.dump(patients_data, file, indent=4)
        popup_gen("Client deleted successfully.")
        clientName_combo['values'] = [patient['name'] for patient in patients_data]
        update_client_list()
        clear_client_fields()
    except Exception as e:
        popup_err(f"Failed to delete client data: {e}")

def clear_client_fields():
    clientName.set('')
    clientID.set('')
    clientDOB.set('')
    serviceProvided.set('')
    SupportPlan.set('')
    serviceProvidedBy.set('')

def save_provider_data():
    new_provider = {
        "name": serviceProvidedBy.get()
    }

    # Check if the provider already exists and update their information
    for provider in providers_data:
        if provider['name'] == new_provider['name']:
            provider.update(new_provider)
            break
    else:
        # If the provider does not exist, append the new provider data
        providers_data.append(new_provider)

    try:
        with open('providers.json', 'w') as file:
            json.dump(providers_data, file, indent=4)
        popup_gen("Provider saved successfully.")
        serviceProvidedBy_combo['values'] = [provider['name'] for provider in providers_data]
    except Exception as e:
        popup_err(f"Failed to save provider data: {e}")

root = Tk()
root.title("KAP Software | AI Powered Patient Report Generator ")
root.geometry("1080x720")
root.configure(bg='#f0f0f0')

style = ttk.Style()
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 14))
style.configure('TEntry', font=('Arial', 14))
style.configure('TButton', font=('Arial', 14), padding=6)
style.configure('TCombobox', font=('Arial', 14))

notebook = ttk.Notebook(root)
notebook.grid(column=0, row=0, sticky=(N, W, E, S))

# First Panel
panel1 = ttk.Frame(notebook, padding="20 20 20 20")
panel1.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(panel1, text='Report Generator')

descriptionCol = 2
textBoxCol = 3
textboxWidth = 30

# company name
companyName = StringVar()
companyName_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=companyName)
companyName_entry.grid(column=textBoxCol, row=1, sticky=(W, E))
ttk.Label(panel1, text="Company Name").grid(column=descriptionCol, row=1, sticky=W)

clientName = StringVar()
clientName_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=clientName)
clientName_combo.grid(column=textBoxCol, row=2, sticky=(W, E))
clientName_combo.bind("<<ComboboxSelected>>", on_client_name_selected)
ttk.Label(panel1, text="Client Name").grid(column=descriptionCol, row=2, sticky=W)

clientID = StringVar()
clientID_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=clientID)
clientID_entry.grid(column=textBoxCol, row=3, sticky=(W, E))
ttk.Label(panel1, text="Client ID").grid(column=descriptionCol, row=3, sticky=W)

clientDOB = StringVar()
clientDOB_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=clientDOB)
clientDOB_entry.grid(column=textBoxCol, row=4, sticky=(W, E))
ttk.Label(panel1, text="Client DOB").grid(column=descriptionCol, row=4, sticky=W)

serviceProvided = StringVar()
serviceProvided_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=serviceProvided)
serviceProvided_entry.grid(column=textBoxCol, row=5, sticky=(W, E))
ttk.Label(panel1, text="Service Provided").grid(column=descriptionCol, row=5, sticky=W)

serviceProvidedBy = StringVar()
serviceProvidedBy_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=serviceProvidedBy)
serviceProvidedBy_combo.grid(column=textBoxCol, row=6, sticky=(W, E))
ttk.Label(panel1, text="Service Provided By").grid(column=descriptionCol, row=6, sticky=W)

SupportPlan = StringVar()
SupportPlan_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=SupportPlan)
SupportPlan_entry.grid(column=textBoxCol, row=7, sticky=(W, E))
ttk.Label(panel1, text="Support Plan").grid(column=descriptionCol, row=7, sticky=W)

# Generate time intervals
time_options = [datetime.time(hour=h, minute=m).strftime("%I:%M %p") for h in range(24) for m in (0, 15, 30, 45)]

startTime = StringVar()
startTime_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=startTime, values=time_options)
startTime_combo.grid(column=textBoxCol, row=8, sticky=(W, E))
ttk.Label(panel1, text="Start Time").grid(column=descriptionCol, row=8, sticky=W)

endTime = StringVar()
endTime_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=endTime, values=time_options)
endTime_combo.grid(column=textBoxCol, row=9, sticky=(W, E))
ttk.Label(panel1, text="End Time").grid(column=descriptionCol, row=9, sticky=W)

startDate = StringVar()
startDate_entry = DateEntry(panel1, width=textboxWidth-2, textvariable=startDate, date_pattern='mm/dd/yyyy')
startDate_entry.grid(column=textBoxCol, row=10, sticky=(W, E))
ttk.Label(panel1, text="Start Date (month/day/year)").grid(column=descriptionCol, row=10, sticky=W)

endDate = StringVar()
endDate_entry = DateEntry(panel1, width=textboxWidth-2, textvariable=endDate, date_pattern='mm/dd/yyyy')
endDate_entry.grid(column=textBoxCol, row=11, sticky=(W, E))
ttk.Label(panel1, text="End Date (month/day/year)").grid(column=descriptionCol, row=11, sticky=W)

button_state = NORMAL

def genAndSave(progress_callback):
    hourFormat = "%I:%M %p"
    dateFormat = "%m/%d/%Y"
    StartDate = datetime.datetime.strptime(startDate.get(), dateFormat)
    EndDate = datetime.datetime.strptime(endDate.get(), dateFormat)
    StartTime = datetime.datetime.strptime(startTime.get(), hourFormat)
    EndTime = datetime.datetime.strptime(endTime.get(), hourFormat)
    difference = EndDate - StartDate

    currentDate = StartDate

    i = 0
    while i <= difference.days:
        response = AIResponse(clientName.get(), SupportPlan.get())
        pDocx(clientName.get(),
              clientID.get(),
              currentDate,
              response,
              serviceProvided.get(),
              serviceProvidedBy.get(),
              StartTime.strftime(hourFormat),
              EndTime.strftime(hourFormat),
              (EndTime - StartTime),
              (((EndTime - StartTime).seconds / 60) / 60) * 4)
        progress_callback(i)
        currentDate = currentDate + datetime.timedelta(days=1)
        i += 1
    popup_gen('Complete!')

def update_progress(value):
    progress_bar['value'] = value
    panel1.update_idletasks()
    if value == progress_bar['maximum']:
        generate_button['state'] = NORMAL

def runGeneration():
    generate_button['state'] = DISABLED
    def wrapper():
        genAndSave(update_progress)

    thread = threading.Thread(target=wrapper)
    thread.start()

def command():
    try:
        hourFormat = "%I:%M %p"
        dateFormat = "%m/%d/%Y"
        StartDate = datetime.datetime.strptime(startDate.get(), dateFormat)
        EndDate = datetime.datetime.strptime(endDate.get(), dateFormat)
        StartTime = datetime.datetime.strptime(startTime.get(), hourFormat)
        EndTime = datetime.datetime.strptime(endTime.get(), hourFormat)
        difference = EndDate - StartDate
        global progress_bar
        progress_bar = ttk.Progressbar(panel1, maximum=difference.days)
        progress_bar.grid(column=textBoxCol, row=14, columnspan=2, pady=10)
        runGeneration()
    except Exception as e:
        popup_err(e)

progress_var = tk.IntVar()
generate_button = ttk.Button(panel1, text="Generate AI Reports", command=command, state=button_state)
generate_button.grid(column=descriptionCol, row=13, columnspan=2, pady=10)

# Load company name button
load_button = ttk.Button(panel1, text="Load Company Name", command=load_company_name)
load_button.grid(column=descriptionCol, row=15, columnspan=2, pady=10)

# Save client data button
save_client_button = ttk.Button(panel1, text="Save Client", command=save_client_data)
save_client_button.grid(column=descriptionCol, row=16, columnspan=2, pady=10)

# Save provider data button
save_provider_button = ttk.Button(panel1, text="Save Provider", command=save_provider_data)
save_provider_button.grid(column=descriptionCol, row=17, columnspan=2, pady=10)

# Second Panel for managing clients
panel2 = ttk.Frame(notebook, padding="20 20 20 20")
panel2.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(panel2, text='Manage Clients')

def update_client_list():
    client_listbox.delete(0, END)
    for patient in patients_data:
        client_listbox.insert(END, patient['name'])

def on_client_select(event):
    selected_index = client_listbox.curselection()
    if selected_index:
        selected_patient = patients_data[selected_index[0]]
        clientName.set(selected_patient['name'])
        clientID.set(selected_patient['id'])
        clientDOB.set(selected_patient['dob'])
        serviceProvided.set(selected_patient['service'])
        SupportPlan.set(selected_patient['support_plan'])
        serviceProvidedBy.set(selected_patient.get('provider', ''))

client_listbox = Listbox(panel2, height=15, font=('Arial', 14))
client_listbox.grid(column=0, row=0, rowspan=8, sticky=(N, S, E, W))
client_listbox.bind("<<ListboxSelect>>", on_client_select)

# Add a frame for editing client details
edit_frame = ttk.Frame(panel2, padding="10 10 10 10")
edit_frame.grid(column=1, row=0, rowspan=8, sticky=(N, S, E, W))

ttk.Label(edit_frame, text="Client Name").grid(column=0, row=0, sticky=W)
clientName_entry_edit = ttk.Entry(edit_frame, width=textboxWidth, textvariable=clientName)
clientName_entry_edit.grid(column=1, row=0, sticky=(W, E))

ttk.Label(edit_frame, text="Client ID").grid(column=0, row=1, sticky=W)
clientID_entry_edit = ttk.Entry(edit_frame, width=textboxWidth, textvariable=clientID)
clientID_entry_edit.grid(column=1, row=1, sticky=(W, E))

ttk.Label(edit_frame, text="Client DOB").grid(column=0, row=2, sticky=W)
clientDOB_entry_edit = ttk.Entry(edit_frame, width=textboxWidth, textvariable=clientDOB)
clientDOB_entry_edit.grid(column=1, row=2, sticky=(W, E))

ttk.Label(edit_frame, text="Service Provided").grid(column=0, row=3, sticky=W)
serviceProvided_entry_edit = ttk.Entry(edit_frame, width=textboxWidth, textvariable=serviceProvided)
serviceProvided_entry_edit.grid(column=1, row=3, sticky=(W, E))

ttk.Label(edit_frame, text="Service Provided By").grid(column=0, row=4, sticky=W)
serviceProvidedBy_combo_edit = ttk.Combobox(edit_frame, width=textboxWidth, textvariable=serviceProvidedBy)
serviceProvidedBy_combo_edit.grid(column=1, row=4, sticky=(W, E))

ttk.Label(edit_frame, text="Support Plan").grid(column=0, row=5, sticky=W)
SupportPlan_entry_edit = ttk.Entry(edit_frame, width=textboxWidth, textvariable=SupportPlan)
SupportPlan_entry_edit.grid(column=1, row=5, sticky=(W, E))

# Save edited client data button
save_edited_client_button = ttk.Button(edit_frame, text="Save Edited Client", command=save_client_data)
save_edited_client_button.grid(column=0, row=6, columnspan=2, pady=10)

# Delete selected client button
delete_client_button = ttk.Button(edit_frame, text="Delete Client", command=delete_client_data)
delete_client_button.grid(column=0, row=7, columnspan=2, pady=10)

# Button to create a new client
new_client_button = ttk.Button(edit_frame, text="New Client", command=clear_client_fields)
new_client_button.grid(column=0, row=8, columnspan=2, pady=10)

# Load patient data on startup
load_patient_data()

# Load providers data on startup
load_providers()

for child in panel1.winfo_children():
    child.grid_configure(padx=10, pady=5)

for child in edit_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()