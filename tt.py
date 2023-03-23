import asposewordscloud as aw

# Load the HTML file from disk
doc = aw.Document("/Users/michaelroth/Downloads/test2.html")

# Save the HTML file as Word DOCX document
doc.save("html-to-word.docx")

doc.