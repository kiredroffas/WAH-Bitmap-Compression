# WAH-Bitmap-Compression
* This Python script creates both unsorted and sorted versions of a bitmap index by reading from a substantially large data file (animals.txt) containing information about pets, their age, and whether they are adopted or not. 
* Both bitmaps are ouput into files bitmapOutput.txt and sortedBitmapOutput.txt.
* The first bitmap has the same order as the data file, with the second bitmap being sorted lexicographically.
* The bitmap indexes have a column for each possible animal, in the order represented in its domain. Following the four animal columns, the bitmap has 10 columns that represent the bins for the Age attribute. Each bin is 10 long, i.e. 1-10, 11-20, 21-30, etc. The last two columns of the bitmap represent True and False in that order for the Adopted attribute. 
* Once both bitmaps are created, both versions are then compressed using WAH (Word Aligned Hybrid) compression using 32 and 64 bit words. 
* Compressed files are output as : compressed32.txt, compressed32sorted.txt, compressed64.txt, and compressed64sorted.txt.
* I attempted to code for special cases when reading fills/literals from the columns of the bitmap including:
    * compressing saved runs and literal < 31/63 at the end of a column
    * compressing back to back fill runs of 1's and 0's with no literal in between 
# Example Database Bitmap Creation:
![Alt text](/screenshots/sc2.png?raw=true "sc2")
# WAH 32/64 Bit Compression Algorithm:
* The WAH compression algorithm is as follows:
    1. Take 31/63 bits from the input.
    2. If all zeros, then increment the zero run count by 1 (stored as binary).
        * Continue incrementing zero run count by 1 if next 31/63 bits are all zeros.
        * If next 31/63 bits are not all zeros then output 32/64 bits with bit 0 = 1 and bit 1 = 0, with bits 2-32/64 being the number of zero count runs (binary number).
    3. If all ones, then increment the ones run count by 1 (stored as binary).
        * Continue incrementing ones run count by 1 if next 31/63 bits are all ones.
        * If next 31/63 bits are not all ones then output 32/64 bits with bit 0 = 1 and bit 1 = 1, with bits 2-32/64 being the number of ones count runs (binary number).
    4. Else if not all zeros or ones, then bit string is stored as a literal, with bit 0 = 0, with bits 1-32/64 being the actual literal bit string (combination of zeros/ones).
## Example WAH 32 Bit
* Runs
    * 2 runs of 31 zeros = <b>10</b>000000 00000000 00000000 00000010 (compressed) = 00000000 00000000 00000000 0000000 00000000 00000000 00000000 0000000 (uncompressed)
    * 2 runs of 31 ones = <b>11</b>000000 00000000 00000000 00000010 (compressed) = 11111111 11111111 11111111 1111111 11111111 11111111 11111111 1111111 (uncompressed)
* Literals
    * mix of 31 zeros and ones = <b>0</b>1010111 10000110 00101010 11010111 (compressed) = 1010111 10000110 00101010 11010111 (uncompressed)
# To run:
* To run this program: python ./bitmapcompress.py   
    * May have to chmod 755
    * animals.txt must be in the same directory as bitmapcompress.py
* Program will ouput total fills/literals per file, and six output .txt files 
# bitmapcompress.py Output
![Alt text](/screenshots/sc1.png?raw=true "sc1")
# Output Testing
* I tested my program with the test data file animals_test.txt (smaller version of animals.txt), which had an exact diff match for each of the 4 files included (animals_test_bitmap, animals_test_bitmap_sorted, animals_compressed_32, animals_compressed_sorted_32).
# Analysis
* Created files:
    * bitmapOutput.txt: bitmap created from the original animals.txt (unsorted)
    * sortedBitmapOutput.txt: bitmap created from the sorted animals.txt (sorted)
    * compressed32.txt: the unsorted bitmap compressed using 32 bit WAH
    * compressed32sorted.txt: the sorted bitmap compressed using 32 bit WAH
    * compressed64.txt: the unsorted bitmap compressed using 64 bit WAH
    * compressed64sorted.txt: the sorted bitmap compressed using 64 bit WAH
* File sizes:
    * animals.txt:            1,311 KB
    * bitmapOutput.txt:       1,661 KB
    * sortedBitmapOutput.txt: 1,661 KB
    * compressed32.txt:       1,612 KB
    * compressed32sorted.txt: 113 KB
    * compressed64.txt:       1,588 KB
    * compressed64sorted.txt: 220 KB
* Initially putting the animals.txt data into bitmaps increased the data size a bit because of the way I had to store the type, age, and adoption status (16 bit lines). The unsorted/sorted bitmaps are the same size because they contain the same entries, just in a different order. However, when it came to compressing the sorting made a huge difference in size, going to nearly ~1/16 the original size, where the unsorted came out a little smaller but nowhere even close to the compression that was made in the sorted. This is because when I compressed on columns in the sorted bitmaps there was much more opportunites to compress multiple runs of 0's and 1's, whereas in the unsorted we had to store nearly every entry as a literal (with the exception of a few fill runs). Different word sizes do seem to have different compression ratios, with it being more efficiently compressed the closer the line size of the data is to the compression type. I.e. if each line in bitmap is 16 long it would be more effiecient to compress with 32-bit WAH as opposed to 64 bit WAH (since 16 closer to 32). Also you would have to consider if you will have enough runs to make using a higher bit compression worth it (i.e. 64 bit could store more consecutive runs).
