import easyocr
reader = easyocr.Reader(['ch_sim','en'])

def input (values, num):
    exist = False
    for index, i in enumerate(values):
        if values[index] < num + 20 and values[index] > num - 20:
            exist = True
    if exist == False:
        values.append(num)
    return values


def output (values, num):
    for index, i in enumerate(values):
        if values[index] < num + 20 and values[index] > num - 20:
            return index
    return False


# i= 0
# array = []
# while i < 100:
#     print(i)
#     array = input(array, i)
#     i += 9
    
# print(array)

# for i in array:
#     print(i)

i = 2
while i < 11:

    xValues = []
    yValues = []

    xStandard = 0
    yStandard = 0
    row = 0
    maxCol = 0
    col = 0
    # for r in reader.readtext('images/img11.v1.jpg'):
    for r in reader.readtext('images/size'+str(i)+'.jpg'):
        if len(r[1]) > 5:
            continue
        
        col += 1

        yStart = r[0][0][1]
        yEnd = r[0][3][1]
        xStart =  r[0][0][0]
        xEnd =  r[0][1][0]
        yAve = yEnd - yStart
        xAve = xEnd - xStart
        
        if yStandard < yStart:
            row += 1
            if xStandard < xStart:
                maxCol = col
                xStandard = xEnd - xAve
            col = 0
            yStandard = yEnd

        xValues = input(xValues, xEnd - xAve)
        yValues = input(yValues, yEnd - yAve)

    xValues.sort()
    yValues.sort()
    
    table = [[]]
    # table = [[0 for c in range(maxCol)] for r in range(row)]

    # for r in reader.readtext('images/img11.v1.jpg'):


    for r in reader.readtext('images/size'+str(i)+'.jpg'):
        if len(r[1]) > 5:
            continue

        yStart = r[0][0][1]
        yEnd = r[0][3][1]
        xStart =  r[0][0][0]
        xEnd =  r[0][1][0]
        yAve = yEnd - yStart
        xAve = xEnd - xStart

        xPosition = output(xValues, xEnd - xAve)
        yPosition = output(yValues, yEnd - yAve)
        
        # print(xPosition, yPosition)
        # table[yPosition][xPosition] = r[1]
        if len(table) <= yPosition + 1:
            table.append([])
        table[yPosition].insert(xPosition, r[1])

        # table[xPosition][yPosition] = r[1]

        htmlCode = "<table>"

        for index, value in enumerate(table):
            htmlCode += "<tr>"
            for index2, value2 in enumerate(table[index]):
                # if len(table[index]) < maxCol:
                #     htmlCode += "<td colspan='"
                #     htmlCode += str(maxCol)
                #     htmlCode += "'>"
                # else:
                htmlCode += "<td>"
                htmlCode += str(table[index][index2])
                htmlCode += "</td>"
            htmlCode += "</tr>"

    # for r in reader.readtext('images/size'+str(i)+'.jpg'):
        
    #     yStart = r[0][0][1]
    #     yEnd = r[0][3][1]
    #     xStart =  r[0][0][0]
    #     xEnd =  r[0][1][0]
    #     yAve = yEnd - yStart
    #     xAve = xEnd - xStart

    #     if xEnd < xStandard:
    #         output += "</tr>"
    #         xStandard = 0

    #     if yStandard > yStart :
    #         output += "<tr>"
    #         yStandard = yAve  
    #     output += "<td>"
    #     output += r[1]
    #     output += "</td>"

    #     if xAve > xStandard:
    #         xStandard = xAve
    #     print(r)    

        htmlCode += "</table>\n"
    print(table)
    print(htmlCode)
    i += 1