PROMPT = """
Analyze the input image and detect ALL instances of objects belonging to the target classes specified below.
Detect every single instance comprehensively without omissions (including small, distant, partially occluded objects, or multiple people/vehicles).

# Target Classes (Class Name: Description)
{classes_info}

* Note: The descriptions above may be written in Japanese. Please interpret them into English concepts to accurately detect the corresponding objects. In the output JSON, always use the exact class name (key) provided above.

# Detection Rules
- Detect ONLY objects belonging to the target classes listed above. Do not detect any other objects.
- Detect every instance of the target classes present in the image comprehensively (no omissions).
- Assign exactly one bounding box per detected object instance.

# Bounding Box (BBox) Coordinate Specification
Each bounding box MUST contain EXACTLY 4 float numbers: [x_min, y_min, x_max, y_max]
- DO NOT output 2 coordinates (points/centers). You MUST output a 4-coordinate bounding box covering the entire object.
- Coordinates must be normalized floats between 0.0 and 1.0 (relative to image width and height):
  - x_min (float, 0.0 to 1.0): Left boundary of the bounding box
  - y_min (float, 0.0 to 1.0): Top boundary of the bounding box
  - x_max (float, 0.0 to 1.0): Right boundary of the bounding box
  - y_max (float, 0.0 to 1.0): Bottom boundary of the bounding box
- Strict constraints:
  - Exactly 4 numbers per bbox: [x_min, y_min, x_max, y_max]
  - 0.0 <= x_min < x_max <= 1.0
  - 0.0 <= y_min < y_max <= 1.0
  - Use decimals between 0.0 and 1.0 (e.g., 0.65, NOT 650).

# Output Format
Output MUST be strictly in JSON format conforming to the schema below:
{{
  "bboxes": [
    {{
      "class_name": "target_class_name",
      "bbox": [0.12, 0.25, 0.48, 0.71]
    }},
    {{
      "class_name": "target_class_name",
      "bbox": [0.60, 0.30, 0.88, 0.55]
    }}
  ]
}}

- Every "bbox" array MUST contain exactly 4 numeric values: [x_min, y_min, x_max, y_max].
- If multiple target objects exist in the image, include every single detected object in the "bboxes" list.
- Return ONLY valid JSON without extra text, Markdown commentary, or explanation.
- If no target objects are found, return: "bboxes": []
"""
