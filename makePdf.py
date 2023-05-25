import pdfkit
import sys
import settings as sets
#Define path to wkhtmltopdf.exe
path_to_wkhtmltopdf = sets.pathToWkhtmltopdf

def makePdf(path1,path2):
	#Point pdfkit configuration to wkhtmltopdf.exe
	config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
	pdfkit.from_file(path1,output_path=path2,configuration=config,options={"enable-local-file-access": ""})

f1=sys.argv[1]
f2=sys.argv[2]
makePdf(f1, f2)