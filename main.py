# Import docx
#
# NOT python-docx
import docx
import csv
import pypandoc
import os

from htmldocx import HtmlToDocx



class Card:
    def __init__(self, text, extra):
        self.text = text
        self.extra = extra

cards = []
first = True

dirr = "/Users/michaelroth/AnkingImages/"

# open .tsv file
with open("/Users/michaelroth/Downloads/elpepe.txt") as file:
    # Passing the TSV file to
    # reader() function
    # with tab delimiter
    # This function will
    # read data from file
    tsv_file = csv.reader(file, delimiter="\t")

    # printing data line by line
    for line in tsv_file:
        if first:
            first = False
            continue
        cards.append(Card(line[3], line[4]))

# 1 cleanse the text
for card in cards:
    card.text = card.text.replace("\"\"", "\"")
    if card.text[0]== "\"":
        card.text = card.text[1:]
    if card.text[~0]=="\"":
        card.text = card.text[:-1]
    card.text = card.text.replace("<div>", "")
    card.text = card.text.replace("</div>", "")
    card.text = "<div>" + card.text + "</div>"
    card.text = card.text.replace("{{", "`{{")
    card.text = card.text.replace("}}", "}}`")

    print(card.text)


for card in cards:
    if(card.extra==""):
        continue

    card.extra = card.extra.replace("\"\"", "\"")
    if card.extra[0] == "\"":
        card.extra = card.extra[1:]
    if card.extra[~0] == "\"":
        card.extra = card.extra[:-1]
    card.extra = card.extra.replace("<div>", "")
    card.extra = card.extra.replace("</div>", "")

    #only image checking
    clone = card.extra
    if card.extra[0:4]=="<img" or card.extra[0:4]=="<br ":
        clone = clone.replace("<br />", "")
        clone = clone[clone.find(">")+1:]
        #if everything breaks, the bug is here (because img text img and the loop bellow will corrupt everything)

        while clone.find("<img") != -1:
            clone = clone[clone.find(">") + 1:]

        if len(clone)==0:
            card.extra = "Extra <br>" + card.extra


    card.extra = "<div>" + card.extra + "</div>"
    card.extra = card.extra.replace("img src=\"", "img src=\""+dirr)
    res = [i for i in range(len(card.extra)) if card.extra.startswith("src=", i)]
    spans = [i for i in range(len(card.extra)) if card.extra.startswith("<span", i)]


    while(len(spans)>0):
        for s in spans:
            p1 = card.extra[0:s]
            p2 = card.extra[s+1:]
            p2 = p2[p2.index(">")+1:].replace("</span>", "", 1)

            card.extra = p1+p2
            break
        spans = [i for i in range(len(card.extra)) if card.extra.startswith("<span", i)]

    # card.extra = card.extra.replace("<b style=\"font-style: italic; \">", "<b>")

    card.extra = card.extra.replace(" \"<", " &quot;<")


    if card.extra.find("<b style=\"font-style: italic; \">") != -1:
        card.extra = card.extra.replace("</b><i>", "")
        card.extra = card.extra.replace("</i><b style=\"font-style: italic; \">", "")
        card.extra = card.extra.replace("<b style=\"font-style: italic; \">", "michaelferrara")

        index = card.extra.find("michaelferrara")
        p2 = card.extra[index:].replace("</b>", "", 1)
        p1 = card.extra[:index]

        # print(p1)
        # print(p2)
        card.extra = p1+p2
        card.extra = card.extra.replace("michaelferrara", "")







    # images = []
    # notfound = []
    #
    # for r in res:
    #     img = ""
    #     for char in card.extra[r+5:]:
    #         if char=="\"":
    #             images.append(img)
    #             break
    #         img+=char
    #
    # for i in images:
    #     # print(i)
    #     exists = os.path.isfile(i)
    #     # print(exists)
    #
    # # print(images)

    # print(card.extra)
    # break;


out = open("outhtml.html", "w")
out.write("<ul>")
for i, card in enumerate(cards):
    out.write("<li>")
    out.write(card.text)
    out.write("<ul>")
    out.write("<li>")
    out.write(card.extra)
    out.write("</li>")
    out.write("</ul>")
    out.write("</li>")
out.write("</ul>")
out.close()

# new_parser = HtmlToDocx()
# new_parser.parse_html_file("outhtml.html", "jb")


output = pypandoc.convert_file(source_file='outhtml.html', format='html', to='docx', outputfile='/Users/michaelroth/Downloads/aanking.docx', extra_args=['-RTS'])




