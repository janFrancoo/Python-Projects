import cv2
import time
import dataset
import argparse
from feature_extract import FeatureExtract

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--limit", help="Result limit")
ap.add_argument("-s", "--show", help="Query result show images")
ap.add_argument("-d", "--data", required=True, help="Path of images folder")
ap.add_argument("-i", "--image", required=True, help="Path of the image that you want to query")
args = vars(ap.parse_args())

show = False
if args["show"] is not None:
    if args["show"] == "True":
        show = True

limit = 2
if args["limit"] is not None:
    limit = args["limit"]

start = time.time()
data = dataset.get_data(args["data"])
end = time.time()
print("Database simulation: " + str(end - start))

query_image = cv2.imread(args["image"])

start = time.time()
feat_extract = FeatureExtract(query_image)
kp, des = feat_extract.extract_features()
bf = cv2.BFMatcher()

res = []
for obj in data:
    matches = bf.knnMatch(des, obj["des"], k=2)
    good = []
    for match_1, match_2 in matches:
        if match_1.distance < 0.75 * match_2.distance:
            good.append([match_1])
    res.append({
        "image": obj["image"],
        "file_name": obj["file_name"],
        "match": len(good)
    })

res.sort(key=lambda x: x.get("match"), reverse=True)
end = time.time()
print("Query: " + str(end - start))

if len(res) < limit:
    limit = len(res)

for i in range(limit):
    print(res[i]["file_name"])
    if show:
        cv2.imshow(str(i), res[i]["image"])
        cv2.waitKey(0)
