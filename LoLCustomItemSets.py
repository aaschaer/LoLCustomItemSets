#made by Aaron Schaer, distribute as you please

import os, json
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askdirectory

#global variables
LOL_path = "" #path to the League of Legends config folder
num_blocks = 10

#global tkinter objects, for some reason they seem to be garbage collected if used locally
root = Tk()
champ_entry = Entry(root)
name_entry = Entry(root)
block_entries = {} #item block inputs
for i in range(num_blocks):
    block_entries["type_"+str(i)] = Entry(root)
    block_entries["data_"+str(i)] = Entry(root,width=100)

#finds the League of Legends config folder
def getLOLPath():
    global LOL_path

    #try standard path in C directory
    standard_path = "C:/Riot Games/League of Legends/Config/Champions"
    if os.path.exists(standard_path):
        LOL_path = standard_path

    #if not found in C, prompt user to input their directory
    else: 
        dir_root = Tk()
        expl = Label(dir_root, text="Unable to find Riot Games folder, please select it.").pack()

        #Select Directory button:
        #has the user navigate to a dir, and then verries it is the Riot Games dir 
        def callback():
            global LOL_path
            user_path = askdirectory()
            if ( os.path.exists(user_path)
            and os.path.exists(user_path + "/League of Legends/Config/Champions") ):
                LOL_path = user_path + "/League of Legends/Config/Champions"
                dir_root.quit()
                dir_root.destroy()
            else:
                showerror("ERROR",
                "invalid directory, make sure you selected the folder named \"Riot Games\"")
        b1 = Button(dir_root,text="Select Directory", command=callback).pack()

        dir_root.mainloop()


#function called by Delete All Sets button
#goes through all Champion folders in Config and removes the sets under Recommended
def deleteAllSets():

    if askyesno('Verify', 'Really delete all existing custom item sets?'): #give the user a warning

        for champ in os.listdir(LOL_path):
            for item_set in os.listdir(LOL_path+"/"+champ+"/Recommended"):
                set_path = LOL_path+"/"+champ+"/Recommended/" + item_set
                if os.path.isfile(set_path):
                    os.remove(set_path)

        showinfo("Done", "All custom item sets have been cleared")


#writes one set into the Config folder
def writeSet(champ,set_name,blocks):

    #check if the champ has a dir, if not make one
    if not os.path.exists(LOL_path+"/"+champ):
         os.makedirs(LOL_path+"/"+champ)
         os.makedirs(LOL_path+"/"+champ+"/Recommended")

    #warn the user if this specific set exists already
    exists = os.path.exists(LOL_path+"/"+champ+"/Recommended/"+set_name+".json")
    if exists:
        #give the user a warning
        okay = askyesno(
         "Okay to overwrite?", set_name+" Already exists for "+champ+", is it okay to overwrite it")

    if (not exists) or okay:
        
        #make output dictionary
        out = {}
        out["title"] = set_name #name of this item set
        out["type"] = "custom" #this is a custom item set
        out["map"] = "any" #TODO: Add support for specific maps
        out["mode"] = "any" #TODO: Add support for specific modes
        out["blocks"] = blocks

        output_file = open(LOL_path+"/"+champ+"/Recommended/"+set_name+".json", "w")
        output_file.write(json.dumps(out))
        output_file.close()

#function called by the save Set button:
#gathers data from global tk objects and then calls writeSet
def saveSet():

    blocks = [] #list of dicts formated in the same was LOL handles blocks
    for i in range(num_blocks):
        block_type = block_entries["type_"+str(i)].get() #get the type (name)
        if block_type != "": #ignore blocks with no entry
            item_data = block_entries["data_"+str(i)].get().split(',') #a list of each item id
            items = [] # a list of dicts with item id and count to match LOL format
            entered = [] #list of items already entered into items to prevent duplicates
            for item in item_data:
                if item not in entered:
                    items.append({"id":item,"count":item_data.count(item)})
                    entered.append(item)
            blocks.append({"type":block_type,"items":items}) #append this block to blocks

    writeSet(champ_entry.get(),name_entry.get(),blocks)


# gets user input using tkinter
def render():
    global root
    global champ_entry
    global name_entry
    global block_entries
    pad = 5 #const for grid padding

    #TODO: add support for Wukong who's tag is MonkeyKing
    #champion input
    champ_label = Label(root,
     text="Champion this set is for.\nRemove all spaces and non alphabet characters\n(e.g. enter Dr. Mundo as DrMundo)"
     ).grid(row=1, column=1,padx=pad)
    champ_entry.grid(row=2,column=1)

    #set name input
    name_label = Label(root,text="Name of this item set").grid(row=4,column=1,padx=pad)
    name_entry.grid(row=5,column=1,padx=pad)

    #map and game mode select will go in column 2

    #item block input directions
    block_name_label = Label(root,
     text="Name of each item block\n(e.g. Starting Items)"
     ).grid(row=1,column=3,padx=pad)
    block_data_label = Label(root,
     text="Comma seperated item ids for each item block\n(e.g. 1056,2003,2003,3340 is a Doran's Ring, 2 Health Potions, and a Warding Totem)"
     ).grid(row=1,column=4,padx=pad)

    #item block inputs
    for i in range(num_blocks):
        block_entries["type_"+str(i)].grid(row=i+2,column=3,padx=pad)
        block_entries["data_"+str(i)].grid(row=i+2,column=4,padx=pad)

    #buttons
    save_button = Button(root,text="Save Set",command=saveSet
     ).grid(row=2+num_blocks,column=4,pady=pad)
    delete_button = Button(root,text="Delete all Sets",command=deleteAllSets
     ).grid(row=2+num_blocks,column=1,pady=pad)

    root.mainloop()


def main():
    getLOLPath() #set global LOL_path variable
    render() #create the main interface


if __name__ == '__main__':
    main()