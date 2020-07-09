import pandas as pd

class KmaSum:
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.make_table(self.input, self.output)
    def read_sample(self, infile):
        """ read a file, give the file location as index, return df"""

        df = pd.read_csv(infile, sep = '\t')
        if not df.empty:
            df['filename'] = infile
            df.set_index('filename', inplace = True)
        return df

    def make_table(self, files, outloc):
        df = pd.concat([self.read_sample(x) for x in files])
        df.to_csv(outloc, sep = '\t')
        print(df)


