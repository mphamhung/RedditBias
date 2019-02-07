from a1_preproc import preproc1

testComment = 'first_pn = ["i","me","my","mine","we","us","our","ours"] second_pn = ["you", "your", "yours", "u", "ur", "urs"] third_pn = ["he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"] future_v = ["ll", "gonna"].'

print(testComment)

for i in range(11):
    print(i)
    testComment = preproc1( testComment, steps = [i])
    print(testComment)


