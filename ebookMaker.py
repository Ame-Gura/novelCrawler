from ebooklib import epub
import pickle
book = epub.EpubBook()

# set metadata
book.set_identifier('id123456')
book.set_title('Ascendance of a Bookworm')
book.set_language('en')

book.add_author('Miya Kazuki')
book.add_author('blastron', uid='coauthor')

# create chapter
chapters = []
with open('chapters', 'rb') as f:
    chapters = pickle.load(f)

booksChapter = []
for chapter in chapters:
    c1 = epub.EpubHtml(title=chapter['h2'], file_name=chapter['h1']+'.xhtml', lang='en')
    paragraph = '<h1>'+chapter['h2']+'</h1>'
    paragraph = paragraph + ''.join(['<p>'+p+'</p>' for p in chapter['p']])
    c1.content= paragraph
    # add chapter
    book.add_item(c1)
    booksChapter.append(c1)



# define Table Of Contents
book.toc = (
             (booksChapter))


# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
book.add_item(nav_css)

# basic spine
book.spine = ['nav']+booksChapter

# write to the file
epub.write_epub('test.epub', book, {})