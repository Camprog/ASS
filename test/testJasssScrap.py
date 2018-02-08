import JasssArticle

# print(soup.prettify())
for article in range(1, 7):
    the_article = JasssArticle(article=article)
    title = the_article.get_title()
    key_worlds = the_article.get_key_worlds()
    authors = the_article.get_authors()
    abstract = the_article.get_abstract()
    print("The first published article in JASSS was: " + title + "\n" + "The key words was: " + str(
        key_worlds) + "\n" + "And authors was: " + str(authors) + "\n" + "Abstract: " + abstract + "\n")
