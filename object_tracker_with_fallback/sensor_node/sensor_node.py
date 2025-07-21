import freenect, cv2, numpy as np
try:
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    cp = np
    GPU_AVAILABLE = False

from shared.db_utils import insert_object

def get_depth_frame():
    depth, _ = freenect.sync_get_depth()
    return depth.astype(np.uint8)

def find_objects(depth):
    _, binary = cv2.threshold(depth, 1, 255, cv2.THRESH_BINARY)
    n, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)
    objs = []
    for i in range(1, n):
        x, y = centroids[i]
        mask = labels == i
        avg_depth = int(cp.asarray(depth[mask]).mean())
        objs.append((x, y, avg_depth))
    return objs

def main():
    print("GPU available:", GPU_AVAILABLE)
    while True:
        frame = get_depth_frame()
        objects = find_objects(frame)
        for x, y, d in objects:
            insert_object(x, y, d)
        for x, y, _ in objects:
            cv2.circle(frame, (int(x), int(y)), 5, 255, -1)
        cv2.imshow('Sensor View', frame)
        if cv2.waitKey(10) == 27:
            break
    cv2.destroyAllWindows()
