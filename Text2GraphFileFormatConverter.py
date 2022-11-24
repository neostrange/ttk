import os

# List all files in a directory using os.listdir
basepath = 'data/text2graph'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        print(entry)
        split_entry= entry.split('_')
        filename = split_entry[0]
        timex = split_entry[1].split('.')[0]
        print("filename: " , filename)
        print("timex", timex)

        # compose the command to run
        command = '../venv/bin/python tarsqi.py --dct ' + timex +' data/text2graph/'+entry+' ' + filename+'.xml'
        stream = os.popen(command) 