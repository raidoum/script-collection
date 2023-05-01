import sys
import struct
from enum import Enum

class Error(Enum):
    ERROR_CODE_OK = 0
    ERROR_CODE_NG = 1

class Endian(Enum):
    ENDIAN_LE   = 0
    ENDIAN_BE   = 1
    ENDIAN_NONE = 2  # 未設定

class Type(Enum):
    TYPE_SIGNED      = 0
    TYPE_FLOAT       = 1
    TYPE_NONE        = 2 # 未設定

class Format(Enum):
    FORMAT_SIGNED_16 = 0
    FORMAT_FLOAT_32  = 1
    FORMAT_NONE      = 2 # 未設定
    
class ParamInfo(object):
    def set(self, src, dst):
        self.src = src
        self.dst = dst
    
    def get(self):
        return self.src, self.dst
        
class EndianInfo(ParamInfo):

    def __init__(self):
        self.src = Endian.ENDIAN_NONE
        self.dst = Endian.ENDIAN_NONE

class FormatInfo(ParamInfo):

    def __init__(self):
        self.src = Format.FORMAT_NONE
        self.dst = Format.FORMAT_NONE

class ConvertInfo(object):

    def __init__(self):
        self.endian = EndianInfo() 
        self.format = FormatInfo()
        self.size   = 0
        
    def set_endian(self, src, dst):
        self.endian.set(src, dst)
    
    def set_format(self, src, dst):
        self.format.set(src, dst)

    def set_size(self, size):
        self.size = size

    def get_endian(self):
        return self.endian.get()

    def get_format(self):
        return self.format.get()

    def get_size(self, size):
        return self.size

def convert_binary_to_numeric(input, type, endian):
    
    # binary -> float
    if type == Type.TYPE_FLOAT:
        if endian == Endian.ENDIAN_BE:
            return struct.unpack('>f', input)[0]

        if endian == Endian.ENDIAN_LE:
            return struct.unpack('<f', input)[0]
    
    # binary -> signed
    elif type == Type.TYPE_SIGNED:
        if endian == Endian.ENDIAN_BE:
            return struct.unpack('>h', input)[0]
        if endian == Endian.ENDIAN_LE:
            return struct.unpack('<h', input)[0]

    # other
    else:
        return input

def convert_numeric_to_binary(input, type, endian):

    # singed -> binary
    if type == Type.TYPE_SIGNED:
        if endian == Endian.ENDIAN_BE:
            return struct.pack('>h', input)

        if endian == Endian.ENDIAN_LE:
            return struct.pack('<h', input)
    
    # float -> binary
    elif type == Type.TYPE_FLOAT:
        if endian == Endian.ENDIAN_BE:
            return struct.pack('>f', input)

        if endian == Endian.ENDIAN_LE:
            return struct.pack('<f', input)
    # other
    else:
        return input

def read_binary(in_file, unit, read_data):

    with open(in_file, "rb") as rf:
        while True:
            bytes = rf.read(unit)
            
            if not bytes:
                break

            # add binary to list
            read_data.append(bytes)
            

def write_binary(out_file, write_data):

    with open(out_file, "wb") as wf:
        for bytes in write_data:
            wf.write(bytes)
        
    
def convert_float32_to_signed16(r_data, w_data, type, endian):

    endian_src, endian_dst = endian
    type_src, type_dst = type

    for data_b in r_data:

        # binary -> flaot
        data_f = convert_binary_to_numeric(data_b, type_src, endian_src)
        
        # float -> int
        data_i = int(pow(2, 15) * data_f)
        
        # int -> binary
        data_b = convert_numeric_to_binary(data_i, type_dst, endian_dst)
        
        # add binary to list
        w_data.append(data_b)


def convert_signed16_to_float32(r_data, w_data, type, endian):

    endian_src, endian_dst = endian
    type_src, type_dst = type

    for data_b in r_data:

        # binary -> signed
        data_i = convert_binary_to_numeric(data_b, type_src, endian_src)
        
        # signed -> float
        data_f = float(data_i) / pow(2, 15)
        
        # float -> binary
        data_b = convert_numeric_to_binary(data_f, type_dst, endian_dst)
        
        # add binary to list
        w_data.append(data_b)


def convert_binary(in_file, out_file, conv_info):

    # binary list
    read_data  = []  
    write_data = []

    endian = conv_info.get_endian()
    format = conv_info.get_format()

    # check format
    if format[0] == Format.FORMAT_FLOAT_32:
        byte_size = 4 # 32bit -> 4byte

    elif format[0] == Format.FORMAT_SIGNED_16:
        byte_size = 2 # 16bit -> 2byte
        
    # read & convert endian
    read_binary(in_file, byte_size, read_data)

    # convert binary 
    if format[0] == Format.FORMAT_FLOAT_32:
        if format[1] == Format.FORMAT_SIGNED_16:
            type = (Type.TYPE_FLOAT, Type.TYPE_SIGNED)
            convert_float32_to_signed16(read_data, write_data, type, endian) 

    elif format[0] == Format.FORMAT_SIGNED_16:
        if format[1] == Format.FORMAT_FLOAT_32:
            type = (Type.TYPE_SIGNED, Type.TYPE_FLOAT)
            convert_signed16_to_float32(read_data, write_data, type, endian) 

    # write
    write_binary(out_file, write_data)

if __name__ == '__main__':
    
    # Signed16bit と Float32bit の変換用スクリプト
    # sys.argv[1] : File Path Input
    # sys.argv[2] : File Path Output 
    # sys.argv[3] : Endian Input
    # sys.argv[4] : Endian Output
    # sys.argv[5] : Format Input
    # sys.argv[6] : Format Output
    
    if (len(sys.argv) < 3):
        print("command line argument too few")
    
    else:
        input_file   = sys.argv[1]
        output_file  = sys.argv[2]
        convert_info = ConvertInfo()

        # Todo: コマンドライン引数からエンディアンやフォーマットを文字列で受け取って、
        #       値をEnumの値を指定するように変更すること

        # sined16bit -> float32bit
        convert_info.set_format(Format.FORMAT_SIGNED_16, Format.FORMAT_FLOAT_32)
        convert_info.set_endian(Endian.ENDIAN_BE, Endian.ENDIAN_LE)

        # float32bit -> sined16bit
        #convert_info.set_format(Format.FORMAT_FLOAT_32, Format.FORMAT_SIGNED_16)
        #convert_info.set_endian(Endian.ENDIAN_LE, Endian.ENDIAN_BE)

        # convert process
        convert_binary(input_file, output_file, convert_info)
