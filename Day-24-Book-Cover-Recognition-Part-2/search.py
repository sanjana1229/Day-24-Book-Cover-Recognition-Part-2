from pyimagesearch.coverdescriptor import CoverDescriptor
from pyimagesearch.covermatcher import CoverMatcher
import argparse
import glob
import csv
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--db", required=True, help="Path to the book database CSV file")
ap.add_argument("-c", "--covers", required=True, help="Path to the directory that contains our book covers")
ap.add_argument("-q", "--query", required=True, help="Path to the query book cover")
args = vars(ap.parse_args())

db = {}

with open(args["db"]) as f:
    reader = csv.reader(f)

    for row in reader:
        db[row[0]] = row[1:]

cd = CoverDescriptor()
queryImage = cv2.imread(args["query"])
gray = cv2.cvtColor(queryImage, cv2.COLOR_BGR2GRAY)

queryKps, queryDescs = cd.describe(gray)

coverPaths = glob.glob(args["covers"] + "/*.png")
cm = CoverMatcher(cd, coverPaths)
results = cm.search(queryKps, queryDescs)

cv2.imshow("Query", queryImage)

if len(results) == 0:
    print("No matches found")
else:
    for (score, coverPath) in results[:3]:
        print("Score:", score)
        print("Cover:", coverPath)

        filename = coverPath.split("\\")[-1]
        book = db[filename]

        print("Author:", book[0])
        print("Title:", book[1])
        print()

        result = cv2.imread(coverPath)
        cv2.imshow("Result", result)
        cv2.waitKey(0)

cv2.destroyAllWindows()