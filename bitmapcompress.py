# Erik Safford
# Bitmaps and WAH 32/64 Bit Compression in Python
# Spring 2019


def unsortedBitmap():
    bitmap = []  # List to hold converted bitmap entries

    file = open("animals.txt", "r")  # Open a file for reading

    for line in file:  # Take in a line from the file at a time
        result = [x.strip() for x in line.split(',')]  # Split the line on ,'s, and strip newline, put into list

        part1 = ""  # Bits relating to the animal type (4 bits) [cat,dog,turtle,bird]
        part2 = ""  # Bits relating to the animal age (10 bits) [1-10,11-20,21-30,...,91-100]
        part3 = ""  # Bits relating to the adoption status (2 bits) [True,False]

        if result[0] == "cat":  # Mark the appropriate bit in part 1 to show type of animal
            part1 = "1000"
        elif result[0] == "dog":
            part1 = "0100"
        elif result[0] == "turtle":
            part1 = "0010"
        elif result[0] == "bird":
            part1 = "0001"

        if 1 <= int(result[1]) <= 10:  # Mark the appropriate bit in part2 to show age of animal
            part2 = "1000000000"
        elif 11 <= int(result[1]) <= 20:
            part2 = "0100000000"
        elif 21 <= int(result[1]) <= 30:
            part2 = "0010000000"
        elif 31 <= int(result[1]) <= 40:
            part2 = "0001000000"
        elif 41 <= int(result[1]) <= 50:
            part2 = "0000100000"
        elif 51 <= int(result[1]) <= 60:
            part2 = "0000010000"
        elif 61 <= int(result[1]) <= 70:
            part2 = "0000001000"
        elif 71 <= int(result[1]) <= 80:
            part2 = "0000000100"
        elif 81 <= int(result[1]) <= 90:
            part2 = "0000000010"
        elif 91 <= int(result[1]) <= 100:
            part2 = "0000000001"

        if result[2] == "True":  # Mark the appropriate bit in part3 to show the adoption status of the animal
            part3 = "10"
        elif result[2] == "False":
            part3 = "01"

        combinedStr = part1 + part2 + part3  # Combine all parts of the converted bits to make bitmap entry
        bitmap.append(combinedStr)  # Append the converted bitmap string to the bitmap list

    file.close()

    bitmapOutput = open("bitmapOutput.txt", "w")  # Open a new file for writing
    for i in range(len(bitmap)):  # Write the bitmap entries to bitmapOutput.txt file
        bitmapOutput.write(bitmap[i] + "\n")  # Add \n to keep formatting correct
    bitmapOutput.close()


def sortedBitmap():
    bitmap = []  # List to hold bitmap entries to be sorted/converted

    file = open("animals.txt", "r")  # Open a file for reading

    for line in file:  # Add each line entry in file to bitmap[] list, removing \n on each line
        bitmap.append(line.strip("\n"))

    bitmap.sort()  # Sort the bitmap2[] entries lexicographically

    for i in range(len(bitmap)):  # Split each entry in bitmap[] on ,'s
        bitmap[i] = bitmap[i].split(",")

    sortedBitmapOutput = open("sortedBitmapOutput.txt", "w")  # Open a output file for writing

    for i in range(len(bitmap)):
        part1 = ""  # Bits relating to the animal type (4 bits) [cat,dog,turtle,bird]
        part2 = ""  # Bits relating to the animal age (10 bits) [1-10,11-20,21-30,...,91-100]
        part3 = ""  # Bits relating to the adoption status (2 bits) [True,False]

        if bitmap[i][0] == "cat":  # Mark the appropriate bit in part 1 to show type of animal
            part1 = "1000"
        elif bitmap[i][0] == "dog":
            part1 = "0100"
        elif bitmap[i][0] == "turtle":
            part1 = "0010"
        elif bitmap[i][0] == "bird":
            part1 = "0001"

        if 1 <= int(bitmap[i][1]) <= 10:  # Mark the appropriate bit in part2 to show age of animal
            part2 = "1000000000"
        elif 11 <= int(bitmap[i][1]) <= 20:
            part2 = "0100000000"
        elif 21 <= int(bitmap[i][1]) <= 30:
            part2 = "0010000000"
        elif 31 <= int(bitmap[i][1]) <= 40:
            part2 = "0001000000"
        elif 41 <= int(bitmap[i][1]) <= 50:
            part2 = "0000100000"
        elif 51 <= int(bitmap[i][1]) <= 60:
            part2 = "0000010000"
        elif 61 <= int(bitmap[i][1]) <= 70:
            part2 = "0000001000"
        elif 71 <= int(bitmap[i][1]) <= 80:
            part2 = "0000000100"
        elif 81 <= int(bitmap[i][1]) <= 90:
            part2 = "0000000010"
        elif 91 <= int(bitmap[i][1]) <= 100:
            part2 = "0000000001"

        if bitmap[i][2] == "True":  # Mark the appropriate bit in part3 to show the adoption status of the animal
            part3 = "10"
        elif bitmap[i][2] == "False":
            part3 = "01"

        combinedStr = part1 + part2 + part3  # Combine all parts of the converted bits to make bitmap entry
        sortedBitmapOutput.write(combinedStr + "\n")  # Write sorted line entries to txt file

    sortedBitmapOutput.close()
    file.close()


def compressBitmap(readFile, writeFile, type):
    file = open(readFile, "r")  # Open a file for reading

    bitmap = []  # This will hold the lines of the bitmapOutput
    lineCount = 0  # Number of lines in bitmapOutput
    bitmapLine = ""  # This will hold a 31 bit section of the file to process
    byteCount = 0  # Number of currently read bytes in the bitmapLine
    total = 0  # The total of all 16 bytes in a bitmapLine, 0 = run zeros, 31 = run ones
    runCount0 = 0  # Number of 0 runs currently being stored in runStr
    runCount1 = 0  # Number of 1 runs currently being stored in runStr
    gRun0 = 0
    gRun1 = 0  # Global counts to keep track of how many type runs/literals
    globalLit = 0

    for line in file:  # For each line entry in file, append the line w/out a \n to the bitmap list
        bitmap.append(line.strip("\n"))
        lineCount += 1  # Keep track of how many entries are in the bitmap list

    compressedFile = open(writeFile, "w")  # Open a txt file for writing

    for x in range(16):  # For as many columns as are in the bitmap (always 16)
        for y in range(lineCount):  # For as many lines are in the bitmap
                                    # type-1 = 31 (32 bit), type-1 = 63 (64 bit)
            if byteCount < type-1:  # If we don't have 31/63 bytes stored
                b = bitmap[y][x]  # Grab the byte from the column we are compressing
                bitmapLine += b   # Add it to a growing run of column bytes
                byteCount += 1    # Increment the number of column bytes we have stored
            if byteCount == type-1:  # If we have 31/63 bytes stored, time to find out if run or literal
                # print(bitmapLine + " column read")  # Have to compress this string and write into new file

                for i in range(byteCount):  # Find byte total of bitmapLine to determine if run/literal
                    total += int(bitmapLine[i])  # Add up all the numbers in the bitmapLine

                if total == 0:  # If total is 0, have a run of 0's (31 zero's)
                    flag = 0
                elif total == type-1:  # If total is 31/63, We have a run of 1's (31 one's/63 one's)
                    flag = 1
                else:  # Else we have some mixture of 0's and 1's, so is a literal
                    flag = -1

                if flag == 0 or flag == 1:  # If bitmapLine is a run of 0's or 1's
                    if flag == 0:  # Keep track of how many type runs
                        gRun0 += 1
                    if flag == 1:
                        gRun1 += 1

                    if flag == 0 and runCount1 == 0:  # If we have a run of 0's and no stored runs of 1's
                        runCount0 += 1  # Increment the number of consecutive 0 runs
                    # This deals with back to back runs
                    elif flag == 0 and runCount1 != 0:  # Else if we have a run of 0's and previous stored runs of 1's
                        runStr = "11" + bin(runCount1)[2:].zfill(type - 2)  # Convert run # to bin, and pad with 0's
                        compressedFile.write(runStr)   # Write compressed runs to file
                        runCount1 = 0  # Reset 1 run count

                        runCount0 += 1  # Increment 0 run count
                    elif flag == 1 and runCount0 == 0:
                        runCount1 += 1  # Increment the number of consecutive 1 runs
                    # This deals with back to back runs
                    elif flag == 1 and runCount0 != 0:
                        runStr = "10" + bin(runCount0)[2:].zfill(type - 2)  # type-2 = 30 (32 bit) or 62 (64 bit)
                        compressedFile.write(runStr)  # Write compressed runs to fil
                        runCount0 = 0  # Reset 0 run count

                        runCount1 += 1 # Increment 1 run count
                elif flag == -1:  # Else if bitmapLine is a literal, write any stored runs to file,
                    # then add 0 to beginning to lit, write lit to file
                    globalLit += 1  # Keep track of number of compressed lits

                    if runCount0 > 0:  # If we have run(s) of 0's saved, write to file
                        runStr = "10" + bin(runCount0)[2:].zfill(type-2)  # type-2 = 30 (32 bit) or 62 (64 bit)
                        compressedFile.write(runStr)  # Write compressed 0 runs to file
                        runCount0 = 0
                    if runCount1 > 0:  # If we have run(s) of 1's saved, write to file
                        runStr = "11" + bin(runCount1)[2:].zfill(type-2)
                        compressedFile.write(runStr)  # Write compressed 1 runs to file
                        runCount1 = 0
                    bitStr = "0" + bitmapLine  # Write literal to file
                    compressedFile.write(bitStr)
                total = 0  # Reset flag variables
                bitmapLine = ""
                byteCount = 0
        # These deal with stored runs/literals less then 31/63 at the end of a column
        if runCount0 > 0:  # If we have run(s) of 0's saved, write to file
            runStr = "10" + bin(runCount0)[2:].zfill(type-2)
            compressedFile.write(runStr)
            runCount0 = 0
        elif runCount1 > 0:  # If we have run(s) of 1's saved, write to file
            runStr = "11" + bin(runCount1)[2:].zfill(type-2)
            compressedFile.write(runStr)
            runCount1 = 0
        if byteCount > 0:  # If we have a literal less then 31/63 at end of column
            bitStr = "0" + bitmapLine
            compressedFile.write(bitStr)  # Write baby lit to file
            globalLit += 1
        bitmapLine = ""
        byteCount = 0
        compressedFile.write("\n")  # \n signifies the end of the compressed column

    compressedFile.close()
    file.close()
    # Print total fills of 0's and 1's, and total literals compressed into writeFile
    print(writeFile+" - \'0 Fills\': "+str(gRun0)+" - \'1 Fills\': "+str(gRun1)+" - \'Literals\': "+str(globalLit))


def main():
    # ************************** UNSORTED BITMAP **********************************************************************
    # Creates "bitmapOutput.txt"
    unsortedBitmap()

    # ************************** SORTED BITMAP ************************************************************************
    # Creates "sortedBitmapOutput.txt"
    sortedBitmap()

    # ************************** UNSORTED 32 BIT COMPRESSION **********************************************************
    # Creates "compressed32.txt"
    compressBitmap("bitmapOutput.txt", "compressed32.txt", 32)

    # ************************** SORTED 32 BIT COMPRESSION ************************************************************
    # Creates "compressed32sorted.txt"
    compressBitmap("sortedBitmapOutput.txt", "compressed32sorted.txt", 32)

    # ************************** UNSORTED 64 BIT COMPRESSION **********************************************************
    # Creates "compressed64.txt"
    compressBitmap("bitmapOutput.txt", "compressed64.txt", 64)

    # ************************** SORTED 64 BIT COMPRESSION ************************************************************
    # Creates "compressed64sorted.txt"
    compressBitmap("sortedBitmapOutput.txt", "compressed64sorted.txt", 64)


main()

