
def readAuthFiles(auth_path):
    with open(auth_path) as f:
        auth_lines = f.readlines()

        return {l.split(":")[0]:l.split(":")[1].strip() for l in auth_lines}


#print(readAuthFiles("./authFiles.txt"))