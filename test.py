from urllib.parse import urljoin

print(
    urljoin(
        'http://www.abc.com/folder1/folder2/index.html',
        'file1'
    )
)