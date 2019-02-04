from a1_preproc import preproc1

testComment = "No, i'm not a ts, i'm just a gay male who likes to look good. I don't mind buying covergirl, it works.  Thats all i care about."

print(testComment)

for i in range(11):
    print(i)
    testComment = preproc1( testComment, steps = [i])
    print(testComment)


