import time
import easyocr
from collections import defaultdict
from PIL import Image

reader = easyocr.Reader(['ch_sim','en'])

startTime = time.time()

table_index = 11
while table_index < 12:
    words = defaultdict(list)
    xPositions = []
    for r in reader.readtext('images/size'+str(table_index)+'.png'):
        if len(r[1]) > 20:
            continue

        yStart = r[0][0][1]
        yEnd = r[0][2][1]
        yMiddle = yEnd - ((yEnd - yStart) / 2)
        xStart =  r[0][0][0]
        xEnd = r[0][2][0]
        xMiddle = xEnd - ((xEnd - xStart) / 2)
        # save x-axis of the middle of the word as the first element of the array
        # and the text is the second element
        words[round(yMiddle, -1)].append([xMiddle, r[1]])
        
    table = []
    for word in words:
        words[word].sort()
        # include rows if only have more than 3 columns
        if len(words[word]) >= 3:
            table.append(words[word])
    # find the row that has the largest column number
    longestRow = max(table)

    startingPoint = 0
    for i, x in enumerate(longestRow):
        # save the starting and the end point of the column in xPositions array
        endPoint = startingPoint + ((x[0] - startingPoint) * 2)
        xPositions.append([startingPoint, endPoint])
        startingPoint = endPoint

    # start building html tag
    htmlCode = "<table>"
    for index, value in enumerate(table):
        # if first row, column tag is th, else td
        htmlCode += "<tr>"
        xPositionIndex = 0
        if index == 0:
            columnTag = "th"
        else:
            columnTag = "td"

        for index2, position in enumerate(xPositions):
            # if middle x_positions of the columns are in between starting and end point of the longest row
            # add text to the column, or add a em
            try:
                if xPositions[index2][0] < table[index][xPositionIndex][0] and table[index][xPositionIndex][0] < xPositions[index2][1]:
                    htmlCode += "<"+columnTag+">"
                    htmlCode += table[index][xPositionIndex][1]
                    htmlCode += "</"+columnTag+">"
                    xPositionIndex += 1
                else:
                    htmlCode += "<"+columnTag+"></"+columnTag+">"
            except IndexError:
                htmlCode += "<"+columnTag+"></"+columnTag+">"
                pass

        htmlCode += "</tr>"

    htmlCode += "</table>\n"
    print(htmlCode)
    table_index += 1

endTime = time.time()
print(endTime - startTime)
