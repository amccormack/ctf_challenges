# Prompt
I realized that the previous command had a mistake. It should be right this time...?

```
$ git filter-branch --index-filter "git rm -f --ignore-unmatch *flag" --prune-empty -- --all
$ git reflog expire --expire=now --all
$ git gc --aggressive --prune=now
```

# Solution
A writeup to this challenge is located [here](https://amccormack.net/2019-05-05-obliterated-file-tsg-ctf.html)
