{
    "Relations": {
        "B": {
            "short_name": "Before",
            "converse": "Bi",
            "is_transitive": "True"
            },
        "Bi": {
            "short_name": "After",
            "converse": "B",
            "is_transitive": "True"
            },
        "D": {
            "short_name": "During",
            "converse": "Di",
            "is_transitive": "True"
            },
        "Di": {
            "short_name": "Contains",
            "converse": "D",
            "is_transitive": "True"
            },
        "E": {
            "short_name": "Equals",
            "converse": "E",
            "is_equality": "True"
            },
        "F": {
            "short_name": "Finishes",
            "converse": "Fi",
            "is_transitive": "True"
            },
        "Fi": {
            "short_name": "FinishedBy",
            "converse": "F",
            "is_transitive": "True"
            },
        "M": {
            "short_name": "Meets",
            "converse": "Mi"
            },
        "Mi": {
            "short_name": "MetBy",
            "converse": "M"
            },
        "O": {
            "short_name": "Overlaps",
            "converse": "Oi"
            },
        "Oi": {
            "short_name": "OverlappedBy",
            "converse": "O"
            },
        "S": {
            "short_name": "Starts",
            "converse": "Si",
            "is_transitive": "True"
            },
        "Si": {
            "short_name": "StartedBy",
            "converse": "S",
            "is_transitive": "True"
            }
        },
    "Transitivity Table": {
        "B": {
            "B": ["B"],
            "BI": ["B","BI","D","DI","E","F","FI","M","MI","O","OI","S","SI"],
            "D": ["B","D","M","O","S"],
            "DI": ["B"],
            "E": ["B"],
            "F": ["B","D","M","O","S"],
            "FI": ["B"],
            "M": ["B"],
            "MI": ["B","D","M","O","S"],
            "O": ["B"],
            "OI": ["B","D","M","O","S"],
            "S": ["B"],
            "SI": ["B"]
            },
        "BI": {
            "B": ["B","BI","D","DI","E","F","FI","M","MI","O","OI","S","SI"],
            "BI": ["BI"],
            "D": ["BI","D","F","MI","OI"],
            "DI": ["BI"],
            "E": ["BI"],
            "F": ["BI"],
            "FI": ["BI"],
            "M": ["BI","D","F","MI","OI"],
            "MI": ["BI"],
            "O": ["BI","D","F","MI","OI"],
            "OI": ["BI"],
            "S": ["BI","D","F","MI","OI"],
            "SI": ["BI"]
            },
        "D": {
            "B": [
                "B"
                ],
            "BI": [
                "BI"
                ],
            "D": [
                "D"
                ],
            "DI": [
                "B",
                "BI",
                "D",
                "DI",
                "E",
                "F",
                "FI",
                "M",
                "MI",
                "O",
                "OI",
                "S",
                "SI"
                ],
            "E": [
                "D"
                ],
            "F": [
                "D"
                ],
            "FI": [
                "B",
                "D",
                "M",
                "O",
                "S"
                ],
            "M": [
                "B"
                ],
            "MI": [
                "BI"
                ],
            "O": [
                "B",
                "D",
                "M",
                "O",
                "S"
                ],
            "OI": [
                "BI",
                "D",
                "F",
                "MI",
                "OI"
                ],
            "S": [
                "D"
                ],
            "SI": [
                "BI",
                "D",
                "F",
                "MI",
                "OI"
                ]
            },
        "DI": {
            "B": [
                "B",
                "DI",
                "FI",
                "M",
                "O"
                ],
            "BI": [
                "BI",
                "DI",
                "MI",
                "OI",
                "SI"
                ],
            "D": [
                "D",
                "DI",
                "E",
                "F",
                "FI",
                "O",
                "OI",
                "S",
                "SI"
                ],
            "DI": [
                "DI"
                ],
            "E": [
                "DI"
                ],
            "F": [
                "DI",
                "OI",
                "SI"
                ],
            "FI": [
                "DI"
                ],
            "M": [
                "DI",
                "FI",
                "O"
                ],
            "MI": [
                "DI",
                "OI",
                "SI"
                ],
            "O": [
                "DI",
                "FI",
                "O"
                ],
            "OI": [
                "DI",
                "OI",
                "SI"
                ],
            "S": [
                "DI",
                "FI",
                "O"
                ],
            "SI": [
                "DI"
                ]
            },
        "E": {
            "B": [
                "B"
                ],
            "BI": [
                "BI"
                ],
            "D": [
                "D"
                ],
            "DI": [
                "DI"
                ],
            "E": [
                "E"
                ],
            "F": [
                "F"
                ],
            "FI": [
                "FI"
                ],
            "M": [
                "M"
                ],
            "MI": [
                "MI"
                ],
            "O": [
                "O"
                ],
            "OI": [
                "OI"
                ],
            "S": [
                "S"
                ],
            "SI": [
                "SI"
                ]
            },
        "F": {
            "B": [
                "B"
                ],
            "BI": [
                "BI"
                ],
            "D": [
                "D"
                ],
            "DI": [
                "BI",
                "DI",
                "MI",
                "OI",
                "SI"
                ],
            "E": [
                "F"
                ],
            "F": [
                "F"
                ],
            "FI": [
                "E",
                "F",
                "FI"
                ],
            "M": [
                "M"
                ],
            "MI": [
                "BI"
                ],
            "O": [
                "D",
                "O",
                "S"
                ],
            "OI": [
                "BI",
                "MI",
                "OI"
                ],
            "S": [
                "D"
                ],
            "SI": [
                "BI",
                "MI",
                "OI"
                ]
            },
        "FI": {
            "B": [
                "B"
                ],
            "BI": [
                "BI",
                "DI",
                "MI",
                "OI",
                "SI"
                ],
            "D": [
                "D",
                "O",
                "S"
                ],
            "DI": [
                "DI"
                ],
            "E": [
                "FI"
                ],
            "F": [
                "E",
                "F",
                "FI"
                ],
            "FI": [
                "FI"
                ],
            "M": [
                "M"
                ],
            "MI": [
                "DI",
                "OI",
                "SI"
                ],
            "O": [
                "O"
                ],
            "OI": [
                "DI",
                "OI",
                "SI"
                ],
            "S": [
                "O"
                ],
            "SI": [
                "DI"
                ]
            },
        "M": {
            "B": [
                "B"
                ],
            "BI": [
                "BI",
                "DI",
                "MI",
                "OI",
                "SI"
                ],
            "D": [
                "D",
                "O",
                "S"
                ],
            "DI": [
                "B"
                ],
            "E": [
                "M"
                ],
            "F": [
                "D",
                "O",
                "S"
                ],
            "FI": [
                "B"
                ],
            "M": [
                "B"
                ],
            "MI": [
                "E",
                "F",
                "FI"
                ],
            "O": [
                "B"
                ],
            "OI": [
                "D",
                "O",
                "S"
                ],
            "S": [
                "M"
                ],
            "SI": [
                "M"
                ]
            },
        "MI": {
            "B": [
                "B",
                "DI",
                "FI",
                "M",
                "O"
                ],
            "BI": [
                "BI"
                ],
            "D": [
                "D",
                "F",
                "OI"
                ],
            "DI": [
                "BI"
                ],
            "E": [
                "MI"
                ],
            "F": [
                "MI"
                ],
            "FI": [
                "MI"
                ],
            "M": [
                "E",
                "S",
                "SI"
                ],
            "MI": [
                "BI"
                ],
            "O": [
                "D",
                "F",
                "OI"
                ],
            "OI": [
                "BI"
                ],
            "S": [
                "D",
                "F",
                "OI"
                ],
            "SI": [
                "BI"
                ]
            },
        "O": {
            "B": [
                "B"
                ],
            "BI": [
                "BI",
                "DI",
                "MI",
                "OI",
                "SI"
                ],
            "D": [
                "D",
                "O",
                "S"
                ],
            "DI": [
                "B",
                "DI",
                "FI",
                "M",
                "O"
                ],
            "E": [
                "O"
                ],
            "F": [
                "D",
                "O",
                "S"
                ],
            "FI": [
                "B",
                "M",
                "O"
                ],
            "M": [
                "B"
                ],
            "MI": [
                "DI",
                "OI",
                "SI"
                ],
            "O": [
                "B",
                "M",
                "O"
                ],
            "OI": [
                "D",
                "DI",
                "E",
                "F",
                "FI",
                "O",
                "OI",
                "S",
                "SI"
                ],
            "S": [
                "O"
                ],
            "SI": [
                "DI",
                "FI",
                "O"
                ]
            },
        "OI": {
            "B": [
                "B",
                "DI",
                "FI",
                "M",
                "O"
                ],
            "BI": [
                "BI"
                ],
            "D": [
                "D",
                "F",
                "OI"
                ],
            "DI": [
                "BI",
                "DI",
                "MI",
                "OI",
                "SI"
                ],
            "E": [
                "OI"
                ],
            "F": [
                "OI"
                ],
            "FI": [
                "DI",
                "OI",
                "SI"
                ],
            "M": [
                "DI",
                "FI",
                "O"
                ],
            "MI": [
                "BI"
                ],
            "O": [
                "D",
                "DI",
                "E",
                "F",
                "FI",
                "O",
                "OI",
                "S",
                "SI"
                ],
            "OI": [
                "BI",
                "MI",
                "OI"
                ],
            "S": [
                "D",
                "F",
                "OI"
                ],
            "SI": [
                "BI",
                "MI",
                "OI"
                ]
            },
        "S": {
            "B": [
                "B"
                ],
            "BI": [
                "BI"
                ],
            "D": [
                "D"
                ],
            "DI": [
                "B",
                "DI",
                "FI",
                "M",
                "O"
                ],
            "E": [
                "S"
                ],
            "F": [
                "D"
                ],
            "FI": [
                "B",
                "M",
                "O"
                ],
            "M": [
                "B"
                ],
            "MI": [
                "MI"
                ],
            "O": [
                "B",
                "M",
                "O"
                ],
            "OI": [
                "D",
                "F",
                "OI"
                ],
            "S": [
                "S"
                ],
            "SI": [
                "E",
                "S",
                "SI"
                ]
            },
        "SI": {
            "B": [
                "B",
                "DI",
                "FI",
                "M",
                "O"
                ],
            "BI": [
                "BI"
                ],
            "D": [
                "D",
                "F",
                "OI"
                ],
            "DI": [
                "DI"
                ],
            "E": [
                "SI"
                ],
            "F": [
                "OI"
                ],
            "FI": [
                "DI"
                ],
            "M": [
                "DI",
                "FI",
                "O"
                ],
            "MI": [
                "MI"
                ],
            "O": [
                "DI",
                "FI",
                "O"
                ],
            "OI": [
                "OI"
                ],
            "S": [
                "E",
                "S",
                "SI"
                ],
            "SI": [
                "SI"
                ]
            }
        }
    }
