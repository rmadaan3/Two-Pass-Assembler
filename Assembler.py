#Kanishk Rana-2017241


# from inputtables import *
import _pickle as pickle
label_table={}
symbol_table={}
stp=0
op_table={"CLA":"0000", "LAC":"0001", "SAC":"0010", "ADD":"0011", "BRN":"0110", "BRP":"0111", "INP":"1000", "DSP":"1001", "MUL":"1010", "DIV":"1011", "STP":"1100","SUB":"0100", "BRZ":"0101"}
literal_table={}
linenumber=1
il=0
# relocation={"offset":0}
instructionloadingcounter=0
testbool00=True
special_op={"DS":"4","DW":"4","DC":"4"}
value_table={}
stpflag=0
errorfile=open("error.txt","w")
# relocationfile=open("relocationfile.txt","w")


def checkifcomment(line):
	"""Checks if line is a comment.

	:param line: string that can be a comment

	"""
	x="//"
	t=c=-1
	for i in line:
		t=t+1
		if x in i:
			c=t
			return c
	return c

def checkifopcodeexists(line):
	"""Checks if opcode is valid.

	:param line: string that can contain opocode
	:returns: boolean value

	"""
	
	
	linelen=len(line)
	if(linelen==1):
		X=line[0]
		return (X in op_table.keys() or X in special_op.keys())
	elif(linelen==3):
		Y=line[1]
		return (Y in op_table.keys() or Y in special_op.keys())
	else:
		Y=line[1]
		X=line[0]
		if((Y in op_table.keys() or Y in special_op.keys()) or ( X in op_table.keys() or X in special_op.keys())):
			return True
		return False

def checkstp(line):
	"""Checks if stop is encountered in line.

	:param line: string to compare with STP
	:returns: boolean value

	"""
	
	
	linelen=len(line)

	if(linelen==1):
		X=line[0]
		return (X=="STP")
	elif(linelen==3):
		Y=line[1]
		return (Y=="STP")
	else:
		X=line[0]
		Y=line[1]
		if(Y=="STP" or X=="STP"):
			return True
	return False

def printtable(dict1):
	"""Used to print tables created in pass 1.

	:param dict1: dictionary used as table

	"""
	chklen=len(dict1.keys())
	if(chklen!=0):
		for i in dict1.keys():
			print(str(i)+"   "+str(dict1[i]))
	else:
		print("Table is Empty")
        
def checkifliteral(line):
	"""Checks if line contains a literal.

	:param line: string that can contain literal
	:returns: boolean value

	"""
	check1=len(line[-1])
	check2=line[-1][0:2]
	check3=line[-1][-1]
	check4=line[-1]
	if(check1>1 and check2=='\'=' and check3=='\'' and check4 not in literal_table.keys()):
		return True
	else:
		return False

def file_len(fname):
	"""Returns length of file.

	:param fname: file containing assembly program
	:returns: integer length of file

	"""
	with open(fname) as f:
		for i, l in enumerate(f):
			continue
	return i + 1



#main
if __name__ == "__main__":
	# content=[]
	
	with open("2017241.txt") as f:
		# print('f=',f.readlines())
		content1=f.readlines()
		# print(content)
	# content=[]
	content=[x.strip("\n") for x in content1]
	
	machinecodefile=open("machinecode.txt","w")
	gmc=0
	instructionloadingcounteraftercontent=8*len(content)
	# instructionloadingcounteraftercontent+=relocation["offset"]

	for l in content:

		line=list(map(str, l.split()))
		val=checkifcomment(line)
		length=0
		illegal=0
		if(val!=-1):
			line=line[:val] 

		check1=len(line)   
		if(check1!=0):

			lineZ=line[0]
			# lineY=line[1]
			if(checkifopcodeexists(line)):
				lineA=line[0]
				if(check1==1):

					if(lineA!='CLA' and lineA!='STP'):
						
						errorfile.write(str(linenumber)+" has less operands")
						#print(str(linenumber)+" has less operands")
						testbool00=False
						
				elif(check1==2):

					# lineB=line[1]
					testbool=line[1] in op_table.keys()
					if(lineA in op_table.keys()):	
						if(lineA=='CLA' or lineA=='STP'):

							errorfile.write(str(linenumber)+" has less operands")
							#print(str(linenumber)+" has less operands")
							testbool00=False
							
					if(testbool):
						if(line[1]!='CLA' and line[1]!='STP'):
							
							errorfile.write(str(linenumber)+" has less operands")
							#print(str(linenumber)+" has less operands")
							testbool00=False
							
				elif(check1==3):
					if(lineA in op_table.keys() or lineA in special_op.keys()):
						
						errorfile.write(str(linenumber)+" has more operands")
						#print(str(linenumber)+" has less operands")
						testbool00=False
						
						
					elif(lineB=='CLA' and lineB=='STP'):
						
						errorfile.write(str(linenumber)+" has an opcode with insufficient operands")
						#print(str(linenumber)+" has less operands")
						testbool00=False
						
				
				if(checkstp(line) and stp==0):
					stp=1
				if(lineA not in op_table.keys()):
					if(lineA not in label_table.keys()):
						label_table[lineA]=instructionloadingcounter
					#print(line[0])
				
				if(checkifliteral(line)):

					lineB=line[-1]
					literal_table[lineB]=instructionloadingcounteraftercontent
					instructionloadingcounteraftercontent+=8
					
				elif(check1>1):

					lineC=line[-2]
					if(lineC in op_table.keys()):
						length+=8
						lineD=line[-1]
						if(lineD not in label_table.keys()):
							symbol_table[lineD]=instructionloadingcounter
						else:
							errorfile.write(str(lineD)+ " has multiple declarations.")
							testbool00=False
							# print("Line "+str(linenumber)+" Multiple declarations of the same variable")
							# print("Above error arised from a check of lenght of instruction being fed of length greater than 1")
							# print()
					elif(lineC in special_op.keys()):
						length+=4
						lineE=line[0]
						lineF=line[2]
						value_table[lineE]=lineF
						
					
					
				elif(check1==1):

					lineG=line[0]

					boolcheck1=lineG not in op_table.keys()
					boolcheck2=lineG not in special_op.keys()
					if( boolcheck1 and boolcheck2):
						illegal=1
			
			
			else:
				print(str(linenumber)+" No valid opcode exists")
				errorfile.write(str(linenumber)+ " No valid opcode.")
				testbool00=False
			
			instructionloadingcounteraftercontent+=8
		#print(testbool00,l)
		linenumber+=1


	for i in symbol_table.keys():
		if(i in label_table.keys()):
			pass
		else:
			errorfile.write("Symbol "+i+" is not defined     ")
			print("Symbol "+i+" is not defined")
			print("Above Error from checking in symbol table")
			print()

	if(stp!=0):
		pass
	else:
		print("No STP opcode")
		errorfile.write("No STP opcode")
	
	errorfile.close()


	with open("value_table_file.txt","wb") as file:
		file.write(pickle.dumps(value_table))

	with open("symbol_table_file.txt","wb") as file:
		file.write(pickle.dumps(symbol_table))

	with open("label_table_file.txt","wb") as file:
		file.write(pickle.dumps(label_table))

	with open("literal_table_file.txt","wb") as file:
		file.write(pickle.dumps(literal_table))

	if testbool00:
		count=0
		for l in content:
			printstr=""
			line=list(map(str, l.split()))
			
			if((checkifcomment(line))!=-1):
				val=checkifcomment(line)
				line=line[:val]   

			check1=len(line) 
			if(check1!=0):
				check2=checkifopcodeexists(line)
				if(check2):
					#print(l)
					line1=bin(count)[2:]
					counter=line1
					#print(counter,count)
					line2=(8-len(counter))*'0'
					counter=line2+counter
					printstr+=counter+"  "

					check3=len(line)
					check4=line[0]
					if(check3==1):
						printstr+=op_table[check4]

					elif(check3==2):
						
						if(check4 in op_table.keys()):
							printstr+=op_table[check4]+"  "
							
							check5=line[1]
							if(check5 in label_table.keys()):
								slice1=bin(label_table[line[1]])
								counter=slice1[2:]
								line3=(8-len(counter))*'0'
								counter=line3+counter 
								printstr+=counter+"  "
							
							elif(check5 in literal_table.keys()):
								line111=int(literal_table[line[1]])
								slice2=bin(line111)
								# print('type of counter=',typeof(line100))
								counter=slice2[2:]
								line4=(8-len(counter))*'0'
								counter=line4+counter
								printstr+=counter+"  "

						elif(check4 in label_table.keys()): 
							printstr+=op_table[line[1]]



					elif(check3==3):

						check6=line[1]
						if(check6 not in special_op.keys()): 
							printstr+=op_table[check6]+"  "
							
							check7=line[2]
							if(check7 in label_table.keys()):
								slice3=bin(label_table[line[2]])
								counter=slice3[2:]
								line4=(8-len(counter))*'0'
								counter+=line4 
								printstr+=counter+"  "
							
							elif(check7 in literal_table.keys()):
								line111=int(literal_table[line[2]])
								slice4=bin(line111)
								counter=slice4[2:]
								line5=(8-len(counter))*'0'
								counter=line5+counter
								printstr+=counter+"  "

					machinecodefile.write(printstr)
					print(printstr)
					count+=8
	else:
		print("Input file is incorrect, machine code translation not possible")


machinecodefile.close()


