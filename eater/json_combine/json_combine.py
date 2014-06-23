import os
import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: python json_combine.py outputfile inputfile1 inputfile2"
    else:
        restaurants = []
        for name in sys.argv[2:]:
            with open(name, "r") as f:
                # Check if file is empty
                f.seek(0, os.SEEK_END)
                if f.tell():
                    f.seek(0, os.SEEK_SET)
                    # TODO: Standardize when to use Decoder
                    restaurants += json.JSONDecoder().decode(json.load(f))
        # TODO: Remove duplicates in unhashable data
        with open(sys.argv[1], "w") as f:
            json.dump(restaurants, f)
