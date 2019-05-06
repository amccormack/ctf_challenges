# Prompt
Working on making a problem of TSG CTF, I noticed that I have staged and committed the flag file by mistake before I knew it. I googled and found the following commands, so I'm not sure but anyway typed them. It should be ok, right?

```
$ git filter-branch --index-filter "git rm -f --ignore-unmatch problem/flag" --prune-empty -- --all
$ git reflog expire --expire=now --all
$ git gc --aggressive --prune=now
```

# Solution
A writeup to this challenge is located [here](https://amccormack.net/2019-05-05-obliterated-file-tsg-ctf.html)
