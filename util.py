


def unicode_cleaner(infile, outfile):
  with open(outfile,"w") as out:
    with open(infile,"r", errors="ignore") as f:
      for line in f.readlines():
        out.write(line)

