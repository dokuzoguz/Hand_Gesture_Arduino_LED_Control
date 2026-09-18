def FingerController(HandLandmarks , Handedness):

    points = HandLandmarks.landmark
    label = Handedness.classification[0].label

    finger_states = []
    if label=="Left":
        finger_states = [
            points[4].x > points[3].x,
            points[8].y < points[7].y,
            points[12].y < points[11].y,
            points[16].y < points[15].y,
            points[20].y < points[19].y
        ]
    else:
        finger_states = [
                points[4].x < points[3].x,
                points[8].y < points[7].y,
                points[12].y < points[11].y,
                points[16].y < points[15].y,
                points[20].y < points[19].y
            ]

    return finger_states