#!/usr/bin/python

import math;
import subprocess
import os
class PieChartGenerator:
    """
        This class is used to generate a pie chart with given output file and data.
        The data format must be {"name":value}.
        The output file is PNG format.
        Usage:
            pcg PieChartGenerator(output_file, 3)
            pcg.generate_pie({"item1":100, "item2":200})
    """
    colors = ['rgb:red,102;green,255;yellow,0',
            'rgb:red,255;green,255;yellow,51',
            'rgb:red,255;green,0;yellow,255',
            'rgb:red,102;green,255;yellow,255',
            'rgb:red,0;green,0;yellow,255',
            'rgb:red,204;green,225;yellow,102',
            'rgb:red,51;green,255;yellow,204',
            'rgb:red,153;green,51;yellow,255',
            'rgb:red,51;green,102;yellow,255',
            'rgb:red,255;green,153;yellow,51']
    def __init__(self, output_file, pie_size):
        """
            output_file specifies the output file path, for PNG format.
            pie_size specifies the size of pie char, with cm.
        """
        self.output_file = output_file
        self.pie_size=pie_size
        self.string =''
        self.need_merge = True

    #the inputs shall be {"name": value}
    def generate_pie(self, inputs):
        total = 0
        for (name, value) in inputs.items():
            total += value
        
        pie_data = []
        sa = 90
        for (name, value) in sorted(inputs.items(), key = lambda d : d[1], reverse = True):
            label=name + '(' +"{:.2f}".format(100.0*value/total) + '\%' + ')'
            pie_data += [(label, sa - 360.0*(value)/total, sa)]
            sa = sa - 360.0*(value)/total
            
        if self.need_merge:
            pie_data = self.__merge_res(pie_data)
        self.__generate_pie_with_data(pie_data)
        
        tt_file = os.getcwd() + '/__temp_output.tex'
        f = open(tt_file, 'w')
        f.write(self.string)
        f.close()
        self.__convert_latex_to_png(tt_file, self.output_file)
        
    def __convert_latex_to_png(self, latex, output_file):
        pdffile = os.getcwd() + '/__temp_output.pdf'
        args = ['pdflatex', latex, '-o', pdffile]
        proc =  subprocess.Popen(args, stdout=subprocess.PIPE).communicate()
        args = ['convert', '-density', '300', pdffile, output_file]
        proc =  subprocess.Popen(args, stdout=subprocess.PIPE).communicate()
    def __merge_res(self, ps):
        merge = False
        mname = ''
        mstart =0
        mend = 0
        res=[]
        for(name, start, end) in ps:
            if math.fabs(end-start)*math.pi*100/360 > 15:
                res += [(name, start, end)]
            else:
                if not merge:
                    mend = end
                merge = True
                
            if merge:
                mstart= start
                if len(mname) == 0:
                    mname += name
                else:
                    mname += ', ' + name
                
        res += [(mname, mstart, mend)]
        
        return res
    def __generate_pie_with_data(self, ps):
        self.__write_chart_head()
        
        ci =0
        for (name, start, end) in ps:
            self.__write_one_arc(name, start, end, PieChartGenerator.colors[ci%len(PieChartGenerator.colors)])
            ci = ci + 1
        self.__write_chart_tail()
        
    def __write_chart_head(self):
        self.string += "\\documentclass{standalone} \n"
        self.string += "\\usepackage{tikz} \n"
        self.string += "\\begin{document} \n"
        self.string += "\\begin{tikzpicture}\n"
                    
    def __write_chart_tail(self):
        self.string += "\\end{tikzpicture} \n\
                    \\end{document}\n"
                    
    def __write_one_arc(self,name, start, end, color):
        ts= '\n\\filldraw[fill={' + color + '}](0, 0) -- (' +str(start) + ' : ' + str(self.pie_size) + 'cm) arc(' + str(start) + ':' + str(end) + ':' + str(self.pie_size) + 'cm) -- cycle;'
        half = (start + end) /2
        wr = self.pie_size + 1.2
        ts += '\\draw(' + str(half) + ':' + str(0.92*self.pie_size)+'cm) -- (' + str(half) + ':' + str(wr) + 'cm);\n'
        
        yc = wr * math.sin(half*math.pi/180)
        xc = wr * math.cos(half*math.pi/180)
        
        nxc = 0
        if xc > 0:
            nxc = xc + 2
        else:
            nxc = xc - 2
        ts += '\\draw(' + str(xc) + ',' + str(yc)+'cm) -- (' + str(nxc) + 'cm ,' + str(yc) + 'cm) node[sloped, above]{' + name + '};\n'
        self.string += ts
        
if __name__== '__main__':
    data = {'Item1': 100,
            'Item2': 90,
            'Item3': 40,
            'Item4': 20,
            'Item5': 10,
            'Item6': 3,
            'Item7': 2}
    pcg = PieChartGenerator(os.getcwd() + '/tt.png', 3)
    pcg.generate_pie(data)
    