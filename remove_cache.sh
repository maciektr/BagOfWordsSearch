rm -rf wiki_pages
rm -f search_web/appdb.db
mkdir wiki_pages
echo "# Ignore everything in this directory
*
# Except this file
!.gitignore" > wiki_pages/.gitignore
