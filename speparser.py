"""LSRM *.spe parser """
import struct
import sys

def str_to_float_def(string, defValue = 0.0):
    try:
        return float(string)
    except:
        return defValue

class Spectrum:
    def __init__(self):
        self.name = ""
        self.tlive = 0.0
        self.treal = 0.0
        self.geometry = ""
        self.distance = 0.0
        self.headerdict = {}
        self.spectr = []

    def print_params(self):
        for key,value in self.headerdict.items():
            if value:
                print(key, value, sep = '=')
            else:
                print(key)

    def save_as_txt(self, filename):
        with open(filename, "w") as f:
            # write header
            f.write('SHIFR=' + self.name + '\n')
            f.write('TLIVE=' + str(self.tlive) + '\n')
            f.write('TREAL=' + str(self.treal) + '\n')
            if 'MEASBEGIN' in self.headerdict:
                f.write('DATE=' + (self.headerdict['MEASBEGIN'].split(" "))[0] + '\n')
                f.write('TIME=' + (self.headerdict['MEASBEGIN'].split(" "))[1] + '\n')

            #write spectr head
            f.write("SPECTRTXT=" + str(len(self.spectr)) + '\n')

            # writing spectr
            i = 1
            for x in self.spectr:
                f.write(str(i) + '\t' + str(x) + '\n')
                i += 1

    def save_as_spe(self, filename):
        f = open(filename, "wb")
        #write header
        f.close()

    @staticmethod
    def write_line(f, line):
        for c in line:
            f.write(c)
        f.write('\n')


class SpectrumReader:
    @staticmethod
    def parse_spe(spe_fname):
        spectr = Spectrum()
        with open(spe_fname, 'rb') as f:
            # read header
            parname = ''
            while parname != "SPECTR":
                parname, parvalue = SpectrumReader.readline(f)
                if parname == "SHIFR":
                    spectr.name = parvalue
                elif parname == "TLIVE":
                    spectr.tlive = str_to_float_def(parvalue)
                elif parname == "TREAL":
                    spectr.treal = str_to_float_def(parvalue)
                elif parname == "GEOMETRY":
                    spectr.geometry = parvalue
                elif parname == "DISTANCE":
                    spectr.distance = str_to_float_def(parvalue)
                elif parname != "SPECTR" and parvalue:
                    spectr.headerdict[parname] = parvalue

            # read binary data
            i = f.read(4)
            while len(i) > 3:
                x = struct.unpack("i", i)
                spectr.spectr.append(x[0])
                i = f.read(4)
        return spectr

    @staticmethod
    def readline(f):
        c = ''
        param_name = ''
        param_value = ''
        is_has_value = False
        while c != '\r':
            b = f.read(1)
            c = b.decode(encoding="cp1251")
            #print(param_name, param_value)
            
            if c == '\r': # next string
                f.read(1) #reading \n
                if is_has_value:
                    return param_name, param_value
                else:
                    return param_name, None
            elif c == '=' and param_name == "SPECTR": # start of spectr section
                return param_name, None
            elif c == '=':
                is_has_value = True
            else:
                if is_has_value:
                    param_value += c
                else:
                    param_name += c


        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit()
    s = SpectrumReader().parse_spe(sys.argv[1])
    s.print_params()
    s.save_as_txt("test.txt")
