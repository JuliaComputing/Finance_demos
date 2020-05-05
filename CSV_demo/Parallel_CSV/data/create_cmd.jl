urls = open("file_urls.txt", "r")

wget_cmds = [Cmd(["wget", i]) for i in readlines(urls)]
